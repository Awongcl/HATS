*** Settings ***
Library           ../HATS/HATS_RPC_Functions.py

*** Variables ***

*** Test Cases ***
Set Serial Port
    [Documentation]    Select Serial port for communication with DUT
    ###====================================== Start of Initialisation ==================================================================
    #RPC_setport(serial_port)
    #Syntax: ${variable}    RPC_setport    'serial_port'
    ${setport}    RPC_setport    /dev/ttyUSB0
    Log    ${setport}

Initialise Serial Communication
    [Documentation]    Initialise Serial port to start communication
    #RPC_init(void)
    #Syntax: ${variable}    RPC_init
    ${init}    RPC_init
    ###====================================== End of Initialisation ====================================================================

I2C Pin Setup
    [Documentation]    I2C21 Interface connectedd to on-board temp, accel sensors
    ###====================================== Start of I2C ==============================================================================
    ##    This function and subsequent functions that are sent to the microcontroller need to be used with wrapper function RPC_0arg/RPC_1arg/RPC_2arg/RPC_3arg/RPC_4arg based on the arguments
    ##    in this format: RPC_'X'arg('func_name',run,func_arg1,func_arg2,...) with number of func_arg corresponding to X in RPC_'X'arg wrapper to use.
    ${success}    Set Variable    setup done
    #I2C_setup(I2C_SDA,I2C_SCL)
    #Syntax: ${variable}    RPC_2arg    I2C_setup    run    'I2C_SDA'    'I2C_SCL'
    ${i2csetup}    RPC_2arg    I2C_setup    run    PB_9    PB_8
    Log    ${i2csetup}
    Should Contain    ${i2csetup}    ${success}

I2C Frequency
    [Documentation]    Function to set I2C Frequency. Default mbedRPC frequency is at 100000Hz
    ...
    ...    Returns the new frequency of I2C line
    #I2C_freq(hertz)
    #Syntax: ${variable}    RPC_1arg    I2C_freq    run
    ${i2cfreq}    RPC_1arg    I2C_freq    run    100000
    Log    ${i2cfreq}

I2C Scan
    [Documentation]    Function to scan for connected I2C peripherals. In-built sensors on sensorpod: Accel sensor addr: 30, Temp sensor addr: 75
    #I2C_scan(void)
    #Syntax: ${variable}    RPC_0arg    I2C_scan    run
    ${i2cscan}    RPC_0arg    I2C_scan    run
    Log    ${i2cscan}
    Should Contain    ${i2cscan}    75    30

I2puttC TMP75
    [Documentation]    Initialise and take a reading from TMP75. TMP75 config reg 0x01 set-up and read of temp sensor 0x00
    ${success} =    Set Variable    Success
    #I2C_write1(slave addr,reg addr,data byte1)
    #Syntax: ${variable}    RPC_3arg    I2C_write1    run    'slave_addr'    'reg_addr'    'data_byte1'
    ${i2cwritepass1}    RPC_3arg    I2C_write1    run    75    1    24
    Log    ${i2cwritepass1}
    Should Contain    ${i2cwritepass1}    ${success}
    #I2C_read(slave addr,reg addr,no. of byte to read)
    #Syntax: ${variable}    RPC_3arg    I2C_read    run    'slave_addr'    'reg_addr'    'no. of byte to read'
    ${i2cread1}    RPC_3arg    I2C_read    run    75    0    2
    Log    ${i2cread1}

