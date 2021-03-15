*** Settings ***
Resource          Resource/AD9833.robot

*** Variables ***
${success}        success

*** Test Cases ***
Generate_waveform
    to_generate_waveform    sine    1000

Sweep
    to_sweep    sine    10    5000    10

Reset
    to_reset
