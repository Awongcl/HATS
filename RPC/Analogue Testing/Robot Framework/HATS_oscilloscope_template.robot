*** Settings ***
Library           ../Automated MANUCA Testing/HATS_VISA_high.py

*** Variables ***

*** Test Cases ***
Initialise VISA Resource Manager
    [Documentation]    Initialise back-end pyvisa-py resource manager. This needs to be called before any other function
    ###============================================ Initialisation=========================================================
    #VISA_init(void)
    #Syntax: ${variable}    VISA_init
    ${visainit} =    VISA_init
    Log    ${visainit}

Search Ports for Resources
    [Documentation]    Scan through available ports (Some ports type such as ethernet port(s) will not be reflected)
    #scan_resource(void)
    #Syntax: ${variable}    scan_resource
    ${sresource}    scan_resource
    Log    ${sresource}

Initialise an oscilloscope instrument
    [Documentation]    Instantiate an instrument of type oscilloscope
    #create_oscillokscope(inst_name,port)
    #Syntax: ${variable}    create_oscilloscope    'instrument_name'    'port'
    ${oscilloscope}    create_oscilloscope    rigol    TCPIP::169.254.27.72::INSTR
    Log    ${oscilloscope}

Get Instrument ID
    [Documentation]    Function to get the ID of the instrument
    #This function and subsequent instrument command functions need to be used with inst_func in this format: inst_func('inst_name',func_name,func_arg1,func_arg2,...)
    #getid(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    getid
    ${success} =    Set Variable    RIGOL TECHNOLOGIES
    ${getid}    inst_func    rigol    getid
    Log    ${getid}
    Should Contain    ${getid}    ${success}

Reset
    [Documentation]    Reset the oscilloscope (To ensure starting off from default settings)
    #reset(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    reset
    ${reset} =    inst_func    rigol    reset
    Sleep    5 seconds
    ###========================================End of Initialisation=======================================================

Autoscale
    [Documentation]    Autoscale on oscilloscope, akin to pressing "AUTO" button
    #autoscale(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    autoscale
    ${autoscale}    inst_func    rigol    autoscale
    Log    ${autoscale}
    Sleep    7 seconds

Set Timebase Scale (X-axis)
    [Documentation]    Set the x-axis timescale per s/div, default value of 1us
    ###========================================Start of Horizontal Settings=====================================================
    #set_timebase_scale(scale=0.000001)
    #Syntax: ${variable}    inst_func    'instrument_name'    set_timebase_scale    'value'
    ${timebase}    inst_func    rigol    set_timebase_scale    0.001
    Log    ${timebase}
    #get_timebase_scale(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_timebase_scale
    ${timebase}    inst_func    rigol    get_timebase_scale
    Log    ${timebase}
    ###========================================End of Horizontal Settings=======================================================

Set Channel Coupling
    [Documentation]    Set the selected channel's coupling type (DC, AC, GND) and call function to verify instrument actual value
    ###========================================Start of Channel Settings=====================================================
    #set_channel_coupling(coupling="DC",channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    set_channel_coupling    'coupling'    'channel'
    ${coupling}    inst_func    rigol    set_channel_coupling    'DC'    1
    Log    ${coupling}
    #get_channel_coupling(channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_channel_coupling    'channel'
    ${coupling}    inst_func    rigol    get_channel_coupling    1
    Log    ${coupling}

Set Channel Bandwidth
    [Documentation]    Set the selected channel's bandwidth limit to (20M, OFF) and call function to verify instrument actual value
    #set_bandwidth_limit(type="OFF",channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    set_bandwidth_limit    'type'    'channel'
    ${bandwidth}    inst_func    rigol    set_bandwidth_limit    'OFF'    1
    Log    ${bandwidth}
    #get_bandwidth_limit(channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_bandwidth_limit    'channel'
    ${bandwidth}    inst_func    rigol    get_bandwidth_limit    1
    log    ${bandwidth}

Set Channel Probe Ratio
    [Documentation]    Set the selected channel's probe ratio to (0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000) and call function to verify instrument actual value
    #set_probe_ratio(probe_ratio=10, channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    set_probe_ratio    'probe_ratio'    'channel'
    ${ratio}    Convert to Number    10
    ${channel}    Convert to Integer    1
    ${probe}    inst_func    rigol    set_probe_ratio    ${ratio}    ${channel}
    Log    ${probe}
    #get_probe_ratio(channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_probe_ratio    'channel'
    ${channel}    Convert to Integer    1
    ${probe}    inst_func    rigol    get_probe_ratio    ${channel}
    Log    ${probe}

