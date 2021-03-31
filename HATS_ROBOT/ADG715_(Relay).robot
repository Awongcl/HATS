*** Settings ***
Resource          Resource/ADG715.robot

*** Test cases ***
set_relay
    to_set_relay    [8]

read_relay
    to_read_relay

reset_relay
    to_reset_relay

test_relay
    to set relay    [2]
    sleep    1s
    to reset relay
    sleep    1s
    to set relay    [4]
    sleep    1s
    to reset relay
    to set relay    [5]
    to reset relay
