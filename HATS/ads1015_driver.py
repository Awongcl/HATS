from smbus2 import SMBus, i2c_msg
import struct
import time


''' Registers (16 bits)'''
CONVERSION_REG = 0x0
CONFIG_REG = 0x1
LOW_THRESH_REG = 0x2
HIGH_THRESH_REG = 0x3

''' MASKS , for reset fields to 0's ''' 
MUX_MASK = 0x0FFF
GAIN_MASK = 0x71FF
RATE_MASK = 0x7F1F
MODE_MASK = 0x7EFF
COMPARATOR_MODE_MASK = 0x7FEF
COMPARATOR_POLARITY_MASK = 0x7FF7



''' bit Shift '''
MUX_SHIFT = 12
OS_SHIFT = 15
CONVERSION_SHIFT = 4
GAIN_SHIFT = 9
RATE_SHIFT = 5
MODE_SHIFT = 8
COMPARATOR_MODE_SHIFT = 4
COMPARATOR_POLARITY_SHIFT = 3

''' Keys '''
MUX = { 'in0/in1': 0b000,   # Differential reading between in0 and in1, voltages must not be negative and must not exceed supply voltage
        'in0/in3': 0b001,   # Differential reading between in0 and in3. 
        'in1/in3': 0b010,   # Differential reading between in1 and in3. 
        'in2/in3': 0b011,   # Differential reading between in2 and in3. 
        'in0/gnd': 0b100,   # Single-ended reading between in0 and GND
        'in1/gnd': 0b101,   # Single-ended reading between in1 and GND
        'in2/gnd': 0b110,   # Single-ended reading between in2 and GND
        'in3/gnd': 0b111}

GAIN = {6.144: 0b000,
        4.096: 0b001,
        2.048: 0b010,
        1.024: 0b011,
        0.512: 0b100,
        0.256: 0b101}

RATE = {128: 0b000,
        250: 0b001,
        490: 0b010,
        920: 0b011,
        1600: 0b100,
        2400: 0b101,
        3300: 0b110}

''' Function to convert any length list to bits '''
def list_to_bits(list):
    shift = (len(list)-1)*8
    data = 0x0000
    for b in list:
        b = b << shift
        data = data | b
        shift -= 8
    return data

''' Function to convert 16bits to byte list '''
def hword_to_byte_list(hword):
    list = []
    msb = (hword & 0xFF00) >> 8
    lsb = hword & 0x00FF
    list.append(msb)
    list.append(lsb)
    return list

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

