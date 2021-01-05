*** Settings ***
Library           ../HATS/ina260.py

*** Test Cases ***
get_all
    [Documentation]    Get all the values, inlcuding:
    ...    Voltage, current and power.
    #get_all()
    get_all

get_voltage
    [Documentation]    Get voltage from voltage bus
    #get_voltage()
    get_voltage

get_current
    [Documentation]    Get current from current reg
    #get_current()
    get_current

get_power
    [Documentation]    Get \ power (Voltage * current )
    #get_power()
    get_power

set_all
    [Documentation]    Sets the average and mode together.
    ...    Average options: 1(default),4,16,64,128,256,512,1024
    ...    Mode options: ”trigger”/”continous”
    #set_all(self,avg =1 ,mode = "continous")
    set_all    1    continous

read_config
    [Documentation]    Read the value of the configure register.
    #read_config()
    read_config

reset
    [Documentation]    Resets device, config reg to default
    #reset()
    reset
