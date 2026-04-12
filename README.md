# ☎️ Asterisk Custom AMD (Answering Machine Detection)

Custom Answering Machine Detection (AMD) implementation for **Asterisk** using **EAGI** and **WebRTC VAD**.

Designed to improve detection accuracy for distinguishing between **HUMAN**, **VOICEMAIL**, and **UNKNOWN** in outbound call systems.

---

## 🚀 Overview

This project provides a custom AMD solution that analyzes live audio streams from Asterisk calls using:

* 📞 **EAGI (Enhanced AGI)** for real-time audio processing
* 🎙️ **WebRTC Voice Activity Detection (VAD)** for speech analysis

The result is returned as Asterisk variables for seamless integration into dialplans.

---

## ⚡ Features

* 🎯 Detects:

  * HUMAN
  * VOICEMAIL
  * UNKNOWN
* 🔊 Real-time audio processing via EAGI
* 🧠 Voice Activity Detection (WebRTC VAD)
* 🔌 Easy integration with Asterisk dialplans
* ⚙️ Lightweight and customizable

---

## 🛠️ Requirements

* Asterisk (tested with EAGI support)
* Python 3.8+
* Required Python packages:

```bash
pip install -r requirements.txt
```

---

## 📦 Installation

```bash
git clone https://github.com/vox-zen/asterisk-custom-amd.git
cd asterisk-custom-amd
pip install -r requirements.txt
chmod +x run_amd_eagi.sh
```

---

## ▶️ Usage

### 1. Configure Dialplan

Example `extensions.conf`:

```asterisk
exten => _X.,1,NoOp(Starting AMD Detection)
 same => n,Answer()
 same => n,EAGI(run_amd_eagi.sh)
 same => n,NoOp(AMD Status: ${AMDSTATUS})
 same => n,NoOp(AMD Cause: ${AMDCAUSE})
 same => n,Hangup()
```

---

### 2. Run Detection Script

The script processes audio from STDIN (EAGI) and returns:

* `AMDSTATUS` → HUMAN / MACHINE / UNKNOWN
* `AMDCAUSE` → detailed reason

---

## 📊 Sample Output

```text
AMDSTATUS=HUMAN
AMDCAUSE=SHORT_GREETING
```

```text
AMDSTATUS=MACHINE
AMDCAUSE=LONG_SILENCE_AFTER_GREETING
```

---

## 🧠 How It Works

1. Asterisk answers the call
2. EAGI streams raw audio to the script
3. WebRTC VAD analyzes voice activity
4. Detection logic classifies the call
5. Results returned to Asterisk variables

---

## 🎯 Use Cases

* Outbound dialers
* Call center automation
* IVR systems
* Spam / voicemail filtering
* Campaign optimization

---

## ⚙️ Customization

You can adjust detection sensitivity by modifying:

* Silence thresholds
* Speech duration
* VAD aggressiveness level

---

## 📁 Project Structure

```bash
custom_amd_eagi.py      # Core detection logic
run_amd_eagi.sh         # EAGI entry script
extensions.conf.example # Sample dialplan
requirements.txt        # Dependencies
```

---

## 🔮 Roadmap

* [ ] Improve detection accuracy with ML models
* [ ] Add logging & metrics
* [ ] Configurable thresholds via config file
* [ ] Integration with monitoring tools

---

## 👤 Author

**Vizi**
Full-Stack Developer (Communication Tools Focus)

---

## ⭐ Support

If this project helps you, consider giving it a ⭐ on GitHub!
