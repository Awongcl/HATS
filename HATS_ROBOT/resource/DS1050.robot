*** Settings ***
Library           ../../HATS/ds1050.py

*** Keywords ***
to_set_cycle
    [Arguments]    ${cycle}=16
    [Documentation]    Sets duty cycle, 32 steps from 00000b to 11111b (0% to 96.88%), each step = 3.125%
    ...    Duty cycle option : 0 - 31 (default = 16)(0% to 96.88%)
    #set_cycle(step = 16)
    #example syntax: set_cycle    20
    set_cycle    ${cycle}

to_set_duty_full
    [Documentation]    Sets the duty cycle to 100%
    #set_full_cycle()
    set_full_cycle

to_shutdown
    [Documentation]    Enters shutdown mode (Low current)
    #shutdown()
    shutdown

to_wakeup
    [Documentation]    Wakes the IC up from shutdown mode
    #wakeup()
    wakeup

to_read
    [Documentation]    Reads the current PWM value, returns raw 5bit value
    ...    To convert raw value to percentage : raw value * 3.125 %
    #read()
    read
