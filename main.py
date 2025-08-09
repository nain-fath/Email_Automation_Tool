import smtplib
import ssl
import json
import pandas as pd
from email.message import EmailMessage
import os
import tkinter as tk
from tkinter import messagebox

# Load email config
with open('config.json') as f:
    config = json.load(f)

smtp_server = config["smtp_server"]
port = config["smtp_port"]
sender_email = config["sender_email"]
password = config["password"]

context = ssl.create_default_context()

# Read email body template from file
with open('email_body.txt', 'r', encoding='utf-8') as f:
    email_body_template = f.read()

def send_email(to_email, subject, body, attachment_path):
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # DEBUG: print the body being sent
    print(f"\n--- Email body preview for {to_email} ---")
    print(body)
    print('--- End of email body ---\n')

    msg.set_content(body)

    # Attach the PDF report
    with open(attachment_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)

    msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.send_message(msg)

# Read recipients CSV
recipients = pd.read_csv('recipients.csv')

for _, row in recipients.iterrows():
    name = row['name']
    to_email = row['email']
    report_path = row['report_file']

    print(f"Preparing to send report to: {name} <{to_email}>")

    if pd.isna(to_email) or pd.isna(report_path) or not os.path.exists(report_path):
        print(f"⚠️ Skipping {name} due to missing email or missing report file.")
        continue

    # Format email body with recipient's name
    try:
        email_body = email_body_template.format(name=name)
    except Exception as e:
        print(f"❌ Error formatting email body for {name}: {e}")
        email_body = "Hello,\n\nPlease find your attached report."

    subject = f"Your Personalized Report, {name}"

    try:
        send_email(to_email, subject, email_body, report_path)
        print(f"📧 Email sent to {name} ({to_email})")
    except Exception as e:
        print(f"❌ Failed to send email to {name}: {e}")

# ✅ POPUP after all emails are processed
print("\n✅ All emails have been processed.\n")

# Show confirmation popup
root = tk.Tk()
root.withdraw()  # Hide the main window
messagebox.showinfo("Bulk Email Status", "✅ Your bulk emails have been sent successfully!")
root.destroy()
