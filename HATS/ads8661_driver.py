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

def write_lsb(reg,hword):
        op = WLSB << 1
        lsb = 0xFF & hword
        dummy = 0x00
        return [op,reg,dummy,lsb]

def to_32bit_list(command,reg,msb,lsb):
        command = command << 24
        reg = reg << 16
        msb = msb << 8
        data = command | reg | msb | lsb
        data = struct.pack('>I',data)
        data = [b for b in data]
        return data

def list_to_32bits(list):
    i = 24 
    data = 0x00000000
    for x in list:
        temp = x << i
        i = i - 8
        data = data | temp
    return data

def list_to_16bits(list):
    i = 8
    data = 0x0000
    for x in list:
        temp = x << i
        i = i - 8
        data = data | temp
    return data


class ADS8661(object):
    
    def __init__(self,bus,device):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 100000
        self.spi.mode = 0b00
        # Include range value in output data
        self.set_dataout_ctr_reg(0x01,0x00)

    ''' Set lower 16 bit of data control reg ''' 
    def set_dataout_ctr_reg(self,msb=0x00,lsb=0x00):
        #value = 0x04 # all 0's
        #value = 0x05 # all 1's
        data = to_32bit_list(W2B,DATAOUT_CTL_REG,msb,lsb)
        self.spi.writebytes(data)

    ''' get lower 16 bit control reg data'''
    def get_dataout_ctr_reg(self):
        data = to_32bit_list(READ_HW,DATAOUT_CTL_REG,PAD8,PAD8)
        self.spi.writebytes(data)
        b = self.spi.readbytes(2)
        return b

    ''' set lower 16 bits of rst_prw_ctr_reg '''
    def set_rst_pwctr_reg(self,msb=0x69,lsb=0x00):
        data = to_32bit_list(WMSB,RST_PWR_CTR_REG,msb,lsb)
        self.spi.writebytes(data)

    ''' Get lower 16 bits of rst_prw_ctr_reg '''
    def get_rst_pwctr_reg(self):
        data = to_32bit_list(READ_HW,RST_PWR_CTR_REG,PAD8,PAD8)
        self.spi.writebytes(data)
        b = self.spi.readbytes(2)
        return b

    ''' set lower 8 bits of range_sel_reg
     options: "+12.288","+-10.24","+-6.144","+-5.12", "+2.56","12.288","10.24","6.144","5.12" '''
    def set_range_sel_reg(self,range="+-12.288"):
        t = RANGE[range]
        self.range = t
        r = PAD8 | t
        data = to_32bit_list(WLSB,RANGE_SEL_REG,PAD8,r)
        self.spi.writebytes(data)

    ''' get lower 16 bits of range_sel_reg '''
    def get_range_sel_reg(self):
        data = to_32bit_list(READ_HW,RANGE_SEL_REG,PAD8,PAD8)
        self.spi.writebytes(data)
        b = self.spi.readbytes(2)
        return b

    ''' Returns current range value in string'''
    def get_range(self):
        data = self.get_range_sel_reg()
        data = list_to_16bits(data)
        for key, value in RANGE.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
            if value == data:
                return key

        
    ''' Get 32 bit raw conversion value '''
    def get_conversion_raw(self):
        data = struct.pack('>I',NOP)
        data = [b for b in data]
        self.spi.writebytes(data)
        b = self.spi.readbytes(4)
        v = list_to_32bits(b)
        return v

    ''' Returns voltage after multiplying the range (scale) with raw value '''
    def get_voltage(self):
        scale = LSB[self.get_range()]
        print(scale)
        data = self.get_conversion_raw()
        data = data >> 20
        #print(hex(data))
        voltage = scale*data
        return voltage


    '''Additional functionds can be built with GPO pin
    Alarm and threshold settings'''


        
        



