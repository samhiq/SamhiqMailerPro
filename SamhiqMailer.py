import sys
import os
import json
import time
import requests
import smtplib
import threading
import subprocess
import openpyxl
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QTextEdit, QPushButton, QProgressBar,
                            QTabWidget, QFileDialog, QMessageBox, QDialog, QGroupBox,
                            QFormLayout, QComboBox, QSpinBox, QCheckBox, QProgressDialog,
                            QDialogButtonBox, QSizePolicy, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr

# Configuration
CONFIG_FILE = 'user_config.json'
VERSION_URL = 'https://raw.githubusercontent.com/samhiq/SamhiqMailer/main/version.json'
NOTIFICATION_URL = 'https://raw.githubusercontent.com/samhiq/SamhiqMailer/main/notifications.json'
CURRENT_VERSION = "2.9"
EXE_NAME = "SamhiqMailer.exe"
os.makedirs('drafts', exist_ok=True)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

# Email services configuration
EMAIL_SERVICES = {
    "Gmail": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "use_tls": True,
        "description": "Gmail (Google Mail)"
    },
    "Outlook": {
        "smtp_server": "smtp-mail.outlook.com",
        "smtp_port": 587,
        "use_tls": True,
        "description": "Outlook (Microsoft)"
    },
    "Yahoo": {
        "smtp_server": "smtp.mail.yahoo.com",
        "smtp_port": 587,
        "use_tls": True,
        "description": "Yahoo Mail"
    },
    "Hotmail": {
        "smtp_server": "smtp-mail.outlook.com",
        "smtp_port": 587,
        "use_tls": True,
        "description": "Hotmail (Microsoft)"
    },
    "AOL": {
        "smtp_server": "smtp.aol.com",
        "smtp_port": 587,
        "use_tls": True,
        "description": "AOL Mail"
    },
    "iCloud": {
        "smtp_server": "smtp.mail.me.com",
        "smtp_port": 587,
        "use_tls": True,
        "description": "Apple iCloud Mail"
    },
    "Zoho": {
        "smtp_server": "smtp.zoho.com",
        "smtp_port": 587,
        "use_tls": True,
        "description": "Zoho Mail"
    },
    "Custom": {
        "smtp_server": "",
        "smtp_port": 587,
        "use_tls": True,
        "description": "Custom SMTP Server"
    }
}

config = load_config()
EMAIL_ADDRESS = config.get("email", "")
EMAIL_PASSWORD = config.get("password", "")
SENDER_NAME = config.get("sender_name", "Samhiq Mailer")
EMAIL_SERVICE = config.get("email_service", "Gmail")
SMTP_SERVER = config.get("smtp", EMAIL_SERVICES[EMAIL_SERVICE]["smtp_server"])
SMTP_PORT = int(config.get("port", EMAIL_SERVICES[EMAIL_SERVICE]["smtp_port"]))
USE_TLS = config.get("use_tls", EMAIL_SERVICES[EMAIL_SERVICE]["use_tls"])

