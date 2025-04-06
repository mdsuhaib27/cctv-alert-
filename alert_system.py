import smtplib
import cv2
import time
import requests
from datetime import datetime
from playsound import playsound
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Email setup
SENDER_EMAIL = " cvbv"
SENDER_PASSWORD = "x x "
RECEIVER_EMAIL = "  xx "

# Telegram setup
BOT_TOKEN = "hbjij "
CHAT_ID = "9099 "

# Delay tracker
last_email_time = 0

def play_alarm():
    try:
        playsound("alert.mp3")
        print("[ALARM] Sound played.")
    except Exception as e:
        print(f"[ERROR] Alarm sound failed: {e}")

def send_alert(subject, message, frame=None):
    global last_email_time

    current_time = time.time()
    if current_time - last_email_time < 30:
        print("[INFO] Alert skipped due to 30s delay.")
        return

    last_email_time = current_time
    play_alarm()

    # 📅 Timestamp
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # 🌍 Live GPS (Replace with dynamic values)
    latitude = 13.0827
    longitude = 80.2707
    maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

    # Save snapshot
    snapshot_path = "snapshot.jpg"
    if frame is not None:
        cv2.imwrite(snapshot_path, frame)

    # ======= EMAIL ALERT =======
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"{subject} | {timestamp}"

        email_body = f"""
        ALERT: {subject}

        MESSAGE:
        {message}

        📅 Date & Time: {timestamp}

        📍 GPS Location: {latitude}, {longitude}
        🌐 Maps Link: {maps_link}
        """

        msg.attach(MIMEText(email_body, 'plain'))

        if frame is not None:
            with open(snapshot_path, "rb") as f:
                image = MIMEApplication(f.read(), Name="snapshot.jpg")
                image['Content-Disposition'] = 'attachment; filename="snapshot.jpg"'
                msg.attach(image)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        print("[EMAIL] Alert sent successfully.")

    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

    # ======= TELEGRAM ALERT =======
    try:
        # Text alert
        text = f"""🚨 {subject}
{message}
📅 {timestamp}
📍 [Live GPS Location]({maps_link})"""
        
        text_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        text_data = {
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }
        response = requests.post(text_url, data=text_data)
        print(f"[TELEGRAM TEXT] Status Code: {response.status_code}")

        # Photo with caption
        if frame is not None:
            photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            with open(snapshot_path, "rb") as photo:
                files = {
                    "photo": photo
                }
                data = {
                    "chat_id": CHAT_ID,
                    "caption": f"{subject}\n📅 {timestamp}\n📍 [GPS]({maps_link})",
                    "parse_mode": "Markdown"
                }
                photo_response = requests.post(photo_url, data=data, files=files)
                print(f"[TELEGRAM PHOTO] Status Code: {photo_response.status_code}")

    except Exception as e:
        print(f"[ERROR] Failed to send Telegram alert: {e}")
