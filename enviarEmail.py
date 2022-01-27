import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailBot:

    def __init__(self, email_para, corpo, assunto, caminho_arquivo=None, nome_arquivo=None):
        self.host = 'smtp.gmail.com'
        self.port = '587'
        self.login = 'douglas.bot.rh.vagas@gmail.com'
        self.senha = '@Vagas123'
        self.email_para = email_para
        self.corpo = corpo
        self.assunto = assunto
        self.caminho_arquivo = caminho_arquivo
        self.nome_arquivo = nome_arquivo

    def enviar(self):
        server = smtplib.SMTP(self.host, self.port)
        server.ehlo()
        server.starttls()
        server.login(self.login, self.senha)

        email_msg = MIMEMultipart()
        email_msg['From'] = self.login
        email_msg['To'] = self.email_para
        email_msg['Subject'] = self.assunto
        email_msg.attach(MIMEText(self.corpo, 'html'))

        if self.nome_arquivo:
            caminho_arquivo_aux = self.caminho_arquivo + "\\" + self.nome_arquivo
            attchment = open(caminho_arquivo_aux, 'rb')

            att = MIMEBase('application', 'octet-stream')
            att.set_payload(attchment.read())
            encoders.encode_base64(att)

            att.add_header('Content-Disposition', f'attachment; filename = {self.nome_arquivo}')
            attchment.close()
            email_msg.attach(att)

        server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
        server.quit()