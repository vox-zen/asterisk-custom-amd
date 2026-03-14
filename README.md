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
```

Install Python dependency:

```bash
pip3 install -r requirements.txt
```

Create directory on your Asterisk server:

```bash
sudo mkdir -p /opt/asterisk/custom_amd
```

Copy the scripts:

```bash
sudo cp custom_amd_eagi.py /opt/asterisk/custom_amd/
sudo cp run_amd_eagi.sh /opt/asterisk/custom_amd/
```

Make the runner executable:

```bash
sudo chmod +x /opt/asterisk/custom_amd/run_amd_eagi.sh
```

Verify Python installation:

```bash
python3 --version
```

---

Note:
This AMD implementation requires EAGI, not standard AGI, because it needs access to the live audio stream from Asterisk.

---

# License

MIT
