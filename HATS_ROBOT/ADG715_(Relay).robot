*** Settings ***
Resource          Resource/ADG715.robot

*** Test cases ***
set_relay
    to_set_relay    [8]

reset_relay
    to_reset_relay

running
    to set relay    [2]
    to reset
    to set relay    [4]
    to reset
    to set relay    [5]
    to reset
