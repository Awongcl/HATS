# -*- coding: utf-8 -*-
import HATS_VISA_base as hv_base


###Sub class for multimeter instrument (HP-34401A)
class multimeter(hv_base.VISAinst):
# ###Instrument Specific methods (multimeter)
#     
# ###General
    #Method to allow measurement taken remotely (RS-232)
    def remote(self):
        """
        Place the multimeter in the remote mode for RS-232 operation.
        All keys on the front panel, except the LOCAL key, are disabled.
        """
        reply = self.open.write('SYSTEM:REMOTE')
        return str(reply)
    
    #Method to stop remote measurement (RS-232)
    def local(self):
        """
        Place the multimeter in the local mode for RS-232 operation. All keys on
        the front panel are fully functional.
        """
        reply = self.open.write('SYSTEM:LOCAL')
        return str(reply)
    
    #Method to check error 
    def error(self):
        """
        Query the multimeter’s error queue.
        """
        self.open.write('SYSTEM:ERROR?')
        reply = self.open.read()
        return str(reply)
    
###Measure
    def measure_VDC(self,ran=None,res=None):
        """
        Preset and make a dc voltage measurement with autoscale or the specified range and resolution. 
        """
        if ran == None:
            self.open.write('MEASURE:VOLTAGE:DC?')
        else:
            if res == None:
                self.open.write('MEASURE:VOLTAGE:DC? ' + str(ran))
            else:
                self.open.write('MEASURE:VOLTAGE:DC? ' + str(ran) + ',' + str(res))
        
        reply = self.open.read()
        return('Voltage(DC): ' + str(reply))
    
    def measure_VDCRATIO(self,ran=None,res=None):
        """
        Preset and make a dc:dc ratio measurement with autoscale or the specified range and resolution. 
        For ratio measurements, the specified range applies to the signal connected to the Input terminals. 
        Autoranging is automatically selected for reference voltage measurements on the Sense terminals.
        """
        if ran == None:
            self.open.write('MEASURE:VOLTAGE:DC:RATIO?')
        else:
            if res == None:
                self.open.write('MEASURE:VOLTAGE:DC:RATIO? ' + str(ran))
            else:
                self.open.write('MEASURE:VOLTAGE:DC:RATIO? ' + str(ran) + ',' + str(res))
        
        reply = self.open.read()
        return('Voltage(DC) Ratio: ' + str(reply))
    
    def measure_VAC(self,ran=None,res=None):
        """
        Preset and make an ac voltage measurement with autoscale or the specified range and resolution. 
        For ac measurements, resolution is actually fixed at 6 1/2 digits. The resolution
        parameter only affects the front-panel display.
        """
        if ran == None:
            self.open.write('MEASURE:VOLTAGE:AC?')
        else:
            if res == None:
                self.open.write('MEASURE:VOLTAGE:AC? '+ str(ran))
            else:
                self.open.write('MEASURE:VOLTAGE:AC? '+ str(ran) + ',' + str(res))
                
        reply = self.open.read()
        return('Voltage(AC): ' + str(reply))
        
    def measure_IDC(self,ran=None,res=None):
        """
        Preset and make a dc current measurement with autoscale or the specified range and resolution.
        """
        if ran == None:
            self.open.write('MEASURE:CURRENT:DC?')
        else:
            if res == None:
                self.open.write('MEASURE:CURRENT:DC? ' + str(ran))
            else:
                self.open.write('MEASURE:CURRENT:DC?' + str(ran) + ',' + str(res))

        reply = self.open.read()
        return('Current(DC): ' + str(reply))    

    def measure_IAC(self,ran=None,res=None):
        """
        Preset and make an ac current measurement with autoscale or the specified range and resolution. 
        For ac measurements, resolution is actually fixed at 6 1/2 digits. The resolution
        parameter only affects the front-panel display.

        """
        if ran == None:
            self.open.write('MEASURE:CURRENT:AC?')
        else:
            if res == None:
                self.open.write('MEASURE:CURRENT:AC? ' + str(ran))
            else:
                self.open.write('MEASURE:CURRENT:AC? ' + str(ran) + ',' + str(res))
        
        reply = self.open.read()
        return('Current(AC): ' + str(reply))    

    def measure_2RES(self,ran=None,res=None):
        """
        Preset and make a 2-wire ohms measurement with autoscale or the specified range and resolution. 
        The reading is sent to the output buffer.
        """
        if ran == None:
            self.open.write('MEASURE:RESISTANCE?')  
        else:
            if res == None:
                self.open.write('MEASURE:RESISTANCE? ' + str(ran))
            else:
                self.open.write('MEASURE:RESISTANCE? ' + str(ran) + ',' + str(res))
                
        reply = self.open.read()
        return('Resistance(2-wire): '+ str(reply))
        
    def measure_4RES(self,ran=None,res=None):
        """
        Preset and make a 4-wire ohms measurement with autoscale or the specified range and resolution. 
        The reading is sent to the output buffer.
        """
        if ran == None:
            self.open.write('MEASURE:FRESISTANCE?')
        else:
            if res == None:
                self.open.write('MEASURE:FRESISTANCE? ' + str(ran))
            else:
                self.open.write('MEASURE:FRESISTANCE? ' + str(ran) + ',' + str(res))
                
        reply = self.open.read()
        return('Resistance(4-wire): '+ str(reply))

    # Returns 0 when no period is detected (HP34401A)
    def measure_PERIOD(self,ran=None,res=None):
        """
        Preset and make a period measurement with autoscale or the specified range and resolution. 
        For period measurements, the multimeter uses one “range” for all inputs between 0.33 seconds 
        and 3.3 msec. With no input signal applied, period measurements return “0”.
        """
        if ran == None:
            self.open.write('MEASURE:PERIOD?')
        else:
            if res == None:
                self.open.write('MEASURE:PERIOD? ' + str(ran))
            else:
                self.open.write('MEASURE:PERIOD? ' + str(ran) + ',' + str(res))
                                
        reply = self.open.read()
        return('Period: ' + str(reply))

    def measure_FREQ(self,ran=None,res=None):
        """
        Preset and make a frequency measurement with autoscale or the specified range andresolution. 
        For frequency measurements, the multimeter uses one “range” for all inputs between 3 Hz and 300 kHz. 
        With no input signal applied, frequency measurements return “0”.
        """
        if ran == None:
            self.open.write('MEASURE:FREQUENCY?')
        else:
            if res == None:
                self.open.write('MEASURE:FREQUENCY? ' + str(ran))
            else:
                self.open.write('MEASURE:FREQUENCY? ' + str(ran) + ',' + str(res))
                                
        reply = self.open.read()
        return('Frequency: ' + str(reply))
    
    def measure_DIODE(self):
        """
        Preset and make a diode measurement. The range and resolution are fixed for diode tests 
        (1 Vdc range with 1 mA current source output and 5 1/2 digits).
        """
        self.open.write('MEASURE:DIODE?')
        reply = self.open.read()
        return('Diode: ' + str(reply))
    
    def measure_CONT(self):
        """
        Preset and make a continuity measurement. 
        The range and resolution are fixed for continuity tests (1 kW range and 5 1/2 digits).
        """
        self.open.write('MEASURE:CONTINUITY?')
        reply = self.open.read()
        return('Continuity: ' + str(reply))
    

    
