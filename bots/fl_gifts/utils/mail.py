import smtplib
from dotenv import load_dotenv
import os
import asyncio
from email.mime.text import MIMEText

load_dotenv()

MY_ADDRESS = os.getenv('MAIL_ADDRESS')
PASSWORD = os.getenv('MAIL_PASSWORD')
mail = "Message_you_need_to_send"
mail_subject = 'test mail'


async def send_gmail(fro, to, mes, pas):
    try:
        msg = MIMEText(mes)
        msg['Subject'] = mail_subject
        msg['From'] = fro
        msg['To'] = to
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fro, pas)
        s.sendmail(fro, to, msg.as_string())
        s.quit()
        print('Письмо отправлено')
    except:
        print('При отправке письма возникла ошибка(')

async def main():
    await send_gmail(MY_ADDRESS, MY_ADDRESS, mail, PASSWORD)


if __name__ == '__main__':
    asyncio.run(main())
