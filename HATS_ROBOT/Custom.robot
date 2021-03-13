*** Settings ***
Resource          resource/ADG715.robot
Resource          resource/ADS1015.robot
Resource          resource/INA260.robot

*** Test Cases ***
LED sequence
    to_set_all    16    continous
    to_set_relay    [2]
    Sleep    1s
    to_get_all
    Sleep    1s
    to_set_relay    [2,4]
    Sleep    1s
    to_get_all
    Sleep    2s
    to_set_relay    [2,4,5]
    Sleep    1s
    to_get_all
    Sleep    2s
    to_set_relay    []
