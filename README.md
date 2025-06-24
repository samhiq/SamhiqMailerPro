# 📬 Samhiq Mailer

**Samhiq Mailer** is a lightweight, high-performance desktop application for sending personalized bulk emails using your own SMTP credentials. Designed for professionals and teams, it features a simple UI, Excel support, retry mechanisms, and real-time logging — all with zero installation.

<p align="center">
  <img src="SamhiqMailer.png" alt="Samhiq Mailer Screenshot" width="700">
</p>

---

## 🚀 Key Features

- Modern, intuitive interface  
- Works with Gmail, Outlook, Yahoo, or any SMTP server  
- One-time login with secure local storage  
- Personalized emails using `{name}` placeholder  
- Import recipients from Excel (.xlsx)  
- Add multiple file attachments  
- Retry failed emails automatically (up to 3 times)  
- Real-time progress bar and detailed log view  
- Built-in auto-updater — no manual checks needed  
- Fully portable `.exe` — no installation required  

---

## 🛠️ Getting Started

### 1. Download the App

👉 [Download Latest Release](https://github.com/samhiq/SamhiqMailer/releases/latest/download/SamhiqMailer.exe)

---

### 2. Setup Folder

- Create a folder named exactly: `SamhiqMailer`  
- Place the downloaded `.exe` file inside this folder  

> ⚠️ **Important:** Folder name must be exactly `SamhiqMailer` for the auto-update system to work.

---

### 3. First Launch

- Double-click `SamhiqMailer.exe`  
- Enter your:
  - **Email address**
  - **App password** (Use an [App Password](https://support.google.com/accounts/answer/185833); never use your main password)  
- These are securely stored locally in a JSON file and not shared online.

---

## ✉️ Sending Emails

### Step 1: Import Recipients
Click **📁 Import Excel** and select your `.xlsx` file:
- **Column A** → Email  
- **Column B** → Name

You can also add a single recipient manually.

---

### Step 2: Compose Message

- Enter your **Subject** and **Message**
- Use `{name}` to personalize each message  
  _Example: `Hello {name}, welcome to our service!`_

---

### Step 3: Add Attachments *(Optional)*

Click **📎 Add Attachment** to include one or more files.

---

### Step 4: Send Emails

Click **Send Emails** and the tool handles the rest — showing live progress and logs for each recipient.

---

## 🔄 Auto-Update System

- Automatically checks for updates on launch  
- Prompts you to download and install the latest version  
- All settings and credentials remain safe during updates  
- Manual update check also available via **🆕 Check for Updates** button  

---

## 📊 Excel File Format Example

| Email              | Name     |
|--------------------|----------|
| user@example.com   | John     |
| jane@domain.com    | Jane     |

Ensure your file follows this format before importing.

---

## 🔐 Privacy & Security

- No data is collected or sent online  
- All credentials are stored **only on your local machine** in `user_config.json`  
- We strongly recommend using [App Passwords](https://support.google.com/accounts/answer/185833)  
- Open-source code available for transparency  

---

## ⚠️ Windows Defender / SmartScreen Warning

Because the `.exe` is not digitally signed:
- Windows may show a SmartScreen warning
- Click **More info → Run anyway** to proceed  
- This is expected and **does not indicate a virus**

---

## 👨‍💻 About the Developer

**Md Sameer Iqbal (Samhiq)**  
📍 Bihar, India  
📧 [contact.samhiq@gmail.com](mailto:contact.samhiq@gmail.com)  
🔗 [GitHub Profile](https://github.com/samhiq)

> Built with passion for reliability and simplicity.  
> 🇮🇳 Proudly developed in India.

---

## 📄 License

This software is free to use, modify, and distribute.  
✅ Commercial use is permitted  
© 2025 Md Sameer Iqbal (Samhiq)

---
