import spidev
import struct
import time

'''OP codes '''
NOP = 0x00000000
PAD8 = 0x00

#write commands
W2B = 0xD0  # Half word
WMSB = 0xD2 # Byte, MSB
WLSB = 0xD4 # Byte, LSB

# read commands
READ = 0x48
READ_HW = 0xC8    # Read half word


''' Registers'''
ID_REG = 0x02
RST_PWR_CTR_REG = 0x04
DATAOUT_CTL_REG = 0x10
RANGE_SEL_REG = 0x14

'''mask'''
MASK9 = 0b000000000

'''PGA values'''
RANGE = {"+-12.288":0b000,"+-10.24":0b001,"+-6.144":0b010,"+-5.12":0b011,
"+2.56":0b100,"12.288":0b1000,"10.24":0b1001,"6.144":0b1010,"5.12":0b1011}

LSB = {"+-12.288":0.006,"+-10.24":0.005,"+-6.144":0.003,"+-5.12":0.0025,
"+2.56":0.00125,"12.288":0.003,"10.24":0.0025,"6.144":0.0015,"5.12":0.00125}

def to_32bit_list(command,reg,msb,lsb):
    """ Concatenate 4 bytes to a list\n
    e.g. C8140000 --> [200, 20, 0, 0]

    :param command: Command
    :type command: hex
    :param reg: Register
    :type reg: hex
    :param msb: MSB
    :type msb: hex
    :param lsb: LSB
    :type lsb: hex
    :return: List 
    :rtype: list
    """
    command = command << 24
    reg = reg << 16
    msb = msb << 8
    data = command | reg | msb | lsb
    data = struct.pack('>I',data)
    data = [b for b in data]
    return data

def list_to_32bits(list):
    """Convert list of bytes back to 32 bits\n
    e.g. [200, 20, 0, 0] -- > C8140000

    :param list: List of bytes
    :type list: list
    :return: 32 bit int
    :rtype: int
    """
    i = 24 
    data = 0x00000000
    for x in list:
        temp = x << i
        i = i - 8
        data = data | temp
    return data

def list_to_16bits(list):
    """Convert list of bytes back to 16 bits

    :param list: List
    :type list: list
    :return: 16 bit int
    :rtype: int
    """
    i = 8
    data = 0x0000
    for x in list:
        temp = x << i
        i = i - 8
        data = data | temp
    return data


class ADS8661(object):
    
    def __init__(self,bus,device):
        """Inits ADS8661

        :param bus: Bus
        :type bus: int
        :param device: SPI BUS
        :type device: int
        """
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 100000
        self.spi.mode = 0b00
        # Include range value in output data
        self.set_dataout_ctr_reg(0x01,0x00)

    
    def set_dataout_ctr_reg(self,msb=0x00,lsb=0x00):
        """Set lower 16 bit of data control register

        :param msb: MSB, defaults to 0x00
        :type msb: hexadecimal
        :param lsb: LSB, defaults to 0x00
        :type lsb: hexadecimal
        """
        #value = 0x04 # all 0's
        #value = 0x05 # all 1's
        data = to_32bit_list(W2B,DATAOUT_CTL_REG,msb,lsb)
        self.spi.writebytes(data)

    def get_dataout_ctr_reg(self):
        """Get lower 16 bit control reg data

        :return: list of 2 bytes
        :rtype: list
        """
        data = to_32bit_list(READ_HW,DATAOUT_CTL_REG,PAD8,PAD8)
        self.spi.writebytes(data)
        b = self.spi.readbytes(2)
        print(type(b))
        return b

    def set_rst_pwctr_reg(self,msb=0x69,lsb=0x00):
        """Set lower 16 bits of rst_prw_ctr_reg 

        :param msb: MSB, defaults to 0x69
        :type msb: hexadecimal
        :param lsb: LSB, defaults to 0x00
        :type lsb: hexadecimal
        """
        data = to_32bit_list(WMSB,RST_PWR_CTR_REG,msb,lsb)
        self.spi.writebytes(data)

    def get_rst_pwctr_reg(self):
        """Get lower 16 bits of rst_prw_ctr_reg

        :return: list of 2 bytes
        :rtype: list
        """
        data = to_32bit_list(READ_HW,RST_PWR_CTR_REG,PAD8,PAD8)
        self.spi.writebytes(data)
        b = self.spi.readbytes(2)
        return b

    def set_range_sel_reg(self,range="+-12.288"):
        """Set lower 8 bits of range_sel_reg\n
        options: "+12.288","+-10.24","+-6.144","+-5.12", "+2.56","12.288","10.24","6.144","5.12"

        :param range: Range, defaults to "+-12.288"
        :type range: str
        """
        t = RANGE[range]
        self.range = t
        r = PAD8 | t
        data = to_32bit_list(WLSB,RANGE_SEL_REG,PAD8,r)
        self.spi.writebytes(data)

    def get_range_sel_reg(self):
        """Set lower 16 bits of range_sel_reg

        :return: list of 2 bytes
        :rtype: list
        """
        data = to_32bit_list(READ_HW,RANGE_SEL_REG,PAD8,PAD8)
        print(list_to_32bits(data))
        self.spi.writebytes(data)
        b = self.spi.readbytes(2)
        return b

    def get_range(self):
        """Returns current range value in string

        :return: Range
        :rtype: str
        """
        data = self.get_range_sel_reg()
        data = list_to_16bits(data)
        for key, value in RANGE.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
            if value == data:
                return key

    def get_conversion_raw(self):
        """Get 32 bit raw conversion value 

        :return: list of 4 bytes
        :rtype: list
        """
        data = struct.pack('>I',NOP)
        data = [b for b in data]
        self.spi.writebytes(data)
        b = self.spi.readbytes(4)
        v = list_to_32bits(b)
        return v

    def get_voltage(self):
        """Returns voltage after multiplying the range (scale) with raw value

        :return: Voltage
        :rtype: float
        """
        scale = LSB[self.get_range()]
        print(scale)
        data = self.get_conversion_raw()
        data = data >> 20
        #print(hex(data))
        voltage = scale*data
        return voltage


    '''Additional functionds can be built with GPO pin
    Alarm and threshold settings'''

   
        
        



