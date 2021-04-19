*** Settings ***
Resource          Resource/ADG715.robot
Resource          Resource/ADS1015.robot
Resource          Resource/ADG2128.robot
Resource          Resource/INA260.robot
Resource          Resource/ADS8661.robot
Resource          Resource/ADG715.robot
Resource          Resource/GPIO.robot

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
    ${3.2}    Convert To Number    3.2
    ${3.4}    Convert To Number    3.4
    to_en_dc_converter    [5]    True
    adg715.to_set_relay    [8]
    ads8661.to_reset
    ads8661.to_set_range    5.12
    to_reset_switch    1
    to_set_switch    1    on    0    0
    to_read_all_switch    1
    Sleep    1
    ${value}    ads8661.to_get_voltage
    Should Be Equal As Numbers    ${value}    ${3.2}    precision=1
    to_set_switch    1    off    0    0
    to_set_switch    1    on    0    1
    to_read_all_switch    1
    Sleep    1s
    ${value}    ads8661. to_get_voltage
    Should Be Equal As Numbers    ${value}    ${3.4}    precision=1
    to_reset_switch    1
    to_get_current
    to_get_power
    Sleep    2
    adg715.to_reset_relay
