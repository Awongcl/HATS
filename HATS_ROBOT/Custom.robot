*** Settings ***
Resource          resource/ADG715.robot
Resource          resource/INA260.robot

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
