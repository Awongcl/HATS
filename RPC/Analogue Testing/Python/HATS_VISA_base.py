# -*- coding: utf-8 -*-
import visa
from pyvisa.constants import *
import time
import re
import io
import struct
from decimal import Decimal
from PIL import Image


###Variables
rm = None


#Initialise VISA with pyvisa-py resource manager
def VISA_init():
    """
    Initiate PyVISA-py backend as resource manager.
    """
    global rm
    rm = visa.ResourceManager('@py')
    return(rm)


#Scan for available resources
def scan_resource():
    """
    Scan and return all available ports. Not all port type will be listed. Eg. available TCPIP type ports will not be listed
    """
    global rm
    return(rm.list_resources())


#List out all opened resources
def opened_resource():
    """
    List ports that are currently connected.
    """
    global rm
    return(rm.list_opened_resources())

#Close pyvisa-py resource manager
def VISA_deinit():
    """
    Deinitialise PyVISA-py backend as resource manager.
    """
    global rm
    rm.close()
    return ("Resource closed")


#General VISA instrument class, the base for instrument-based subclasses
class VISAinst():
    def __init__(self,port):
        self.port = port
        self.open = rm.open_resource(str(port))
    
    def deinit(self):
        """
        De-initialise port connection with VISA resource manager.
        """
        self.open.close()
        return (str(self.port) + " deinitialized")
    
    
    #List down port related settings, useful for RS-232 connectivity
    def info(self):
        """
        Returns a list of connection related parameters and settings 
        """
        string = 'Instrument-'+ str(self.port) + '\n' + 'Parity: ' + str(self.open.parity) + ', Stop Bit: ' + str(self.open.stop_bits) + ', Baudrate: ' + str(self.open.baud_rate) \
             + ', Databits: ' + str(self.open.data_bits) + ', Timeout: ' + str(self.open.timeout) + 'ms'
        return(string)

    #Method to set parity
    # Parity: None - 0, Odd - 1, Even - 2, Mark -3, Space - 4
    def parity(self, input_par):
        """
        Input the assigned integer for the corresponding value.
        Parity: None - 0, Odd - 1, Even - 2, Mark -3, Space - 4

        """
        if input_par == 0:
            self.open.parity = Parity.none
        elif input_par == 1:
            self.open.parity = Parity.odd
        elif input_par == 2:
            self.open.parity = Parity.even
        elif input_par == 3: #mark doesn't work for serial 
            self.open.parity = Parity.mark
        elif input_par == 4:
            self.open.parity = Parity.space
        else:
            return ("Invalid input")
        return ('Parity: ' + str(self.open.parity))
    
    #Method to set number of stopbits
    # StopBits: one - 1, One-half - 1.5, Two - 2
    def stopbit(self, input_sb):
        """
        Input the assigned integer for the corresponding value.
        StopBits: one - 1, One-half - 1.5, Two - 2
        """
        if float(input_sb) == 1:
            self.open.stop_bits = StopBits.one
        elif float(input_sb)== 1.5:
            self.open.stop_bits = StopBits.one_and_a_half
        elif float(input_sb) == 2:
            self.open.stop_bits = StopBits.two
        else:
            return("Invalid input")
        return ('Stop Bit: ' + str(self.open.stop_bits))
    
    
    # Method to change baudrate, range of 0 to 4294967295            
    def baudrate(self,input_br):
        """
        Set baudrate between the range of 0 to 4294967295
        """
        self.open.baud_rate = int(input_br)
        return ('Baudrate: ' + str(self.open.baud_rate))
    
    
    # Method to change databits, range of 5 to 8
    def databits(self,input_db):
        """
        Set databits, range of 5 to 8
        """
        self.open.data_bits = int(input_db)
        return ('Databits: ' + str(self.open.data_bits))
    
    
    # Method to set read termination character/sequence
    def rtermination(self,input_rt):
        """
        Set the read terminator sequence/characters
        """
        self.open.read_termination = str(input_rt)
        return('Read Terminator: ' + repr(str(self.open.read_termination)))

    
    # Method to set write termination character/sequence
    def wtermination(self,input_wt):
        """
        Set the write terminator sequence/characters
        """
        self.open.write_termination = str(input_wt)
        return('Write Terminator: ' + repr(str(self.open.write_termination)))
    
    
    # Method to set timeout in millisecond, set to 0 for no timeout
    def timeout(self,input_to):
        """
        Set the timeout in ms to wait for instrument response
        """
        self.open.timeout = int(input_to)
        return ('Timeout: ' + str(self.open.timeout) + 'ms')
    
### General Methods for user SCPI command inputs    
    # Method to send in general query(write follow by read)
    def query(self,input_query):
        """
        Send a user input SCPI command to instrument followed by a read
        """
        reply = self.open.query(str(input_query))
        return str(reply)
    
    
    # Method to read from instrument
    def read(self):
        """
        Read from instrument
        """
        reply = self.open.read()
        return str(reply)
    
    
    # Method to write to instrument
    def write(self,input_w):
        """
        Write to instrument
        """
        reply = self.open.write(str(input_w))
        return str(reply)
    
    
### General Methods for SCPI commands common in all instruments
    def getid(self):
        """
        Get Instrument ID
        """
        reply = self.open.query('*IDN?')
        return str(reply)
    
    def reset(self):
        """
        Reset instrument
        """
        self.open.write('*RST')
        return ('Reset')
    
    def clear(self):
        """
        Clear instrument
        """
        self.open.write('*CLS')
        return('Cleared')
    
    def trigger(self):
        """
        Force trigger
        """
        self.open.write('*TRG')
        return('Trigger sent')

    def test(self):
        """
        Perform a self-test and then return the self-test results.
        """
        reply = self.open.query('*TST?')
        return str(reply)
        
