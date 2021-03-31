import RPi.GPIO as GPIO
import time

''' Pins '''
DC5V_EN = 17
DC3V3_EN = 27
DC1V8_EN = 22
ADC_RST = 24
DAC_EN = 23
LDO_EN = 5
RELAY_RST = 6
MATRIX_1_RST = 19
MATRIX_2_RST = 26
PGA_G0 = 16
PGA_G1 = 20
PGA_G2 = 21
CE0 = 8



# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setwarnings(False) # disable runtime warning message
GPIO.setup(MATRIX_1_RST, GPIO.OUT)
GPIO.setup(MATRIX_2_RST, GPIO.OUT)
GPIO.setup(ADC_RST, GPIO.OUT)
GPIO.setup(DAC_EN, GPIO.OUT)
GPIO.setup(LDO_EN, GPIO.OUT)
GPIO.setup(RELAY_RST, GPIO.OUT)
GPIO.setup(DC5V_EN, GPIO.OUT)
GPIO.setup(DC1V8_EN, GPIO.OUT)
GPIO.setup(DC3V3_EN, GPIO.OUT)    
GPIO.setup(PGA_G0, GPIO.OUT)
GPIO.setup(PGA_G1, GPIO.OUT)
GPIO.setup(PGA_G2, GPIO.OUT)

GPIO.setup(CE0, GPIO.OUT)


vdict = {5:DC5V_EN,3.3:DC3V3_EN,1.8:DC1V8_EN}
PGA_GAIN = {0:0b000,1:0b001,2:0b010,5:0b011,10:0b100,20:0b101,50:0b110,100:0b111}
PGA_DICT = {1:PGA_G0,2:PGA_G1,3:PGA_G2}



def dcdc_en(arr=[],bool=False):
    """Enable or disable on baord DCDC converters\n
    Input a list of voltages, options: 5, 3.3 and 1.8
    e.g to enabl3 5V and 3.3V = [5,3.3], bool = True

    :param arr: List of voltage values
    :type arr: list
    :param bool: On= True, Off = False, defaults to False
    :type bool: bool
    """
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
    """Enables or disables on board LDO\n
    Power for ADS1015 and ADS8661

    :param bool: On = True, off = False defaults to False
    :type bool: bool
    """
    if(bool == False):
        GPIO.output(LDO_EN, GPIO.LOW)
    elif(bool == True):
        GPIO.output(LDO_EN, GPIO.HIGH)        

def adc_rst():
    """Resets ADS8661
    """
    GPIO.output(ADC_RST, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(ADC_RST, GPIO.HIGH)

def relay_rst():
    """Resets relay
    """
    GPIO.output(RELAY_RST, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RELAY_RST, GPIO.HIGH)

def matrix_1_rst():
    """Resets Crosspoint matrix 1
    """
    GPIO.output(MATRIX_1_RST, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(MATRIX_1_RST, GPIO.HIGH)

def matrix_2_rst():
    """Resets Crosspoint matrix 2
    """
    GPIO.output(MATRIX_2_RST, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(MATRIX_2_RST, GPIO.HIGH)

def set_pga_gain(gain=1):
    """Set gain of the PGA at DAC output\n
    Gain options: 0,1,2,5,10,20,50,100

    :param gain: Gain
    :type gain: int
    """
    bits = PGA_GAIN[gain]
    G0 = bits & 0x1
    G1 = bits & 0x2 
    G1 = G1 >> 1
    G2 = bits & 0x4 
    G2 = G2>> 2
    PGA_ARR = [G0,G1,G2]
    for i in range(1,4):
        #print(PGA_ARR[i-1])
        if PGA_ARR[i-1] == 0 :
            GPIO.output(PGA_DICT[i], GPIO.LOW)
        else:
            GPIO.output(PGA_DICT[i], GPIO.HIGH)

def testing():
    GPIO.output(CE0,GPIO.HIGH)

#ldo_en(False)
#dcdc_en([5,1.8],False)