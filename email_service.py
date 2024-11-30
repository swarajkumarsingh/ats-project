import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("AWS_SES_FROM_MAIL_ID")

def send_email_to(to_email, subject, body_html, attachment_path=None):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['To'] = to_email
        msg['From'] = FROM_EMAIL

        body_part = MIMEText(body_html, 'html')
        msg.attach(body_part)

        if attachment_path:
            with open(attachment_path, 'rb') as f:
                part = MIMEApplication(f.read())
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
                msg.attach(part)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() 
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"Email sent: {to_email}")
    except smtplib.SMTPAuthenticationError as auth_err:
        print(f"Authentication Error: {auth_err}")
    except Exception as e:
        print(f"Error: {e}")



hr_body_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ATS Score Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .container {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }
        .header {
            background-color: #007bff;
            color: #fff;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
        }
        .content {
            padding: 20px;
        }
        .content p {
            font-size: 16px;
            line-height: 1.5;
        }
        .footer {
            background-color: #f4f4f4;
            padding: 10px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>ATS Score Results</h1>
        </div>
        <div class="content">
            <p>Dear Company and Team,</p>
            <p>We are pleased to inform you that the candidates who have passed the ATS score are included in the attached CSV file.</p>
            <p>For any further details or questions, please do not hesitate to reach out.</p>
            <p>Best regards,</p>
            <p>Company</p>
        </div>
        <div class="footer">
            <p>&copy; 2024 Company. All rights reserved.</p>
        </div>
    </div>
</body>
</html>

'''


def candidate_email_body(candidate_name):
    body_html = f'''
    <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Congratulations!</title>
</head>
<body style="font-family: Arial, sans-serif; color: #333; margin: 0; padding: 0; background-color: #f4f4f4;">
    <div style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #fff; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
        <div style="background-color: #28a745; color: #fff; padding: 20px; text-align: center;">
            <h1 style="margin: 0;">Congratulations!</h1>
        </div>
        <div style="padding: 20px;">
            <p style="font-size: 16px; line-height: 1.5;">Dear <span style="font-weight: bold; color: #007bff;">{candidate_name}</span>,</p>
            <p style="font-size: 16px; line-height: 1.5;">Congratulations on successfully clearing the ATS process!</p>
            <p style="font-size: 16px; line-height: 1.5;">We appreciate your efforts and look forward to the next steps.</p>
            <p style="font-size: 16px; line-height: 1.5;">Best regards,</p>
            <p style="font-size: 16px; line-height: 1.5;">Company</p>
        </div>
        <div style="background-color: #f4f4f4; padding: 10px; text-align: center;">
            <p style="margin: 0;">&copy; 2024 Company. All rights reserved.</p>
        </div>
    </div>
</body>
</html>

'''
    return body_html
