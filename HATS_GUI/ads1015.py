import time
from ads1015_driver import ADS1015

I2C_ADDRESS_DEFAULT = 0x48  # Default i2c address for Pimoroni breakout
I2C_ADDRESS_ALTERNATE = 0x49  # Default alternate i2c address for Pimoroni breakout
I2C_ADDRESS_ADDR_GND = 0x48  # Address when ADDR pin is connected to Ground
I2C_ADDRESS_ADDR_VDD = 0x49  # Address when ADDR pin is connected to VDD
I2C_ADDRESS_ADDR_SDA = 0x50  # Address when ADDR pin is connected to SDA. Device datasheet recommends using this address last (sec 8.5.1.1)
I2C_ADDRESS_ADDR_SCL = 0x51  # Address when ADDR pin is connected to SCL
'''
'in0/in1' - Differential reading between in0 and in1, voltages must not be negative and must not exceed supply voltage
'in0/in3' - Differential reading between in0 and in3
'in1/in3' - Differential reading between in1 and in3
'in2/in3' - Differential reading between in2 and in3
'in0/gnd' - Single-ended reading between in0 and GND
'in1/gnd' - Single-ended reading between in1 and GND
'in2/gnd' - Single-ended reading between in2 and GND
'in3/gnd' - Single-ended reading between in3 and GND
'''
CHANNELS = ['in0/gnd','in1/gnd','in2/gnd','in3/gnd',
'in0/in1','in0/in3','in1/in3','in2/in3']

ads1015 = ADS1015(I2C_ADDRESS_ADDR_VDD) #Initialize IC



def read_voltage(mode='single',sample_rate=1600,gain=2.048):
    # 'single'/'continuous' 
    ads1015.set_mode(mode)
    #one of 128, 250, 490, 920, 1600 (default), 2400 or 330
    ads1015.set_sample_rate(sample_rate)
    #one of 6.144, 4.096, 2.048 (default), 1.024, 0.512 or 0.256
    ads1015.set_programmable_gain(gain)
    ##print(ads1015.get_conversion_value())
    print('Reading ADS1015 values.....')
    # Print nice channel column headers.
    print('| {:>1} | {:>1} | {:>1} | {:>1} | {:>1} | {:>1} | {:>1} | {:>1} |'.format(
    'in0/gnd','in1/gnd','in2/gnd','in3/gnd','in0/in1','in0/in3','in1/in3','in2/in3'))
    print('-' * 80)
    # Main loop.
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        values[i] = ads1015.get_voltage(channel = CHANNELS[i])
        
    print('| {0:^7} | {1:^7} | {2:^7} | {3:^7} | {4:^7} | {5:^7} | {6:^7} | {7:^7} |'.format(*values))
    return "success"


def get_configs():
    print("Mode: "+ads1015.get_mode())
    print("Gain: {:6.3f}v".format(ads1015.get_programmable_gain()))
    print("Sample Rate:  {}".format(ads1015.get_sample_rate()))

def digital_comparator(High_thresh=20000,Low_thresh=5000,mode='window'):
    # Mode can be 'window'/'traditional'
    ads1015.set_comparator_mode(mode)
    ads1015.set_high_threshold(High_thresh)
    ads1015.set_low_threshold(Low_thresh)
    print("High threshold: {:6.3f}v".format(ads1015.get_high_threshold()))
    print("Low threshold:  {}".format(ads1015.get_low_threshold()))


