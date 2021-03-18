import gpio
from adg2128_driver import ADG2128

I2C_ARRR_000 = 0x70
I2C_ADDR_001 = 0x71

adg2128_1 = ADG2128(I2C_ARRR_000)
adg2128_2 = ADG2128(I2C_ADDR_001)


def set_switch(device,control,x=0,y=0):
    """ Set state of a  single switch\n
    Device options: 1,2\n
    Control options: "on","off"\n
    X options: 0-11
    Y options: 0-7
    :param device: Device
    :type device: int
    :param control: State
    :type control: str
    :param x: X
    :type x: int
    :param y: Y
    :type y: int
    """
  
    if int(device) == 1:
        adg2128_1.set_switch(control,x,y)
    elif int(device) == 2:
        adg2128_2.set_switch(control,x,y)
    else:
        return

def set_multiple_switch(device,control,list=[]):
    """Set multiple switch state at once\n
    Device options : 1,2
    Control options: "on"/"off"\n
    list input : pairs of switches [x,y]\n
    e.g [1,2,5,6,7,8] = X1&Y2 , X5&y6, X7&Y8\n
    Register will latched during the sending sequence\n
    Register will be update at once after the last command\n
    Meaning all switches will be update simultaneously 


    :param device: Device
    :type device: int
    :param control: "on" or "off"
    :type control: str
    :param list: Pairs of switches, defaults to []
    :type list: list
    """
    if int(device) == 1:
        adg2128_1.set_multiple_switch(control,list)
    elif int(device) == 2:
        adg2128_2.set_multiple_switch(control,list)
    else:
        return
        
def read_switch(device,line):
    """Read back to is read the current state of a line e.g X1\n
    When X0 is entered, this function returns a byte to indicate which Y is connected.\n
    e.g Param = X0, returns 0x03 = 0000 0011\n
    X0 is connected with Y0 and Y1
    Line options: X0-7
    Device options: 1,2

    :param device: Device
    :type device: int
    :param line: Line
    :type line: str
    :return: 2 Bytes, first byte = dummy ,second byte = data
    :rtype: List of bytes
    """
    if int(device) == 1:
        data = adg2128_1.read_back(line)
    elif int(device) == 2:
        data = adg2128_2.read_back(line)
    else:
        return
    
    #print(hex(data))
    for i in range(0,8):
        t = data & 0x01   
        if t == 1:
            print("{} & Y{}".format(line.upper(),i))
        data = data >> 1

    return data

def reset_switch(device=3):
    """Resets switch\n
    Device options : 1,2,3(3 = 1 and 2)
    
    :param device: Device
    :type device: int
    """

    if int(device) == 1:
        gpio.matrix_1_rst()
    elif int(device):
        gpio.matrix_2_rst()
    elif int(device):
        gpio.matrix_1_rst()
        gpio.matrix_2_rst()



