## Features
- Custom AMD for Asterisk using EAGI
- WebRTC VAD based voice activity detection
- Realtime classification for HUMAN / VOICEMAIL / UNKNOWN
- Detailed AMDCAUSE output for tuning and debugging

## Requirements
- Asterisk with EAGI support
- Python 3
- webrtcvad

## Files
- `custom_amd_eagi.py` - main AMD detection script
- `run_amd_eagi.sh` - shell wrapper for EAGI
- `requirements.txt` - Python dependencies
- `extensions.conf.example` - minimal dialplan example

## Output Variables
- `AMD_NOTIFY` = HUMAN | VOICEMAIL | UNKNOWN
- `AMDSTATUS` = HUMAN | MACHINE | NOTSURE
- `AMDCAUSE` = detailed detection reason
