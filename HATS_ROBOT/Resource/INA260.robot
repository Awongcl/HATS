*** Settings ***
Library           ../../HATS/ina260.py

*** Keywords ***
to_get_all
    [Documentation]    Get all readings, inlcuding voltage, current and power
    #get_all()
    get_all

to_get_voltage
    [Documentation]    Get voltage from voltage bus
    #get_voltage()
    ${voltage}    get_voltage
    [Return]    ${voltage}

to_get_current
    [Documentation]    Get current from current reg
    #get_current()
    get_current

to_get_power
    [Documentation]    Get power (Voltage * current )
    #get_power()
    get_power

to_set_all
    [Arguments]    ${average}=1    ${mode}= continous
    [Documentation]    Sets the average and mode together.
    ...    Average options: 1(default),4,16,64,128,256,512,1024
    ...    Mode options: ”triggered”/”continous”(defaullt)
    #set_all(self,avg =1 ,mode = "continous")
    #exampel syntex: set_all    16    triggered
    set_all    ${average}    ${mode}

to_get_config
    [Documentation]    Get the current average and mode
    #get_config()
    get_config

to_read_config
    [Documentation]    Read the value of the configure register.
    ...    16 bit hex value, detail please refer to datasheet
    #read_config()
    ${read_config}    read_config
    [Return]    ${read_config}

to_reset
    [Documentation]    Resets device, config reg to default
    #reset()
    reset