###Configure
    # Method to check current configuration
    def configure(self):
        """
        Query the multimeter’s present configuration.
        """
        self.open.write('CONFIGURE?')
        reply = self.open.read()
        return('Current Configuration: ' + str(reply))
    
    def configure_VDC(self,ran=None,res=None):
        """
        Preset and configure the multimeter for dc voltage measurements 
        with autoscale or the specified range and resolution.
        """
        if ran == None:
            self.open.write('CONFIGURE:VOLTAGE:DC')
        else:
            if res == None:
                self.open.write('CONFIGURE:VOLTAGE:DC ' + str(ran))
            else:
                self.open.write('CONFIGURE:VOLTAGE:DC ' + str(ran) + ',' + str(res))
        
        self.open.write('CONFIGURE?')
        reply = self.open.read()
        return('Voltage(DC) Configuration: ' + str(reply))
    
    def configure_VDCRATIO(self,ran=None,res=None):
        """
        Preset and configure the multimeter for dc:dc ratio measurements with autoscale or 
        the specified range and resolution. For ratio measurements, the specified range 
        applies to the signal connected to the Input terminals. 
        Autoranging is automatically selected for reference voltage measurements on the Sense terminals.
        """
        if ran == None:
            self.open.write('CONFIGURE:VOLTAGE:DC:RATIO')
        else:
            if res == None:
                self.open.write('CONFIGURE:VOLTAGE:DC:RATIO ' + str(ran))
            else:
                self.open.write('CONFIGURE:VOLTAGE:DC:RATIO ' + str(ran) + ',' + str(res))
        
        self.open.write('CONFIGURE?')
        reply = self.open.read()
        return('Voltage(DC) Ratio Configuration: ' + str(reply))
    
    def configure_VAC(self,ran=None,res=None):
        """
        Preset and configure the multimeter for ac voltage measurements with autoscale or 
        the specified range and resolution. For ac measurements, resolution is actually 
        fixed at 6 1/2 digits. The resolution parameter only affects the front-panel display.
        """
        if ran == None:
            self.open.write('CONFIGURE:VOLTAGE:AC')
        else:
            if res == None:
                self.open.write('CONFIGURE:VOLTAGE:AC '+ str(ran))
            else:
                self.open.write('CONFIGURE:VOLTAGE:AC '+ str(ran) + ',' + str(res))
        
        self.open.write('CONFIGURE?')
        reply = self.open.read()
        return('Voltage(AC) Configuration: ' + str(reply))
        
    def configure_IDC(self,ran=None,res=None):
        """
        Preset and configure the multimeter for dc current measurements with autoscale or 
        the specified range and resolution.
        """
        if ran == None:
            self.open.write('CONFIGURE:CURRENT:DC')
        else:
            if res == None:
                self.open.write('CONFIGURE:CURRENT:DC ' + str(ran))
            else:
                self.open.write('CONFIGURE:CURRENT:DC ' + str(ran) + ',' + str(res))

        self.open.write('CONFIGURE?')
        reply = self.open.read()
        return('Current(DC) Configuration: ' + str(reply))    

    def configure_IAC(self,ran=None,res=None):
        """
        Preset and configure the multimeter for ac current measurements with autoscale or the 
        specified range and resolution. For ac measurements, resolution is actually fixed at 
        6 1/2 digits. The resolution parameter only affects the front-panel display.
        """
        if ran == None:
            self.open.write('CONFIGURE:CURRENT:AC')
        else:
            if res == None:
                self.open.write('CONFIGURE:CURRENT:AC ' + str(ran))
            else:
                self.open.write('CONFIGURE:CURRENT:AC ' + str(ran) + ',' + str(res))
        
        self.open.write('CONFIGURE?')
        reply = self.open.read()
        return('Current(AC) Configuration: ' + str(reply))    

    def configure_2RES(self,ran=None,res=None):
        """
        Preset and configure the multimeter for 2-wire ohms measurements with autoscale or the 
        specified range and resolution.
        """
        if ran == None:
            self.open.write('CONFIGURE:RESISTANCE')  
        else:
            if res == None:
                self.open.write('CONFIGURE:RESISTANCE ' + str(ran))
            else:
                self.open.write('CONFIGURE:RESISTANCE ' + str(ran) + ',' + str(res))
                
        self.open.write('CONFIGURE?')
        reply = self.open.read()
        return('Resistance(2-wire) Configuration: '+ str(reply))
        
    def configure_4RES(self,ran=None,res=None):
        """
        Preset and configure the multimeter for 4-wire ohms measurements with autoscale or the 
        specified range and resolution.
        """
        if ran == None:
            self.open.write('CONFIGURE:FRESISTANCE')
        else:
            if res == None:
                self.open.write('CONFIGURE:FRESISTANCE ' + str(ran))
            else:
                self.open.write('CONFIGURE:FRESISTANCE ' + str(ran) + ',' + str(res))
                
        self.open.write('CONFIGURE?')
        reply = self.open.read()
        return('Resistance(4-wire) Configuration: '+ str(reply))

    def configure_FREQ(self,ran=None,res=None):
        """
        Preset and configure a frequency measurement with autoscale or the specified range and resolution. 
        For frequency measurements, the multimeter uses one “range” for all
        inputs between 3 Hz and 300 kHz. With no input signal applied, frequency measurements return “0”.
        """
        if ran == None:
            self.open.write('CONFIGURE:FREQUENCY')
        else:
            if res == None:
                self.open.write('CONFIGURE:FREQUENCY ' + str(ran))
            else:
                self.open.write('CONFIGURE:FREQUENCY ' + str(ran) + ',' + str(res))
                                
        self.open.write('CONFIGURE?')
        reply = self.open.read()
        return('Frequency Configuration: ' + str(reply))        
    
    def configure_PERIOD(self,ran=None,res=None):
        """
        Preset and configure a period measurement with autoscale or the specified range and resolution. 
        For period measurements, the multimeter uses one “range” for all inputs between 0.33 seconds 
        and 3.3 msec. With no input signal applied, period measurements return “0”.
        """
        if ran == None:
            self.open.write('CONFIGURE:PERIOD')
        else:
            if res == None:
                self.open.write('CONFIGURE:PERIOD ' + str(ran))
            else:
                self.open.write('CONFIGURE:PERIOD ' + str(ran) + ',' + str(res))
                                
        self.open.write('CONFIGURE?')
        reply = self.open.read()
        return('Period Configuration: ' + str(reply))

    def configure_DIODE(self):
        """
        Preset and configure the multimeter for diode measurements.
        """
        self.open.write('CONFIGURE:DIODE')
        self.open.write('CONFIGURE?')
        reply = self.open.read()
        return('Diode Configuration: ' + str(reply))
    
    def configure_CONT(self):
        """
        Preset and configure the multimeter for continuity measurements.
        """
        self.open.write('CONFIGURE:CONTINUITY')
        self.open.write('CONFIGURE?')
        reply = self.open.read()
        return('Continuity Configuration: ' + str(reply))
    
    def configure_NPLCYCLES(self,func, val):
        """
        Select the integration time in number of power line cycles for the 
        present function (the default is 10 PLC).
        """
        self.open.write(str(func) + ':NPLCYCLES ' + str(val))
        self.open.write(str(func) + ':NPLCYCLES?')
        reply = self.open.read()
        return('NPL Cycles: ' + str(reply))
    
    # Method to check the range of function's NPL Cycles
    def range_NPLCYCLES(self,func):
        """
        Query the minimum and maximum values for NPLCycles.
        """
        self.open.write(str(func) + ':NPLCYCLES? MIN')
        replymin = self.open.read()
        self.open.write(str(func) + ':NPLCYCLES? MAX')
        replymax = self.open.read()
        return('NPL Cycles range: ' + str(replymin) + ',' + str(replymax))
    
    
    # Method to check current NPL Cycles configuration
    def check_NPLCYCLES(self,func):
        """
        Query the integration time for the selected function.
        """
        self.open.write(str(func) + ':NPLCYCLES?')
        reply = self.open.read()
        return('NPL Cycles: ' + str(reply))
        
    def configure_FAPERTURE(self,val):
        """
        Select the aperture time (or gate time) for frequency measurements (the default is 0.1 seconds). 
        Specify 10 ms (4 1/2 digits), 100 ms (default; 5 1/2 digits), or 1 second (6 1/2 digits). 
        MIN = 0.01 seconds. MAX = 1 second.
        """
        self.open.write('FREQUENCY:APERTURE ' + str(val))
        self.open.write('FREQUENCY:APERTURE?')
        reply = self.open.read()
        return('Frequency Aperture: ' + str(reply))
    
    def check_FPAPERTURE(self):
        """
        Query the aperture time for frequency measurements.
        """
        self.open.write('FREQUENCY:APERTURE?')
        reply = self.open.read()
        return('Frequency Aperture: ' + str(reply))
        
    def range_FAPERTURE(self):
        """
        Query the minimum and maximum value for frequency aperature.
        """
        self.open.write('FREQUENCY:APERTURE? MAX')
        replymax = self.open.read()
        self.open.write('FREQUENCY:APERTURE? MIN')
        replymin = self.open.read()
        return('Frequency Aperture range: ' + str(replymin) + ',' + str(replymax))

    def configure_PAPERTURE(self,val):
        """
        Select the aperture time (or gate time) for period measurements (the default is 0.1 seconds). 
        Specify 10 ms (4 1/2 digits), 100 ms (default; 5 1/2 digits), or 1 second (6 1/2 digits). 
        MIN = 0.01 seconds. MAX = 1 second.
        """
        self.open.write('PERIOD:APERTURE ' + str(val))
        self.open.write('PERIOD:APERTURE?')
        reply = self.open.read()
        return('Period Aperture: ' + str(reply))
    
    def check_PAPERTURE(self):
        """
        Query the aperture time for period measurements.
        """
        self.open.write('PERIOD:APERTURE?')
        reply = self.open.read()
        return('Period Aperture: ' + str(reply))
        
    def range_PAPERTURE(self):
        """
        Query the minimum and maximum value for period aperature.
        """
        self.open.write('PERIOD:APERTURE? MAX')
        replymax = self.open.read()
        self.open.write('PERIOD:APERTURE? MIN')
        replymin = self.open.read()
        return('Period Aperture range: ' + str(replymin) + ',' + str(replymax))    