I2C LIS3DSH
    [Documentation]    LIS3DSH set-up and reading of x-axis
    ${success} =    Set Variable    Success
    #I2C_write1(slave addr,reg addr,data byte1)
    #Syntax: ${variable}    RPC_3arg    I2C_write1    run    'slave_addr'    'reg_addr'    'data_byte1'
    ${i2cwritepass1}    RPC_3arg    I2C_write1    run    30    32    95
    Log    ${i2cwritepass1}
    Should Contain    ${i2cwritepass1}    ${success}
    ${i2cwritepass1}    RPC_3arg    I2C_write1    run    30    36    128
    Log    ${i2cwritepass1}
    Should Contain    ${i2cwritepass1}    ${success}
    ${i2cwritepass1}    RPC_3arg    I2C_write1    run    30    46    0
    Log    ${i2cwritepass1}
    Should Contain    ${i2cwritepass1}    ${success}
    ${i2cwritepass1}    RPC_3arg    I2C_write1    run    30    37    16
    Log    ${i2cwritepass1}
    Should Contain    ${i2cwritepass1}    ${success}
    ${i2cwritepass1}    RPC_3arg    I2C_write1    run    30    32    0
    Log    ${i2cwritepass1}
    Should Contain    ${i2cwritepass1}    ${success}
    ${i2cwritepass1}    RPC_3arg    I2C_write1    run    30    32    55
    Log    ${i2cwritepass1}
    Should Contain    ${i2cwritepass1}    ${success}
    #I2C_read(slave addr,reg addr,no. of byte to read)
    #Syntax: ${variable}    RPC_3arg    I2C_read    run    'slave_addr'    'reg_addr'    'no. of byte to read'
    ${i2cread1}    RPC_3arg    I2C_read    run    30    40    2
    Log    ${i2cread1}
    ###====================================== End of I2C ====================================================================

SPI1 Pin Setup
    [Documentation]    Test Case calls RPC function to set SPI MOSI, MISO, SCK pins for SPI1 interface
    ###====================================== Start of SPI ===================================================================
    ${success}    Set Variable    setup done
    #SPI_pinsetup(SPI_MOSI,SPI_MISO,SPI_SCK)
    #Syntax: ${variable}    RPC_3arg    SPI_pinsetup    run    'SPI_MOSI'    'SPI_MISO'    'SPI_SCK'
    ${spipinsetup}    RPC_3arg    SPI_pinsetup    run    PB_5    PA_6    PA_5
    Log    ${spipinsetup}
    Should Contain    ${spipinsetup}    ${success}

SPI2 Pin Setup
    [Documentation]    Test Case calls RPC function to set SPI MOSI, MISO, SCK pins for SPI2 interface
    ${success}    Set Variable    setup done
    #SPI_pinsetup(SPI_MOSI,SPI_MISO,SPI_SCK)
    #Syntax: ${variable}    RPC_3arg    SPI_pinsetup    run    'SPI_MOSI'    'SPI_MISO'    'SPI_SCK'
    ${spipinsetup}    RPC_3arg    SPI_pinsetup    run    PC_3    PC_2    PB_10
    Log    ${spipinsetup}
    Should Contain    ${spipinsetup}    ${success}

SPI4 Pin Setup
    [Documentation]    Test Case calls RPC function to set SPI MOSI, MISO, SCK pins for SPI4 interface
    ${success}    Set Variable    setup done
    #SPI_pinsetup(SPI_MOSI,SPI_MISO,SPI_SCK)
    #Syntax: ${variable}    RPC_3arg    SPI_pinsetup    run    'SPI_MOSI'    'SPI_MISO'    'SPI_SCK'
    ${spipinsetup}    RPC_3arg    SPI_pinsetup    run    PE_6    PE_5    PE_12
    Log    ${spipinsetup}
    Should Contain    ${spipinsetup}    ${success}

SPI CS Pin Setup
    [Documentation]    CS0 is SPI1_CS, CS1 is SPI2_CS, CS2 is SPI4_CS
    ${success}    Set Variable    setup done
    #SPI_cssetup(CS0,CS1,CS2)
    #Syntax: ${variable}    RPC_3arg    SPI_cssetup    run    'CS0'    'CS1'    'CS2'
    ${spicssetup}    RPC_3arg    SPI_cssetup    run    PA_4    PB_12    PE_4
    Log    ${spicssetup}
    Should Contain    ${spicssetup}    ${success}

SPI Format
    [Documentation]    Test Case calls RPC function to set SPI bits per frame and mode
    ...
    ...    By default, without calling this function, SPI bits per frame = 8, Mode = 0
    ${Invalid}    Set Variable    Invalid
    # SPI_format(bits per frame,mode)
    # Default bits per frame = 8 , mode = 0
    # Mode 0 = POL(0), PHA(0)
    # Mode 1 = POL(0), PHA(1)
    # Mode 2 = POL(1), PHA(0)
    # Mode 3 = POL(1), PHA(1)
    #Syntax: ${variable}    RPC_2arg    SPI_format    run    'bits per frame'    'mode'
    ${spiformat}    RPC_2arg    SPI_format    run    8    0
    Should Not Contain    ${spiformat}    ${Invalid}
    Log    ${spiformat}

