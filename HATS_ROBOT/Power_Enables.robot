*** Settings ***
Resource          Resource/GPIO.robot

*** Test Cases ***
enable_dcdc
    to_en_dc_converter    [3.3]    True

enable_dac
    to_en_dac    False

enable_ldo
    to_en_ldo    False
