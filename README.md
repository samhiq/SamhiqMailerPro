# 📬 Samhiq Mailer

**Samhiq Mailer** is a sleek and powerful desktop application for sending personalized bulk emails using your own SMTP credentials. It’s built for speed, simplicity, and reliability — with automatic updates, Excel import, HTML formatting, and real-time logging.

---

## ✨ Features

✅ Modern and easy-to-use interface  
✅ Send emails via your Gmail, Yahoo, Outlook or custom SMTP  
✅ Automatically prompts email credentials on first use  
✅ Personalize messages using `{name}` in your content  
✅ Import recipient list directly from Excel (.xlsx)  
✅ Attach multiple files to your emails  
✅ Retry failed emails automatically (up to 3 times)  
✅ Real-time progress bar during sending and downloading  
✅ Auto-update system — always stay up-to-date  
✅ Detailed log window with email-by-email feedback  
✅ No programming knowledge needed — ready to use!

---

## 🚀 Getting Started

1. **📥 Download the latest version**  
   👉 [Click here to download SamhiqMailer.exe](https://github.com/samhiq/SamhiqMailer/releases/latest/download/SamhiqMailer.exe)

2. **📁 Folder Setup & First Use Instructions**  
   - After downloading, **create a new folder named exactly:**
     ```
     SamhiqMailer
     ```
   - Move the downloaded `SamhiqMailer.exe` into this folder.  
   - This folder name is **required** so that the auto-update system works correctly.
   - Double-click the `.exe` to launch the app.
   - On the **first run**, the app will ask you to enter:
     - Your **email address**
     - Your **app password** (do not use your main email password)
   - These credentials are securely stored in a local config file and only asked once.

3. **📊 Add Recipients**  
   - Option 1: Click **📁 Import Excel** and upload a `.xlsx` file with **Email** in column A and **Name** in column B.
   - Option 2: Manually enter a single recipient using the input fields.

4. **📝 Compose Your Email**  
   - Fill in the subject and message body.
   - Use `{name}` in your message to auto-insert recipient names.

5. **📎 Attach Files (optional)**  
   - Click **📎 Add Attachment** to include one or more files with the email.

6. **📤 Send**  
   - Click **🚀 Send Emails** — the app will take care of the rest!

---

## 🔄 Auto Update Feature

Samhiq Mailer checks for updates automatically on launch.

- You’ll get a notification if a new version is available.
- One click downloads the latest `.exe`, replaces the old one, and restarts the app.
- Manual check is also available via the **🆕 Check for Updates** button.

📂 Your data and configurations remain intact after updates.

---

## 📁 Excel Format Example

| Email              | Name     |
|--------------------|----------|
| user@example.com   | John     |
| jane@domain.com    | Jane     |

---

## 🔐 Privacy & Security Notice

This application requires your **email and app password** to send messages through your own SMTP server. These credentials are:

- Stored securely **only on your device** in a local file.
- Never uploaded or shared online.
- Used solely for the purpose of sending your emails.

We value your privacy. Your data stays with you.

---

## ⚠️ Windows Defender SmartScreen Notice

Since this app is **not digitally signed with a code-signing certificate**, Windows may show a warning like:

> **"Windows protected your PC"**  
> *Microsoft Defender SmartScreen prevented an unrecognized app from starting.*

This does **not mean the file is unsafe** — it simply means the `.exe` is not signed by a known publisher.

### ✅ Here's how to proceed:

1. When you see the warning, click **More info**.
2. Then click the **Run anyway** button.

> 🔐 Once the app gains trust and more downloads, SmartScreen will stop flagging it automatically.  
> 💡 You can also consider building trust by code-signing the `.exe` in the future (paid option).

---

## 👨‍💻 Developer Info

**Md Sameer Iqbal (Samhiq)**  
📧 [contact.samhiq@gmail.com](mailto:contact.samhiq@gmail.com)  
🔗 [GitHub: samhiq](https://github.com/samhiq)

> 💡 Designed, developed and maintained with passion.  
> 🇮🇳 Proudly made in India.

---

## 📌 License

This software is free to use and distribute. Commercial use is allowed.  
© 2025 Md Sameer Iqbal (Samhiq)
