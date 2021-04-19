*** Settings ***
Library           ../HATS/HATS_VISA_high.py

*** Variables ***

*** Test Cases ***
Initialise VISA Resource Manager
    [Documentation]    Initialise back-end pyvisa-py resource manager. This needs to be called before any other function
    ###============================================ Start of Initialisation=========================================================
    ## Initialisation includes setting up parameters for RS-232 communication
    #VISA_init(void)
    #Syntax: ${variable}    VISA_init
    ${visainit}    VISA_init
    Log    ${visainit}

Search Ports for Resources
    [Documentation]    Scan through available ports (Some ports type such as ethernet port(s) will not be reflected)
    #scan_resource(void)
    #Syntax: ${variable}    scan_resource
    ${sresource}    scan_resource
    Log    ${sresource}

Initialise an instrument
    [Documentation]    Instantiate an instrument of type multimeter
    #create_multimeter(inst_name,port)
    #Syntax: ${variable}    create_multimmeter    'instrument_name'    'port'
    ${multimeter}    create_multimeter    hp    ASRL/dev/ttyUSB0::INSTR
    Log    ${multimeter}

List Opened Resources
    [Documentation]    List out resources that are currently opened (Verification function, not necessary for initialisation)
    #opened_resource(void)
    #Syntax: ${variable}    opened_resource
    ${oresource}    opened_resource
    Log    ${oresource}

HP34401A RS-232 Settings
    [Documentation]    Initialising RS-232 interface configuration for HP34401A. This includes setting baudrate, stopbits, read termination and write termination signals
    #This function and subsequent instrument command functions need to be used with inst_func in this format: inst_func('inst_name',func_name,func_arg1,func_arg2,...)
    ${success} =    Set Variable    Baudrate
    #baudrate(input_br)
    #Syntax: ${variable}    inst_func    'instrument_name'    baudrate    'input_br'
    ${baudrate}    inst_func    hp    baudrate    9600
    Log    ${baudrate}
    Should Contain    ${baudrate}    ${success}
    ${success} =    Set Variable    StopBits.two
    #stopbits(input_sb)
    #Syntax: ${variable}    inst_func    'instrument_name'    stopbits    'input_sb'
    ${stopbit}    inst_func    hp    stopbit    2
    Log    ${stopbit}
    Should Contain    ${stopbit}    ${success}
    ${success} =    Set Variable    n
    #rtermination(input_rt) Note: Additional forward slash is required to be added for operators such as '\n' or '\r' with double apostrophe for system to send the correct literal. Eg "\\n" for '\n'
    #Syntax: ${variable}    inst_func    'instrument_name'    rtermination    'input_rt'
    ${rterminator}    inst_func    hp    rtermination    "\\n"
    Log    ${rterminator}
    Should Contain    ${rterminator}    ${success}
    #wtermination(input_wt) Note: Additional forward slash is required to be added for operators such as '\n' or '\r' with double apostrophe for system to send the correct literal. Eg "\\n" for '\n'
    #Syntax: ${variable}    inst_func    'instrument_name'    wtermination    'input_wt'
    ${wterminator}    inst_func    hp    wtermination    "\\n"
    Log    ${wterminator}
    Should Contain    ${wterminator}    ${success}

Set timeout
    [Documentation]    Set VISA timeout (ms). This is the time that PC will wait for a response from instrument for any queries/read
    ${success} =    Set Variable    Timeout
    #timeout(input_to)
    #Syntax: ${variable}    inst_func    'instrument_name'    timeout    'input_to'
    ${timeout}    inst_func    hp    timeout    5000
    Log    ${timeout}
    Should Contain    ${timeout}    ${success}

Check Interface Properties
    [Documentation]    Check interface properties such as baudrate, parity, stopbits, r/w terminators (Verification function, not necessary for initialisation)
    ${success} =    Set Variable    ASRL/dev/ttyUSB0::INSTR
    #info(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    info
    ${info}    inst_func    hp    info
    Log    ${info}
    Should Contain    ${info}    ${success}

Send Clear
    [Documentation]    Clear the Status Byte summary register and all event registers of instrument. (To ensure starting off from default settings)
    ${success} =    Set Variable    Cleared
    #clear(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    clear
    ${clear}    inst_func    hp    clear
    Log    ${clear}
    Should Contain    ${clear}    ${success}

Get Instrument ID
    [Documentation]    Function to get the ID of the instrument
    ${success} =    Set Variable    HEWLETT-PACKARD,34401A,0,7-5-2
    #getid(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    getid
    ${getid}    inst_func    hp    getid
    Log    ${getid}
    Should Contain    ${getid}    ${success}

Reset
    [Documentation]    Reset the oscilloscope (To ensure starting off from default settings)
    ${success} =    Set Variable    Reset
    #reset(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    reset
    ${reset}    inst_func    hp    reset
    Log    ${reset}
    Should Contain    ${reset}    ${success}
    Sleep    5 seconds

Activate Remote Measurement
    [Documentation]    Enable measurement to be taken through RS-232
    #remote(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    REMote
    ${remote}    inst_func    hp    remote
    Log    ${remote}
    ###========================================End of Initialisation=======================================================

