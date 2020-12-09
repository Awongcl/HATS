
import time
from ads1015 import ADS1015

CHANNELS = ['in0/gnd', 'in1/gnd', 'in2/gnd', 'in3/gnd']

print("""read-all.py - read all three inputs of the ADC Press Ctrl+C to exit!
""")

ads1015 = ADS1015()
ads1015.set_mode('single')
ads1015.set_programmable_gain(6.1444)
ads1015.set_sample_rate(3200)
reference = ads1015.get_reference_voltage()

print("Reference voltage: {:6.3f}v \n".format(reference))

try:
    while True:
        for channel in CHANNELS:
            #value = ads1015.get_compensated_voltage(channel=channel, reference_voltage=reference)
            #print("{}: {:6.3f}v".format(channel, value))
            value = ads1015.get_voltage(channel = channel)
            print("{}: {:6.3f}v".format(channel, value))


        print("")
        time.sleep(1)

except KeyboardInterrupt:
    pass
