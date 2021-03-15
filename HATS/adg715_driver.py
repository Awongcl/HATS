from smbus2 import SMBus, i2c_msg

I2C_ADDR_GND = 0x48

# Switch order 0x<S8 S7 S6 S5 S4 S3 S2 S1>
# E.g to toggle S8 and S1 = 0x81
SARR = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80]


class ADG715:
    def __init__(self, i2c_addr=I2C_ADDR_GND,i2c_dev=None):
        """Inits ADG715

        :param i2c_addr: I2C address, defaults to I2C_ADDR_GND
        :type i2c_addr: [type], optional
        :param i2c_dev: I2C DEV, defaults to None
        :type i2c_dev: [type], optional
        """
        self._i2c_addr = i2c_addr
        self._i2c_dev = i2c_dev

    def numToHex(self,arr):
        """ Convert numbers in array to hex

        :param arr: Array of numbers, indication of "on" switch
            Example switch 2,5 is high, [2,5]
        :type arr: arr
        :return: Hex value
        :rtype: Hex
        """
        t = 0x00
        for i in arr:
            t = t | SARR[i-1]
        return t

    def write(self,value):
        """Write to ADG715

        :param value: Hex value representing "On switches"
            e.g If switch 2,5 is high = 00010010 = 0x12
        :type value: Byte
        """
        with SMBus(1) as bus:
            # Write a single byte to address 80
            b = self.numToHex(value)
            msg = i2c_msg.write(I2C_ADDR_GND, [b])
            bus.i2c_rdwr(msg)
            

    def read(self):
        """Read the current hex value in register

        :return: Returns the hex value representing switch states
        :rtype: Byte
        """
        with SMBus(1) as bus:
            data = bus.read_byte(I2C_ADDR_GND)
            return data
        

    def reset(self):
        """ Resets to default (all switch low)
        """
        with SMBus(1) as bus:
            # Write a byte to address 80, offset 0
            msg = i2c_msg.write(I2C_ADDR_GND, [0x00])
            bus.i2c_rdwr(msg)

