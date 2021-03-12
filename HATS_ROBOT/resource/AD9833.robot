*** Settings ***
Library           ../../HATS/ad9833.py

*** Keywords ***
to_generate_waveform
    [Arguments]    ${waveform}=sine    ${frequency}=1000
    [Documentation]    Generate desire waveform and frequency
    ...    Waveform options : sine,square,triangle,sleep
    ...    Frequency range : 0-12.5 mhz
    #generate('waveform',freuqency)
    #example syntax :    generate    sine    1000
    ${Generate_waveform}    generate    ${waveform}    ${frequency}
    Should Contain    ${Generate_waveform}    ${success}

to_sweep
    [Arguments]    ${waveform}=sine    ${begin}=1000    ${end}=5000    ${inc_freq}=10
    [Documentation]    Sweeps from beginning to ending frequency with adjustable interval
    ...    Freuqncy range: 0 - 12.5 Mhz
    #sweep('waveform',begin_freq,end_freq,inc_freq)
    #example syntax: sweep    sine    10    5000    10
    sweep    ${waveform}    ${begin}    ${end}    ${inc_freq}

to_reset
    [Documentation]    Resets the waveform generator
    #reset()
    reset
