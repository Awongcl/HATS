*** Settings ***
Resource          Resource/DS1050.robot

*** Test Cases ***
set_cycle
    to_set_cycle    5

set_duty_full
    to_set_full_cycle

shutdow
    to_shutdown

wakeup
    to_wakeup

read
    to_read
    Log    Reg read
