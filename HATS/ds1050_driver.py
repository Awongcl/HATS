from smbus2 import SMBus, i2c_msg

I2C_ADDR = 0x28

def dec_to_bin(x):
        return int(bin(x)[2:])

class DS1050:
    def __init__(self, i2c_addr=I2C_ADDR,i2c_dev=None):
        self._i2c_addr = i2c_addr
        self._i2c_dev = i2c_dev


    #set PWM duty cycle
    def set_cycle(self,step=16):
        # 32 steps from 00000b to 11111b, each step = 3.125%
        #0% to 96.88% duty cycle option
        step |= 0x00
        with SMBus(1) as bus:
            msg = i2c_msg.write(I2C_ADDR, [step])
            bus.i2c_rdwr(msg)
            percent = 3.0275*step
            print('{}% duty cycle set!'.format(percent))

    #set 100% duty cycle
    def set_full_cycle(self):
        # Write a single byte to address
        with SMBus(1) as bus:
            msg = i2c_msg.write(I2C_ADDR, [0x20])
            bus.i2c_rdwr(msg)
            print('Full duty cycle set!')
    # goes into shutdown mode, low current    
    def shutdown(self):
        with SMBus(1) as bus:
            msg = i2c_msg.write(I2C_ADDR, [0xC0])
            bus.i2c_rdwr(msg)
            print('Entered shutdown mode!')

    #recall the ic from shutdown mode
    def wakeup(self):
        with SMBus(1) as bus:
            msg = i2c_msg.write(I2C_ADDR, [0x80])
            bus.i2c_rdwr(msg)
            print('Recalled from shutdown mode!')

    def read(self):    
        with SMBus(1) as bus:
            data = bus.read_byte(I2C_ADDR)
            print("Reg Value: {}".format(data))