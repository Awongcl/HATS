from ina260_driver import INA260

I2C_ADDR = 0x40

# Initialize IC
ina260 = INA260(I2C_ADDR)

def get_voltage():
    voltage = ina260.get_voltage()
    print("Voltage: {} V".format(voltage))
    return voltage

def get_current():
    current = ina260.get_current()
    print("Current: {} A".format(current))
    return current


def get_power():
    power = ina260.get_power()
    print("Power: {} W".format(power))
    return power

def get_all():
    get_voltage()
    get_current()
    get_power()

def get_id():
    print(ina260.get_id())

def set_all(avg=1,mode="continous"):
    ina260.set_all(avg,mode)
    print("Average of {} and {} mode set!".format(avg,mode))

def get_config():
    print("Average :",ina260.get_average())  
    print("Mode :",ina260.get_mode())  


def read_config():
    config = ina260.read_config()
    print(config)   
    return config 

def reset():
    ina260.reset()

