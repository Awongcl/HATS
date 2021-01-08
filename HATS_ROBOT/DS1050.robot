*** Settings ***
Library           ../HATS/ds1050.py

*** Test Cases ***
set_cycle
    [Documentation]    Sets duty cycle, 32 steps from 00000b to 11111b, each step = 3.0275%
    ...    Duty cycle option : 0 - 32 (default = 16)(0% to 96.88%)
    #set_cycle(step = 16)
    set_cycle    20

set_duty_full
    [Documentation]    Sets the duty cycle to 100%
    #set_full_cycle()
    set_full_cycle

shutdown
    [Documentation]    Enters shutdown mode (Low current)
    #shutdown()
    shutdown

wakeup
    [Documentation]    Wakes the IC up from shutdown mode
    #wakeup()
    wakeup

read
    [Documentation]    Reads the current PWM value, returns raw 5bit value
    #read()
    read
