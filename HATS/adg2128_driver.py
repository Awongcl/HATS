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
    def __init__(self, i2c_addr=I2C_ARRR_000,i2c_dev=None):
        self.i2c_addr = i2c_addr
        self.i2c_dev = i2c_dev

    ''' Set switch state
        Control options: "on"/"off"
        x options : 0-11
        y options : 0-7
        This method changes the switch state after sending one command
    '''
    def set_switch(self,control,x,y):
        msb = ((CONTROL[control] << 7) | X[x] << 3) | Y[y]
        lsb = 0x00 | NO_LATCH
        print([hex(msb),hex(lsb)])
        with SMBus(1) as bus :
            msg = i2c_msg.write(self.i2c_addr,[msb,lsb])
            bus.i2c_rdwr(msg)
          

    ''' Set multiple switch state at once
        Control options: "on"/"off"
        list input : pairs of switches [x,y]
        e.g [1,2,5,6,7,8] = X1&Y2 , X5&y6, X7&Y8
        Register will latched during the sending sequence
        Register will be update at once after the last command
    '''
    def set_multiple_switch(self,control,list=[]):
        with SMBus(1) as bus :
            for i  in range(0,len(list),2):
                if i != len(list)-2:
                    lsb = 0x00 | LATCH
                else:
                    lsb = 0x00 | NO_LATCH
                
                msb = ((CONTROL[control] << 7) | X[list[i]] << 3) | Y[list[i+1]]
                print([hex(msb),hex(lsb)])
                #msg = i2c_msg.write(self.i2c_addr,[msb,lsb])
                #bus.i2c_rdwr(msg)

    def read_back(self,line):
        with SMBus(1) as bus:
            msg = i2c_msg.write(self.i2c_addr, [RB[line],0x00])
            bus.i2c_rdwr(msg)
            data = bus.read_i2c_block_data(self.i2c_addr,0,2)
        return data           

    ''' Resets the IC '''
    def reset(self):
        return 0


ic = ADG2128(I2C_ARRR_000)
ic.set_switch("off",0,4)
data = ic.read_back("x0")
print(data)
