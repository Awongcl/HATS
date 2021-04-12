# -*- coding: utf-8 -*-
import HATS_VISA_base as hv_base
import HATS_VISA_oscilloscope as hv_os
import HATS_VISA_multimeter as hv_mm
import matplotlib.pyplot as plt
import time

inst = dict()
### Function wrappers
def VISA_init():
    """
    Initiate PyVISA-py backend as resource manager.
    """
    return hv_base.VISA_init()

def scan_resource():
    """
    Scan and return all available ports. Not all port type will be listed. Eg. available TCPIP type ports will not be listed
    """
    return hv_base.scan_resource()
        
def opened_resource():
    """
    List ports that are currently connected.
    """
    return hv_base.opened_resource()

def VISA_deinit():
    """
    Deinitialise PyVISA-py backend as resource manager.
    """
    return hv_base.VISA_deinit()


###Instrument Creation
def create_visainst(inst_name,port):
    """
    Create a VISA instrument (basic)
    """
    global inst
    inst_name = str(inst_name)
    inst[inst_name] = hv_base.VISAinst(port)
    return inst[inst_name]
    
def create_oscilloscope(inst_name,port):
    """
    Create a VISA instrument (oscilllloscope)
    """
    global inst
    inst_name = str(inst_name)
    inst[inst_name] = hv_os.oscilloscope(port)
    return inst[inst_name]
    
def create_multimeter(inst_name,port):
    """
    Create a VISA instrument (multimeter)
    """
    global inst
    inst_name = str(inst_name)
    inst[inst_name] = hv_mm.multimeter(port)
    return inst[inst_name]
    
def inst_deinit(inst_name):
    """
    Delete instrument instance
    """
    global inst
    assert inst_name in inst
    del inst[inst_name]
    inst_name = "'" + str(inst_name) + "'"
    return inst_name + ' closed'
    

###Methods & attribute wrapper
    #Note: String arguments have to be exeplicitly wrapped "'str'"
    #rterminator/wterminator such as "'\n'" need to be input as "'\\n'" to send literal
def inst_func(inst_name,func_name,*args):
    """
    Instrument instance wrapper
    """
    global inst
    assert inst_name in inst
    assert func_name in dir(inst[inst_name])
    att = func_name in vars(inst[inst_name])
    func_arg = '('
    for i in args:
        func_arg = func_arg + str(i) + ','
    func_arg = func_arg[:-1]
    if len(func_arg) != 0:
        func_arg = func_arg + ')'
    elif att == 0: #Not an attribute
        func_arg = '()'
    comm = 'inst[\''+str(inst_name) +'\'].'+ str(func_name) + func_arg
    resp = eval(comm)
    return resp

    
###Function wrapper for robot framework
def plt_plot(x,y):
    return plt.plot(x,y)

def plt_show():
    return plt.show()

def plt_savefig():
    """
    Save a plot inot .png file with date and time as file name.
    """
    filename = time.strftime("%Y-%m-%d_%H-%M-%S.png", time.localtime())
    return plt.savefig(filename)
