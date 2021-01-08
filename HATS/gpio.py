import RPi.GPIO as GPIO
import time

''' Pins '''
ADC_RST = 24


# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setwarnings(False) # disable runtime warning message
GPIO.setup(ADC_RST, GPIO.OUT)







def adc_rst():
    GPIO.output(ADC_RST, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(ADC_RST, GPIO.HIGH)


