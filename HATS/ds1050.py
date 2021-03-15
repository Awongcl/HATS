from ds1050_driver import DS1050

I2C_ADDR = 0x28
# initialize IC
ds1050 = DS1050(I2C_ADDR)


'''
32 steps from 00000b to 11111b, each step = 3.0275%
0% to 96.88% duty cycle option
'''
def set_cycle(cycle = 16):
    ds1050.set_cycle(cycle)
    percent = 3.0275*cycle
    print('{} % duty cycle set!'.format(percent))

def set_full_cycle():
    ds1050.set_full_cycle()
    print('Full duty cycle set!')

def shutdown():
    ds1050.shutdown()
    print('Entered shutdown mode!')

def wakeup():
    ds1050.wakeup()
    print('Recalled from shutdown mode!')

def read():
    reg = ds1050.read()
    print("Reg Value: {}".format(reg))
    percent = 3.0275*reg
    print("Duty cycle: {}%".format(percent))
    return reg
