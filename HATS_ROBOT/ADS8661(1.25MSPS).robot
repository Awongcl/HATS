*** Settings ***
Resource          resource/ADS8661.robot

*** Test Cases ***
get_voltage
    to_get_voltage

set_range
    to_set_range    10.24

get_raw_conversion
    to_get_raw_conversion

get_range
    to_get_range

reset
    to_Reset
