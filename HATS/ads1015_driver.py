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

def list_to_bits(list):
    """Converts any length list to binary bits
    e.g. [2,3] --> 00110010

    :param list: List of integers
    :type list: List
    :return: Stream of binary bits in hex form
    :rtype: hex
    """
    shift = (len(list)-1)*8
    data = 0x0000
    for b in list:
        b = b << shift
        data = data | b
        shift -= 8
    return data


def hword_to_byte_list(hword):
    """Function to convert 16 bits (2 bytes) to byte list
    e.g. 0x1234 -- > [12,34]
    :param hword: Halfword
        
    :type hword: hex
    :return: Byte list
    :rtype: list
    """
    list = []
    msb = (hword & 0xFF00) >> 8
    lsb = hword & 0x00FF
    list.append(msb)
    list.append(lsb)
    return list

def twos_comp(val, bits):
    """compute the 2's complement of int value val

    :param val: Value to be compute
    :type val: int
    :param bits: Number of bits to represent value
    :type bits: int
    :return: 2's complement of int value
    :rtype: int
    """
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

class ADS1015:
    def __init__(self, i2c_addr, alert_pin=None, i2c_dev=None):
        """Inits ADS1015

        :param i2c_addr: I2C address
        :type i2c_addr: 
        :param alert_pin: defaults to None
        :type alert_pin: 
        :param i2c_dev: defaults to None
        :type i2c_dev: 
        """
        self.i2c_addr = i2c_addr
        self.i2c_dev = i2c_dev
        self.alert_pin = alert_pin

    
    def get_conversion_reg(self):
        """Get 16 bit raw conversion value from conversion register

        :return: Returns 16 bits value in int
        :rtype: int
        """
        self.start_conversion()
        if not self.conversion_ready():
            time.sleep(0.05)
        with SMBus(1) as bus:
            data = list_to_bits(bus.read_i2c_block_data(self.i2c_addr,CONVERSION_REG,2))
            return data


    def get_raw_voltage(self):
        """ Extracts 12 bit raw voltage from the 16 bit conversion register

        :return: 12 bit value as int
        :rtype: int
        """
        return self.get_conversion_reg() >> CONVERSION_SHIFT


    def get_voltage(self):
        """Get voltage from raaw data by multiplying gain

        :return: Voltage
        :rtype: float
        """
        data = self.get_conversion_reg() >> CONVERSION_SHIFT
        lsb = (self.get_gain()*2)/(2**12)

        return data*lsb

    
    def start_conversion(self):
        """Starts a conversion
        """
        data = 0x8000 | self.get_config_reg()
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)

    def conversion_ready(self):
        """Check is the conversion ready

        :return: Boolean
        :rtype: Boolean
        """
        data = self.get_config_reg() >> OS_SHIFT
        if data == 1:
            return True
        return False

    def get_config_reg(self):
        """Get 16 bit configuration value from configuration register

        :return: Returns 16 bits value in int
        :rtype: int
        """
        with SMBus(1) as bus:
            data = list_to_bits(bus.read_i2c_block_data(self.i2c_addr,CONFIG_REG,2))
            return data

    def set_mux(self,channel = "in0/gnd"):
        """Sets the internal mux to switch between channel\n
        'in0/in1' - Differential reading between in0 and in1 (default)\n
        'in0/in3' - Differential reading between in0 and in3\n
        'in1/in3' - Differential reading between in1 and in3\n
        'in2/in3' - Differential reading between in2 and in3\n
        'in0/gnd' - Single-ended reading between in0 and GND\n
        'in1/gnd' - Single-ended reading between in1 and GND\n
        'in2/gnd' - Single-ended reading between in2 and GND\n
        'in3/gnd' - Single-ended reading between in3 and GND

        :param channel: e.g 'in0/gnd' - Single-ended reading between in0 and GND,, defaults to "in0/gnd"
        :type channel: str
        """
        reg = self.get_config_reg() & MUX_MASK
        data = reg | (MUX[channel] << MUX_SHIFT)
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)
    
    
    def get_mux(self):
        """Get the current mux setting

        :return: Mux state
        :rtype: str
        """
        data = 0b111 & (self.get_config_reg() >> MUX_SHIFT)
        for key, value in MUX.items(): 
            if value == data:
                return key

    def set_gain(self,gain=2.048):
        """Set the gain of the PGA \n
        Options: (+-) 6.144,4.096,2.048(default),1.024,0.512,0.256

        :param gain: Gain, defaults to 2.048
        :type gain: float
        """
        reg = self.get_config_reg() & GAIN_MASK
        data = reg | (GAIN[gain] << GAIN_SHIFT)
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)
    
    def get_gain(self):
        """Get current gain setting

        :return: Gain value
        :rtype: float
        """
        data = 0b111 & (self.get_config_reg() >> GAIN_SHIFT)
        for key, value in GAIN.items(): 
            if value == data:
                return key

    def set_sample_rate(self,rate=1600):
        """Set sampling rate \n
        Options: 125,250,490,920,1600(default),2400,3300,3300 SPS

        :param rate: Sampling rate, defaults to 1600
        :type rate: int
        """
        reg = self.get_config_reg() & RATE_MASK
        data = reg | (RATE[rate] << RATE_SHIFT)
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)

    def get_sample_rate(self):
        """Get sampling rate

        :return: Current sampling rate
        :rtype: int
        """
        data = 0b111 & (self.get_config_reg() >> RATE_SHIFT)
        for key, value in RATE.items(): 
            if value == data:
                return key

    def set_mode(self,mode = "single"):
        """Set conversion mode\n
        Options : "single"/"continous"\n
        Single-shot - ADC performs one conversion of the input signal upon request, stores the conversion value to an
        internal conversion register, and then enters a power-down state.\n
        Continous - The rate of continuous conversion is equal to the programmed
        data rate. Data can be read at any time and always reflect the most recent completed conversion.

        :param mode: Mode, defaults to "single"
        :type mode: str
        """
        if mode == "single":
            m = 1
        else:
            m = 0
        reg = self.get_config_reg() & MODE_MASK
        data = reg | (m << MODE_SHIFT)
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)

    def get_mode(self):
        """Get current operation mode

        :return: Operation mode
        :rtype: str
        """
        data = 0b1 & (self.get_config_reg() >> MODE_SHIFT)
        if data == 1:
            return "single"
        return "continous"

    def set_comparator_mode(self,mode="traditional"):
        """Set comparator mode\n
        Options: "window"/"traditional"\n
        In traditional comparator mode, the ALERT/RDY pin asserts (active low by
        default) when conversion data exceeds the limit set in the high-threshold register (Hi_thresh). The comparator
        then deasserts only when the conversion data falls below the limit set in the low-threshold register (Lo_thresh). In
        window comparator mode, the ALERT/RDY pin asserts when the conversion data exceed the Hi_thresh register
        or fall below the Lo_thresh register value.

        :param mode: Mode, defaults to "traditional"
        :type mode: str, optional
        """
        if mode == "window":
            m = 1
        else:
            m = 0
        reg = self.get_config_reg() & COMPARATOR_MODE_MASK
        data = reg | (m << COMPARATOR_MODE_SHIFT)
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)
    
    def get_comparator_mode(self):
        """Get comparator mode

        :return: Comparator mode
        :rtype: str
        """
        data = 0b1 & (self.get_config_reg() >> COMPARATOR_MODE_SHIFT)
        if data == 1:
            return "window"
        return "traditional"

    def set_threshold(self,low,high):
        """Set Low and high threshold for digital comparator\n
        Threshold values : Must be within the gain values, e.g. gain = +-4.096V,
        then threshold must be within +-4.046V

        :param low: low threashold
        :type low: int
        :param high: high threashold
        :type high: int
       
        """
        mask = 0x0000
        gain = self.get_gain()
        lsb = (gain*2)/(2**12)
        l = hword_to_byte_list(mask | (int(low/lsb) << 4))
        h = hword_to_byte_list(mask | (int(high/lsb) << 4))
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,LOW_THRESH_REG,l)
            bus.write_i2c_block_data(self.i2c_addr,HIGH_THRESH_REG,h)

    def get_threshold(self):
        """Get Low and High threshold values\n
        e.g [1,4] l--> low = 1V and high = 4V

        :return: A list containing low and high threashold
        :rtype: list
        """
        gain = self.get_gain()
        lsb = (gain*2)/(2**12)
        with SMBus(1) as bus:
            low = list_to_bits(bus.read_i2c_block_data(self.i2c_addr,LOW_THRESH_REG,2)) >> 4
            high = list_to_bits(bus.read_i2c_block_data(self.i2c_addr,HIGH_THRESH_REG,2)) >> 4
        return [twos_comp(low,12)*lsb,twos_comp(high,12)*lsb]


    def set_comparator_polarity(self,polarity="low"):
        """Set comparator polarity\n
        Options: "low"/"high"

        :param polarity: Polarity, defaults to "low",Polarity of the ALERT/RDY pin
        :type polarity: str
        """
        if polarity == "low":
            b = 0
        else:
            b = 1
        reg = self.get_config_reg() & COMPARATOR_POLARITY_MASK
        data = reg | (b << COMPARATOR_POLARITY_SHIFT)
        data = hword_to_byte_list(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(self.i2c_addr,CONFIG_REG,data)
    

    def get_comparator_polarity(self):
        """Get comparator polarity

        :return: Comparator polarity
        :rtype: str
        """
        data = 0b1 & (self.get_config_reg() >> COMPARATOR_POLARITY_SHIFT)
        if data == 1:
            return "Active High"
        return "Active Low"

    def reset(self):
        """Resets ADS1015 to default values and settings
        """
        with SMBus(1) as bus:
            data = 0x06 # reset value
            # Write a single byte
            msg = i2c_msg.write(0x00, [data])
            bus.i2c_rdwr(msg)




