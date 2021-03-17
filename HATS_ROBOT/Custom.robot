*** Settings ***
Resource          Resource/ADG715.robot
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
    to_set_relay    [2]
    to_set_relay    [3]
    to_set_relay    [4]
    to_set_relay    [5]
    to_set_relay    [6]
    to_set_relay    [7]
    to_set_relay    [8]
