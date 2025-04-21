import smtplib
import RPi.GPIO as GPIO
import time

channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel) :
    if GPIO.input(channel) :
        print ("water detected!")
        send_email("water detected!")
    else :
        print ("water not detected!")
        send_email("water not detected!")

def send_email(message) :
    from_email_addr = "17605229265@163.com"
    from_email_pass = "QSPWa32LkjeZ25kL"
    to_email_addr = "17605229265@163.com"

    msg = smtplib.SMTP()
    msg.set_debuglevel(0)
    msg.login(from_email_addr, from_email_pass)
    msg.sendmail(from_email_addr, to_email_addr, message)
    msg.quit()
    print ("email sent")


GPIO.add_evevt_detect(channel, GPIO.BOTH, bouncetime = 300)
GPIO.add_evevt_callback(channel, callback)


try :
    while True:
        if GPIO.input(channel):
           print ("soil is dry")
        else:
           print ("soil is wet")
        time.sleep(10800)
except KeyboardInterrupt:
    GPIO.cleanup()
