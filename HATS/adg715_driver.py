from smbus2 import SMBus, i2c_msg

I2C_ADDR_GND = 0x48

# Switch order 0x<S8 S7 S6 S5 S4 S3 S2 S1>
# E.g to toggle S8 and S1 = 0x81
SARR = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80]


class ADG715:
    def __init__(self, i2c_addr=I2C_ADDR_GND,i2c_dev=None):
        self._i2c_addr = i2c_addr
        self._i2c_dev = i2c_dev

    def numToHex(self,arr):
        t = 0x00
        for i in arr:
            t = t | SARR[i-1]
    
        return t

    # write byte 
    def write(self,value):
        with SMBus(1) as bus:
            # Write a single byte to address 80
            b = self.numToHex(value)
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