SPI Frequency
    [Documentation]    Set SPI frequency to 100KHz
    #SPI_freq(hertz)
    #Default Frequency = 1MHz
    #Syntax: ${variable}    RPC_1arg    SPI_freq    run    'hertz'
    ${spifreq}    RPC_1arg    SPI_freq    run    100000
    Log    ${spifreq}

SPI Read Bit Value
    [Documentation]    Test Case calls RPC function to set SPI read value
    ...
    ...    By default, without calling this function, SPI read = 1
    ${Invalid}    Set Variable    Invalid
    #SPI_rvalue(read value)
    #Default Read Value = 1
    #Syntax: ${variable}    RPC_1arg    SPI_rvalue    run    'read_value'
    ${spirvalue}    RPC_1arg    SPI_rvalue    run    1
    Should Not Contain    ${spirvalue}    ${Invalid}
    Log    ${spirvalue}

SPI Write Bit Value
    [Documentation]    Test Case calls RPC function to set SPI write value
    ...
    ...    By default, without calling this function, SPI write = 0
    ${Invalid}    Set Variable    Invalid
    #SPI_wvalue(write value)
    #Default Write Value = 1
    #Syntax: ${variable}    RPC_1arg    SPI_wvalue    run    'write_value'
    ${spiwvalue}    RPC_1arg    SPI_wvalue    run    0
    Should Not Contain    ${spiwvalue}    ${Invalid}
    Log    ${spiwvalue}

SPI Device Select
    [Documentation]    SPI Device: 0 - PA_4, 1 - PB_12, 2 - PE_4
    ${Invalid}    Set Variable    Invalid
    #SPI_devselect(pin select)
    #Syntax: ${variable}    RPC_1arg    SPI_devselect    run    'pin_select'
    ${spidevsel}    RPC_1arg    SPI_devselect    run    0
    Should Not Contain    ${spidevsel}    ${Invalid}
    Log    ${spidevsel}

SPI MPL115A1
    [Documentation]    For DEMO/Test. Set-up and read from MPL115A1 Sensor (External module)
    #SPI_write(reg_addr,byte)
    #Syntax: ${variable}    RPC_2arg    SPI_write    run    'reg_addr'    'byte'
    ${spiwrite}    RPC_2arg    SPI_write    run    36    0
    Log    ${spiwrite}
    Sleep    0.5
    #SPI_read(reg_addr)
    #Syntax: ${variable}    RPC_1arg    SPI_read    run    'reg_addr'
    ${spiread}    RPC_1arg    SPI_read    run    0
    Log    ${spiread}
    #SPI_read(reg_addr)
    #Syntax: ${variable}    RPC_1arg    SPI_read    run    'reg_addr'
    ${spiread}    RPC_1arg    SPI_read    run    2
    Log    ${spiread}
    #SPI_read(reg_addr)
    #Syntax: ${variable}    RPC_1arg    SPI_read    run    'reg_addr'
    ${spiread}    RPC_1arg    SPI_read    run    4
    Log    ${spiread}
    #SPI_read(reg_addr)
    #Syntax: ${variable}    RPC_1arg    SPI_read    run    'reg_addr'
    ${spiread}    RPC_1arg    SPI_read    run    6
    Log    ${spiread}