Set Channel Vertical Scale (Y-axis)
    [Documentation]    Set the selected channel's y-axis scale (v/div) and call function to verify instrument actual value
    #set_channel_scale(scale=1,channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    set_channel_scale    'scale'    'channel'
    ${scale}    Convert to Number    1
    ${channel}    Convert to Integer    1
    ${vscale}    inst_func    rigol    set_channel_scale    ${scale}    ${channel}
    Log    ${vscale}
    #get_channel_scale(channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_channel_scale    'channel'
    ${channel}    Convert to Integer    1
    ${vscale}    inst_func    rigol    set_channel_scale    ${channel}
    Log    ${vscale}
    ###========================================End of Channel Settings=======================================================

Set Trigger Source
    [Documentation]    Set the channel scource for trigger and call function to verify instrument actual value
    ###========================================Start of Trigger Settings=====================================================
    #set_trigger_source(channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    set_trigger_source    'channel'
    ${channel}    Convert to Integer    1
    ${triggersource}    inst_func    rigol    set_trigger_source    ${channel}
    Log    ${triggersource}
    #get_trigger_source(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_trigger_source
    ${triggersource}    inst_func    rigol    get_trigger_source
    Log    ${triggersource}

Set Trigger Type
    [Documentation]    Set the trigger type (PULS,RUNT,WIND,NEDG,SLOP,VID,PATT,DEL,TIM,DUR,SHOL,RS232,IIC,SPI,EDGE) and call function to verify instrument actual value
    #set_trigger_mode(mode="EDGE")
    #Syntax: ${variable}    inst_func    'instrument_name'    set_trigger_mode    'mode'
    ${mode}    inst_func    rigol    set_trigger_mode    'EDGE'
    Log    ${mode}
    #get_trigger_mode(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_trigger_mode
    ${mode}    inst_func    rigol    get_trigger_mode
    Log    ${mode}

Set Trigger Edge Slope
    [Documentation]    Set the trigger slope for EDGE trigger type (POS,NEG,RFALI) and call function to verify instrument actual value
    #set_trigger_direction(direction="POS")
    #Syntax: ${variable}    inst_func    'instrument_name'    set_trigger_direction    'direction'
    ${direction}    inst_func    rigol    set_trigger_direction    'POS'
    Log    ${direction}
    #get_trigger_direction(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_trigger_direction
    ${direction}    inst_func    rigol    get_trigger_direction
    Log    ${direction}

Set Trigger Sweep
    [Documentation]    Set the trigger sweep (AUTO, NORM, SING) and call function to verify instrument actual value
    #set_trigger_sweep(mode="AUTO")
    #Syntax: ${variable}    inst_func    'instrument_name'    'mode'
    ${sweep}    inst_func    rigol    set_trigger_sweep    'AUTO'
    Log    ${sweep}
    #get_trigger_sweep(void)
    #Syntax: ${variable}    inst_func    'instrument_name'
    ${sweep}    inst_func    rigol    get_trigger_sweep
    Log    ${sweep}

Set Trigger Level
    [Documentation]    Set Trigger level and call function to verify instrument actual value
    #set_trigger_level(level,source=None)
    #Syntax: ${variable}    inst_func    'instrument_name'    set_trigger_level    'level'    'source'
    ${level}    Convert to Number    2
    ${triggerlevel}    inst_func    rigol    set_trigger_level    ${level}
    Log    ${triggerlevel}
    #get_trigger_level(source=None)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_trigger_level    'source'
    ${triggerlevel}    inst_func    rigol    get_trigger_level
    Log    ${triggerlevel}
    ###========================================End of Trigger Settings=====================================================

Sleep
    [Documentation]    Sleep to allow time for instrument to take waveform sample after trigger, modify the value in seconds as needed
    Sleep    10 seconds

Force Trigger
    [Documentation]    Manually trigger oscilloscope. Only for mode(NORM, SING)
    #force_trigger(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    force_trigger
    ${trigger}    inst_func    rigol    force_trigger
    Log    ${trigger}
    Sleep    5 seconds

