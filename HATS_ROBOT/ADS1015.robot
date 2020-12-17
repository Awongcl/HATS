*** Settings ***
Library           ../HATS/ads1015.py

*** Variables ***
${success}        ${EMPTY}

*** Test Cases ***
Read_Voltage
    [Documentation]    Reads the voltage from all the channels.
    ...    Results:
    ...    First row = voltage
    ...    Second rwo = raw value
    #read_voltage(mode='single',sample_rate=1600,gain=2.048)
    ${read_voltage}    read_voltage    single    3200    4.032
    Should Contain    ${read_voltage}    ${success}

Read_voltage_single_Channel
    [Documentation]    Reads voltage from a single(selected) channel
    #read_voltage(mode='single',sample_rate=1600,gain=2.048,channel='in0/gnd')
    ${read_voltage}    read_voltage_single    single    1600    2.048    in0/gnd
    Should Contain    ${read_voltage}    ${success}

Reset
    [Documentation]    Reset the ADC (Registers)
    #reset()
    reset

Get_Config
    [Documentation]    Get the current configuration of the ADC.
    ...    This includes: Sample rate, gain , mode, high/low threshold.
    #get_config
    Get Configs

set_digital_comparator
    [Documentation]    Set the mode, high and low threshold of the comparator.
    #set_digital_comparator(high_thresh=20000,low_thresh=5000,mode='window')
    Set Digital Comparator    2000    500    traditional
