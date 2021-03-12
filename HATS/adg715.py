from adg715_driver import ADG715

I2C_ADDR_GND = 0x48

adg715 = ADG715(I2C_ADDR_GND)


def set_relay(value=[]):
    adg715.write(value)
    adg715.read()

def reset():
    adg715.reset()
    adg715.read()



set_relay()
