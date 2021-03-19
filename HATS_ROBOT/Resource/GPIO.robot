*** Settings ***
Library           ../../HATS/gpio.py

*** Keywords ***
to_en_dc_converter
    [Arguments]    ${list}=[]    ${bool}=False
    [Documentation]    Enable or disable on baord DCDC converters
    ...    Input a list of voltages
    ...    List options: 5, 3.3 and 1.8
    ...    Bool options: True/False
    ...    e.g to enabl3 5V and 3.3V = [5,3.3], bool = True
    #example syntex: dcdc_en    [5,3.3]    True
    dcdc_en    ${list}    ${bool}

to_en_dac
    [Arguments]    ${bool}
    [Documentation]    Enable or disable on baord DAC power supply
    ...    Enables wave gen and pwm gen
    ...    Options: True/False
    dac_en    ${bool}

to_en_ldo
    [Arguments]    ${bool}
    [Documentation]    Enable or disable on baord LDO power supply
    ...    Enables ADC's
    ...    Options: True/False
    ldo_en    ${bool}
