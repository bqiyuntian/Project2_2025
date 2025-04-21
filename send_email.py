import smtplib
from email.message import EmailMessage

#Set email and password and recipient emaic
from_email_addr = "17605229265@163.com"
from_email_pass = "QSPWa32LkjeZ25kL"
to_email_addr = "17605229265@163.com"

#creat a message objet
msg = EmailMessage()

#sent
body = "Hello from Raspberry Pi"
msg.set_content(body)

msg['From'] = from_email_addr
msg['To'] = to_email_addr

msg['Subject'] = 'TEST EMAIL'

server = smtplib.SMTP('smtp.163.com', 25)

server.starttls()

server.login(from_email_addr, from_email_pass)

server.send_message(msg)

print ('Email sent')

server.quit()
