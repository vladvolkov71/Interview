import email
import smtplib
import ssl
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser


def config_user():
    conf = configparser.ConfigParser()
    conf.read('mail.ini')
    name = conf["YANDEX"]["name"]
    passw = conf["YANDEX"]["password"]
    return name, passw


class YandexMail:
    def __init__(self, login_name, passw):
        self.login_name = login_name
        self.password = passw
        self.snmp_server = "smtp.yandex.ru"
        self.imap_server = "imap.yandex.ru"
        self.snmp_port = 465
        self.context = ssl.create_default_context()

    def send(self, recipients: list, message=None, subject=None):
        self.subject = subject
        self.recipients = recipients
        self.message = message
        msg = MIMEMultipart()
        msg['From'] = self.login_name
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message, 'plain', 'utf-8'))
        with smtplib.SMTP_SSL(self.snmp_server, self.snmp_port, context=self.context) as ms:
            try:
                ms.login(self.login_name, self.password)
                ms.sendmail(self.login_name, self.recipients, msg.as_string())
                print('Ваши письма(письмо) отправлены')
                ms.quit()
            except smtplib.SMTPAuthenticationError:
                print('Имя или пароль не верны')
                print('Ваши письма(письмо) НЕ отправлены')
            except smtplib.SMTPSenderRefused:
                print('Почтовый сервер отказал в отправке письма(писем).')
                print('Ваши письма(письмо) НЕ отправлены.')

    def receive(self, header=None):
        self.header = header
        mail = imaplib.IMAP4_SSL(self.imap_server)
        try:
            mail.login(self.login_name, self.password)
            mail.select("inbox")
            criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
            result, data = mail.uid('search', criterion)
            if not data[0].split():
                return f'Писем с подходящим заголовком {self.header} нет'
            else:
                latest_email_uid = data[0].split()[-1]
                result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
                raw_email = data[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
            mail.logout()
            return email_message
        except imaplib.IMAP4.error:
            return f'Имя/пароль не верны, или почтовый сервер не доступен'


if __name__ == '__main__':
    user_name, password = config_user()
    mail1 = YandexMail(user_name, password)
    mail1.send(['vasya@email.ru', 'petya@gmail.com'], 'Message1', 'Subject1')
    print(mail1.receive('rrr'))
