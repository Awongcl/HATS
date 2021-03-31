*** Settings ***
Resource          Resource/ADG715.robot
Resource          Resource/ADS1015.robot
Resource          Resource/ADG2128.robot
Resource          Resource/INA260.robot

*** Test Cases ***
LED sequence
    ${success}    Convert To Number    5
    to_set_all    16    triggered
    to_set_relay    [2]
    Sleep    1s
    ${value}    to_get_voltage
    Should Be Equal As Numbers    ${value}    ${success}    precision=0
    to_set_relay    [4]
    Sleep    1s
    ${value}    to_get_voltage
    Should Be Equal As Numbers    ${value}    ${success}    precision=0
    Sleep    1s
    to_set_relay    []

Relay
    to_set_relay    [1]
    to_set_relay    [1]

Demo
    ${success}    Convert To Number    3.3
    to_set_relay    [8]
    sleep    1s
    to_get_power
    to_get_voltage_single_channel    continous    1600    4.096    in0/gnd
    to_get_voltage_single_channel    continous    1600    4.096    in1/gnd
    to_set_relay    []