Measurement Source
    [Documentation]    Set channel to take measurements from and call function to verify instrument actual value
    ###========================================Start of Measurement Settings=====================================================
    #set_measurement_source(channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    set_measurement_source    'channel'
    ${channel}    Convert to Integer    1
    ${source}    inst_func    rigol    set_measurement_source    ${channel}
    Log    ${source}
    #get_measurement_source(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_measurement_source
    ${source}    inst_func    rigol    get_measurement_source
    Log    ${source}

Clear Measurement
    [Documentation]    Clear one or all of the last five measurement items enabled ("ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ALL")
    #clear_measurement(item="ALL")
    #Syntax: ${variable}    inst_func    'instrument_name'    clear_measurement    'item'
    ${measure}    inst_func    rigol    clear_measurement    'ALL'
    Log    ${measure}
    Sleep    1 second

Measure Item 1 (Period)
    [Documentation]    Measure an item from obtained waveform ("VMAX","VMIN","VPP","VTOP","VBAS","VAMP","VAVG","VRMS","OVER","PRES","MAR","MPAR"
    ...    ,"PER","FREQ","RTIM","FTIM","PWID","NWID","PDUT","NDUT","RDEL","FDEL","RPH","FPH","TVMAX","TVMIN","PSLEW","NSLEW","VUP","VMID","VLOW",
    ...    "VARI","PVRMS") and call function to verify instrument actual value
    #show_measurement(item, channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    show_measurement    'item'    'channel'
    ${channel}    Convert to Integer    1
    ${measure}    inst_func    rigol    show_measurement    'PER'    ${channel}
    Log    ${measure}
    #get_measurement(item, type="CURR",channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_measurement    'item'    'type'    'channel'
    ${channel}    Convert to Integer    1
    ${measure}    inst_func    rigol    get_measurement    'PER'    'CURR'    ${channel}
    Log    ${measure}
    Sleep    1 second

Measure Item 2 (Frequency)
    [Documentation]    Measure an item from obtained waveform ("VMAX","VMIN","VPP","VTOP","VBAS","VAMP","VAVG","VRMS","OVER","PRES","MAR","MPAR"
    ...    ,"PER","FREQ","RTIM","FTIM","PWID","NWID","PDUT","NDUT","RDEL","FDEL","RPH","FPH","TVMAX","TVMIN","PSLEW","NSLEW","VUP","VMID","VLOW",
    ...    "VARI","PVRMS") and call function to verify instrument actual value
    #show_measurement(item, channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    show_measurement    'item'    'channel'
    ${channel}    Convert to Integer    1
    ${measure}    inst_func    rigol    show_measurement    'FREQ'    ${channel}
    Log    ${measure}
    #get_measurement(item, type="CURR",channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_measurement    'item'    'type'    'channel'
    ${channel}    Convert to Integer    1
    ${measure}    inst_func    rigol    get_measurement    'FREQ'    'CURR'    ${channel}
    Log    ${measure}
    Sleep    1 second

Measure Item 3 (Vrms)
    [Documentation]    Measure an item from obtained waveform ("VMAX","VMIN","VPP","VTOP","VBAS","VAMP","VAVG","VRMS","OVER","PRES","MAR","MPAR"
    ...    ,"PER","FREQ","RTIM","FTIM","PWID","NWID","PDUT","NDUT","RDEL","FDEL","RPH","FPH","TVMAX","TVMIN","PSLEW","NSLEW","VUP","VMID","VLOW",
    ...    "VARI","PVRMS") and call function to verify instrument actual value
    #show_measurement(item, channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    show_measurement    'item'    'channel'
    ${channel}    Convert to Integer    1
    ${measure}    inst_func    rigol    show_measurement    'VRMS'    ${channel}
    Log    ${measure}
    #get_measurement(item, type="CURR",channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_measurement    'item'    'type'    'channel'
    ${channel}    Convert to Integer    1
    ${measure}    inst_func    rigol    get_measurement    'VRMS'    'CURR'    ${channel}
    Log    ${measure}
    Sleep    1 second

