import gpio
from smbus2 import SMBus, i2c_msg

I2C_ARRR_000 = 0x70
I2C_ADDR_001 = 0x71
''' Protocol (24 bit ): I2C address -> data|Ax3-Ax0|AY2-AY0 - > xxxxxxLDSW
data 0 = off, 1 = on
x = dont care
If LDSW = 1, the switch position changes after the new word is read.
If LDSW = 0, the input data is latched, but the switch position is not changed.
Setting LDSW on the last word allows all of the switches in that sequence to be simultaneously
updated.

'''
''' On/Off bit '''
CONTROL = {"off":0x0, 
           "on":0x1}

''' AX0-11 '''
X ={0:0x0,
    1:0x1,
    2:0x2,
    3:0x3,
    4:0x4,
    5:0x5,
    6:0x8,
    7:0x9,
    8:0xA,
    9:0xB,
    10:0xC,
    11:0xD}

''' AY0-8 '''
Y ={0:0x0,
    1:0x1,
    2:0x2,
    3:0x3,
    4:0x4,
    5:0x5,
    6:0x6,
    7:0x7}

''' LDSW ''' 
LATCH = 0x0 # Latch the register until LDSW = 1 
NO_LATCH = 0x1
''' Read back '''
RB = {"x0":0x34,
    "x1":0x3C}


class ADG2128:
    def __init__(self, i2c_addr,i2c_dev=None):
        """Inits ADG2818

        :param i2c_addr: I2C address, defaults to I2C_ARRR_000
        :type i2c_addr: hex
        :param i2c_dev: I2C Dev, defaults to None
        :type i2c_dev: None
        """
        self.i2c_addr = i2c_addr
        self.i2c_dev = i2c_dev

    def set_switch(self,control,x,y):
        """Set switch state\n
        Control options: "on"/"off"\n
        x options : 0-11\n
        y options : 0-7\n
        This method changes the switch state after sending one command

        :param control: "on" or "off"
        :type control: str
        :param x: X
        :type x: int
        :param y: Y
        :type y: int
        """
        msb = ((CONTROL[control] << 7) | X[x] << 3) | Y[y]
        lsb = 0x00 | NO_LATCH
        print([hex(msb),hex(lsb)])
        with SMBus(1) as bus :
            msg = i2c_msg.write(self.i2c_addr,[msb,lsb])
            bus.i2c_rdwr(msg)
          

    def set_multiple_switch(self,control,list=[]):
        """Set multiple switch state at once\n
        Control options: "on"/"off"\n
        list input : pairs of switches [x,y]\n
        e.g [1,2,5,6,7,8] = X1&Y2 , X5&y6, X7&Y8\n
        Register will latched during the sending sequence\n
        Register will be update at once after the last command\n
        Meaning all switches will be update simultaneously 

        :param control: "on" or "off"
        :type control: str
        :param list: Pairs of switches, defaults to []
        :type list: list
        """
        with SMBus(1) as bus :
            for i  in range(0,len(list),2):
            
                if i != len(list)-2:
                    lsb = 0x00 | LATCH
                else:
                    lsb = 0x00 | NO_LATCH
                
                msb = ((CONTROL[control] << 7) | X[list[i]] << 3) | Y[list[i+1]]
                print([hex(msb),hex(lsb)])
                msg = i2c_msg.write(self.i2c_addr,[msb,lsb])
                bus.i2c_rdwr(msg)
                #bus.close()

    def read_back(self,line):
        """Read back to is read the current state of a line e.g X1\n
        When X0 is entered, this function returns a byte to indicate which Y is connected.\n
        e.g Param = X0, returns 0x03 = 0000 0011\n
        X0 is connected with Y0 and Y1
        Line options: X0-7

        :param line: Line
        :type line: str
        :return: 1 Byte of data
        :rtype: byte
        """
        with SMBus(1) as bus:
            msg = i2c_msg.write(self.i2c_addr, [RB[line],0x00])
            bus.i2c_rdwr(msg)
            data = bus.read_i2c_block_data(self.i2c_addr,0,2)
        return data[1]         


  
        