Measure Voltage (DC)
    [Documentation]    Take a Voltage (DC) Measurement. Range and Resolution can be left empty for automatic ranging
    ${success} =    Set Variable    DC
    ###========================================Start of measurement========================================================
    #measure_VDC(ran=None,res=None)
    #Syntax: ${variable}    inst_func    'instrument_name'    meeasure_VDC    'ran'    'res'
    ${measurevdc}    inst_func    hp    measure_VDC
    Log    ${measurevdc}
    Should Contain    ${measurevdc}    ${success}

Measure Voltage (AC)
    [Documentation]    Take a Voltage (AC) Measurement. Range and Resolution can be left empty for automatic ranging
    ${success} =    Set Variable    AC
    #measure_VAC(ran=None,res=None)
    #Syntax: ${variable}    inst_func    'instrument_name'    meeasure_VAC    'ran'    'res'
    ${measurevac}    inst_func    hp    measure_VAC
    Log    ${measurevac}
    Should Contain    ${measurevac}    ${success}

Measure Current (DC)
    [Documentation]    Take a Current (DC) Measurement. Range and Resolution can be left empty for automatic ranging
    ${success} =    Set Variable    DC
    #measure_IDC(ran=None,res=None)
    #Syntax: ${variable}    inst_func    'instrument_name'    meeasure_IDC    'ran'    'res'
    ${measureidc}    inst_func    hp    measure_IDC
    Log    ${measureidc}
    Should Contain    ${measureidc}    ${success}

Measure Current (AC)
    [Documentation]    Take a Current (AC) Measurement. Range and Resolution can be left empty for automatic ranging
    ${success} =    Set Variable    AC
    #measure_IAC(ran=None,res=None)
    #Syntax: ${variable}    inst_func    'instrument_name'    meeasure_IAC    'ran'    'res'
    ${measureiac}    inst_func    hp    measure_IAC
    Log    ${measureiac}
    Should Contain    ${measureiac}    ${success}

Measure Resistance (2-wire)
    [Documentation]    Take a 2-wire Resistance Measurement. Range and Resolution can be left empty for automatic ranging
    ${success} =    Set Variable    Resistance
    #measure_2RES(ran=None,res=None)
    #Syntax: ${variable}    inst_func    'instrument_name'    meeasure_2RES    'ran'    'res'
    ${measure2res}    inst_func    hp    measure_2RES
    Log    ${measure2res}
    Should Contain    ${measure2res}    ${success}

Measure Period
    [Documentation]    Take a Continuity Measurement. Range and Resolution can be left empty for automatic ranging
    ${success} =    Set Variable    Period
    #measure_PERIOD(ran=None,res=None)
    #Syntax: ${variable}    inst_func    'instrument_name'    meeasure_PERIOD    'ran'    'res'
    ${measureperiod}    inst_func    hp    measure_PERIOD
    Log    ${measureperiod}
    Should Contain    ${measureperiod}    ${success}

Measure Frequency
    [Documentation]    Take a Frequency Measurement for inputs between 3 Hz - 300kHz (HP34401A). Range and Resolution can be left empty for automatic ranging
    ${success} =    Set Variable    Frequency
    #measure_FREQ(ran=None,res=None)
    #Syntax: ${variable}    inst_func    'instrument_name'    meeasure_FREQ    'ran'    'res'
    ${measurefreq}    inst_func    hp    measure_FREQ
    Log    ${measurefreq}
    Should Contain    ${measurefreq}    ${success}

Measure Continuity
    [Documentation]    Take a 2-wire Resistance Measurement
    ${success} =    Set Variable    Continuity
    #measure_CONT(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    meeasure_CONT
    ${measurecont}    inst_func    hp    measure_CONT
    Log    ${measurecont}
    Should Contain    ${measurecont}    ${success}
    ###========================================End of measurement========================================================

Check Error Buffer
    [Documentation]    Check error buffer for any queued error that might have been stored
    ${success} =    Set Variable    No error
    #error(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    error
    ${error}    inst_func    hp    error
    Log    ${error}
    Should Contain    ${error}    ${success}

Deinitialise an instrument
    [Documentation]    Deinitialise instrument by closing the port and deleting the instrument
    ###========================================Start of Teardown=====================================================
    #deinit(void)
    #Syntax: ${variable}    inst_func    'instrument_name'    deinit
    ${instdeinit}    inst_func    hp    deinit
    Log    ${instdeinit}
    #Starting from this point, instrument is no longer controlled and inst_func is no longer called
    #inst_deinit(inst_name)
    #Syntax: ${variable}    inst_deinit    'instrument_name'
    ${instdeinit}    inst_deinit    hp
    Log    ${instdeinit}

Deinitialise VISA Resource Manager
    [Documentation]    Denitialise back-end pyvisa-py resource manager
    #VISA_deinit(void)
    #Syntax: ${variable}    VISA_deinit
    ${visadeinit}    VISA_deinit
    Log    ${visadeinit}
    ###========================================End of Teardown=====================================================
