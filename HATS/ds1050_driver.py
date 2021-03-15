from smbus2 import SMBus, i2c_msg

I2C_ADDR = 0x28

def dec_to_bin(x):
    """Converts decimal to binary

    :param x: Decimal
    :return: Binary in int format
    :rtype: int
    """
    return int(bin(x)[2:])

class DS1050:
    def __init__(self, i2c_addr=I2C_ADDR,i2c_dev=None):
        """Inits DS1050 PWM generator

        :param i2c_addr: I2C address, defaults to I2C_ADDR
        :type i2c_addr: Hex
        :param i2c_dev: Defaults to None
        :type i2c_dev: int


        """
        self._i2c_addr = i2c_addr
        self._i2c_dev = i2c_dev

    def set_cycle(self,step=16):
        """ Sets PWM duty cycle\n
        32 steps from 0-31(00000b to 11111b), each step = 3.125%

        :param step: Step, defaults to 16
        :type step: int
        """
        step |= 0x00
        with SMBus(1) as bus:
            msg = i2c_msg.write(I2C_ADDR, [step])
            bus.i2c_rdwr(msg)

    def set_full_cycle(self):
        """Sets the duty cycle to 100%
        """
       
        with SMBus(1) as bus:
            msg = i2c_msg.write(I2C_ADDR, [0x20])
            bus.i2c_rdwr(msg)
               
    def shutdown(self):
        """ Goes into shutdown mode, low current 
        """
        with SMBus(1) as bus:
            msg = i2c_msg.write(I2C_ADDR, [0xC0])
            bus.i2c_rdwr(msg)
            
    def wakeup(self):
        """ Recalls the ic from shutdown mode
        """
        with SMBus(1) as bus:
            msg = i2c_msg.write(I2C_ADDR, [0x80])
            bus.i2c_rdwr(msg)
            

    def read(self):  
        """ Reads the current PWM value from register

        :return: 5 Bit Binary, 00000b to 11111b
        """
        with SMBus(1) as bus:
            data = bus.read_byte(I2C_ADDR)
        return data