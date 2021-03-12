*** Settings ***
Library           ../HATS/ads8661.py

*** Test Cases ***
get_voltage
    [Documentation]    Gets voltage reading from analog input
    ...    AIN_P - AIN_GND
    #get_votlage()
    get_voltage

set_range
    [Documentation]    Set the range of the PGA
    ...    options: "+12.288"(default),"+-10.24","+-6.144","+-5.12", "+2.56","12.288","10.24","6.144","5.12"
    #set_range()
    set_range    5.12

get_raw_conversion
    [Documentation]    Get the raw 32bit conversion value
    ...    Bit field please refer to data sheet (ADS8661)
    #get_raw_conversion()
    Get Raw Conversion

get_range
    [Documentation]    Get the current range of the PGA
    #get_range()
    Get Range

reset
    [Documentation]    Resets IC to default values, power on state
    #reset()
    Reset
