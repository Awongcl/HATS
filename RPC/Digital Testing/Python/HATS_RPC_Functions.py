import serial, time


###Port set-up
port = str
pc = None

### Function to set communication port
def RPC_setport(serial_port):
    global port
    port = serial_port
    return("Serial Port set: ",port)

### Function to get currently assigned communication port
def RPC_getport():
    global port
    return ("Port in use: ",port)

### Function to initialise chosen communication port
def RPC_init():
    global pc, port
    pc = serial.Serial(port,baudrate=9600,timeout=1)
    return("Initialized")

### Basic RPC Function for all different number of inputs
def RPC_0arg(name,cmd):
    global pc
    data = '/' + str(name) + '/' + str(cmd) + ' \n'
    databytes = bytes(data,'utf-8')
    pc.write(databytes)
    reply = str(pc.readlines())
    return(reply)
    

def RPC_1arg(name, cmd, val1):
    global pc
    data = ('/' + str(name) + '/' + str(cmd) + ' ' + str(val1) + ' \n')
    databytes = bytes(data,'utf-8')
    pc.write(databytes)
    reply = str(pc.readlines())
    return(reply)
    

def RPC_2arg(name, cmd, val1, val2):
    global pc
    data = ('/' + str(name) + '/' + str(cmd) + ' ' + str(val1) + 
            ' ' + str(val2) +' \n')
    databytes = bytes(data,'utf-8')
    pc.write(databytes)
    reply = str(pc.readlines())
    return(reply)


def RPC_3arg(name, cmd, val1, val2, val3):
    global pc
    data = ('/' + str(name) + '/' + str(cmd) + ' ' + str(val1) + 
            ' ' + str(val2) + ' ' + str(val3) +' \n')
    databytes = bytes(data,'utf-8')
    pc.write(databytes)
    reply = str(pc.readlines())
    return(reply)


def RPC_4arg(name, cmd, val1, val2, val3, val4):
    global pc
    data = ('/' + str(name) + '/' + str(cmd) + ' ' + str(val1) + 
            ' ' + str(val2) + ' ' + str(val3) + ' ' + str(val4) +' \n')
    databytes = bytes(data,'utf-8')
    pc.write(databytes)
    reply = str(pc.readlines())
    return(reply)

###Clear RPC and ready it for new input
def RPC_newline():
    global pc
    databytes = b'\n'
    pc.write(databytes)
    reply = str(pc.readlines())
    return(reply)


###Read Lines from Serial port
def RPC_readlines():
    global pc
    reply = str(pc.read(2048))
    return(reply)

### Deinitialise port
def RPC_close():
    pc.close()
    return "Port Closed"