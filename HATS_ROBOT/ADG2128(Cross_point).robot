*** Settings ***
Resource          Resource/ADG2128.robot

*** Test Cases ***
set_switch
    to_set_switch    1    on    0    0

set_multiple_switch
    to_set_multiple_switch    1    on    [0,1,1,2]

read_switch
    to_read_switch    1    x0

read_all_switch
    to_read_all_switch    1

reset_switch
    to_reset_switch    1
