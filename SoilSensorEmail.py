import smtplib
import RPi.GPIO as GPIO
import time
from email.message import EmailMessage
import logging

logging.basicConfig(filename = 'soil_sensor.log', level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

from_email_addr = "17605229265@163.com"
from_email_pass = "QSPWa32LkjeZ25kL"
to_email_addr = "17605229265@163.com"

last_send_time = 0

def setup_gpio(channel):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN)
    GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime = 300)
    GPIO.add_event_callback(channel, callback)

def callback(channel):
    current_value = GPIO.input(channel)
    status = "water not detected" if current_value else "water detected"
    logging.info(f"{status}!")      

def send_email(subject, body) :
    global last_send_time
    current_time = time.time()
    
    if current_time - last_send_time >= 6*60*60:
        server = smtplib.SMTP('smtp.163.com', 25)
        server.starttls()
        server.login(from_email_addr, from_email_pass)
   
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = from_email_addr
        msg['To'] = to_email_addr
        
        try:
            server.send_message(msg)
            logging.info("email sent")
            last_send_time = current_time
           
        except Exception as e:
            logging.error(f"failed tosend email: {e}")
        finally:
            server.quit()
    else:
        logging.info("time interval not reached, email not send")
      

def main() :
    global last_send_time
    channel = 4
    last_send_time = 0

    setup_gpio(channel)
    callback(channel)
    while True:
        current_time = time.time()
        current_hour = time.localtime(current_time).tm_hour
        logging.info(f"current time hour: {current_hour}")

        if current_hour % 6 == 0:
            current_value = GPIO.input(channel)
            status = "watter needed" if current_value else "water enough"
            subject = "soil sensor update"
            body =f"hello,the soil sensor status is: {status}"
            send_email(subject, body) 

        time.sleep(60*60)

if __name__== "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Program terminated by user")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        GPIO.cleanup()
    
