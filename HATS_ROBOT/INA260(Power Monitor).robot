*** Settings ***
Resource          resource/INA260.robot

*** Test Cases ***
get_all
    to_get_all

get_voltage
    ${success}    Convert To Number    4.9
    ${voltage}    to_get_voltage
    Log    ${voltage}
    Should Be Equal As Numbers    ${voltage}    ${success}    precision=1

get_current
    to_get_current

get_power
    to_get_power

get_config
    to_get_config

set_all
    to_set_all    16    triggered

read_config
    to_read_config

reset
    to_reset
