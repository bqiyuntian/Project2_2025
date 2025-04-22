import smtplib
import RPi.GPIO as GPIO
import time
from email.message import EmailMessage

channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

from_email_addr = "17605229265@163.com"
from_email_pass = "QSPWa32LkjeZ25kL"
to_email_addr = "17605229265@163.com"

last_send_time = 0

def callback(channel) :
  
    if GPIO.input(channel) :
        print ("water detected!")
     
    else :
        print ("water not detected!")
       
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime = 300)
GPIO.add_event_callback(channel, callback)

def send_email(subject, body) :
    global last_send_time
    current_time = time.time()
    
    if current_time - last_sent_time >= 6*60*60:
        server = smtplib.SMTP('smtp.163.com', 25)
        server.starttls()
        server.login(from_email_addr, from_email_pass)
   
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = from_email_addr
        msg['To'] = to_email_addr

        server.send_message(msg)
        server.quit()    
        print ("email sent")
        last_send_time = current_time
    else:
       print("time interval not reached, email not sent")
def main() :
    while True:
        current_time = time.localtime()
        current_hour = current_time.tm_hour + 8
        print ("current time hour:", current_hour)
     
        time.sleep(60*60)

        if current_hour % 6 == 0:
            current_value = GPIO.input(channel)
            status = "watter detected" if current_value else "water not detscted"
            subject = "soil sensor update"
            body =f"hello,the soil sensor status is: {status}"
            send_email(subject, body) 
           

if __name__== "__main__":
    main()
    