Measure Item 4 (Vpeak-to-peak)
    [Documentation]    Measure an item from obtained waveform ("VMAX","VMIN","VPP","VTOP","VBAS","VAMP","VAVG","VRMS","OVER","PRES","MAR","MPAR"
    ...    ,"PER","FREQ","RTIM","FTIM","PWID","NWID","PDUT","NDUT","RDEL","FDEL","RPH","FPH","TVMAX","TVMIN","PSLEW","NSLEW","VUP","VMID","VLOW",
    ...    "VARI","PVRMS") and call function to verify instrument actual value
    #show_measurement(item, channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    show_measurement    'item'    'channel'
    ${channel}    Convert to Integer    1
    ${measure}    inst_func    rigol    show_measurement    'VPP'    ${channel}
    Log    ${measure}
    #get_measurement(item, type="CURR",channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_measurement    'item'    'type'    'channel'
    ${channel}    Convert to Integer    1
    ${measure}    inst_func    rigol    get_measurement    'VPP'    'CURR'    ${channel}
    Log    ${measure}
    Sleep    1 second

Measure Item 5 (V Average)
    [Documentation]    Measure an item from obtained waveform ("VMAX","VMIN","VPP","VTOP","VBAS","VAMP","VAVG","VRMS","OVER","PRES","MAR","MPAR"
    ...    ,"PER","FREQ","RTIM","FTIM","PWID","NWID","PDUT","NDUT","RDEL","FDEL","RPH","FPH","TVMAX","TVMIN","PSLEW","NSLEW","VUP","VMID","VLOW",
    ...    "VARI","PVRMS") and call function to verify instrument actual value
    #show_measurement(item, channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    show_measurement    'item'    'channel'
    ${channel}    Convert to Integer    1
    ${measure}    inst_func    rigol    show_measurement    'VAVG'    ${channel}
    Log    ${measure}
    #get_measurement(item, type="CURR",channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_measurement    'item'    'type'    'channel'
    ${channel}    Convert to Integer    1
    ${measure}    inst_func    rigol    get_measurement    'VAVG'    'CURR'    ${channel}
    Log    ${measure}
    Sleep    1 second
    ###========================================End of Measurement Settings=====================================================

Take a Screenshot
    [Documentation]    Take a screenshot of the oscilloscope display and save the .png file in the same folder as this script
    #take_screenshot(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    take_screenshot
    Sleep    5 Seconds
    ${screenshot}    inst_func    rigol    take_screenshot
    Log    ${screenshot}

Plot waveform
    [Documentation]    Sample the waveform and plot them on a graph and save it as a .png file in the same folder as this script
    #get_waveform_samples(channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_waveform_samples    'channel'
    ${value}    Convert to Integer    1
    ${x}    ${y} =    inst_func    rigol    get_waveform_samples    ${value}
    Log    ${x}
    Log    ${y}
    ${plot}    plt_plot    ${x}    ${y}
    Log    ${plot}
    ${save}    plt_savefig
    Log    ${save}

Plot waveform 2
    [Documentation]    Sample the waveform and plot them on a graph and show graph as a pop-up. Image pop-up will pause test-case and have to be closed to continue running the test cases
    #get_waveform_samples(channel=1)
    #Syntax: ${variable}    inst_func    'instrument_name'    get_waveform_samples    'channel'
    ${value}    Convert to Integer    2
    ${x}    ${y} =    inst_func    rigol    get_waveform_samples    ${value}
    Log    ${x}
    Log    ${y}
    ${plot}    plt_plot    ${x}    ${y}
    Log    ${plot}
    ${show}    plt_show
    Log    ${show}

Deinitialise an instrument
    [Documentation]    Deinitialise instrument by closing the port and deleting the instrument
    ###========================================Start of Teardown=====================================================
    #deinit(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    deinit
    ${instdeinit}    inst_func    rigol    deinit
    Log    ${instdeinit}
    #Starting from this point, instrument is no longer controlled and inst_func is no longer called
    #inst_deinit(inst_name)
    #Syntax: ${variable}    inst_deinit    'instrument_name'
    ${instdeinit}    inst_deinit    rigol
    Log    ${instdeinit}

Deinitialise VISA Resource Manager
    [Documentation]    Denitialise back-end pyvisa-py resource manager
    #VISA_deinit(void)
    #Syntax: ${variable}    VISA_deinit
    ${visadeinit}    VISA_deinit
    Log    ${visadeinit}
    ###========================================End of Teardown=====================================================
