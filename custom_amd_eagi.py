import os
import sys
import time
import struct
import select
import webrtcvad


def agi_print(s: str) -> None:
    sys.stdout.write(s + "\n")
    sys.stdout.flush()


def agi_setvar(k: str, v: str) -> None:
    agi_print(f'SET VARIABLE {k} "{v}"')


def agi_read_env() -> None:
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            break


def rms16_le(pcm: bytes) -> float:
    n = len(pcm) // 2
    if n <= 0:
        return 0.0
    s = 0
    for i in range(0, n * 2, 2):
        v = struct.unpack_from("<h", pcm, i)[0]
        s += v * v
    return (s / n) ** 0.5


def main() -> int:
    agi_read_env()

    audio_fd = 3
    vad = webrtcvad.Vad(1)

    FRAME_MS = 20
    FRAME_BYTES = 320
    SAMPLE_RATE = 8000

    # Analysis window
    MAX_SEC_AUDIO = 5.0
    WALL_TIMEOUT_SEC = 5.5

    max_frames = int((MAX_SEC_AUDIO * 1000) / FRAME_MS)
    deadline = time.time() + WALL_TIMEOUT_SEC

    # Tuning
    RMS_MIN = 50
    MIN_VOICE_RUN_FRAMES = 2

   # Gap to count speech segments completed
    SIL_GAP_FRAMES = int(300 / FRAME_MS)       # 300 ms
    # False negative VAD tolerance in run speech
    RUN_BREAK_FRAMES = int(120 / FRAME_MS)     # 120 ms

    # Rule voicemail
    VM_LONG_RUN_FRAMES = int(900 / FRAME_MS)   # 900 ms
    VM_MIN_SPEECH_FRAMES = int(1600 / FRAME_MS) # 1600 ms
    
    HUMAN_MAX_SPEECH_FRAMES = int(1200 / FRAME_MS)   # 1200 ms
    HUMAN_MAX_RUN_FRAMES = int(700 / FRAME_MS)       # 700 ms
    HUMAN_AFTER_SPEECH_GAP_FRAMES = int(300 / FRAME_MS)

    total_frames = 0
    speech_frames = 0
    onset_frame = None

    current_voice_run = 0
    confirmed_voice_run = 0
    longest_confirmed_run = 0

    in_speech = False
    gap_run = 0
    gaps = 0

    voice_confirmed = False

    while total_frames < max_frames and time.time() < deadline:
        r, _, _ = select.select([audio_fd], [], [], 0.05)
        if not r:
            continue

        try:
            pcm = os.read(audio_fd, FRAME_BYTES)
        except OSError:
            break

        if not pcm or len(pcm) < FRAME_BYTES:
            continue

        total_frames += 1

        is_voice = False
        if rms16_le(pcm) >= RMS_MIN:
            try:
                is_voice = vad.is_speech(pcm, SAMPLE_RATE)
            except Exception:
                is_voice = False

        if is_voice:
            current_voice_run += 1
            gap_run = 0

            if current_voice_run == MIN_VOICE_RUN_FRAMES:
                voice_confirmed = True
                if onset_frame is None:
                    onset_frame = total_frames - (MIN_VOICE_RUN_FRAMES - 1)
                confirmed_voice_run = MIN_VOICE_RUN_FRAMES
            elif current_voice_run > MIN_VOICE_RUN_FRAMES:
                confirmed_voice_run += 1

            if voice_confirmed:
                speech_frames += 1
                if confirmed_voice_run > longest_confirmed_run:
                    longest_confirmed_run = confirmed_voice_run
                in_speech = True

        else:
            current_voice_run = 0

            if voice_confirmed:
                gap_run += 1

                # Short miss VAD tolerance: still consider the same run section
                if gap_run <= RUN_BREAK_FRAMES:
                    speech_frames += 1
                    confirmed_voice_run += 1
                    if confirmed_voice_run > longest_confirmed_run:
                        longest_confirmed_run = confirmed_voice_run
                else:
                    confirmed_voice_run = 0
                    voice_confirmed = False

                if in_speech and gap_run == SIL_GAP_FRAMES:
                    gaps += 1
                    in_speech = False

    # ===== Decision =====
    if onset_frame is None:
        amd_notify = "UNKNOWN"
        amdstatus = "NOTSURE"
        cause = f"no_confirmed_speech_{MAX_SEC_AUDIO:.1f}s"

    else:
        # HUMAN:
        # relatively short utterances, not long runs, and there are stop/pause signs
        if (
            speech_frames <= HUMAN_MAX_SPEECH_FRAMES and
            longest_confirmed_run <= HUMAN_MAX_RUN_FRAMES and
            (gaps >= 1 or gap_run >= HUMAN_AFTER_SPEECH_GAP_FRAMES)
        ):
            amd_notify = "HUMAN"
            amdstatus = "HUMAN"
            cause = (
                f"human_speech={speech_frames * FRAME_MS}ms "
                f"run={longest_confirmed_run * FRAME_MS}ms gaps={gaps} "
                f"onset={onset_frame * FRAME_MS}ms total={total_frames * FRAME_MS}ms"
            )

        # MACHINE:
        # long / continuous greeting
        elif (
            longest_confirmed_run >= VM_LONG_RUN_FRAMES or
            (speech_frames >= VM_MIN_SPEECH_FRAMES and gaps <= 1)
        ):
            amd_notify = "VOICEMAIL"
            amdstatus = "MACHINE"
            cause = (
                f"vm_speech={speech_frames * FRAME_MS}ms "
                f"run={longest_confirmed_run * FRAME_MS}ms gaps={gaps} "
                f"onset={onset_frame * FRAME_MS}ms total={total_frames * FRAME_MS}ms"
            )
            
        elif (
            speech_frames >= int(500 / FRAME_MS) and
            speech_frames <= int(1200 / FRAME_MS) and
            longest_confirmed_run <= int(500 / FRAME_MS) and
            gaps <= 1
        ):
            amd_notify = "HUMAN"
            amdstatus = "HUMAN"
            cause = (
                f"human_short_speech={speech_frames * FRAME_MS}ms "
                f"run={longest_confirmed_run * FRAME_MS}ms gaps={gaps} "
                f"onset={onset_frame * FRAME_MS}ms total={total_frames * FRAME_MS}ms"
            )

        else:
            amd_notify = "UNKNOWN"
            amdstatus = "NOTSURE"
            cause = (
                f"uncertain_speech={speech_frames * FRAME_MS}ms "
                f"run={longest_confirmed_run * FRAME_MS}ms gaps={gaps} "
                f"onset={onset_frame * FRAME_MS}ms total={total_frames * FRAME_MS}ms"
            )

    agi_setvar("AMD_NOTIFY", amd_notify)
    agi_setvar("AMDSTATUS", amdstatus)
    agi_setvar("AMDCAUSE", cause)
    return 0


if __name__ == "__main__":
    sys.exit(main())