SPI LIS3DSH Set-up
    [Documentation]    For DEMO/Test. Set-up and LIS3DSH(External Module)
    #SPI_write(reg_addr,byte)
    #Syntax: ${variable}    RPC_2arg    SPI_write    run    'reg_addr'    'byte'
    ${spiwrite}    RPC_2arg    SPI_write    run    32    95
    Log    ${spiwrite}
    #SPI_write(reg_addr,byte)
    #Syntax: ${variable}    RPC_2arg    SPI_write    run    'reg_addr'    'byte'
    ${spiwrite}    RPC_2arg    SPI_write    run    36    128
    Log    ${spiwrite}
    #SPI_write(reg_addr,byte)
    #Syntax: ${variable}    RPC_2arg    SPI_write    run    'reg_addr'    'byte'
    ${spiwrite}    RPC_2arg    SPI_write    run    46    0
    Log    ${spiwrite}
    #SPI_write(reg_addr,byte)
    #Syntax: ${variable}    RPC_2arg    SPI_write    run    'reg_addr'    'byte'
    ${spiwrite}    RPC_2arg    SPI_write    run    37    16
    Log    ${spiwrite}
    #SPI_write(reg_addr,byte)
    #Syntax: ${variable}    RPC_2arg    SPI_write    run    'reg_addr'    'byte'
    ${spiwrite}    RPC_2arg    SPI_write    run    32    0
    Log    ${spiwrite}
    #SPI_write(reg_addr,byte)
    #Syntax: ${variable}    RPC_2arg    SPI_write    run    'reg_addr'    'byte'
    ${spiwrite}    RPC_2arg    SPI_write    run    32    55
    Log    ${spiwrite}

SPI LIS3DSH Read
    [Documentation]    For DEMO/Test. Read x-axis from LIS3DSH(External Module)
    #SPI_read(reg_addr)
    #Syntax: ${variable}    RPC_1arg    SPI_read    run    'reg_addr'
    ${spiread}    RPC_1arg    SPI_read    run    40
    Log    ${spiread}
    ###====================================== End of SPI ===================================================================

UART Pin Setup
    [Documentation]    Test Case calls RPC function to set UART TX & RX pins for UART Interface
    ...
    ...    This function needs to be called before other UART functions
    ...
    ...    Returns "UART pin setup done!" if pins declared successfully, mbed OS crash if failed/pins not declared in mbed OS
    ###====================================== Start of UART ===============================================================================
    ${success}    Set Variable    setup done
    #UART_setup(UART_TX,UART_RX)
    #Syntax: ${variable}    RPC_2arg    UART_setup    run    'UART_TX'    'UART_RX'
    ${uartpin}    RPC_2arg    UART_setup    run    PD_5    PD_6
    Log    ${uartpin}
    Should Contain    ${uartpin}    ${success}

UART2 Pin Setup
    [Documentation]    Test Case calls RPC function to set UART TX & RX pins for UART2 Interface
    #UART_setup(UART_TX,UART_RX)
    #Syntax: ${variable}    RPC_2arg    UART_setup    run    'UART_TX'    'UART_RX'
    ${success}    Set Variable    setup done
    ${uartpin}    RPC_2arg    UART_setup    run    PD_9    PD_8
    Log    ${uartpin}
    Should Contain    ${uartpin}    ${success}

UART Baud
    [Documentation]    Test Case calls RPC function to set UART baud rate
    ...
    ...    Baudrate:" user input" is always returned by function
    #UART_baud(baudrate)
    #Syntax: ${variable}    RPC_1arg    UART_baud    run    'baudrate'
    ${uartbaud}    RPC_1arg    UART_baud    run    9600
    Log    ${uartbaud}

