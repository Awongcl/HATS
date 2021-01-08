*** Settings ***
Library           ../HATS/ad9833.py

*** Variables ***
${success}        success

*** Test Cases ***
Generate_waveform
    [Documentation]    Generate desire waveform and frequency
    ...    Waveform options : sine,square,triangle,sleep
    ...    Frequency range : 0-12.5 mhz
    #generate('waveform',freuqency)
    ${Generate_waveform}    generate    sine    1000
    Should Contain    ${Generate_waveform}    ${success}

Sweep
    [Documentation]    Sweeps from beginning to ending frequency with adjustable interval
    ...    Freuqncy range: 0 - 12.5 Mhz
    #sweep('waveform',begin_freq,end_freq,inc_freq)
    sweep    sine    10    5000    10

Reset
    [Documentation]    Resets the waveform generator
    #reset()
    reset