# HTML Templates
html_template = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Email from {sender_name}</title>
  <style>
    body {{
      margin: 0;
      padding: 0;
      background: #f5f7fa;
      font-family: 'Segoe UI', Roboto, sans-serif;
      color: #333333;
    }}
    .container {{
      max-width: 620px;
      margin: 40px auto;
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
      overflow: hidden;
    }}
    .header {{
      background: linear-gradient(135deg, #004e92, #000428);
      color: #ffffff;
      padding: 35px 20px;
      text-align: center;
      font-size: 26px;
      font-weight: bold;
      letter-spacing: 1px;
      border-top-left-radius: 12px;
      border-top-right-radius: 12px;
    }}
    .body {{
      padding: 40px 30px 20px 30px;
    }}
    .body h2 {{
      color: #004e92;
      font-size: 22px;
      margin-bottom: 20px;
    }}
    .body p {{
      font-size: 16px;
      line-height: 1.7;
      margin-bottom: 20px;
    }}
    .signature {{
      font-size: 16px;
      margin-top: 40px;
      font-weight: 500;
    }}
    .signature strong {{
      color: #000428;
    }}
    .footer {{
      background: #f1f3f6;
      padding: 18px;
      text-align: center;
      font-size: 13px;
      color: #777777;
      border-bottom-left-radius: 12px;
      border-bottom-right-radius: 12px;
    }}
    .footer span {{
      color: #004e92;
      font-weight: bold;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      {sender_name}
    </div>
    <div class="body">
      <h2>Dear {name},</h2>
      <p>{content}</p><br>
      <div class="signature">
        Warm Regards,<br>
        <strong>{sender_name}</strong>
      </div>
    </div>
    <div class="footer">
      Sent using <span>Samhiq Mailer</span> – Designed & Developed by<br> Md Sameer Iqbal (Samhiq)
    </div>
  </div>
</body>
</html>"""

feedback_html_template = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Feedback Mail</title>
  <style>
    body {{
      font-family: 'Segoe UI', sans-serif;
      background-color: #f4f6f8;
      margin: 0;
      padding: 0;
    }}
    .container {{
      max-width: 600px;
      margin: 30px auto;
      background: #ffffff;
      border-radius: 10px;
      padding: 30px;
      box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }}
    h2 {{
      color: #0052cc;
      font-size: 22px;
      margin-bottom: 20px;
    }}
    p {{
      font-size: 16px;
      margin-bottom: 10px;
      color: #333;
    }}
    .footer {{
      margin-top: 30px;
      font-size: 13px;
      color: #777;
      text-align: center;
    }}
    .footer span {{
      color: #0052cc;
      font-weight: bold;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h2>📬 New Feedback Received</h2>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Mobile No:</strong> {mobile}</p>
    <p><strong>Message:</strong></p>
    <p>{message}</p>
    <div class="footer">
      Sent via <span>Samhiq Mailer</span> – Feedback System
    </div>
  </div>
</body>
</html>"""

class StyledButton(QPushButton):
    def __init__(self, text, icon=None, color=None, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        
        if icon:
            self.setIcon(QIcon(icon))
        
        self.color = color or "#2196F3"
        self.hover_color = self.adjust_color(self.color, 1.2)
        self.pressed_color = self.adjust_color(self.color, 0.8)
        
        self.update_style()
    
    def adjust_color(self, color, factor):
        color = QColor(color)
        h, s, v, a = color.getHsvF()
        return QColor.fromHsvF(h, s, min(1.0, v * factor), a).name()
    
    def update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
            }}
            QPushButton:pressed {{
                background-color: {self.pressed_color};
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #666666;
            }}
        """)

class EmailWorker(QThread):
    progress_update = pyqtSignal(int)
    status_update = pyqtSignal(str)
    log_update = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, recipients, subject, body, attachments):
        super().__init__()
        self.recipients = recipients
        self.subject = subject
        self.body = body
        self.attachments = attachments

    def run(self):
        total = len(self.recipients)
        self.log_update.emit("Connecting to SMTP server...")
        
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            if USE_TLS:
                server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            self.log_update.emit("✅ Logged in successfully.")
        except Exception as e:
            self.log_update.emit(f"❌ Failed to connect: {e}")
            return

        now = time.localtime()
        dt = {
            "{date}": time.strftime("%d-%m-%Y", now),
            "{time}": time.strftime("%H:%M:%S", now),
            "{sender_name}": SENDER_NAME,
            "{current_version}": CURRENT_VERSION,
        }

        for i, (email, name) in enumerate(self.recipients):
            msg = MIMEMultipart()
            msg['From'] = formataddr((SENDER_NAME, EMAIL_ADDRESS))
            msg['To'] = email
            msg['Subject'] = self.subject

            personalized_body = self.body
            for tag, value in dt.items():
                personalized_body = personalized_body.replace(tag, value)
            personalized_body = personalized_body.replace("{name}", name)

            content_html = html_template.format(name=name, content=personalized_body, sender_name=SENDER_NAME)
            msg.attach(MIMEText(content_html, 'html'))

            for filepath in self.attachments:
                with open(filepath, 'rb') as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(filepath))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(filepath)}"'
                    msg.attach(part)

            for attempt in range(3):
                try:
                    self.log_update.emit(f"Sending to {email} (Attempt {attempt+1}/3)...")
                    server.send_message(msg)
                    self.log_update.emit(f"✅ Email sent to {email}")
                    break
                except Exception as e:
                    self.log_update.emit(f"Retry {attempt+1} failed for {email}: {e}")
                    if attempt == 2:
                        self.log_update.emit(f"❌ Failed to send to {email} after 3 attempts")

            progress = int(((i + 1) / total) * 100)
            self.progress_update.emit(progress)
            self.status_update.emit(f"Sending... ({i + 1}/{total})")
            time.sleep(0.3)

        server.quit()
        self.status_update.emit(f"✅ Sent {total} emails successfully.")
        self.log_update.emit("All emails sent successfully.")
        self.finished.emit(total)

class UpdateWorker(QThread):
    update_status = pyqtSignal(str, bool)
    progress = pyqtSignal(int)
    update_available = pyqtSignal(str, str)
    no_update = pyqtSignal()
    
    def __init__(self, auto_check=True):
        super().__init__()
        self.auto_check = auto_check
        self.temp_file = "update_temp.exe"
        self.backup_file = "backup_old.exe"

    def run(self):
        try:
            self.update_status.emit("Checking for updates...", False)
            latest_version, download_url = self.check_version()
            
            if latest_version > CURRENT_VERSION:
                self.update_available.emit(latest_version, download_url)
            else:
                if not self.auto_check:
                    self.no_update.emit()
                
        except Exception as e:
            self.update_status.emit(f"Failed to check updates: {str(e)}", True)

    def check_version(self):
        response = requests.get(VERSION_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("version"), data.get("download_url")

    def download_update(self, url):
        try:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                downloaded = 0
                
                with open(self.temp_file, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            progress = int((downloaded / total_size) * 100)
                            self.progress.emit(progress)
            return True
        except Exception as e:
            self.update_status.emit(f"Download failed: {str(e)}", True)
            return False

    def verify_download(self):
        if not os.path.exists(self.temp_file):
            raise Exception("Downloaded file not found")
        if os.path.getsize(self.temp_file) < 1024:
            raise Exception("Downloaded file is too small")
        return True

    def apply_update(self):
        updater_script = f"""@echo off
timeout /t 1 /nobreak >nul
taskkill /f /im "{EXE_NAME}" >nul 2>&1
move "{EXE_NAME}" "{self.backup_file}" >nul
move "{self.temp_file}" "{EXE_NAME}" >nul
start "" "{EXE_NAME}"
del "{self.backup_file}" >nul
del "%~f0"
"""
        with open("apply_update.bat", "w") as f:
            f.write(updater_script)
        
        subprocess.Popen(["apply_update.bat"], shell=True)
        QApplication.quit()

class NotificationWorker(QThread):
    notifications_fetched = pyqtSignal(str)

    def run(self):
        try:
            resp = requests.get(NOTIFICATION_URL, timeout=5)
            data = resp.json()
            notification_text = """
            <html>
            <head>
            <style>
                .notification-container {
                    font-family: 'Segoe UI', Arial, sans-serif;
                    color: #333333;
                }
                .notification {
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                    border-bottom: 1px solid #e0e0e0;
                }
                .date {
                    color: #004e92;
                    font-size: 10pt;
                    font-weight: 600;
                    margin-bottom: 4px;
                }
                .title {
                    color: #222222;
                    font-size: 10.5pt;
                    font-weight: 600;
                    margin-bottom: 6px;
                }
                .message {
                    color: #444444;
                    font-size: 10pt;
                    line-height: 1.4;
                }
            </style>
            </head>
            <body>
            <div class="notification-container">
            """
            
            for item in data.get("notifications", []):
                entry = f"""
                <div class="notification">
                    <div class="date">📅 {item.get('date', '')}</div>
                    <div class="title">📝 {item.get('title')}</div>
                    <div class="message">{item.get('message')}</div>
                </div>
                """
                notification_text += entry
            
            notification_text += "</div></body></html>"
            self.notifications_fetched.emit(notification_text)
        except Exception as e:
            error_msg = f"""
            <html>
            <body style="font-family: 'Segoe UI'; color: #d32f2f;">
            ❌ Could not fetch notifications: {e}
            </body>
            </html>
            """
            self.notifications_fetched.emit(error_msg)

class SamhiqMailerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.attachments = []
        self.recipients = []
        self.email_worker = None
        self.notification_worker = None
        self.update_worker = None
        self.update_dialog = None
        
        self.init_ui()
        self.setup_update_handler()
        self.cleanup_old_files()
        self.check_for_update(auto=True)
        self.fetch_notifications()
        self.apply_theme()

    def init_ui(self):
        self.setWindowTitle(f"Samhiq Mailer Pro v{CURRENT_VERSION}")
        self.setGeometry(100, 100, 1100, 800)
        
        # Set window icon
        self.setWindowIcon(QIcon("icon.png"))  # Make sure to have an icon.png file
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # App title
        title = QLabel("Samhiq Mailer")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setWeight(QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #004e92;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Version label
        version_label = QLabel(f"v{CURRENT_VERSION}")
        version_label.setStyleSheet("color: #666666; font-style: italic;")
        header_layout.addWidget(version_label)
        
        main_layout.addWidget(header)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #e0e0e0;")
        main_layout.addWidget(separator)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                padding: 8px 12px;
                min-width: 100px;
                background: #f5f5f5;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #004e92;
            }
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                background: white;
            }
        """)
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_mailer_tab()
        self.create_notification_tab()
        self.create_feedback_tab()
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

    def create_mailer_tab(self):
        mailer_widget = QWidget()
        self.tab_widget.addTab(mailer_widget, "📧 Mailer")
        
        layout = QVBoxLayout(mailer_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # Button row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        self.settings_btn = StyledButton("⚙️ Settings", color="#FFB300")
        self.settings_btn.clicked.connect(self.configure_user_credentials)
        button_layout.addWidget(self.settings_btn)
        
        self.import_btn = StyledButton("📁 Import Excel", color="#2196F3")
        self.import_btn.clicked.connect(self.import_excel)
        button_layout.addWidget(self.import_btn)
        
        self.attach_btn = StyledButton("📎 Attach", color="#2196F3")
        self.attach_btn.clicked.connect(self.add_attachment)
        button_layout.addWidget(self.attach_btn)
        
        self.clear_btn = StyledButton("🧹 Clear", color="#F44336")
        self.clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_btn)
        
        self.send_btn = StyledButton("🚀 Send", color="#4CAF50")
        self.send_btn.clicked.connect(self.start_sending)
        button_layout.addWidget(self.send_btn)
        
        self.update_btn = StyledButton("🔄 Update", color="#9C27B0")
        self.update_btn.clicked.connect(lambda: self.check_for_update(auto=False))
        button_layout.addWidget(self.update_btn)
        
        layout.addLayout(button_layout)
        
        # Form section
        form_group = QGroupBox("Compose Email")
        form_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                color: #004e92;
                font-weight: bold;
            }
        """)
        form_layout = QVBoxLayout(form_group)
        form_layout.setSpacing(10)
        
        # Recipient fields
        recipient_layout = QHBoxLayout()
        recipient_layout.setSpacing(10)
        
        email_label = QLabel("Recipient Email:")
        email_label.setStyleSheet("font-weight: bold;")
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("user@example.com")
        recipient_layout.addWidget(email_label)
        recipient_layout.addWidget(self.email_entry)
        
        name_label = QLabel("Recipient Name:")
        name_label.setStyleSheet("font-weight: bold;")
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Optional")
        recipient_layout.addWidget(name_label)
        recipient_layout.addWidget(self.name_entry)
        
        form_layout.addLayout(recipient_layout)
        
        # Subject
        subject_label = QLabel("Subject:")
        subject_label.setStyleSheet("font-weight: bold;")
        self.subject_entry = QLineEdit()
        self.subject_entry.setPlaceholderText("Email subject here...")
        form_layout.addWidget(subject_label)
        form_layout.addWidget(self.subject_entry)
        
        # Body
        body_label = QLabel("Message Body:")
        body_label.setStyleSheet("font-weight: bold;")
        self.body_text = QTextEdit()
        self.body_text.setPlaceholderText(
            "Write your email content here...\n\n"
            "Available tags:\n"
            "{name} - Recipient's name\n"
            "{sender_name} - Your sender name\n"
            "{date} - Current date\n"
            "{time} - Current time\n"
            "{current_version} - App version"
        )
        self.body_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        form_layout.addWidget(body_label)
        form_layout.addWidget(self.body_text)
        
        layout.addWidget(form_group)
        
        # Progress and status
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-weight: bold; color: #004e92;")
        layout.addWidget(self.status_label)
        
        # Log area
        log_group = QGroupBox("Activity Log")
        log_group.setStyleSheet(form_group.styleSheet())
        log_layout = QVBoxLayout(log_group)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMinimumHeight(120)
        self.log_area.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, monospace;
                font-size: 10pt;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        
        log_layout.addWidget(self.log_area)
        layout.addWidget(log_group)

    def create_notification_tab(self):
        notification_widget = QWidget()
        self.tab_widget.addTab(notification_widget, "🔔 Notifications")
        
        layout = QVBoxLayout(notification_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        self.refresh_btn = StyledButton("🔄 Refresh", color="#2196F3")
        self.refresh_btn.clicked.connect(self.fetch_notifications)
        layout.addWidget(self.refresh_btn)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        self.notification_area = QTextEdit()
        self.notification_area.setReadOnly(True)
        self.notification_area.setAcceptRichText(True)
        self.notification_area.setStyleSheet("""
            QTextEdit {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 12px;
            }
        """)
        
        scroll.setWidget(self.notification_area)
        layout.addWidget(scroll)

    def create_feedback_tab(self):
        feedback_widget = QWidget()
        self.tab_widget.addTab(feedback_widget, "💬 Feedback")
        
        layout = QVBoxLayout(feedback_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        form_group = QGroupBox("Send Feedback to Developer")
        form_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                color: #004e92;
                font-weight: bold;
            }
        """)
        form_layout = QVBoxLayout(form_group)
        
        # Name field
        name_label = QLabel("Your Name:")
        name_label.setStyleSheet("font-weight: bold;")
        self.fb_name = QLineEdit()
        self.fb_name.setPlaceholderText("Your name")
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.fb_name)
        
        # Mobile field
        mobile_label = QLabel("Mobile Number:")
        mobile_label.setStyleSheet("font-weight: bold;")
        self.fb_mobile = QLineEdit()
        self.fb_mobile.setPlaceholderText("Optional but helpful for response")
        form_layout.addWidget(mobile_label)
        form_layout.addWidget(self.fb_mobile)
        
        # Message field
        message_label = QLabel("Your Feedback:")
        message_label.setStyleSheet("font-weight: bold;")
        self.fb_message = QTextEdit()
        self.fb_message.setPlaceholderText("Describe your feedback, suggestions, or issues...")
        self.fb_message.setMinimumHeight(120)
        self.fb_message.setStyleSheet("""
            QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        form_layout.addWidget(message_label)
        form_layout.addWidget(self.fb_message)
        
        layout.addWidget(form_group)
        
        # Submit button
        self.submit_btn = StyledButton("📨 Submit Feedback", color="#4CAF50")
        self.submit_btn.clicked.connect(self.send_feedback)
        layout.addWidget(self.submit_btn)
        
        layout.addStretch()

    def apply_theme(self):
        palette = QApplication.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, Qt.white)
        palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.black)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, Qt.black)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        QApplication.setPalette(palette)

    def setup_update_handler(self):
        self.update_dialog = QProgressDialog("", None, 0, 100, self)
        self.update_dialog.setWindowTitle("Update Check")
        self.update_dialog.setWindowModality(Qt.WindowModal)
        self.update_dialog.setCancelButton(None)
        self.update_dialog.setAutoClose(False)
        self.update_dialog.setMinimumDuration(0)
        self.update_dialog.reset()

    def cleanup_old_files(self):
        for f in ["update_temp.exe", "backup_old.exe", "apply_update.bat"]:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass

    def check_for_update(self, auto=False):
        if hasattr(self, 'update_worker') and self.update_worker and self.update_worker.isRunning():
            return
            
        self.update_worker = UpdateWorker(auto)
        self.update_worker.update_status.connect(self.handle_update_status)
        self.update_worker.progress.connect(self.update_dialog.setValue)
        self.update_worker.update_available.connect(self.on_update_available)
        self.update_worker.no_update.connect(self.on_no_update)
        self.update_worker.finished.connect(self.on_update_finished)
        
        if not auto:
            self.update_dialog.setLabelText("Checking for updates...")
            self.update_dialog.show()
        
        self.update_worker.start()

    def handle_update_status(self, message, is_error):
        self.update_dialog.setLabelText(message)
        if is_error:
            QTimer.singleShot(2000, self.update_dialog.close)
            if not self.update_worker.auto_check:
                QMessageBox.critical(self, "Update Error", message)

    def show_update_status(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Status")
        dialog.setFixedSize(500, 300)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(30, 30, 30, 20)
        layout.setSpacing(20)
        
        title_label = QLabel("Up to Date")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #004e92;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        
        version_label = QLabel(f"You are using the latest version (v{CURRENT_VERSION})")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("font-size: 11pt;")
        layout.addWidget(version_label, alignment=Qt.AlignCenter)
        
        ok_btn = StyledButton("OK", color="#4CAF50")
        ok_btn.clicked.connect(dialog.accept)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        dialog.move(self.geometry().center() - dialog.rect().center())
        dialog.exec_()

    def on_update_available(self, version, download_url):
        self.update_dialog.setLabelText(f"Version {version} available!")
        reply = QMessageBox.question(
            self, "Update Available",
            f"A new version {version} is available. Update now?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.update_dialog.setLabelText("Downloading update...")
            self.update_dialog.setRange(0, 100)
            
            if self.update_worker.download_update(download_url):
                try:
                    self.update_dialog.setLabelText("Verifying update...")
                    if self.update_worker.verify_download():
                        self.update_dialog.setLabelText("Applying update...")
                        self.update_worker.apply_update()
                except Exception as e:
                    self.update_status.emit(f"Update failed: {str(e)}", True)
        else:
            self.update_dialog.close()

    def on_no_update(self):
        if not self.update_worker.auto_check:
            self.show_update_status()
        self.update_dialog.close()

    def on_update_finished(self):
        if not self.update_dialog.wasCanceled():
            self.update_dialog.reset()

    def log(self, message):
        self.log_area.append(message)
        self.log_area.verticalScrollBar().setValue(self.log_area.verticalScrollBar().maximum())

    def configure_user_credentials(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Configure Email Settings")
        dialog.setModal(True)
        dialog.resize(500, 500)
        
        layout = QVBoxLayout(dialog)
        
        # Email Service Selection
        service_group = QGroupBox("📧 Email Service Provider")
        service_layout = QVBoxLayout(service_group)
        
        service_label = QLabel("Select your email service:")
        service_label.setStyleSheet("font-weight: bold;")
        service_layout.addWidget(service_label)
        
        service_combo = QComboBox()
        for service_name, service_info in EMAIL_SERVICES.items():
            service_combo.addItem(f"{service_info['description']}", service_name)
        
        current_service = config.get("email_service", "Gmail")
        service_index = service_combo.findData(current_service)
        if service_index >= 0:
            service_combo.setCurrentIndex(service_index)
        
        service_layout.addWidget(service_combo)
        layout.addWidget(service_group)
        
        # Email Credentials
        creds_group = QGroupBox("🔐 Email Credentials")
        creds_layout = QFormLayout(creds_group)
        
        email_label = QLabel("Email Address:")
        email_label.setStyleSheet("font-weight: bold;")
        email_entry = QLineEdit(EMAIL_ADDRESS)
        email_entry.setPlaceholderText("your.email@gmail.com")
        creds_layout.addRow(email_label, email_entry)
        
        pass_label = QLabel("App Password:")
        pass_label.setStyleSheet("font-weight: bold;")
        pass_entry = QLineEdit(EMAIL_PASSWORD)
        pass_entry.setEchoMode(QLineEdit.Password)
        pass_entry.setPlaceholderText("App Password (not regular password)")
        creds_layout.addRow(pass_label, pass_entry)
        
        name_label = QLabel("Sender Name:")
        name_label.setStyleSheet("font-weight: bold;")
        name_entry = QLineEdit(SENDER_NAME)
        name_entry.setPlaceholderText("Your Name or Organization")
        creds_layout.addRow(name_label, name_entry)
        
        layout.addWidget(creds_group)
        
        # Custom SMTP Settings
        smtp_group = QGroupBox("🛠️ Custom SMTP Settings")
        smtp_layout = QFormLayout(smtp_group)
        
        smtp_server_label = QLabel("SMTP Server:")
        smtp_server_label.setStyleSheet("font-weight: bold;")
        smtp_server_entry = QLineEdit()
        smtp_server_entry.setPlaceholderText("smtp.yourserver.com")
        smtp_layout.addRow(smtp_server_label, smtp_server_entry)
        
        smtp_port_label = QLabel("SMTP Port:")
        smtp_port_label.setStyleSheet("font-weight: bold;")
        smtp_port_entry = QSpinBox()
        smtp_port_entry.setRange(1, 65535)
        smtp_port_entry.setValue(587)
        smtp_layout.addRow(smtp_port_label, smtp_port_entry)
        
        use_tls_check = QCheckBox("Use TLS/STARTTLS")
        use_tls_check.setChecked(True)
        smtp_layout.addRow("Security:", use_tls_check)
        
        layout.addWidget(smtp_group)
        
        def on_service_changed():
            selected_service = service_combo.currentData()
            if selected_service == "Custom":
                smtp_group.show()
                smtp_server_entry.setText(config.get("smtp", ""))
                smtp_port_entry.setValue(int(config.get("port", 587)))
                use_tls_check.setChecked(config.get("use_tls", True))
            else:
                smtp_group.hide()
                service_info = EMAIL_SERVICES[selected_service]
                smtp_server_entry.setText(service_info["smtp_server"])
                smtp_port_entry.setValue(service_info["smtp_port"])
                use_tls_check.setChecked(service_info["use_tls"])
        
        service_combo.currentTextChanged.connect(on_service_changed)
        on_service_changed()
        
        # Help text
        help_text = QLabel("""
        <b>📝 Setup Instructions:</b><br>
        • <b>Gmail:</b> Use App Password (not regular password)<br>
        • <b>Outlook/Hotmail:</b> Enable 2-factor auth and use App Password<br>
        • <b>Yahoo:</b> Generate App Password in Account Security<br>
        • <b>Custom:</b> Enter your own SMTP server details
        """)
        help_text.setWordWrap(True)
        help_text.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #bbdefb;
            }
        """)
        layout.addWidget(help_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        test_btn = StyledButton("🧪 Test Connection", color="#FF9800")
        test_btn.clicked.connect(lambda: self.test_smtp_connection(
            smtp_server_entry.text(),
            smtp_port_entry.value(),
            use_tls_check.isChecked(),
            email_entry.text(),
            pass_entry.text()
        ))
        button_layout.addWidget(test_btn)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        button_layout.addWidget(button_box)
        
        layout.addLayout(button_layout)
        
        if dialog.exec_() == QDialog.Accepted:
            config['email'] = email_entry.text().strip()
            config['password'] = pass_entry.text().strip()
            config['sender_name'] = name_entry.text().strip()
            config['email_service'] = service_combo.currentData()
            config['smtp'] = smtp_server_entry.text().strip()
            config['port'] = smtp_port_entry.value()
            config['use_tls'] = use_tls_check.isChecked()
            
            save_config(config)
            
            QMessageBox.information(self, "✅ Settings Saved", 
                f"Email settings updated successfully!\n\n"
                f"Service: {EMAIL_SERVICES[config['email_service']]['description']}\n"
                f"Server: {config['smtp']}:{config['port']}\n"
                f"TLS: {'Enabled' if config['use_tls'] else 'Disabled'}\n\n"
                f"Please restart the application to apply changes.")

    def test_smtp_connection(self, server, port, use_tls, email, password):
        if not all([server, port, email, password]):
            QMessageBox.warning(self, "Missing Information", "Please fill all fields before testing.")
            return
        
        progress = QProgressDialog("Testing connection...", "Cancel", 0, 0, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setAutoClose(False)
        progress.setAutoReset(False)
        progress.show()
        
        def test_connection():
            try:
                test_server = smtplib.SMTP(server, port)
                if use_tls:
                    test_server.starttls()
                test_server.login(email, password)
                test_server.quit()
                return True, "Connection successful!"
            except Exception as e:
                return False, str(e)
        
        def run_test():
            success, message = test_connection()
            progress.close()
            
            if success:
                QMessageBox.information(self, "✅ Connection Successful", 
                    f"Successfully connected to {server}:{port}\n\n"
                    f"Your email settings are working correctly!")
            else:
                QMessageBox.critical(self, "❌ Connection Failed", 
                    f"Failed to connect to {server}:{port}\n\n"
                    f"Error: {message}\n\n"
                    f"Please check your settings and try again.")
        
        threading.Thread(target=run_test, daemon=True).start()

    def import_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel files (*.xlsx)")
        if not file_path:
            return
        
        try:
            wb = openpyxl.load_workbook(file_path)
            sheet = wb.active
            self.recipients = []
            
            for row in sheet.iter_rows(min_row=2, values_only=True):
                email, name = row[:2]
                if email:
                    self.recipients.append((email, name or ""))
            
            QMessageBox.information(self, "Imported", f"Imported {len(self.recipients)} recipients.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import Excel file: {str(e)}")

    def add_attachment(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files to Attach")
        if files:
            self.attachments.extend(files)
            QMessageBox.information(self, "Attached", f"Added {len(files)} file(s).")

    def clear_all(self):
        self.subject_entry.clear()
        self.body_text.clear()
        self.email_entry.clear()
        self.name_entry.clear()
        self.attachments.clear()
        self.recipients.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("Ready")
        self.log_area.clear()

    def start_sending(self):
        subject = self.subject_entry.text().strip()
        body = self.body_text.toPlainText().strip()
        
        manual_email = self.email_entry.text().strip()
        manual_name = self.name_entry.text().strip() or "User"
        
        if manual_email:
            self.recipients.append((manual_email, manual_name))
        
        if not subject or not body or not self.recipients:
            QMessageBox.warning(self, "Missing Info", "Enter subject, body, and at least one recipient.")
            return
        
        self.email_worker = EmailWorker(self.recipients.copy(), subject, body, self.attachments.copy())
        self.email_worker.progress_update.connect(self.progress_bar.setValue)
        self.email_worker.status_update.connect(self.status_label.setText)
        self.email_worker.log_update.connect(self.log)
        self.email_worker.finished.connect(self.on_emails_sent)
        self.email_worker.start()

    def on_emails_sent(self, count):
        QMessageBox.information(self, "Done", f"Sent {count} emails successfully.")

    def send_feedback(self):
        name = self.fb_name.text().strip()
        mobile = self.fb_mobile.text().strip()
        message = self.fb_message.toPlainText().strip()
        
        if not name or not message:
            QMessageBox.warning(self, "Incomplete", "Name and message fields are required.")
            return
        
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            
            msg = MIMEMultipart()
            msg['From'] = formataddr((name, EMAIL_ADDRESS))
            msg['To'] = "contact.samhiq@gmail.com"
            msg['Subject'] = f"User Feedback from {name}"
            
            content = feedback_html_template.format(
                name=name, 
                mobile=mobile, 
                message=message.replace('\n', '<br>')
            )
            msg.attach(MIMEText(content, 'html'))
            
            server.send_message(msg)
            server.quit()
            
            QMessageBox.information(self, "Submitted", "Developer has received your request and will reply at the earliest.")
            
            self.fb_name.clear()
            self.fb_mobile.clear()
            self.fb_message.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send feedback: {str(e)}")

    def fetch_notifications(self):
        self.notification_area.setText("<span style='font-size:10pt;'>🔄 Fetching notifications...</span>")
        
        self.notification_worker = NotificationWorker()
        self.notification_worker.notifications_fetched.connect(self.notification_area.setHtml)
        self.notification_worker.start()

def main():
    # Clean up any previous update files
    for f in ["update_temp.exe", "backup_old.exe", "apply_update.bat"]:
        try:
            if os.path.exists(f):
                os.remove(f)
        except:
            pass
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setApplicationName("Samhiq Mailer")
    app.setApplicationVersion(CURRENT_VERSION)
    app.setOrganizationName("Samhiq")
    
    window = SamhiqMailerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()