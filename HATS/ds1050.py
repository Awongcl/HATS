from ds1050_driver import DS1050

I2C_ADDR = 0x28

ds1050 = DS1050(I2C_ADDR)


# 32 steps from 00000b to 11111b, each step = 3.0275%
#0% to 96.88% duty cycle option
#ds1050.set_cycle(16)
ds1050.wakeup()