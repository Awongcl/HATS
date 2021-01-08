from i2cdevice import Device, Register, BitField, _int_to_bytes
from i2cdevice.adapter import Adapter, LookupAdapter
from smbus2 import SMBus, i2c_msg

I2C_ADDR_GND = 0x48

class ADG715:
    def __init__(self, i2c_addr=I2C_ADDR_GND,i2c_dev=None):
        self._i2c_addr = i2c_addr
        self._i2c_dev = i2c_dev
    # write byte 
    def write(self,b):
        with SMBus(1) as bus:
            # Write a single byte to address 80
            msg = i2c_msg.write(I2C_ADDR_GND, [b])
            bus.i2c_rdwr(msg)
            print('wrote')

    # read the status of the register
    def read(self):
        with SMBus(1) as bus:
            data = bus.read_byte(I2C_ADDR_GND)
            print("Reg Value: {}".format(data))
            


    #reset to default (all close)
    def reset(self):
        with SMBus(1) as bus:
            # Write a byte to address 80, offset 0
            msg = i2c_msg.write(I2C_ADDR_GND, [0x00])
            bus.i2c_rdwr(msg)