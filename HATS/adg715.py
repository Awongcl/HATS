from adg715_driver import ADG715

I2C_ADDR_GND = 0x48

adg715 = ADG715(I2C_ADDR_GND)


def set_relay(value=[]):
    adg715.write(value)
    print("Reg Value: {}".format(adg715.read()))

def reset_relay():
    adg715.reset()
    print("ADG175 reset!")
    print("Reg Value: {}".format(adg715.read()))


set_relay([2,4,5])