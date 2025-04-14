#!/usr/bin/python
import RPi.GPIO as GPIO
import PCF8591 as ADC #Import the library for the PCF8591 module
import time #Import the time library for adding delays

#Initialize the PCF8591 moudle at 12C address 0x48
#This address is used for communication with the Raspberry Pi
ADC.setup(0x48)

try:
   while True: #Start an inifinite loop to continuously monitor the sensor
      potentiometer_value = ADC.read(0)
      print (potentionmeter_value)

      time.sleep(0.2)

except KeyboardInterrupt:
  print ("Exit")

#GPIO SETUP
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
        if GPIO.input(channel):
                 print  ("Water Detected!")
        else :
                 print  ("Water Detected!")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300) # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback) # assign function to GPIO PIN, Run function on change

# infinite loop
while True:
        time.sleep(1)

