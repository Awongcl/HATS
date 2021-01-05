
from i2cdevice import Device, Register, BitField, _int_to_bytes
from i2cdevice.adapter import Adapter, LookupAdapter
from smbus2 import SMBus, i2c_msg
import struct
''' device address '''
I2C_ADDR = 0x40

''' registers address '''
CONFIG_REG = 0x00
CURRENT_REG = 0x01
VOLTAGE_REG = 0x02
POWER_REG = 0x03
ID_REG = 0xFE

''' configuration register fields '''
RESET = 0x8000
DEFAULT_CONFIG = 0x6127
AVERAGE = {1:0b000,4:0b001,16:0b010,64:0b011,128:0b100,256:0b101,512:0b110,1024:0b111}
MODE = {"triggered":0b011,"continous":0b111}



''' function to convert a list to a word '''
def list_to_word(list): 
    msb = list[0]
    lsb = list[1]
    msb = msb << 8
    word = msb | lsb
    return(word) 

def word_to_bytes(word):
    list = []
    msb = (word & 0xFF00) >> 8
    lsb = word & 0x00FF
    list.append(msb)
    list.append(lsb)
    return list

class INA260:
    def __init__(self, i2c_addr=I2C_ADDR,i2c_dev=None):
        self.i2c_addr = i2c_addr
        self.i2c_dev = i2c_dev
        


    ''' Get voltage from voltage bus '''
    def get_voltage(self):
        with SMBus(1) as bus:
            data = bus.read_i2c_block_data(I2C_ADDR,VOLTAGE_REG,2)
            return list_to_word(data)* 0.00125


    ''' get current for current register '''
    def get_current(self):
        with SMBus(1) as bus:
            data = bus.read_i2c_block_data(I2C_ADDR,CURRENT_REG,2)
            return list_to_word(data)* 0.00125

    ''' get power based on the volatge and current registers '''
    def get_power(self):
        with SMBus(1) as bus:
            data = bus.read_i2c_block_data(I2C_ADDR,POWER_REG,2)
            return list_to_word(data)* 0.01


    ''' get the id of the ic '''
    def get_id(self):
        with SMBus(1) as bus:
            data = bus.read_i2c_block_data(I2C_ADDR,ID_REG,2)
            return list_to_word(data)

    ''' set the number of averages from the read data 
        options : 1(default),4,16,64,128,256,512,1024
    '''
    def set_average(self,avg = 1):
        data = DEFAULT_CONFIG & 0xF1FF
        data |= AVERAGE[avg] << 9
        data = word_to_bytes(data)
        with SMBus(1) as bus:
            data = bus.write_i2c_block_data(I2C_ADDR,CONFIG_REG,data)
        
        print("Average of {} set!".format(avg))


    ''' set mode
        trigger/ continous '''
    def set_mode(self,mode = "continous"):
        data = (DEFAULT_CONFIG & 0xFFF0 )| MODE[mode]
        data = word_to_bytes(data)
        with SMBus(1) as bus:
            data = bus.write_i2c_block_data(I2C_ADDR,CONFIG_REG,data)

        print("{} mode set!".format(mode))

    ''' set all  values of the config register'''
    def set_all(self,avg =1 ,mode = "continous"):
        data = (DEFAULT_CONFIG & 0xFFF0 )| MODE[mode]
        data &= 0xF1FF
        data |= AVERAGE[avg] << 9
        data = word_to_bytes(data)
        with SMBus(1) as bus:
            data = bus.write_i2c_block_data(I2C_ADDR,CONFIG_REG,data)

        print("Average of {} and {} mode set!".format(avg,mode))


    ''' reads the config register '''
    def read_config(self):
        with SMBus(1) as bus:
            data = bus.read_i2c_block_data(I2C_ADDR,CONFIG_REG,2)
            return hex(list_to_word(data))

    ''' resets ic '''
    def reset(self):
        data = word_to_bytes(RESET)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(I2C_ADDR,CONFIG_REG,data)
        print("IC reset!")
          
          


