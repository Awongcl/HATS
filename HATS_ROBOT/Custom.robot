*** Settings ***
Resource          Resource/ADG715.robot
Resource          Resource/ADS1015.robot
Resource          Resource/ADG2128.robot
Resource          Resource/INA260.robot
Resource          Resource/ADS8661.robot

*** Test Cases ***
LED sequence
    ${success}    Convert To Number    3.3
    to_set_all    16    continous
    Sleep    1s
    ${value}    to_get_voltage_single_channel    continous    1600    4.096    in0/gnd
    Should Be Equal As Numbers    ${value}    ${success}    precision=0
    Sleep    1s
    ${value}    to_get_voltage_single_channel    continous    1600    4.096    in0/gnd
    Should Be Equal As Numbers    ${value}    ${success}    precision=0
    Sleep    1s

Relay
    to_set_relay    [1]
    to_set_relay    [1]

Demo
    ${3.3}    Convert To Number    3.3
    to_reset_switch    2
    to_set_switch    2    on    0    1
    to_read_all_switch    2
    Sleep    1s
    to_set_range    5.12
    ads8661.to_get_voltage
    to_set_switch    2    off    0    1
    to_set_switch    2    on    0    2
    to_read_all_switch    2
    Sleep    1s
    ads8661. to_get_voltage