###Sense Configuration
    def sense_setBANDWIDTH(self,val):
        """
        Specify the lowest frequency expected in the input signal. 
        The multimeter selects the slow, medium (default), or fast ac filter based 
        on the frequency you specify. MIN = 3 Hz. MAX = 200 Hz.
        """
        self.open.write('SENSE:DETECTOR:BANDWIDTH ' + str(val))
        self.open.write('SENSE:DETECTOR:BANDWIDTH?')
        reply = self.open.read()
        return('Sense bandwidth: ' + str(reply))
    
    def sense_rangeBANDWIDTH(self):
        """
        Query the minimum and maximum value for detector bandwidth
        """
        self.open.write('SENSE:DETECTOR:BANDWIDTH? MAX')
        replymax = self.open.read()
        self.open.write('SENSE:DETECTOR:BANDWIDTH? MIN')
        replymin = self.open.read()
        return('Sense bandwidth range: ' + str(replymin) + ',' + str(replymax))
    
    def sense_checkBANDWIDTH(self):
        """
        Query the ac filter. Returns “3”, “20”, or “200”.
        """
        self.open.write('SENSE:DETECTOR:BANDWIDTH?')
        reply = self.open.read()
        return('Sense bandwidth: ' + str(reply))
    
    def sense_setAUTOZERO(self,val):
        """
        Disable or enable (default) the autozero mode. The OFF and ONCE parameters have a similar effect. 
        Autozero OFF does not issue a new zero measurement until the next time the multimeter 
        goes to the “wait-for-trigger” state. Autozero ONCE issues an immediate zero measurement.
        """
        self.open.write('SENSE:ZERO:AUTO ' + str(val))
        self.open.write('SENSE:ZERO:AUTO?')
        reply = self.open.read()
        return('Sense autozero: ' + str(reply))
        
    def sense_checkAUTOZERO(self):
        """
        Query the autozero mode. Returns “0” (OFF or ONCE) or “1” (ON).
        """
        self.open.write('SENSE:ZERO:AUTO?')
        reply = self.open.read()
        return('Sense autozero: ' + str(reply))

