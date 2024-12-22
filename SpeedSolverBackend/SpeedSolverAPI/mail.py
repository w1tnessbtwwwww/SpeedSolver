from app.utils.email_service.email_service import EmailService

from app.utils.verify_codes_generator.code_generator import generate_confirmation_code
import asyncio
service = EmailService()
asyncio.run(service.send_verify_code("Подтверждение регистрации", "example@exmaple.exm", generate_confirmation_code()))