UART Format
    [Documentation]    Test Case calls RPC function to set UART format for bits, parity and stopbits
    ...
    ...    bits: The number of bits in a word (5-8; default = 8)
    ...    parity: The parity used (SerialBase::None, SerialBase::Odd, SerialBase::Even, SerialBase::Forced1, SerialBase::Forced0; default = SerialBase::None
    ...    stop_bits: The number of stop bits (1 or 2; default = 1)
    ...
    ...    Returns, new format if successful, "Invalid" if failed returned
    ${failed}    Set Variable    Invalid
    #UART_format(bit,parity,stopbits)
    #Syntax: ${variable}    RPC_3arg    UART_format    run    'bit'    'parity'    'stopbits'
    ${uartformat}    RPC_3arg    UART_format    run    8    None    1
    Should Not Contain    ${uartformat}    ${failed}

UART Write
    [Documentation]    Test Case calls RPC function to write to UART Interface
    ...
    ...    Returns, "Written" if successful, "No Space to write" if UART interface is occupied
    ${success}    Set Variable    Written
    #UART_write(data)
    #Syntax: ${variable}    RPC_1arg    UART_write    run    'data'
    ${uartwrite}    RPC_1arg    UART_write    run    "Hello"
    Log    ${uartwrite}
    Should Contain    ${uartwrite}    ${success}

UART Read
    [Documentation]    Test Case calls RPC function to read lines from UART Interface
    ...
    ...    Returns, data if successful, "No data to read" if UART interface has nothing to read
    ${failed}    Set Variable    Invalid
    #UART_read(lines to read)
    #Note: This is a polling function
    #Syntax: ${variable}    RPC_1arg    UART_read    run    'lines to read'
    ${uartread}    RPC_1arg    UART_read    run    1
    Log    ${uartread}
    Should Not Contain    ${uartread}    ${failed}

UART Write Read
    [Documentation]    Test Case calls RPC function to write followed by read from UART Interface
    ...
    ...    For write portion, returns, "Written" if write is successful, "No Space to write" if UART interface is occupied
    ...
    ...    For read portion, returns, data if successful, "No data to read" if UART interface has nothing to read
    ${success}    Set Variable    Written
    #UART_writeread(data to write, lines to read)
    #Note: This is a polling function
    #Syntax: ${variable}    RPC_2arg    UART_writeread    run    'data to write'    'lines to read'
    ${uartwriteread}    RPC_2arg    UART_writeread    run    "Hello"    1
    Log    ${uartwriteread}
    Should Contain    ${uartwriteread}    ${success}

UART Newline
    [Documentation]    Test Case calls RPC function to write "\ n" to UART Interface
    ...
    ...    Returns, "Newline" if successful, "No space to write" if UART interface is occupied
    ${success}    Set Variable    Newline
    #UART_newline(void)
    #Syntax: ${variable}    RPC_0arg    UART_newline    run
    ${uartnewline}    RPC_0arg    UART_newline    run
    Log    ${uartnewline}
    Should Contain    ${uartnewline}    ${success}
    ###====================================== End of UART ===================================================================

Ethernet Set Static Variables
    [Documentation]    Test Case calls RPC function to set Ethernet static variables (IP,GATEWAY,MASK) to be used for Non-DHCP Ethernet interface
    ...
    ...    Returns the newly set values
    ###====================================== Start of Ethernet ===================================================================
    #Eth_staticvar(IP,GATEWAY,MASK)
    #Syntax: ${variable}    RPC_3arg    Eth_staticvar    run    'IP'    'GATEWAY'    'MASK'
    ${ethstaticvar}    RPC_3arg    Eth_staticvar    run    192.168.1.66    192.168.1.1    255.255.255.0
    Log    ${ethstaticvar}

Ethernet Read Static Variables
    [Documentation]    Test Case calls RPC function to read previously set Ethernet static variables (IP,GATEWAY,MASK)
    ...
    ...    Returns the corresponding values
    #Eth_readvar(void)
    #Syntax: ${variable}    RPC_0arg    Eth_readvar    run
    ${ethreadstatic}    RPC_0arg    Eth_readvar    run
    Log    ${ethreadstatic}

Ethernet Static
    [Documentation]    Test Case calls RPC function to send packet to Ethernet interface
    ...
    ...    Static variables must have been set to use this function
    ...
    ...    Returns data and number of bytes received (maxed at 256 bytes) from ethernet interface
    ${success}    Set Variable    received
    #Eth_static(Destination IP, Destination port, Data to send)
    #Syntax: ${variable}    RPC_3arg    Eth_static    run    'Destination IP'    'Destination port'    'Data to send'
    ${ethstatic}    RPC_3arg    Eth_static    run    www.mbed.com    80    ping
    Log    ${ethstatic}
    Sleep    5 seconds
    ${readline}    RPC_readlines
    Log    ${readline}
    Should Contain    ${ethstatic}|${readline}    ${success}

Ethernet DHCP
    [Documentation]    Test Case calls RPC function to send packet to Ethernet interface using DHCP
    ...
    ...    Returns data and number of bytes received (maxed at 256 bytes) from ethernet interface
    ${success}    Set Variable    received
    #Eth_DHCP(Destination IP, Destination port, Data to send)
    #Syntax: ${variable}    RPC_3arg    Eth_DHCP    run    'Destination IP'    'Destination port'    'Data to send'
    ${ethdhcp}    RPC_3arg    Eth_DHCP    run    www.mbed.com    80    ping
    Log    ${ethdhcp}
    Sleep    5 seconds
    ${readline}    RPC_readlines
    Log    ${readline}
    Should Contain    ${ethdhcp}|${readline}    ${success}
    ###====================================== Start of Ethernet ===================================================================

USBMSD Device info
    [Documentation]    Test Case calls RPC function to check the flash drive properties
    ...
    ...    Returns flash drive capacity and block sizes
    ###====================================== Start of USBMSD ===================================================================
    #USBMSD_info(void)
    #Syntax: ${variable}    RPC_0arg    USBMSD_info    run
    ${usbmsdinfo}    RPC_0arg    USBMSD_info    run
    Log    ${usbmsdinfo}

USBMSD File Size
    [Documentation]    Test Case calls RPC function to check the file size of a selected file in flash drive
    ...
    ...    Returns file size in bytes
    ${success}    Set Variable    bytes
    #USBMSD_filesize(file name)
    #Syntax: ${variable}    RPC_1arg    USBMSD_filesize    run    'file name'
    ${usbmsdfilesize}    RPC_1arg    USBMSD_filesize    run    test.txt
    Log    ${usbmsdfilesize}
    Sleep    5 seconds
    ${readline}    RPC_readlines
    Log    ${readline}
    Should Contain    ${usbmsdfilesize}|${readline}    ${success}

USBMSD Read
    [Documentation]    Test Case calls RPC function to read from a selected file in flash drive
    ...
    ...    Returns file size and data
    ${success}    Set Variable    Size
    #USBMSD_read(file name)
    #Syntax: ${variable}    RPC_1arg    USBMSD_read    run    'file name'
    ${usbmsdread}    RPC_1arg    USBMSD_read    run    test.txt
    Log    ${usbmsdread}
    Sleep    5 seconds
    ${readline}    RPC_readlines
    Log    ${readline}
    Should Contain    ${usbmsdread}|${readline}    ${success}

USBMSD Write
    [Documentation]    Test Case calls RPC function to create and write a file in flash drive
    ...
    ...    Returns "Written" when successful
    ${success}    Set Variable    Written
    #USBMSD_write(file name, data to write)
    #Syntax: ${variable}    RPC_2arg    USBMSD_write    run    'file name'    'data to write'
    ${usbmsdwrite}    RPC_2arg    USBMSD_write    run    testwrite.txt    writingfromrobotframework
    Log    ${usbmsdwrite}
    Should Contain    ${usbmsdwrite}    ${success}

USBMSD Append
    [Documentation]    Test Case calls RPC function to open and append a file in flashdrive/create and write if file does not exist
    ...
    ...    Returns "Written" when successful
    ${success}    Set Variable    Written
    #USBMSD_append(file name, data to write)
    #Syntax: ${variable}    RPC_2arg    USBMSD_append    run    'file name'    'data to write'
    ${usbmsdappend}    RPC_2arg    USBMSD_append    run    testappend.txt    appendingfromrobotframework
    Log    ${usbmsdappend}
    Should Contain    ${usbmsdappend}    ${success}

USBMSD Read 2
    [Documentation]    Test Case calls RPC function to read from a selected file in flash drive
    ...
    ...    Returns file size and data
    ${success}    Set Variable    Size
    #USBMSD_read(file name)
    #Syntax: ${variable}    RPC_1arg    USBMSD_read    run    'file name'
    ${usbmsdread}    RPC_1arg    USBMSD_read    run    testwrite.txt
    Log    ${usbmsdread}
    Sleep    5 seconds
    ${readline}    RPC_readlines
    Log    ${readline}
    Should Contain    ${usbmsdread}|${readline}    ${success}
    ###====================================== End of USBMSD ===================================================================

SDCard Pin Set-up
    [Documentation]    Test Case calls RPC function to set-up pins for SPI SDCard communication. (MOSI,MISO,SCK,CS)
    ###====================================== Start of SDCard ===================================================================
    #SDCard_setup(MOSI,MISO,SCK,CS)
    #Syntax: ${variable}    RPC_4arg    SDCard_setup    run    'MOSI'    'MISO'    'SCK'    'CS'
    ${sdcardsetup}    RPC_4arg    SDCard_setup    run    PC_12    PC_11    PC_10    PC_9
    Log    ${sdcardsetup}

SDCard Frequency
    [Documentation]    Test Case calls RPC function to set frequency for SPI SDCard communication. Max Frequency at 25Mhz
    ...
    ...    Returns the set frequency
    ${success}    Set Variable    Frequency
    #SDCard_freq(hz)
    #Syntax: ${variable}    RPC_1arg    SDCard_freq    run    'hz'
    ${sdcardfreq}    RPC_1arg    SDCard_freq    run    100000
    Log    ${sdcardfreq}
    Should Contain    ${sdcardfreq}    ${success}

SDCard Info
    [Documentation]    Test Case calls RPC function to check the SDCard properties
    ...
    ...    Returns SDCard properties block sizes
    #SDCard_info(void)
    #Syntax: ${variable}    RPC_0arg    SDCard_info    run
    ${usbmsdinfo}    RPC_0arg    SDCard_info    run
    Log    ${usbmsdinfo}

SDCard File Size
    [Documentation]    Test Case calls RPC function to check the file size of a selected file in SDCard
    ...
    ...    Returns file size in bytes
    ${success}    Set Variable    bytes
    #SDCard_filesize(file name)
    #Syntax: ${variable}    RPC_1arg    SDCard_filesize    run    'file name'
    ${sdcardfilesize}    RPC_1arg    SDCard_filesize    run    test.txt
    Log    ${sdcardfilesize}
    Sleep    5 seconds
    ${readline}    RPC_readlines
    Log    ${readline}
    Should Contain    ${sdcardfilesize}|${readline}    ${success}

SDCard Read
    [Documentation]    Test Case calls RPC function to read from a selected file in SDCard
    ...
    ...    Returns file size and data
    ${success}    Set Variable    Size
    #SDCard_read(file name)
    #Syntax: ${variable}    RPC_1arg    SDCard_read    run    'file name'
    ${sdcardread}    RPC_1arg    SDCard_read    run    test.txt
    Log    ${sdcardread}
    Sleep    5 seconds
    ${readline}    RPC_readlines
    Log    ${readline}
    Should Contain    ${sdcardread}|${readline}    ${success}

SDCard Write
    [Documentation]    Test Case calls RPC function to create and write a file in SDCard
    ...
    ...    Returns "Written" when successful
    ${success}    Set Variable    Written
    #SDCard_write(file name, data to write)
    #Syntax: ${variable}    RPC_2arg    SDCard_write    run    'file name'    'data to write'
    ${sdcardwrite}    RPC_2arg    SDCard_write    run    testwrite.txt    writingfromrobotframework
    Log    ${sdcardwrite}
    Should Contain    ${sdcardwrite}    ${success}

SDCard Append
    [Documentation]    Test Case calls RPC function to open and append a file in SDCard/create and write if file does not exist
    ...
    ...    Returns "Written" when successful
    ${success}    Set Variable    Written
    #SDCard_append(file name, data to write)
    #Syntax: ${variable}    RPC_2arg    SDCard_append    run    'file name'    'data to write'
    ${sdcardappend}    RPC_2arg    SDCard_append    run    testappend.txt    appendingfromrobotframework
    Log    ${sdcardappend}
    Should Contain    ${sdcardappend}    ${success}
    ###====================================== End of SDCard ===================================================================

LED1 Set-up
    [Documentation]    DigitalOut. Initialising PE_9 (LED1) pin
    ###====================================== Start of DigitalOut (Board LED) ===================================================================
    ##For DigitalOut, other than 'run' we will be using other keywords such as 'new','read','write','delete'. As it is an in-built library, its behaviour is slightly different from the rest.
    ${pincheck}    Set Variable    PE_9
    #DigitalOut(pin_name, obj_name)
    #Syntax: ${variable}    RPC_2arg    DigitalOut    new    'pin_name'    'obj_name'
    ${createpin}    RPC_2arg    DigitalOut    new    PE_9    PE_9
    Should Contain    ${createpin}    ${pincheck}
    Log    ${createpin}

LED1 On/Off
    [Documentation]    Turning PE_9 (LED1) ON.
    ${High}    Set Variable    1
    ${Low}    Set Variable    0
    #PE_9(value 'if any')
    #Syntax: ${variable}    RPC_0arg    'obj_name'    read
    ${pinread1}    RPC_0arg    PE_9    read
    Should Contain    ${pinread1}    ${High}
    Log    ${pinread1}
    #PE_9(value 'if any')
    #Syntax: ${variable}    RPC_1arg    'obj_name'    write    'value'
    ${pinwrite}    RPC_1arg    PE_9    write    0
    Log    ${pinwrite}
    #PE_9(value 'if any')
    #Syntax: ${variable}    RPC_0arg    'obj_name'    read
    ${pinread2}    RPC_0arg    PE_9    read
    Should Contain    ${pinread2}    ${Low}
    Log    ${pinread2}

LED2 Set-up
    [Documentation]    DigitalOut. Initialising PE_10 (LED2) pin
    ${pincheck}    Set Variable    PE_10
    #DigitalOut(pin_name, obj_name)
    #Syntax: ${variable}    RPC_2arg    DigitalOut    new    'pin_name'    'obj_name'
    ${createpin}    RPC_2arg    DigitalOut    new    PE_10    PE_10
    Should Contain    ${createpin}    ${pincheck}
    Log    ${createpin}

LED2 On/Off
    [Documentation]    Turning PE_10 (LED2) ON.
    ${High}    Set Variable    1
    ${Low}    Set Variable    0
    #PE_10(value 'if any')
    #Syntax: ${variable}    RPC_0arg    'obj_name'    read
    ${pinread1}    RPC_0arg    PE_10    read
    Should Contain    ${pinread1}    ${High}
    Log    ${pinread1}
    #PE_10(value 'if any')
    #Syntax: ${variable}    RPC_1arg    'obj_name'    write    'value'
    ${pinwrite}    RPC_1arg    PE_10    write    0
    Log    ${pinwrite}
    #PE_10(value 'if any')
    #Syntax: ${variable}    RPC_0arg    'obj_name'    read
    ${pinread2}    RPC_0arg    PE_10    read
    Should Contain    ${pinread2}    ${Low}
    Log    ${pinread2}

LED3 Set-up
    [Documentation]    DigitalOut. Initialising PE_11 (LED3) pin
    ${pincheck}    Set Variable    PE_11
    #DigitalOut(pin_name, obj_name)
    #Syntax: ${variable}    RPC_2arg    DigitalOut    new    'pin_name'    'obj_name'
    ${createpin}    RPC_2arg    DigitalOut    new    PE_11    PE_11
    Should Contain    ${createpin}    ${pincheck}
    Log    ${createpin}

LED3 On/Off
    [Documentation]    Turning PE_12 (LED3) ON.
    ${High}    Set Variable    1
    ${Low}    Set Variable    0
    #PE_11(value 'if any')
    #Syntax: ${variable}    RPC_0arg    'obj_name'    read
    ${pinread1}    RPC_0arg    PE_11    read
    Should Contain    ${pinread1}    ${High}
    Log    ${pinread1}
    #PE_11(value 'if any')
    #Syntax: ${variable}    RPC_1arg    'obj_name'    write    'value'
    ${pinwrite}    RPC_1arg    PE_11    write    0
    Log    ${pinwrite}
    #PE_11(value 'if any')
    #Syntax: ${variable}    RPC_0arg    'obj_name'    read
    ${pinread2}    RPC_0arg    PE_11    read
    Should Contain    ${pinread2}    ${Low}
    Log    ${pinread2}
    ###====================================== End of DigitalOut (Board LED) ===================================================================

Close Serial
    [Documentation]    To Close Serial Port connected to DUT
    ###====================================== Start of Teardown ===================================================================
    #RPC_close(void)
    #Syntax: RPC_close
    RPC_close
    ###====================================== End of Teardown ===================================================================
