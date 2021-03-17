import RPi.GPIO as GPIO
import time

''' Pins '''
DC5V_EN = 17
DC3V3_EN = 27
DC1V8_EN = 22
ADC_RST = 24
DAC_EN = 23
LDO_EN = 5


# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setwarnings(False) # disable runtime warning message
GPIO.setup(ADC_RST, GPIO.OUT)
GPIO.setup(DAC_EN, GPIO.OUT)
GPIO.setup(LDO_EN, GPIO.OUT)
GPIO.setup(DC5V_EN, GPIO.OUT)
GPIO.setup(DC1V8_EN, GPIO.OUT)
GPIO.setup(DC3V3_EN, GPIO.OUT)


vdict = {5:DC5V_EN,3.3:DC3V3_EN,1.8:DC1V8_EN}


def dcdc_en(arr,bool=False):
    for v in arr:
        if(bool==True):
            GPIO.output(vdict[v], GPIO.HIGH)
        elif(bool == False):
            GPIO.output(vdict[v], GPIO.LOW)
        




def dac_en(bool=True):
    if(bool == False):
        GPIO.output(DAC_EN, GPIO.LOW)
    elif(bool == True):
        GPIO.output(DAC_EN, GPIO.HIGH)

def ldo_en(bool=False):
    if(bool == False):
        GPIO.output(LDO_EN, GPIO.LOW)
    elif(bool == True):
        GPIO.output(LDO_EN, GPIO.HIGH)        

def adc_rst():
    GPIO.output(ADC_RST, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(ADC_RST, GPIO.HIGH)

dac_en(True)
ldo_en(True)
dcdc_en([5,3.3],True)