class ADS1015:
    def __init__(self, i2c_addr, alert_pin=None, i2c_dev=None):
        self.i2c_addr = i2c_addr
        self.i2c_dev = i2c_dev
        self.alert_pin = alert_pin

    ''' Get 12 bit raw conversion value '''
    def get_conversion_reg(self):
        self.start_conversion()
        if not self.conversion_ready():
            time.sleep(0.001)
        with SMBus(1) as bus:
            data = list_to_bits(bus.read_i2c_block_data(self.i2c_addr,CONVERSION_REG,2))
            return data

    ''' Get raw voltage '''
    def get_raw_voltage(self):
        return self.get_conversion_reg() >> CONVERSION_SHIFT

    ''' Get voltage from raw data '''
    def get_voltage(self):
        data = self.get_conversion_reg() >> CONVERSION_SHIFT
        lsb = (self.get_gain()*2)/(2**12)
        return data*lsb

    ''' start a conversion ''' 
    def start_conversion(self):
        data = 0x8000 | self.get_config_reg()
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)

    ''' Check if conversion is done ''' 
    def conversion_ready(self):
        #print(hex(self.get_config_reg()))
        data = self.get_config_reg() >> OS_SHIFT
        if data == 1:
            return True
        return False

    ''' Get 16 bit configuration register value '''
    def get_config_reg(self):
        with SMBus(1) as bus:
            data = list_to_bits(bus.read_i2c_block_data(self.i2c_addr,CONFIG_REG,2))
            return data

    '''
        'in0/in1' - Differential reading between in0 and in1 (default)
        'in0/in3' - Differential reading between in0 and in3
        'in1/in3' - Differential reading between in1 and in3
        'in2/in3' - Differential reading between in2 and in3
        'in0/gnd' - Single-ended reading between in0 and GND
        'in1/gnd' - Single-ended reading between in1 and GND
        'in2/gnd' - Single-ended reading between in2 and GND
        'in3/gnd' - Single-ended reading between in3 and GND
    '''
    def set_mux(self,channel = "in0/gnd"):
        reg = self.get_config_reg() & MUX_MASK
        data = reg | (MUX[channel] << MUX_SHIFT)
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)
    

    ''' Get current mux setting ''' 
    def get_mux(self):
        data = 0b111 & (self.get_config_reg() >> MUX_SHIFT)
        for key, value in MUX.items(): 
            if value == data:
                return key


    ''' Set the gain of the PGA 
    Options: +- 6.144,4.096,2.048(default),1.024,0.512,0.256'''
    def set_gain(self,gain=2.048):
        reg = self.get_config_reg() & GAIN_MASK
        data = reg | (GAIN[gain] << GAIN_SHIFT)
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)
    
    def get_gain(self):
        data = 0b111 & (self.get_config_reg() >> GAIN_SHIFT)
        for key, value in GAIN.items(): 
            if value == data:
                return key

    ''' Set sampling rate 
        Options: 125,250,490,920,1600(default),2400,3300,3300 SPS''' 
    def set_sample_rate(self,rate=1600):
        reg = self.get_config_reg() & RATE_MASK
        data = reg | (RATE[rate] << RATE_SHIFT)
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)

    ''' Get sample rate '''
    def get_sample_rate(self):
        data = 0b111 & (self.get_config_reg() >> RATE_SHIFT)
        for key, value in RATE.items(): 
            if value == data:
                return key

    ''' Set mode 
        Options : "single"/"continous" '''
    def set_mode(self,mode = "single"):
        if mode == "single":
            m = 1
        else:
            m = 0
        reg = self.get_config_reg() & MODE_MASK
        data = reg | (m << MODE_SHIFT)
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)

    ''' Get device mode '''
    def get_mode(self):
        data = 0b1 & (self.get_config_reg() >> MODE_SHIFT)
        if data == 1:
            return "single"
        return "continous"

    ''' Set comparator mode
        Options : "window"/"traditional"(default) '''
    def set_comparator_mode(self,mode="traditional"):
        if mode == "window":
            m = 1
        else:
            m = 0
        reg = self.get_config_reg() & COMPARATOR_MODE_MASK
        data = reg | (m << COMPARATOR_MODE_SHIFT)
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)
    
    ''' Get comparatr mode '''
    def get_comparator_mode(self):
        data = 0b1 & (self.get_config_reg() >> COMPARATOR_MODE_SHIFT)
        if data == 1:
            return "window"
        return "traditional"

    ''' Set Low and high threshold for digital comparator '''
    def set_threshold(self,low,high):
        mask = 0x0000
        gain = self.get_gain()
        lsb = (gain*2)/(2**12)
        l = hword_to_byte_list(mask | (int(low/lsb) << 4))
        h = hword_to_byte_list(mask | (int(high/lsb) << 4))
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,LOW_THRESH_REG,l)
            bus.write_i2c_block_data(self.i2c_addr,HIGH_THRESH_REG,h)

    ''' Get Low and High threshold values '''
    def get_threshold(self):
        gain = self.get_gain()
        lsb = (gain*2)/(2**12)
        with SMBus(1) as bus:
            low = list_to_bits(bus.read_i2c_block_data(self.i2c_addr,LOW_THRESH_REG,2)) >> 4
            high = list_to_bits(bus.read_i2c_block_data(self.i2c_addr,HIGH_THRESH_REG,2)) >> 4
        return [twos_comp(low,12)*lsb,twos_comp(high,12)*lsb]


    ''' Set comparator polarity 
        Options: "low"/"high" '''
    def set_comparator_polarity(self,polarity="low"):
        if polarity == "low":
            b = 0
        else:
            b = 1
        reg = self.get_config_reg() & COMPARATOR_POLARITY_MASK
        data = reg | (b << COMPARATOR_POLARITY_SHIFT)
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)
    

    ''' Get comparatr polarity '''
    def get_comparator_polarity(self):
        data = 0b1 & (self.get_config_reg() >> COMPARATOR_POLARITY_SHIFT)
        if data == 1:
            return "Active High"
        return "Active Low"

    ''' Resets IC to default '''
    def reset(self):
        with SMBus(1) as bus:
            data = 0x06 # reset value
            # Write a single byte
            msg = i2c_msg.write(0x00, [data])
            bus.i2c_rdwr(msg)




