*** Settings ***
Library           ../../HATS/adg2128.py

*** Keywords ***
to_set_switch
    [Arguments]    ${device}    ${control}    ${x}    ${y}
    [Documentation]    Set state of a single switch
    ...    Device options: 1,2
    ...    Control options: on, off
    ...    X options: 0-11 , Y options: 0-7
    #example syntax: set_swtich    1    on    0    1
    set_switch    ${device}    ${control}    ${x}    ${y}

to_set_multiple_switch
    [Arguments]    ${device}    ${control}    ${list}=[]
    [Documentation]    Set multiple switch state at once
    ...    Device options : 1,2 Control options: “on”/”off”
    ...    list input : pairs of switches [x,y]
    ...    e.g [1,2,5,6,7,8] = X1&Y2 , X5&y6, X7&Y8
    ...    Register will latched during the sending sequence
    ...    Register will be update at once after the last command
    ...    Meaning all switches will be update simultaneously
    #example syntax: set_multiple_switch    1 on [1,2,1,3]
    set_multiple_switch    ${device}    ${control}    ${list}

to_read_switch
    [Arguments]    ${device}    ${line}
    [Documentation]    Read back to is read the current state of a line e.g X1
    ...    When X0 is entered, this function returns a byte to indicate which Y is connected.
    ...    e.g Param = X0, returns 0x03 = 0000 0011
    ...    X0 is connected with Y0 and Y1
    ...    Line options: X0-7
    ...    Device options: 1,2
    #example syntax:    read_switch    1    x0
    read_switch    ${device}    ${line}

to_reset_switch
    [Arguments]    ${device}
    [Documentation]    Resets switch
    ...    Device options : 1,2,3(3 = 1 and 2)
    #example syntax:    reset_switch    1
    reset_switch    ${device}
