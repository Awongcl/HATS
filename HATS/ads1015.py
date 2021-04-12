from ads1015_driver import ADS1015
import time


I2C_ADDRESS_ADDR_GND = 0x48  # Address when ADDR pin is connected to Ground
I2C_ADDRESS_ADDR_VDD = 0x49  # Address when ADDR pin is connected to VDD
I2C_ADDRESS_ADDR_SDA = 0x50  # Address when ADDR pin is connected to SDA
I2C_ADDRESS_ADDR_SCL = 0x51  # Address when ADDR pin is connected to SCL

CHANNELS = ['in0/gnd','in1/gnd','in2/gnd','in3/gnd',
'in0/in1','in0/in3','in1/in3','in2/in3']


ads1015 = ADS1015(I2C_ADDRESS_ADDR_VDD)

def get_all_voltage(mode = "single",sample_rate=1600,gain=2.048):
    # 'single'/'continuous' 
    ads1015.set_mode(mode)
    #one of 128, 250, 490, 920, 1600 (default), 2400 or 330
    ads1015.set_sample_rate(sample_rate)
    #one of 6.144, 4.096, 2.048 (default), 1.024, 0.512 or 0.256
    ads1015.set_gain(gain)
    ##print(ads1015.get_conversion_value())
    print('Reading ADS1015 values.....')
    # Print nice channel column headers.
    print('| {:>1} | {:>1} | {:>1} | {:>1} | {:>1} | {:>1} | {:>1} | {:>1} |'.format(
    'in0/gnd','in1/gnd','in2/gnd','in3/gnd','in0/in1','in0/in3','in1/in3','in2/in3'))
    print('-' * 80)
    # Main loop.
    # Read all the ADC channel values in a list.
    values = [0]*8
    raw = [0]*8
    for i in range(8):
        ads1015.set_mux(CHANNELS[i])
        values[i] = ads1015.get_voltage()
        raw[i] = ads1015.get_raw_voltage()
        
    print('| {0:^7} | {1:^7} | {2:^7} | {3:^7} | {4:^7} | {5:^7} | {6:^7} | {7:^7} |'.format(*values))
    print('| {0:^7} | {1:^7} | {2:^7} | {3:^7} | {4:^7} | {5:^7} | {6:^7} | {7:^7} |'.format(*raw))

def get_voltage(mode = "single",rate=1600,gain=2.048,channel="in0/gnd"):
    ads1015.set_sample_rate(rate)
    ads1015.set_gain(gain)
    ads1015.set_mux(channel)
    ads1015.set_mode(mode)
    voltage = ads1015.get_voltage()
    print("{} V".format(voltage))
    return voltage

def get_config():
    #print("Channel : {}".format(ads1015.get_mux()))
    print("Gain : {}".format(ads1015.get_gain()))
    print("Sample Rate : {}".format(ads1015.get_sample_rate()))
    print("Mode : {}".format(ads1015.get_mode()))
    print("Comparator mode : {}".format(ads1015.get_comparator_mode()))
    l = ads1015.get_threshold()[0]
    h = ads1015.get_threshold()[1]
    print("Threshold(Low,High) : {}V,{}V".format(l,h))
    print("Comparator Polarity: {}".format(ads1015.get_comparator_polarity()))
        
def set_digital_comparator(mode='traditional',low=0,high=0):
    ads1015.set_comparator_mode(mode)
    ads1015.set_threshold(low,high)
    print("Digital compaarator set!")

def reset():
    ads1015.reset()
    print("IC reset!")
    






