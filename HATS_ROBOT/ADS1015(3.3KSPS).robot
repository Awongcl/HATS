*** Settings ***
Resource          resource/ADS1015.robot

*** Variables ***

*** Test Cases ***
get_all_voltage
    to_get_all_voltage    single    1600    4.096

get_voltage_single_Channel
    get_voltage    single    1600    4.096    in0/gnd

set_digital_comparator
    to_set_digital_comparator    traditional    1    1

Get_Config
    to_get_config

reset_ads1015
    to_reset_ads1015
