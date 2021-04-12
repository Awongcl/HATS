*** Settings ***
Library           ../../HATS/ads1015.py

*** Keywords ***
to_get_all_voltage
    [Arguments]    ${mode}=single    ${sample_rate}=1600    ${gain}=2.048
    [Documentation]    Reads the voltages from all the channels.
    ...    mode options: 'single'/'continuous'
    ...    sample rate options: 128, 250, 490, 920, 1600 (default), 2400 or 330
    ...    Gain options:(+-) 6.144, 4.096, 2.048 (default), 1.024, 0.512 or 0.256
    ...    Results:
    ...    First row = voltage
    ...    Second rwo = raw value
    #get_all_voltage(mode = "single",sample_rate=1600,gain=2.048)
    # example syntax:    get_all_voltage    single    1600    2.048
    get_all_voltage    ${mode}    ${sample_rate}    ${gain}

to_get_voltage_single_Channel
    [Arguments]    ${mode}=single    ${sample_rate}=1600    ${gain}=2.048    ${channel}=in0/gnd
    [Documentation]    Reads voltage from a single(selected) channel
    ...    First 3 options same as above
    ...    Channel options: in0/gnd,in1/gnd,in2/gnd,in3/gnd,in0/in1,in0/in3,in1/in3,in2/in3
    #get_voltage(mode = "single",gain=2.048,rate=1600,channel="in0/gnd")
    #example syntax: get_voltage    single    1600    4.096    in0/gnd
    ${voltage}    ads1015.get_voltage    ${mode}    ${sample_rate}    ${gain}    ${channel}
    [Return]    ${voltage}

to_set_digital_comparator
    [Arguments]    ${mode}=traditional    ${low}=1    ${high}=1
    [Documentation]    Set the mode, high and low threshold of the comparator.
    ...    Threshold values( Important !) : Must be within the gain values, e.g. gain = +-4.096V, then threshold must be within +-4.046V
    ...    Modes : 'window', 'traditional'
    ...    e.g in window mode, alert/rdy pion asserts when the input is outside the bound of low and high threshold
    #set_digital_comparator(mode='traditional',low=0,high=0)
    # example syntax: Set Digital Comparator    traditional    1    2
    set_digital_comparator    ${mode}    ${low}    ${high}

to_get_config
    [Documentation]    Get the current configuration of the ADC.
    ...    This includes: Sample rate, gain , mode, comparator mode,high/low threshold, comparator polarity
    #get_config()
    Get Config

to_reset_ads1015
    [Documentation]    Resets the ADC (Registers)
    #reset()
    reset
