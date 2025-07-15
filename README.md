# 📬 Samhiq Mailer Pro (SMTP)

**Samhiq Mailer Pro** is a powerful and intuitive desktop application that lets you send personalized bulk emails using your own SMTP credentials with real-time logging, smart retry logic, and a user-friendly UI.  
Whether you're managing newsletters, announcements, or customer communication, Samhiq Mailer is your go-to solution.

---

<p align="center">
  <img src="SamhiqMailer.png" alt="Samhiq Mailer Screenshot" width="700">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/SMTP-Gmail%20Supported-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Python-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-red?style=flat-square" />
</p>

---

## ✨ Core Highlights

- ✅ **Clean, powerful UI** — designed for productivity and ease of use  
- 📧 **Gmail SMTP Ready** — compatible with App Passwords  
- 📂 **Excel Integration** — import recipient lists with ease  
- 📝 **Dynamic Personalization** — use `{name}` to personalize each email  
- 📎 **Multi-file Attachments** — attach documents, images, or any file type  
- 🔄 **Auto Retry System** — retries failed emails automatically  
- 📊 **Real-Time Progress Logs** — see delivery status as it happens  
- 🔧 **Auto-Updater** — keeps you on the latest version, hassle-free  
- 💼 **Fully Portable** — no installation required, single `.exe` app  

---

## 🚀 Installation Guide

### Option 1 — 📦 Download `.exe`

➡️ [Download Latest Version EXE](https://github.com/samhiq/SamhiqMailer/releases/latest/download/SamhiqMailer.exe)

**Setup Instructions:**

1. Create a folder named `SamhiqMailer`  
2. Move the downloaded `SamhiqMailer.exe` into this folder  
3. Double-click to launch  

> ⚠️ The folder name must be `SamhiqMailer` for automatic updates to work correctly.

### Option 2 — <img src="https://img.shields.io/badge/Python-Install-blue?logo=python&logoColor=white&style=flat-square" alt="Python pip badge" height="20"/>

```bash
pip install samhiqmailer
samhiqmailer
```

---

## 🛠️ First Launch Setup

On first run, the app will ask for your:

- 📧 Gmail email address  
- 🔐 Gmail App Password (not your actual email password)

> Your login info is stored securely in a local file: `user_config.json`.  
> No data is ever uploaded or shared.

[📖 How to generate a Gmail App Password](https://support.google.com/accounts/answer/185833)

---

## 📤 Sending Emails (Workflow)

### Step 1 — Import Excel File

Your Excel file should look like this:

| Email              | Name     |
|--------------------|----------|
| user@example.com   | John     |
| jane@domain.com    | Jane     |

Click **📁 Import Excel** and select your `.xlsx` file.

---

### Step 2 — Compose Message

Use `{name}` for personalization:

```
Subject: Welcome, {name}!
Body: Hello {name}, thank you for joining us!
```

---

### Step 3 — Add Attachments (Optional)

Click **Add Attachment** and select one or more files.

---

### Step 4 — Send Emails

Click **Send Emails**. The app will:

- Send each email one by one  
- Retry failures automatically (up to 3 times)  
- Show progress in the log panel  

---

## 🔄 Auto-Update System

- ✅ Automatically checks for updates when the app starts  
- ⬇️ Downloads and installs silently  
- 🔐 Keeps your data and config intact  

---

## 🛡️ Windows Defender SmartScreen Notice

When launching `SamhiqMailer.exe` for the first time, Windows may show this message:

> **"Windows protected your PC"**  
> *Microsoft Defender SmartScreen prevented an unrecognized app from starting.*

### 💡 Why This Appears

This happens because the app is **not digitally signed** with a commercial certificate.  
Digital signing is usually done by large corporations — Samhiq Mailer is an independent tool.

### ✅ Trust & Safety

- The `.exe` is 100% safe if downloaded from the **official GitHub link**  
- It connects only to **Gmail SMTP** and **GitHub for updates**  
- Your credentials and data are stored **only on your device**

### ✔️ How to Proceed

1. Click **More info**  
2. Click **Run anyway**  

You will not see this message again after the first launch.

---

## 🔐 Privacy & Security

- 🔒 Credentials are stored locally  
- 🧱 No data leaves your system except to Gmail's SMTP server  
- 📴 Fully offline-capable except for email and updates  

Your privacy is our priority.

---

## 👤 Developer Info

**Md Sameer Iqbal (Samhiq)**  
📍 Simri Bakhtiyarpur, Bihar, India  
📧 [contact.samhiq@gmail.com](mailto:contact.samhiq@gmail.com)  
🔗 [GitHub: @samhiq](https://github.com/samhiq)

> Designed with care. Built for the community. Proudly developed in 🇮🇳 India.

---

## 📄 License

```
Samhiq Mailer — © Md Sameer Iqbal. All Rights Reserved.

Use and modify freely for personal or business use.
Redistribution allowed only with this license included.
Software is provided "as-is" without warranty of any kind.
```
