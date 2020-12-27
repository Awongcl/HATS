from adg715_driver import ADG715

I2C_ADDR_GND = 0x48

adg715 = ADG715(I2C_ADDR_GND)

adg715.write(0xFF)
adg715.read()