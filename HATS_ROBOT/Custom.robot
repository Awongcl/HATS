*** Settings ***
Resource          resource/adg715.robot
Resource          resource/ADS1015.robot

*** Test Cases ***
custome test
    to_set_relay    [2,4,5]
    to_get_all_voltage    single    1600    4.096
    Sleep    5s
    to_set_relay    []
