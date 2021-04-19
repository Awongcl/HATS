*** Settings ***
Library           ../../HATS/ads8661.py

*** Keywords ***
to_get_voltage
    [Documentation]    Gets voltage reading from analog input
    ...    Differential between AIN_P - AIN_GND pins
    #get_votlage()
    ${voltage}    ads8661.get_voltage
    [Return]    ${voltage}

to_set_range
    [Arguments]    ${gain}=+-12.288
    [Documentation]    Set the range/gain of the PGA
    ...    options: "+-12.288"(default),"+-10.24","+-6.144","+-5.12", "+2.56","12.288","10.24","6.144","5.12"
    #set_range()
    #example syntax:    set_range    5.12
    ads8661.set_range    ${gain}

to_get_raw_conversion
    [Documentation]    Get the raw 32bit conversion value
    ...    Bit fielsd please refer to data sheet (ADS8661)
    #get_raw_conversion()
    ads8661.Get Raw Conversion

to_get_range
    [Documentation]    Get the current range/gain settings of the PGA
    #get_range()
    ads8661.Get Range

to_reset
    [Documentation]    Resets IC to default values, power on state
    #reset()
    ads8661.Reset
