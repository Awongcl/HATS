*** Settings ***
Resource          Resource/GPIO.robot

*** Test Cases ***
enable_dcdc
    to_en_dc_converter    [5]    True

enable_dac
    to_en_dac    True

enable_ldo
    to_en_ldo    True
