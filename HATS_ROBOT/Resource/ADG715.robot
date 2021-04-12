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
    adg715.set_relay    ${list}

to_read_relay
    [Documentation]    To read the current state of the relays
    ...    Relays 1-8 is = 0x0000 0000
    ...    If relay 1 and 2 is ON, returns 0x0000 0011 = 3 in int
    adg715.read_relay

to_reset_relay
    adg715.reset_relay
