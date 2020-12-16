*** Settings ***
Library           ../HATS_GUI/ads1015.py

*** Variables ***
${success}        ${EMPTY}

*** Test Cases ***
Read_Voltage
    #read_voltage(mode='single',sample_rate=1600,gain=2.048)
    ${read_voltage}    Read Voltage    single    1600    2.048
    Should Contain    ${read_voltage}    ${success}