###Input configuration        
    def input_setAUTOIMPEDANCE(self,val):
        """
        Disable or enable the automatic input resistance mode for dc voltage measurements. 
        With AUTO OFF (default), the input resistance is fixed at 10 MW for all ranges. 
        With AUTO ON, the resistance is set to >10 GW for the 100 mV, 1 V, and 10 V ranges.
        """
        self.open.write('INPUT:IMPEDANCE:AUTO ' + str(val))
        self.open.write('INPUT:IMPEDANCE:AUTO?')
        reply = self.open.read()
        return('Input auto impedance: ' + str(reply))   
    
    def input_checkAUTOIMPEDANCE(self):
        """
        Query the input resistance mode. Returns “0” (OFF) or “1” (ON).
        """
        self.open.write('INPUT:IMPEDANCE:AUTO?')
        reply = self.open.read()
        return('Input auto impedance: ' + str(reply))  

        
###Math Operations
    #Method to set function NULL|DB|DBM|AVERage|LIMit    
    def calculate_setFUNC(self,val):
        """
        Select the math function. Only one function can be enabled at a time. 
        The default function is null.
        """
        self.open.write('CALCULATE:FUNCTION ' + str(val))
        self.open.write('CALCULATE:FUNCTION?')
        reply = self.open.read()
        return('Function selected: ' + str(reply))
    
    def calculate_checkFUNC(self):
        """
        Query the present math function. Returns NULL, DB, DBM, AVER, or LIM.
        """
        self.open.write('CALCULATE:FUNCTION?')
        reply = self.open.read()
        return('Function selected: ' + str(reply))
    
    def calculate_setSTATE(self,val):
        """
        Disable or enable the selected math function.
        """
        self.open.write('CALCULATE:STATE ' + str(val))
        self.open.write('CALCULATE:STATE?')
        reply = self.open.read()
        if '1' in reply:
            return('Math function is ON')
        elif '0' in reply:
            return('Math function is OFF')
        else:
            return(str(reply))
        
    def calculate_checkSTATE(self):
        """
        Query the state of the math function. Returns “0” (OFF) or “1” (ON).
        """
        self.open.write('CALCULATE:STATE?')
        reply = self.open.read()
        if '1' in reply:
            return('Math function is ON')
        elif '0' in reply:
            return('Math function is OFF')
        else:
            return(str(reply))

    def calculate_AVG(self):
        """
        Read the minimum & maximum value found during a min-max operation. 
        Read the average of all readings & number of readings taken since min-max was enabled.
        """
        self.open.write('CALCULATE:AVERAGE:MINIMUM?')
        reply_min = self.open.read()
        self.open.write('CALCULATE:AVERAGE:MAXIMUM?')
        reply_max = self.open.read()
        self.open.write('CALCULATE:AVERAGE:AVERAGE?')
        reply_avg = self.open.read()
        self.open.write('CALCULATE:AVERAGE:COUNT?')
        reply_count = self.open.read()
        return('Average\'s values:\nMin: ' + str(reply_min) + \
                '\nMax: ' + str(reply_max) + '\nAVG: ' + str(reply_avg)\
                    + '\nCount: ' + str(reply_count) )
    
    def calculate_setNULLOFFSET(self,val):
        """
        Store a null value in the multimeter’s Null Register. 
        You must turn on the math operation before writing to the math register. 
        You can set the null value to any number between 0 and ±120% of the highest range, 
        for the present function. MIN = –120% of the highest range. MAX = 120% of the highest range.
        """
        self.open.write('CALCULATE:NULL:OFFSET ' + str(val))
        self.open.write('CALCULATE:NULL:OFFSET?')
        reply = self.open.read()
        return('Null offset: ' + str(reply))
    
    def calculate_checkNULLOFFSET(self):
        """
        Query the null value.
        """
        self.open.write('CALCULATE:NULL:OFFSET?')
        reply = self.open.read()
        return('Null offset: ' + str(reply))

    def calculate_rangeNULLOFFSET(self):
        """
        Query the minimum and maximum value for null offset
        """
        self.open.write('CALCULATE:NULL:OFFSET? MIN')
        replymin = self.open.read()
        self.open.write('CALCULATE:NULL:OFFSET? MAX')
        replymax = self.open.read()
        return('Null offset range: ' + str(replymin) + ',' + str(replymax))

    def calculate_setDBREF(self,val):
        """
        Store a relative value in the dB Relative Register. 
        You must turn on the math operation before writing to the math register. 
        You can set the relative value to any number between 0 dBm and ±200 dBm. 
        MIN = –200.00 dBm. MAX = 200.00 dBm.
        """
        self.open.write('CALCULATE:DB:REFERENCE ' + str(val))
        self.open.write('CALCULATE:DB:REFERENCE?')
        reply = self.open.read()
        return('dB reference: ' + str(reply))
        
    def calculate_checkDBREF(self):
        """
        Query the dB relative value.
        """
        self.open.write('CALCULATE:DB:REFERENCE?')
        reply = self.open.read()
        return('dB reference: ' + str(reply))

    def calculate_rangeDBREF(self):
        """
        Query the minimum and maximum value for dB relative value.
        """
        self.open.write('CALCULATE:DB:REFERENCE? MIN')
        replymin = self.open.read()
        self.open.write('CALCULATE:DB:REFERENCE? MAX')
        replymax = self.open.read()
        return('dB reference range: ' + str(replymin) + ',' + str(replymax)) 

    def calculate_setDBMREF(self,val):
        """
        Set the lower limit for limit testing. 
        You can set the value to any number between 0 and ±120% of the highest range, 
        for the present function. 
        MIN = –120% of the highest range. MAX = 120% of the highest range.
        """
        self.open.write('CALCULATE:DBM:REFERENCE ' + str(val))
        self.open.write('CALCULATE:DBM:REFERENCE?')
        reply = self.open.read()
        return('dBm reference: ' + str(reply))
        
    def calculate_checkDBMREF(self):
        """
        Query the dBm reference resistance.
        """
        self.open.write('CALCULATE:DBM:REFERENCE?')
        reply = self.open.read()
        return('dBm reference: ' + str(reply))

    def calculate_rangeDBMREF(self):
        """
        Query the minimum and maximum value for dBm relative value.
        """
        self.open.write('CALCULATE:DBM:REFERENCE? MIN')
        replymin = self.open.read()
        self.open.write('CALCULATE:DBM:REFERENCE? MAX')
        replymax = self.open.read()
        return('dBm reference range: ' + str(replymin) + ',' + str(replymax))       

    def calculate_setLOWERLIMIT(self,val):
        """
        Set the lower limit for limit testing. 
        You can set the value to any number between 0 and ±120% of the highest range, 
        for the present function. 
        MIN = –120% of the highest range. MAX = 120% of the highest range.
        """
        self.open.write('CALCULATE:LIMIT:LOWER ' + str(val))
        self.open.write('CALCULATE:LIMIT:LOWER?')
        reply = self.open.read()
        return('Lower Limit: ' + str(reply))
    
    def calculate_checkLOWERLIMIT(self):
        """
        Query the lower limit.
        """
        self.open.write('CALCULATE:LIMIT:LOWER?')
        reply = self.open.read()
        return('Lower Limit: ' + str(reply))
    
    def calculate_rangeLOWERLIMIT(self):
        """
        Query the minimum and maximum value for lower limit value.
        """
        self.open.write('CALCULATE:LIMIT:LOWER? MIN')
        replymin = self.open.read()
        self.open.write('CALCULATE:LIMIT:LOWER? MAX')
        replymax = self.open.read()
        return('Lower Limit range: ' + str(replymin) + ',' + str(replymax))         
      
    def calculate_setUPPERLIMIT(self,val):
        """
        Set the lower limit for limit testing. 
        You can set the value to any number between 0 and ±120% of the highest range, 
        for the present function. 
        MIN = –120% of the highest range. MAX = 120% of the highest range.
        """
        self.open.write('CALCULATE:LIMIT:UPPER ' + str(val))
        self.open.write('CALCULATE:LIMIT:UPPER?')
        reply = self.open.read()
        return('Upper Limit: ' + str(reply))
    
    def calculate_checkUPPERLIMIT(self):
        """
        Query the upper limit.
        """
        self.open.write('CALCULATE:LIMIT:UPPER?')
        reply = self.open.read()
        return('Upper Limit: ' + str(reply))
    
    def calculate_rangeUPPERLIMIT(self):
        """
        Query the minimum and maximum value for upper limit value.
        """
        self.open.write('CALCULATE:LIMIT:UPPER? MIN')
        replymin = self.open.read()
        self.open.write('CALCULATE:LIMIT:UPPER? MAX')
        replymax = self.open.read()
        return('Upper Limit range: ' + str(replymin) + ',' + str(replymax))         

