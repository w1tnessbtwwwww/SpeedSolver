from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from app.cfg.settings import settings
from app.utils.result import Result, err, success

class EmailService:

    @staticmethod
    def send_verify_code(subject: str, send_to: str, code: int):
        smtp_server = 'smtp.mail.ru'
        smtp_port = 587
        smtp_username = settings.MAIL_EMAIL
        smtp_password = settings.MAIL_PASSWORD

        from_addr = settings.MAIL_EMAIL
        to_addr = send_to
        # Отправитель и получатель

        # Создание сообщения
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject

        # Текст сообщения
        msg.attach(MIMEText(str(code), 'plain'))

        # Отправка сообщения
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            text = msg.as_string()
            server.sendmail(from_addr, to_addr, text)
            print('Сообщение успешно отправлено')
        except Exception as e:
            print(f'Ошибка при отправке сообщения: {e}')
        finally:
            server.quit()