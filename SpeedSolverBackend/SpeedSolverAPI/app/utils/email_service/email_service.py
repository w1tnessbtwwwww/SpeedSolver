from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from app.cfg.settings import settings
from app.utils.result import Result, err, success
from app.utils.verify_codes_generator.code_generator import generate_confirmation_code

class EmailService:

    @staticmethod
    async def send_verify_code(subject: str, send_to: str) -> str:
        smtp_server = 'smtp.mail.ru'
        smtp_port = 587

        print(settings.MAIL_EMAIL)
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


        code = generate_confirmation_code()
        # Текст сообщения
        msg.attach(MIMEText(f"Здравствуйте!\nВаш код подтверждения для регистрации в сервисе SpeedSolver: {code}"))

        # Отправка сообщения
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            text = msg.as_string()
            server.sendmail(from_addr, to_addr, text)
            print('Сообщение успешно отправлено')
            return code
        except Exception as e:
            print(f'Ошибка при отправке сообщения: {e}')
        finally:
            server.quit()