###Memory
    #Method to store/do not store reading values. 'CALC' - store , '' - Do not store
    def data_setSTORE(self,val):
        """
        Selects whether readings taken using the INITiate command are stored in the 
        multimeter’s internal memory (default) or not stored at all. 
        In the default state (DATA:FEED RDG_STORE, "CALC"), up to 512 readings are 
        stored in memory when INIT is executed.
        """
        self.open.write('DATA:FEED RDG_STORE, "' + str(val) + '"')
        self.open.write('DATA:FEED?')
        reply = self.open.read()
        if 'CALC' in reply:
            return('Reading: stored')
        else:
            return('Reading: ' + str(reply)) 
    
    def data_check(self):
        """
        Query if reading is stored in internal memory and the number of readings in multimeter 
        internal memory 
        """
        self.open.write('DATA:FEED?')
        reply_feed = self.open.read()
        self.open.write('DATA:POINTS?')
        reply_points = self.open.read()
        if 'CALC' in reply_feed:
            return('Reading: stored\n' + 'No. of readings in memory: ' + str(reply_points))
        else:
            return('Reading: ' + str(reply_feed) + '\nNo. of readings in memory: ' + str(reply_points))   
        
###Triggering       
    def trigger_setSOURCE(self,src):
        """
        Select the source from which the multimeter will accept a trigger. 
        The multimeter will accept a software (bus) trigger, an immediate 
        internal trigger (this is the default source), or a hardware trigger 
        from the rear-panel Ext Trig (external trigger) terminal.
        """
        self.open.write('TRIGGER:SOURCE ' + str(src))
        self.open.write('TRIGGER:SOURCE?')
        reply = self.open.read()
        return('Trigger Source: ' + str(reply))
    
    def trigger_checkSOURCE(self):
        """
        Query the present trigger source.
        """
        self.open.write('TRIGGER:SOURCE?')
        reply = self.open.read()
        return('Trigger Source: ' + str(reply))        
    
    def trigger_setDELAY(self,val):
        """
        Insert a trigger delay between the trigger signal and each sample that follows. 
        If you do not specify a trigger delay, the multimeter automatically selects a delay for you. 
        Select from 0 to 3600 seconds. MIN = 0 seconds. MAX = 3600seconds.
        """
        self.open.write('TRIGGER:DELAY '+ str(val))
        self.open.write('TRIGGER:DELAY?')
        reply = self.open.read()   
        return('Trigger Delay: ' + str(reply))
    
    def trigger_checkDELAY(self):
        """
        Query the trigger delay.
        """
        self.open.write('TRIGGER:DELAY?')
        reply = self.open.read()   
        return('Trigger Delay: ' + str(reply))     
    
    def trigger_rangeDELAY(self):
        """
        Query the minimum and maximum trigger delay
        """
        self.open.write('TRIGGER:DELAY? MIN')
        replymin = self.open.read()           
        self.open.write('TRIGGER:DELAY? MAX')
        replymax = self.open.read()    
        return('Trigger Delay Range: ' + str(replymin) + ',' + str(replymax))
    
    def trigger_setAUTODELAY(self,val):
        """
        Disable or enable an automatic trigger delay.
        """
        self.open.write('TRIGGER:DELAY:AUTO ' + str(val))
        self.open.write('TRIGGER:DELAY:AUTO?')
        reply = self.open.read()
        return('Trigger auto-delay status: ' + str(reply))
    
    def trigger_checkAUTODELAY(self):
        """
        Query the automatic trigger delay setting. Returns “0” (OFF) or “1” (ON).
        """
        self.open.write('TRIGGER:DELAY:AUTO?')
        reply = self.open.read()
        return('Trigger auto-delay status: ' + str(reply))

    def trigger_setCOUNT(self,val):
        """
        Set the number of triggers the multimeter will accept before returning to the “idle” state. 
        Select from 1 to 50,000 triggers. The INFinite parameter instructs the multimeter to 
        continuously accept triggers (you must send a device clear to return to the “idle” state). 
        Trigger count is ignored while in local operation. MIN = 1. MAX = 50,000.
        """
        self.open.write('TRIGGER:COUNT '+ str(val))
        self.open.write('TRIGGER:COUNT?')
        reply = self.open.read()         
        return('Trigger Count: ' + str(reply))
    
    def trigger_checkCOUNT(self):
        """
        Query the trigger count.
        """
        self.open.write('TRIGGER:COUNT?')
        reply = self.open.read()         
        return('Trigger Count: ' + str(reply))     
    
    def trigger_rangeCOUNT(self):
        """
        Query the minimum and maximum trigger count.
        """
        self.open.write('TRIGGER:COUNT? MIN')
        replymin = self.open.read()           
        self.open.write('TRIGGER:COUNT? MAX')
        replymax = self.open.read()    
        return('Trigger Count Range: ' + str(replymin) + ',' + str(replymax))       
    
    def sample_setCOUNT(self,val):
        """
        Set the number of readings (samples) the multimeter takes per trigger. 
        Select from 1 to 50,000 readings per trigger. MIN = 1. MAX = 50,000.
        """
        self.open.write('SAMPLE:COUNT '+ str(val))
        self.open.write('SAMPLE:COUNT?')
        reply = self.open.read()         
        return('Sample Count: ' + str(reply))
      
    def sample_checkCOUNT(self):
        """
        Query the sample count.
        """
        self.open.write('SAMPLE:COUNT?')
        reply = self.open.read()         
        return('Sample Count: ' + str(reply))    

    def sample_rangeCOUNT(self):
        """
        Query the minimum and maximum sample count.
        """
        self.open.write('SAMPLE:COUNT? MIN')
        replymin = self.open.read()           
        self.open.write('SAMPLE:COUNT? MAX')
        replymax = self.open.read()    
        return('Sample Count Range: ' + str(replymin) + ',' + str(replymax)) 
        
    #Method to takea a reading, to be used after configure method for the same effect as measure
    def reading(self):
        """
        Change the state of the trigger system from the “idle” state to the “wait-for-trigger” state. 
        Measurements will begin when the specified trigger conditions are satisfied following the 
        receipt of the READ? command. Readings are sent immediately to the output buffer.
        """
        self.open.write('READ?')
        reply = self.open.read()
        return('Read Response: ' + str(reply))
        
    def fetch(self):
        """
        Transfer readings stored in the multimeter’s internal memory by the initiate command 
        to the multimeter’s output buffer where you can read them into your bus controller.
        """
        self.open.write('FETCH?')
        reply = self.open.read()
        return('Fetch: ' + str(reply))
    
    def initiate(self):
        """
        Change the state of the triggering system from the “idle” state to the “wait-for-trigger” state. 
        Measurements will begin when the specified trigger conditions are satisfied after this command 
        is received. The readings are placed in the multimeter’s internal memory. 
        Readings are stored in memory until you are able to retrieve them. 
        Use the fetch command to retrieve reading results.
        """
        self.open.write('INITIATE')
        return('Initiated')

