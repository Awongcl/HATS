#!/usr/bin/python3
from ads8661_driver import ADS8661
import gpio
import struct

# device and spi_ch
spi_ch = 1
adc = ADS8661(0, spi_ch)


def get_voltage():
    print("{} V".format(adc.get_voltage()))
    return 0

def get_raw_conversion():
    print(hex(adc.get_conversion_raw()))

def set_range(range="5.12"):
    adc.set_range_sel_reg(range)     
    print("Range set to {}".format(range))
    

def get_range():
    print("Range: {}".format(adc.get_range()))


# reset is not in the driver file because it is controld by the PI's GPIO, not SPI
def reset():
    gpio.adc_rst()
    print("AGS8661 ADC reset!")

