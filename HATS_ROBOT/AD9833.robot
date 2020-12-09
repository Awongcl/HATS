*** Settings ***
Library           ../ad9833_oled/freq.py

*** Test Cases ***
Generate
    [Documentation]    Generate desire waveform and frequency
    #Generate waveforrm
    Generate    sine    1000
