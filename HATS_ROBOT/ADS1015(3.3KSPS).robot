*** Settings ***
Resource          Resource/ADS1015.robot

*** Variables ***

*** Test Cases ***
get_all_voltage
    to_get_all_voltage    continous    1600    6.144

get_voltage_single_Channel
    get_voltage    continous    1600    4.096    in0/gnd

set_digital_comparator
    to_set_digital_comparator    traditional    1    1

Get_Config
    to_get_config

reset_ads1015
    to_reset_ads1015
