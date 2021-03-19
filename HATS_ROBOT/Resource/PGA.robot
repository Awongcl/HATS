*** Settings ***
Library           ../../HATS/gpio.py

*** Keywords ***
to_set_pga
    [Arguments]    ${gain}=1
    [Documentation]    Set the gain of PGA
    ...    Gain options: 0,1,2,5,10,20,50,100
    set_pga_gain    ${gain}
