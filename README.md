## Features
- Custom AMD for Asterisk using EAGI
- WebRTC VAD based voice activity detection
- Realtime classification for HUMAN / VOICEMAIL / UNKNOWN
- Detailed AMDCAUSE output for tuning and debugging

## Requirements
- Asterisk with EAGI support
- Python 3
- webrtcvad

- ## Installation

Clone the repository:

```bash
git clone https://github.com/vox-zen/asterisk-custom-amd.git
cd asterisk-custom-amd

pip3 install -r requirements.txt

sudo mkdir -p /opt/asterisk/custom_amd
sudo cp custom_amd_eagi.py /opt/asterisk/custom_amd/
sudo cp run_amd_eagi.sh /opt/asterisk/custom_amd/
sudo chmod +x /opt/asterisk/custom_amd/run_amd_eagi.sh

python3 --version


---

# Usage

Tambahkan ini **setelah installation**.

```md
## Usage

Call the AMD script from your Asterisk dialplan using **EAGI**.

Example:


## Files
- `custom_amd_eagi.py` - main AMD detection script
- `run_amd_eagi.sh` - shell wrapper for EAGI
- `requirements.txt` - Python dependencies
- `extensions.conf.example` - minimal dialplan example

## Output Variables
- `AMD_NOTIFY` = HUMAN | VOICEMAIL | UNKNOWN
- `AMDSTATUS` = HUMAN | MACHINE | NOTSURE
- `AMDCAUSE` = detailed detection reason
