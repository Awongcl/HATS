from ina260_driver import INA260

I2C_ADDR = 0x40

# Initialize IC
ina260 = INA260(I2C_ADDR)
#ina260.get_id()

ina260.reset()
print(ina260.read_config())
ina260.set_all(16,"continous")
print(ina260.read_config())

print(ina260.get_voltage())
print(ina260.get_current())
print(ina260.get_power())