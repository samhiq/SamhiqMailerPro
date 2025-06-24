# 📬 Samhiq Mailer

**Samhiq Mailer** is a sleek and powerful desktop application for sending personalized bulk emails using your own SMTP credentials. It’s built for speed, simplicity, and reliability — with automatic updates, Excel import, HTML formatting, retry logic, and real-time logging.

<p align="center">
  <img src="SamhiqMailer.png" alt="Samhiq Mailer Screenshot" width="700">
</p>

---

## ✨ Features

✅ Modern and easy-to-use interface  
✅ Send emails via Gmail, Yahoo, Outlook, or any SMTP provider  
✅ Automatically prompts for email credentials on first use  
✅ Personalize messages using `{name}` in your content  
✅ Import recipient list from Excel (.xlsx)  
✅ Attach multiple files with ease  
✅ Retries failed emails automatically (up to 3 times)  
✅ Real-time progress bar during sending & downloading  
✅ Auto-update system to stay up-to-date  
✅ Detailed log window with real-time status  
✅ Fully portable — no installation required  

---

## 🚀 Getting Started

### 1. 📥 Download the App  
👉 [Download SamhiqMailer.exe](https://github.com/samhiq/SamhiqMailer/releases/latest/download/SamhiqMailer.exe)

### 2. 🗂️ Setup Folder  
Create a folder named exactly SamhiqMailer:

Then place the `SamhiqMailer.exe` file inside this folder.  
⚠️ This folder name is **required** so that the auto-update system works properly.

### 3. 🔐 First-Time Launch  
- Double-click the `.exe` to open the app.
- You'll be prompted to enter:
  - Your **email address**
  - Your **app password** (never use your main password)
- These are securely stored locally and only asked once.

---

## 🧾 Compose & Send

### ➕ Add Recipients
- **Option 1**: Click **📁 Import Excel** and select a `.xlsx` file.
  - **Column A**: Email  
  - **Column B**: Name  
- **Option 2**: Use manual entry for a single recipient.

### 📝 Create Message
- Fill in the **subject** and **message body**.
- Use `{name}` in your message to personalize it (e.g., *Hello {name}!*).

### 📎 Attach Files (Optional)
Click **📎 Add Attachment** to include one or more files.

### 🚀 Send Emails
Click **Send Emails** and the application will take care of the rest.

---

## 🔄 Auto-Update System

Samhiq Mailer includes an **inbuilt updater**:

- On launch, it checks for a newer version.
- If available, it prompts to download and apply the update automatically.
- Your email configuration and settings are **not affected** by updates.

You can also manually trigger updates using the **🆕 Check for Updates** button.

---

## 🧠 Notes & Tips

- 📌 **Use App Passwords**: For Gmail, enable 2FA and use [App Passwords](https://support.google.com/accounts/answer/185833).
- 🔐 **Your data is private**: Email credentials are only stored on your own system in a local JSON file and never shared.
- 🪟 **SmartScreen / Windows Defender Warning**:
  - Since the app is not digitally signed, Windows may show a warning.
  - Click **More info → Run anyway** to proceed.  
  - This is expected for unsigned apps and does **not** indicate a virus.

---

## 📁 Excel Format Example

| Email              | Name     |
|--------------------|----------|
| user@example.com   | John     |
| jane@domain.com    | Jane     |

---

## 🔐 Privacy & Security Notice

- This tool does **not collect or transmit any personal data**.
- Your email and app password are stored **only on your computer**, in a file named `user_config.json`.
- We recommend using **app-specific passwords** for extra safety.
- Source code is available for full transparency.

---

## 👨‍💻 Developer Info

**Md Sameer Iqbal (Samhiq)**  
📧 [contact.samhiq@gmail.com](mailto:contact.samhiq@gmail.com)  
🔗 [GitHub: samhiq](https://github.com/samhiq)

> 💡 Designed, developed, and maintained with passion.  
> 🇮🇳 Proudly made in India.

---

## 📌 License

This software is free to use, modify, and distribute.  
Commercial use is allowed.  
© 2025 Md Sameer Iqbal (Samhiq)

---
