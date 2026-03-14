# Asterisk Custom AMD (Answering Machine Detection)

Custom Answering Machine Detection (AMD) script for **Asterisk** using **EAGI** and **WebRTC VAD**.

This project provides a lightweight and tunable AMD implementation designed for outbound IVR systems, voice bots, and automated calling platforms.

The script analyzes realtime audio from Asterisk using EAGI and classifies the call as:

- HUMAN
- VOICEMAIL
- UNKNOWN

It exposes detection results through standard AGI variables so they can be used directly inside Asterisk dialplans.

---

# Features

- Custom AMD for Asterisk using **EAGI**
- WebRTC VAD based voice activity detection
- Realtime classification for **HUMAN / VOICEMAIL / UNKNOWN**
- Detailed `AMDCAUSE` output for tuning and debugging
- Lightweight and easy to integrate with existing dialplans
- Designed for outbound IVR / autodialer systems

---

# Requirements

Before using this script make sure your server has:

- Asterisk (with **EAGI support**)
- Python 3
- pip3
- webrtcvad Python library

Tested on typical Linux Asterisk servers.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/vox-zen/asterisk-custom-amd.git
cd asterisk-custom-amd

Install Python dependency:

pip3 install -r requirements.txt

Create directory on your Asterisk server:

sudo mkdir -p /opt/asterisk/custom_amd

Copy the scripts to the server:

sudo cp custom_amd_eagi.py /opt/asterisk/custom_amd/
sudo cp run_amd_eagi.sh /opt/asterisk/custom_amd/

Make the runner executable:

sudo chmod +x /opt/asterisk/custom_amd/run_amd_eagi.sh

Verify Python installation:

python3 --version

Note:

This AMD implementation requires EAGI, not standard AGI, because it needs access to the live audio stream from Asterisk.

Usage

Call the AMD script from your Asterisk dialplan using EAGI.

Example minimal dialplan:

[custom-amd-test]
exten => s,1,Answer()
 same => n,Playback(silence/1)
 same => n,Wait(1)
 same => n,EAGI(/opt/asterisk/custom_amd/run_amd_eagi.sh)

 same => n,NoOp(AMD_NOTIFY=${AMD_NOTIFY})
 same => n,NoOp(AMDSTATUS=${AMDSTATUS})
 same => n,NoOp(AMDCAUSE=${AMDCAUSE})

 same => n,GotoIf($["${AMD_NOTIFY}"="VOICEMAIL"]?vm:human)

 same => n(human),Playback(hello-world)
 same => n,Hangup()

 same => n(vm),Hangup()

The script will process the incoming audio stream and classify the call automatically.

Output Variables

The script exports the following AGI variables:

Variable	Description
AMD_NOTIFY	HUMAN / VOICEMAIL / UNKNOWN
AMDSTATUS	HUMAN / MACHINE / NOTSURE
AMDCAUSE	Detailed detection reason

Example dialplan debug:

NoOp(AMD_NOTIFY=${AMD_NOTIFY})
NoOp(AMDSTATUS=${AMDSTATUS})
NoOp(AMDCAUSE=${AMDCAUSE})
How It Works

The script listens to the live audio stream provided by Asterisk EAGI.

Audio is analyzed in realtime using:

WebRTC VAD (voice activity detection)

RMS energy filtering

speech run length detection

silence gap analysis

Based on the detected speech pattern the script determines whether the call is answered by:

A human (short greeting)

A voicemail system (long greeting)

Unknown / ambiguous audio

Tuning Parameters

The AMD behavior can be tuned inside the script.

Important parameters include:

Parameter	Description
RMS_MIN	Minimum audio energy threshold
MIN_VOICE_RUN_FRAMES	Minimum frames to consider speech
SIL_GAP_FRAMES	Silence gap threshold
VM_LONG_RUN_FRAMES	Continuous speech threshold for voicemail
VM_MIN_SPEECH_FRAMES	Minimum speech frames for machine detection
HUMAN_MAX_SPEECH_FRAMES	Maximum speech frames for human
HUMAN_MAX_RUN_FRAMES	Maximum continuous speech run for human

Adjust these values depending on your carrier audio quality and voicemail patterns.

Files
File	Description
custom_amd_eagi.py	Main AMD detection script
run_amd_eagi.sh	Shell wrapper used by EAGI
requirements.txt	Python dependencies
extensions.conf.example	Minimal Asterisk dialplan example
Limitations

Optimized primarily for 8 kHz telephony audio

Detection accuracy may vary depending on carrier audio quality

Voicemail greetings in different languages may require tuning

This script is intended as a customizable AMD base implementation

Use Cases

Typical use cases include:

Outbound autodialer systems

Voice bot platforms

IVR call automation

Telemarketing call filtering

Research and experimentation with AMD algorithms

Contributing

Contributions and improvements are welcome.

Feel free to open an issue or submit a pull request.

License

MIT License


---

# Setelah kamu paste README ini

Lakukan **2 hal kecil supaya repo kamu terlihat profesional**:

### Isi About repo

Klik ⚙️ di kanan repo lalu isi:

**Description**


Custom Answering Machine Detection for Asterisk using EAGI and WebRTC VAD


**Topics**


asterisk
amd
agi
eagi
ivr
telephony
python
webrtcvad
voicemail-detection


---

# Hasil akhir repo kamu nanti akan terlihat seperti


asterisk-custom-amd
│
├── README.md
├── custom_amd_eagi.py
├── run_amd_eagi.sh
├── requirements.txt
└── extensions.conf.example
