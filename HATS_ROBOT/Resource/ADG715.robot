*** Settings ***
Library           ../../HATS/adg715.py

*** Keywords ***
to_set_relay
    [Arguments]    ${list}=[]
    [Documentation]    Sets the relay state (ON/OFF)
    ...    Total of 8 relays , numbered from 1-8
    ...    Input format : e.g turn on 1 and 8 : [1,8]
    ...    The return reg value is in DEC, convert back into BINARY
    ...    e.g 26 = 00011010 = switch [2,4,5]
    ...    Switch will be low if not indicated.
    #set_relay(arr[ ])
    #example syntax: set_relay    [1,8]
    set_relay    ${list}

to_reset_relay
    reset_relay
