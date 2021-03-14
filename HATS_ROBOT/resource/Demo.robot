*** Settings ***
Library           ../../HATS/ina260.py

*** Keywords ***
to_get_voltage
    [Documentation]    Get voltage from voltage bus
    #get_voltage()
    ${voltage}    get_voltage
    [Return]    ${voltage}

to_set_all
    [Arguments]    ${average}=1    ${mode}= continous
    [Documentation]    Sets the average and mode together.
    ...    Average options: 1(default),4,16,64,128,256,512,1024
    ...    Mode options: ”triggered”/”continous”(defaullt)
    #set_all(self,avg =1 ,mode = "continous")
    #exampel syntex: set_all    16    triggered
    set_all    ${average}    ${mode}
