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



def list_to_word(list): 
    """Convert list of 2 bytes to 16 bits

    :param list: List
    :type list: int
    :return: Halfword
    :rtype: int

    """
    msb = list[0]
    lsb = list[1]
    msb = msb << 8
    word = msb | lsb
    return(word) 

def word_to_bytes(word):
    """ Convert 16 bits into list of 2 bytes

    :param word: Halfword
    :type word: hexadecimal
    :return: list of 2 bytes
    :rtype: list
    """
    list = []
    msb = (word & 0xFF00) >> 8
    lsb = word & 0x00FF
    list.append(msb)
    list.append(lsb)
    return list

class INA260:
    def __init__(self, i2c_addr=I2C_ADDR,i2c_dev=None):
        """Inits INA260

        :param i2c_addr: I2C address, defaults to I2C_ADDR
        :type i2c_addr: hexadecimal
        :param i2c_dev: int, defaults to None
        :type i2c_dev: int
        """
        self.i2c_addr = i2c_addr
        self.i2c_dev = i2c_dev
    
    def get_voltage(self):
        """Get voltage from voltage bus

        :return: Voltage
        :rtype: float
        """
        if(self.get_mode() == "triggered"):
            self.set_mode("triggered")
            #print("triggered")
        with SMBus(1) as bus:
            data = bus.read_i2c_block_data(I2C_ADDR,VOLTAGE_REG,2)
            return list_to_word(data)* 0.00125

    def get_current(self):
        """ Get current from current register

        :return: Current
        :rtype: float
        """
        with SMBus(1) as bus:
            data = bus.read_i2c_block_data(I2C_ADDR,CURRENT_REG,2)
            return list_to_word(data)* 0.00125

    ''' get power based on the volatge and current registers '''
    def get_power(self):
        """Get power based on the volatge and current registers

        :return: Power (Voltage*Current)
        :rtype: float
        """
        with SMBus(1) as bus:
            data = bus.read_i2c_block_data(I2C_ADDR,POWER_REG,2)
            return list_to_word(data)* 0.01

    def get_id(self):
        """Get the id of the ic

        :return: ID of the IC
        :rtype: int
        """
        with SMBus(1) as bus:
            data = bus.read_i2c_block_data(I2C_ADDR,ID_REG,2)
            return list_to_word(data)

    def set_average(self,avg = 1):
        """Set the number of averages from the read data\n
        options : 1(default),4,16,64,128,256,512,1024

        :param avg: Average, defaults to 1
        :type avg: int
        """
        data = DEFAULT_CONFIG & 0xF1FF
        data |= AVERAGE[avg] << 9
        data = word_to_bytes(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(I2C_ADDR,CONFIG_REG,data)

    def set_mode(self,mode = "continous"):
        """ Set mode\n
        Options: "triggered"/"continous" 

        :param mode: Mode, defaults to "continous"
        :type mode: str
        """
        data = (DEFAULT_CONFIG & 0xFFF0 )| MODE[mode]
        data = word_to_bytes(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(I2C_ADDR,CONFIG_REG,data)

    def set_all(self,avg =1 ,mode = "continous"):
        """Set all  values of the config register\n
        Average optios: options : 1(default),4,16,64,128,256,512,1024\n
        Mode options: Options: "triggered"/"continous" 

        :param avg: Average, defaults to 1
        :type avg: int
        :param mode: Mode, defaults to "continous"
        :type mode: str
        """
        data = (DEFAULT_CONFIG & 0xFFF0 )| MODE[mode]
        data &= 0xF1FF
        data |= AVERAGE[avg] << 9
        data = word_to_bytes(data)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(I2C_ADDR,CONFIG_REG,data)

    def read_config(self):
        """Reads the config register

        :return: 16 bit hex
        :rtype: hexadecimal
        """
        with SMBus(1) as bus:
            data = bus.read_i2c_block_data(I2C_ADDR,CONFIG_REG,2)
            return hex(list_to_word(data))

    def get_mode(self):
        """Get mode

        :return: Mode
        :rtype: str
        """
        hex = self.read_config()
        hex = int(hex,16)
        hex = hex & 0x0004
        if(hex == 4):
            return "continous"
        else:
            return "triggered"

    def get_average(self):
        """Get average

        :return: Average
        :rtype: int
        """
        hex = self.read_config()
        hex = int(hex,16)
        hex = (hex & 0x0700) >> 9
        for avg, b in AVERAGE.items():  
            if b == hex:
                return avg

    def reset(self):
        """Resets IC
        """
        data = word_to_bytes(RESET)
        with SMBus(1) as bus:
            bus.write_i2c_block_data(I2C_ADDR,CONFIG_REG,data)
        print("IC reset!")
          
          


