# HoneyGuard – Deception-Based Security Tool

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Issues](https://img.shields.io/github/issues/Prasadsarkate/HoneyGuard)
![Stars](https://img.shields.io/github/stars/Prasadsarkate/HoneyGuard?style=social)

**HoneyGuard** is a deception / honeypot utility that plants realistic-looking decoy files (“honeyfiles”), continuously monitors them for unauthorized access, rotates them, and emits alerts via a web dashboard or configured alert channels.

---

## 🧩 Features

- Generate decoy honeyfiles (e.g. docs, spreadsheets) with configurable content and format  
- Automated rotation of honeyfiles on schedule to avoid detection  
- Monitor file system events (access, modification, deletion) in real time  
- Web dashboard (Flask + Socket.IO) for viewing alerts and status  
- Configurable alert channels (email, webhooks, push notifications)  
- Encrypted logs, plugin support, and stub ML analyzer for anomaly scoring

---

## 📁 Repository Structure

```
├── main.py
├── requirements.txt
├── setup.py
├── config/
│   ├── settings.yaml
│   └── alerts.yaml
├── src/
│   ├── core/
│   ├── utils/
│   └── web_ui/
├── honeyfiles/
├── logs/
├── screenshot/
└── docs/
    └── design_architecture.md
```

---

## 🛠️ Installation & Setup

### Prerequisites

- Python **3.9+**  
- `git`  
- (Optional) Virtual environment tool (`venv` or `conda`)

### Steps

```bash
git clone https://github.com/Prasadsarkate/HoneyGuard.git
cd HoneyGuard

# Create virtual environment
python -m venv .venv
# Activate:
#   Linux / macOS: source .venv/bin/activate
#   Windows (PowerShell): .\.venv\Scripts\Activate.ps1
#   Windows (cmd): .\.venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

### Running the Application

```bash
python3 main.py
```

This will:
- Generate an initial set of honeyfiles  
- Start the rotation scheduler  
- Begin monitoring events (blocking)  
- Launch the web dashboard server (if configured in settings)

To explicitly run the dashboard server:

```bash
python3 src/web_ui/app.py
```
```bash
username :- admin@honeyguard.com
password :- secure123
```

Then open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ⚙️ Configuration

### Main Config Files

- `config/settings.yaml` — general settings (paths, intervals, file templates)  
- `config/alerts.yaml` — alert channel settings (email, webhooks, etc.)  
- `src/utils/logger.py` — logging level, format, output paths  

### Example Settings Table

| Setting           | Description                           | Default        |
|-------------------|---------------------------------------|----------------|
| rotation_interval | Time (in minutes) between file rotate | 60             |
| honeyfile_dir     | Path to store honeyfiles              | honeyfiles/    |
| log_file          | Path to log alerts                    | logs/alerts.log|

---

## 📖 Usage Examples

Generate honeyfiles manually:

```python
from src.core.file_generator import generate_honeyfiles
generate_honeyfiles()
```

Test alert API (when dashboard is running):

```http
GET /api/alerts
```

Example response:

```json
[
  {
    "timestamp": "2025-09-05 12:00:00",
    "level": "ALERT",
    "file": "honeypot.txt",
    "action": "deleted",
    "ip": "192.168.1.5",
    "user": "attacker"
  }
]
```

---

## 📸 Screenshots

![Login Page](screenshot/loginpage.png)  
*Screenshot: login screen of dashboard*

![Dashboard – Alerts](screenshot/dashboard1.png)  
*Screenshot: real-time alerts view*

![Dashboard – Analytics](screenshot/dashboard2.png)  
*Screenshot: metrics / stats view*

![Backend / Logs](screenshot/backend.png)  
*Screenshot: backend log view*

---

## 📊 Architecture

Refer to [docs/design_architecture.md](docs/design_architecture.md).  
_Add a diagram here for quick overview (recommended)._  

---

## 🧾 Logs & Alerts

- Logs saved under `logs/alerts.log` (JSON lines)  
- Alerts streamed realtime via Socket.IO on dashboard  
- Web API endpoint `/api/alerts` returns JSON of logged alerts  

---

## 🔒 Security Notes

- **Change default credentials** in `src/web_ui/app.py` before exposing publicly  
- Use **HTTPS/TLS** when deploying  
- Protect dashboard endpoints with proper authentication  
- Avoid committing secrets to repo; use `.env` or secret manager  

---

## 🚀 Roadmap

- [ ] SIEM integration (Splunk/ELK)  
- [ ] Advanced ML anomaly detection  
- [ ] Docker image for easier deployment  
- [ ] Cloud provider hooks (AWS, Azure, GCP)  

---

## 🧪 Development

- Run tests with `pytest` (if tests exist)  
- Editable install:

```bash
pip install -e .
```

---

## 🤝 Contributing

1. Fork the repo  
2. Create a feature branch (`git checkout -b feature/xyz`)  
3. Commit changes with clear messages  
4. Submit a pull request  

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
