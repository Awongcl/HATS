from ina260_driver import INA260

I2C_ADDR = 0x40

# Initialize IC
ina260 = INA260(I2C_ADDR)


def get_voltage():
    print("Voltage: {} V".format(ina260.get_voltage()))

def get_current():
    print("Current: {} A".format(ina260.get_current()))

def get_power():
    print("Power: {} W".format(ina260.get_power()))

def get_all():
    get_voltage()
    get_current()
    get_power()

def get_id():
    print(ina260.get_id())

def set_all(avg=1,mode="continous"):
    ina260.set_all(avg,mode)

def read_config():
    print(ina260.read_config())    

def reset():
    ina260.reset()

