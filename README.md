# 🎣 Phishing Awareness Simulation Tool

A Flask-based phishing simulation platform designed for **security awareness training**. This tool allows security teams to run controlled phishing campaigns, track who clicks simulated phishing links, and use the results to educate employees — all within a safe, ethical environment.

> ⚠️ **Ethical Use Only** — This tool is intended exclusively for authorized security awareness training within organizations. Never use it against individuals or systems without explicit written permission.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Local Deployment — Step by Step](#-local-deployment--step-by-step)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Usage Guide](#-usage-guide)
- [Email Templates](#-email-templates)
- [Troubleshooting](#-troubleshooting)
- [Disclaimer](#-disclaimer)

---

## ✨ Features

- 📧 Send simulated phishing emails to a list of targets
- 🔗 Unique tracking tokens per recipient
- 📊 Campaign dashboard with click-rate analytics
- 🕵️ Captures IP address and User-Agent of anyone who clicks
- 🗄️ SQLite database (zero setup required)
- 🖥️ Clean web UI built with Flask
- 🔒 SMTP-based email delivery (Gmail, Outlook, etc.)

---

## 📁 Project Structure

```
Phishing-Awareness-Simulation-Tool/
│
├── app.py              # Main Flask application & routes
├── config.py           # Configuration (SMTP, DB, secrets)
├── mailer.py           # Email builder & SMTP sender
├── models.py           # SQLAlchemy database models
├── tracker.py          # Click-tracking logic
│
├── templates/          # Jinja2 HTML templates
│   ├── email_templates/
│   │   ├── password_reset.html
│   │   └── it_alert.html
│   └── ...             # Dashboard & UI templates
│
└── static/             # CSS, JS, images
```

---

## 🛠️ Prerequisites

Make sure the following are installed on your machine before proceeding:

| Requirement | Version | Notes |
|---|---|---|
| Python | 3.8+ | [Download](https://www.python.org/downloads/) |
| pip | Latest | Comes with Python |
| Git | Any | [Download](https://git-scm.com/) |
| SMTP Account | — | Gmail recommended for testing |

---

## 🚀 Local Deployment — Step by Step

### Step 1 — Clone the Repository

```bash
git clone https://github.com/JimilPrabtani/-Phishing-Awareness-Simulation-Tool-.git
cd -Phishing-Awareness-Simulation-Tool-
```

---

### Step 2 — Create a Virtual Environment

Creating a virtual environment keeps your project dependencies isolated from your system Python.

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

> ✅ You should see `(venv)` at the beginning of your terminal prompt once activated.

---

### Step 3 — Install Dependencies

```bash
pip install flask flask-sqlalchemy
```

> 💡 If a `requirements.txt` file is present, run `pip install -r requirements.txt` instead.

---

### Step 4 — Configure Environment Variables

The application reads its settings from environment variables. Set them before running the app.

**On macOS / Linux:**
```bash
export FLASK_SECRET_KEY="your-very-secret-key"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export SENDER_NAME="IT Security Team"
export BASE_URL="http://localhost:5000"
```

**On Windows (Command Prompt):**
```cmd
set FLASK_SECRET_KEY=your-very-secret-key
set SMTP_SERVER=smtp.gmail.com
set SMTP_PORT=587
set SMTP_USERNAME=your-email@gmail.com
set SMTP_PASSWORD=your-app-password
set SENDER_NAME=IT Security Team
set BASE_URL=http://localhost:5000
```

**On Windows (PowerShell):**
```powershell
$env:FLASK_SECRET_KEY="your-very-secret-key"
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SMTP_USERNAME="your-email@gmail.com"
$env:SMTP_PASSWORD="your-app-password"
$env:SENDER_NAME="IT Security Team"
$env:BASE_URL="http://localhost:5000"
```

> 📌 **Gmail users:** You must generate an [App Password](https://myaccount.google.com/apppasswords) (not your regular password) and enable 2-Step Verification on your Google account.

---

### Step 5 — Initialize the Database

The app uses SQLite, so no external database setup is needed. Run the following to create the database tables:

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"
```

> ✅ This will create a `philips_sim.db` file in your project directory.

---

### Step 6 — Run the Application

```bash
python app.py
```

You should see output similar to:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Open your browser and navigate to:
```
http://localhost:5000
```

<img width="2104" height="961" alt="cli" src="https://github.com/user-attachments/assets/1a6752eb-fa8a-45d1-ac39-d72c20dedf28" />


---

## ⚙️ Configuration

All configuration options live in `config.py` and can be overridden via environment variables:

| Variable | Default | Description |
|---|---|---|
| `FLASK_SECRET_KEY` | `change-me-in-production` | Flask session secret — **change this!** |
| `SMTP_SERVER` | `smtp.gmail.com` | SMTP server hostname |
| `SMTP_PORT` | `587` | SMTP port (587 for TLS) |
| `SMTP_USERNAME` | *(empty)* | Your email address |
| `SMTP_PASSWORD` | *(empty)* | Your email app password |
| `SENDER_NAME` | `IT Security Team` | Display name in phishing emails |
| `BASE_URL` | `http://localhost:5000` | Public URL for tracking links |

---

## 📖 Usage Guide

### Creating a Campaign
1. Navigate to `http://localhost:5000`
2. Click **"New Campaign"**
3. Enter a campaign name and choose a phishing email template
4. Add target email addresses
5. Click **"Send Campaign"** to dispatch the simulated phishing emails

<img width="3072" height="1670" alt="Dashboard" src="https://github.com/user-attachments/assets/cb3ead12-4acc-47a5-84b9-4d2f62a560db" />


### Viewing Results
- Go to the **Dashboard** to see all campaigns
- Click on a campaign to view detailed stats:
  - Total targets
  - Number of clicks
  - Click rate (%)
  - Per-recipient details (IP, User-Agent, timestamp)

<img width="3072" height="1670" alt="results" src="https://github.com/user-attachments/assets/662f5d2e-5829-4f64-9892-f79a67ba550f" />
<img width="3072" height="1670" alt="results" src="https://github.com/user-attachments/assets/6947d9f8-af40-49b1-a7ee-d8f3a8db9dec" />
<img width="3072" height="1670" alt="Screenshot From 2026-03-06 01-31-32" src="https://github.com/user-attachments/assets/55ffa85d-b0e3-4a94-88d0-c211975cc856" />



---

## 📧 Email Templates

Two built-in phishing simulation templates are included:

| Template ID | Subject Line | Scenario |
|---|---|---|
| `password_reset` | Important: Password Reset Required | Fake password reset request |
| `it_alert` | IT SECURITY: Unusual login detected | Fake security alert |

Templates are located in `templates/email_templates/`. You can create custom templates by adding new `.html` files there and registering them in `mailer.py`.

---

## 🔧 Troubleshooting

### SMTP Authentication Failed
- Ensure your Gmail account has **2-Step Verification** enabled
- Use an **App Password**, not your normal Gmail password
- [Generate an App Password →](https://myaccount.google.com/apppasswords)

### Emails Not Being Received
- Check your spam/junk folder
- Verify `SMTP_USERNAME` and `SMTP_PASSWORD` are correctly set
- Confirm `BASE_URL` is reachable from the target's browser

### Database Errors
- Delete `philips_sim.db` and re-run the database initialization command in Step 5
- Ensure you are running commands from inside the project directory with the virtual environment activated

### Port Already in Use
```bash
# Find and kill the process using port 5000
# macOS / Linux:
lsof -ti:5000 | xargs kill -9

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

## ⚠️ Disclaimer

This tool is built strictly for **educational and authorized security awareness training purposes**.

- ✅ Only use against systems and individuals you have **explicit written authorization** to test
- ✅ Inform your organization's legal/compliance team before running campaigns
- ❌ Do NOT use for malicious purposes
- ❌ Do NOT target individuals outside your organization

The author is not responsible for any misuse of this tool. Always act ethically and within the bounds of the law.

---

## 📄 License

This project is intended for educational use. Please review your organization's policies before deployment.

---

*Built with ❤️ using Flask & Python*
