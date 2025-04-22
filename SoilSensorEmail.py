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

lastValue = -1
lastTime = 0

def callback(channel) :
    global lastValue
    if GPIO.input(channel) :
        print ("water detected!")
        lastValue = 1
    else :
        print ("water not detected!")
        lastValue = 0
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime = 300)
GPIO.add_event_callback(channel, callback)

def send_email(subject, body) :
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

def main() :
    global lastTime, lastValue
    while True:
        current_time = time.localtime()
        current_hour = current_time.tm_hour + 8
        print ("current time hour:", current_hour)
     
        if current_hour != lastTime:
            print ("time to send the first email of the day")
            send_email("test email", "hello from raspberry pi")
            lastTime = current_hour
  
        difference = current_hour - lastValue
        if difference > 3:
            print("time difference > 3. time to send an email")
            send_email("water needed", "please water your plant.")
            lastValue = current_hour

        else:
            print("hour difference < 4. Do not email")

        time.sleep(60)

if __name__== "__main__":
    main()
    
