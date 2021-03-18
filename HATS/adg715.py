from adg715_driver import ADG715

I2C_ADDR_GND = 0x48

adg715 = ADG715(I2C_ADDR_GND)


def set_relay(value=[]):
    adg715.write(value)
    print("Reg Value: {}".format(adg715.read()))

def read_relay():
    """To read the current state of the relays\n
    Relays 1-8 is = 0x0000 0000\n
    If relay 1 and 2 is ON, returns 0x0000 0011 = 3 in int
    """
    print("Reg Value: {}".format(adg715.read()))


def reset_relay():
    adg715.reset()
    print("ADG175 reset!")
    print("Reg Value: {}".format(adg715.read()))


