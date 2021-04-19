# -*- coding: utf-8 -*-
import HATS_VISA_base as hv_base
import time
import re
import io
import struct
from decimal import Decimal
from PIL import Image


###Sub-class for oscilloscope instrument (RIGOL-DS1054Z)
# A good part of this class is adapted and inspired from https://github.com/nathankjer/instruments
class oscilloscope(hv_base.VISAinst):
###Instrument Specific methods (oscilloscope)
    
###Internal use methods
    def _interpret_channel(self, channel):
        """
        Wrapper to allow specifying channels by their name (str) or by their
        number (int)
        """
        if type(channel) == int:
            assert channel <= 4 and channel >= 1
            channel = "CHAN" + str(channel)
        return channel

    def _interpret_source(self, source):
        """
        Wrapper to allow specifying sources by their name (str) or by their
        number (int)
        """
        if type(source) == int:
            assert source <= 2 and source >= 1
            source = "SOUR" + str(source)
        return source

    def _interpret_reference(self, reference):
        """
        Wrapper to allow specifying references by their name (str) or by their
        number (int)
        """
        if type(reference) == int:
            assert reference <= 10 and reference >= 1
            reference = "REF" + str(reference)
        return reference

    def _interpret_item(self, item):
        """
        Wrapper to allow specifying items by their name (str) or by their number
        (int)
        """
        if type(item) == int:
            assert item <= 5 and item >= 1
            item = "ITEM" + str(item)
        return item

    def _interpret_decoder(self,decoder):
        """
        Wrapper to allow specifying decoder (Decoder 1 / 2)
        """
        if type(decoder) == int:
            assert decoder <= 1 and decoder >= 2
            decoder = "DEC" + str(decoder)
        return decoder

    def _interpret_etable(self,etable):
        """
        Wrapper to allow specifying etable (Etable 1 / 2)
        """       
        if type(etable) == int:
            assert etable <= 1 and etable >= 2
            etable = "ETAB" + str(etable)
        return etable


    def _masked_float(self, number):
        number = float(number)
        if number == 9.9e37:
            return None
        else:
            return number
        
###Oscilloscope methods
    def autoscale(self):
        """
        Enable the waveform auto setting function. The oscilloscope will
        automatically adjust the vertical scale, horizontal timebase and trigger
        mode according to the input signal to realize optimum wave display. This
        command is equivalent to pressing the AUTO key at the front panel.
        """
        assert not self.mask_is_enabled()
        self.open.write(":AUT")
        return ("Autoscale")
    
    def clear(self):
        """
        Clear all the waveforms on the screen. If the oscilloscope is in the RUN
        state, waveform will still be displayed. This command is equivalent to
        pressing the CLEAR key at the front panel.
        """
        self.open.write(":CLE")

    def run(self):
        """
        Make the oscilloscope start running. equivalent to pressing the RUN/STOP
        key at the front panel.
        """
        self.open.write(":RUN")

    def stop(self):
        """
        Make the oscilloscope stop running. equivalent to pressing the RUN/STOP
        key at the front panel.
        """
        self.open.write(":STOP")

    def get_averages(self):
        """
        Query the number of averages under the average acquisition mode.
        """
        return int(self.open.query(":ACQ:AVER?"))

    def set_averages(self, count=2):
        """
        Set the number of averages under the average acquisition mode.
        """
        assert count in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
        self.open.write(":ACQ:AVER {0}".format(count))

    def get_memory_depth(self):
        """
        Query the memory depth of the oscilloscope namely the number of waveform
        points that can be stored in a single trigger sample. The default unit
        is pts (points).
        """
        response = self.open.query(":ACQuire:MDEPth?")
        if "AUTO" in response:
            return response
        else:
            return int(response)

    def set_memory_depth(self, memory_depth="AUTO"):
        """
        Query the memory depth of the oscilloscope namely the number of waveform
        points that can be stored in a single trigger sample. The default unit
        is pts (points).
        """
        assert self.is_running()
        if type(memory_depth) in (float, int):
            num_channels_shown = self.num_channels_shown()
            if num_channels_shown <= 1:
                assert memory_depth in [12000, 120000, 1200000, 12000000, 24000000]
            elif num_channels_shown <= 2:
                assert memory_depth in [6000, 60000, 600000, 6000000, 12000000]
            else:
                assert memory_depth in [3000, 30000, 300000, 3000000, 6000000]
        elif "AUTO" in memory_depth:
            pass
        else:
            raise ValueError
        self.open.write(":ACQuire:MDEPth {0}".format(memory_depth))

    def get_acquisition_type(self):
        """
        Query the acquisition mode when the oscilloscope samples.
        """
        return self.open.query(":ACQ:TYPE?")

    def set_acquisition_type(self, type="NORM"):
        """
        Set the acquisition mode when the oscilloscope samples.
        """
        assert type in ["NORM", "AVER", "PEAK", "HRES"]
        self.open.write(":ACQ:TYPE {0}".format(type))

    def get_sample_rate(self):
        """
        Query the current sample rate. The default unit is Sa/s.
        """
        return self._masked_float(self.open.query(":ACQuire:SRATe?"))

    def start_calibration(self):
        """
        The oscilloscope starts to execute the self-calibration.
        """
        return self.open.write("CAL:STAR")

    def quit_calibration(self):
        """
        Exit the calibration at any time.
        """
        return self.open.write("CAL:QUIT")

    def get_bandwidth_limit(self, channel=1):
        """
        Get the bandwidth limit parameter of the specified channel.
        """
        channel = self._interpret_channel(channel)
        return self.open.query(":{0}:BWL?".format(channel))

    def set_bandwidth_limit(self, type="OFF", channel=1):
        """
        Set the bandwidth limit parameter of the specified channel.
        """
        channel = self._interpret_channel(channel)
        assert type in ["20M", "OFF"]
        self.open.write(":{0}:BWL {1}".format(channel, type))

    def get_channel_coupling(self, channel=1):
        """
        Get the coupling mode of the specified channel.
        """
        channel = self._interpret_channel(channel)
        return self.open.query(":{0}:COUP?".format(channel))

    def set_channel_coupling(self, coupling="DC", channel=1):
        """
        Set the coupling mode of the specified channel.
        """
        channel = self._interpret_channel(channel)
        assert coupling in ["AC", "DC", "GND"]
        self.open.write(":{0}:COUP {1}".format(channel, coupling))

    def channel_is_shown(self, channel=1):
        """
        Query the status of the specified channel.
        """
        channel = self._interpret_channel(channel)
        if channel == "MATH":
            return self.math_is_shown()
        else:
            return bool(int(self.open.query(":{0}:DISP?".format(channel))))

    def show_channel(self, channel=1):
        """
        Enable the specified channel.
        """
        channel = self._interpret_channel(channel)
        if channel == "MATH":
            return self.show_math()
        else:
            self.open.write(":{0}:DISP 1".format(channel))

    def hide_channel(self, channel=1):
        """
        Disable the specified channel.
        """
        channel = self._interpret_channel(channel)
        if channel == "MATH":
            return self.hide_math()
        else:
            self.open.write(":{0}:DISP 0".format(channel))

    def num_channels_shown(self):
        return sum([int(self.channel_is_shown(channel)) for channel in range(1, 5)])

    def channel_is_inverted(self, channel=1):
        """
        Query the status of the inverted display mode of the specified channel.
        """
        channel = self._interpret_channel(channel)
        return bool(int(self.open.query(":{0}:INV?".format(channel))))

    def invert_channel(self, channel=1):
        """
        Enable or disable the inverted display mode of the specified channel.
        """
        channel = self._interpret_channel(channel)
        self.open.write(":{0}:INV 1".format(channel))

    def uninvert_channel(self, channel=1):
        """
        Enable or disable the inverted display mode of the specified channel.
        """
        channel = self._interpret_channel(channel)
        self.open.write(":{0}:INV 0".format(channel))

    def get_channel_offset(self, channel=1):
        """
        Query the vertical offset of the specified channel. The default unit is
        V.
        """
        channel = self._interpret_channel(channel)
        if channel == "MATH":
            return self.get_math_offset()
        else:
            return self._masked_float(self.open.query(":{0}:OFFSet?".format(channel)))

    def set_channel_offset(self, offset=0, channel=1):
        """
        Set the vertical offset of the specified channel. The default unit is V.
        """
        channel = self._interpret_channel(channel)
        if channel == "MATH":
            self.set_math_offset(offset)
        else:
            if self.get_channel_scale() >= 0.5:
                assert abs(offset) <= self.get_probe_ratio() * 100
            else:
                assert abs(offset) <= self.get_probe_ratio() * 2
            self.open.write(":{0}:OFFSet {1}".format(channel, offset))

    def get_channel_range(self, channel=1):
        """
        Query the vertical range of the specified channel. The default unit is
        V.
        """
        channel = self._interpret_channel(channel)
        return self._masked_float(self.open.query(":{0}:RANG?".format(channel)))

    def set_channel_range(self, range=8, channel=1):
        """
        Set the vertical range of the specified channel. The default unit is V.
        """
        channel = self._interpret_channel(channel)
        assert range >= 0.008 and range<= 800
        self.open.write(":{0}:RANG {1}".format(channel, range))

    def get_calibration_time(self, channel=1):
        """
        Query the delay calibration time of the specified channel to calibrate
        the zero offset of the corresponding channel. The default unit is s.
        """
        channel = self._interpret_channel(channel)
        return self._masked_float(self.open.query(":{0}:TCAL?".format(channel)))

    def set_calibration_time(self, t=0, channel=1):
        """
        Set the delay calibration time of the specified channel to calibrate the
        zero offset of the corresponding channel. The default unit is s.
        """
        channel = self._interpret_channel(channel)
        timebase_scale = self.get_timebase_scale()
        possible_times = [
            round(x * timebase_scale / 50, 10)
            for x in range(
                int(-1 / (2e5 * timebase_scale)), int(1 / (2e5 * timebase_scale) + 1)
            )
        ]
        t = min(possible_times, key=lambda x: abs(x - t))
        self.open.write(":{0}:TCAL {1}".format(channel, t))

    def get_channel_scale(self, channel=1):
        """
        Query the vertical scale of the specified channel. The default unit is
        V.
        """
        channel = self._interpret_channel(channel)
        if channel == "MATH":
            return self.get_math_scale()
        else:
            return self._masked_float(self.open.query(":{0}:SCALe?".format(channel)))

#    def set_channel_scale(self, scale=1, channel=1):
#        """
#        Set the vertical scale of the specified channel. The default unit is V.
#        """
#        channel = self._interpret_channel(channel)
#        if channel == "MATH":
#            self.set_math_scale(scale)
#        else:
#            possible_scales = [
#                val * self.get_probe_ratio(channel)
#                for val in [1e-3, 2e-3, 5e-3, 1, 2, 5, 1e1, 2e1, 5e1]
#            ]
#            scale = min(possible_scales, key=lambda x: abs(x - scale))
#            self.open.write(":{0}:SCALe {1}".format(channel, scale))

    def set_channel_scale(self, scale=1, channel=1):
        """
        Set the vertical scale of the specified channel. The default unit is V.
        """
        channel = self._interpret_channel(channel)
        if channel == "MATH":
            self.set_math_scale(scale)
        else:
            self.open.write(":{0}:SCALe {1}".format(channel, scale))

    def get_probe_ratio(self, channel=1):
        """
        Query the probe ratio of the specified channel.
        """
        channel = self._interpret_channel(channel)
        return self._masked_float(self.open.query(":{0}:PROBe?".format(channel)))

    def set_probe_ratio(self, probe_ratio=10, channel=1):
        """
        Set the probe ratio of the specified channel.
        """
        channel = self._interpret_channel(channel)
        assert probe_ratio in [
            0.01,
            0.02,
            0.05,
            0.1,
            0.2,
            0.5,
            1,
            2,
            5,
            10,
            20,
            50,
            100,
            200,
            500,
            1000,
        ]
        self.open.write(":{0}:PROBe {1}".format(channel, probe_ratio))

    def get_channel_unit(self, channel=1):
        """
        Query the amplitude display unit of the specified channel.
        """
        channel = self._interpret_channel(channel)
        return self.open.query(":{0}:UNIT?".format(channel))

    def set_channel_unit(self, unit="VOLT", channel=1):
        """
        Set the amplitude display unit of the specified channel.
        """
        channel = self._interpret_channel(channel)
        assert unit in ["VOLT", "WATT", "AMP", "UNKN"]
        self.open.write(":{0}:UNIT {1}".format(channel, unit))

    def vernier_is_enabled(self, channel=1):
        """
        Query the fine adjustment status of the vertical scale of the specified
        channel.
        """
        channel = self._interpret_channel(channel)
        return bool(int(self.open.query(":{0}:VERN?".format(channel))))

    def enable_vernier(self, channel=1):
        """
        Enable the fine adjustment of the vertical scale of the specified
        channel.
        """
        channel = self._interpret_channel(channel)
        self.open.write(":{0}:VERN 1".format(channel))

    def disable_vernier(self, channel=1):
        """
        Disable the fine adjustment of the vertical scale of the specified
        channel.
        """
        channel = self._interpret_channel(channel)
        self.open.write(":{0}:VERN 0".format(channel))

    def get_cursor_mode(self):
        """
        Query the cursor measurement mode.
        """
        return self.open.query(":CURS:MODE?")

    def set_cursor_mode(self, mode="OFF"):
        """
        Set the cursor measurement mode.
        """
        assert mode in ["OFF", "MAN", "TRAC", "AUTO", "XY"]
        if mode == "XY":
            assert "XY" in self.get_timebase_mode() 
        self.open.write(":CURS:MODE {0}".format(mode))

    def get_cursor_type(self):
        """
        Query the cursor type in manual cursor measurement mode.
        """
        cursor_mode = self.get_cursor_mode()
        assert "MAN" in cursor_mode
        cursor_mode = cursor_mode.replace("\n","")
        return self.open.query(":CURS:{0}:TYPE?".format(cursor_mode))

    def set_cursor_type(self, type="X"):
        """
        Set the cursor type in manual cursor measurement mode.
        """
        cursor_mode = self.get_cursor_mode()
        assert "MAN" in cursor_mode
        cursor_mode = cursor_mode.replace("\n","")
        assert type in ["X", "Y"]
        self.open.write(":CURS:{0}:TYPE {1}".format(cursor_mode, type))

    def get_cursor_source(self, source=None):
        """
        Query the channel source of the cursor.
        """
        cursor_mode = self.get_cursor_mode()
        cursor_mode = cursor_mode.replace("\n","")
        if "MAN" in cursor_mode:
            return self.open.query(":CURS:{0}:SOUR?".format(cursor_mode))
        elif "TRAC" in cursor_mode:
            assert source is not None
            source = self._interpret_source(source)
            return self.open.query(":CURS:{0}:{1}?".format(cursor_mode, source))

    def set_cursor_source(self, channel=1, source=None):
        """
        Set the channel source of the cursor.
        """
        channel = self._interpret_channel(channel)
        assert channel in ["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH"]
        assert self.channel_is_shown(channel)
        cursor_mode = self.get_cursor_mode()
        cursor_mode = cursor_mode.replace("\n","")
        if "MAN" in cursor_mode:
            self.open.write(":CURS:{0}:SOUR {1}".format(cursor_mode, channel))
        elif "TRAC" in cursor_mode:
            assert source is not None
            source = self._interpret_source(source)
            self.open.write(":CURS:{0}:{1} {2}".format(cursor_mode, source, channel))
        else:
            raise ValueError

    def get_cursor_time_unit(self):
        """
        Query the horizontal unit in the manual cursor measurement mode.
        """
        cursor_mode = self.get_cursor_mode()
        cursor_mode = cursor_mode.replace("\n","")
        assert "MAN" in cursor_mode
        return self.open.query(":CURS:{0}:TUN?".format(cursor_mode))

    def set_cursor_time_unit(self, unit="S"):
        """
        Set the horizontal unit in the manual cursor measurement mode.
        """
        cursor_mode = self.get_cursor_mode()
        cursor_mode = cursor_mode.replace("\n","")
        assert "MAN" in cursor_mode
        assert unit in ["S", "HZ", "DEGR", "PERC"]
        self.open.write(":CURS:{0}:TUN {1}".format(cursor_mode, unit))

    def get_cursor_vertical_unit(self):
        """
        Query the vertical unit in the manual cursor measurement mode.
        """
        cursor_mode = self.get_cursor_mode()
        cursor_mode = cursor_mode.replace("\n","")
        assert "MAN" in cursor_mode
        return self.open.query(":CURS:{0}:VUN?".format(cursor_mode))

    def set_cursor_vertical_unit(self, unit="SOUR"):
        """
        Set the vertical unit in the manual cursor measurement mode.
        """
        cursor_mode = self.get_cursor_mode()
        cursor_mode = cursor_mode.replace("\n","")
        assert "MAN" in cursor_mode
        assert unit in ["PERC", "SOUR"]
        self.open.write(":CURS:{0}:VUN {1}".format(cursor_mode, unit))

    def get_cursor_position(self, cursor="A", axis="X"):
        """
        Query the position of a cursor.
        """
        cursor_mode = self.get_cursor_mode()
        cursor_mode = cursor_mode.replace("\n","")
        assert any(i in cursor_mode for i in ["MAN", "TRAC", "XY"])
        assert cursor in ["A", "B"]
        assert axis in ["X", "Y"]
        return int(self.open.query(":CURS:{0}:{1}{2}?".format(cursor_mode, cursor, axis)))

    def set_cursor_position(self, cursor="A", axis="X", position=None):
        """
        Set the position of a cursor.
        """

        # Input checks
        assert cursor in ["A", "B"]
        assert axis in ["X", "Y"]
        if position is None:
            default_positions = {"A": {"X": 100, "Y": 100}, "B": {"X": 500, "Y": 300}}
            position = default_positions[cursor][axis]

        cursor_mode = self.get_cursor_mode()
        cursor_mode = cursor_mode.replace("\n","")
        assert cursor_mode in ["MAN", "TRAC", "XY"]
        if cursor_mode == "TRAC" and axis == "Y":
            raise ValueError
        possible_positions = {"X": range(5, 595), "Y": range(5, 395)}
        position = min(possible_positions[axis], key=lambda x: abs(x - position))
        self.open.write(":CURS:{0}:{1}{2} {3}".format(cursor_mode, cursor, axis, position))

    def get_cursor_value(self, cursor="A", axis="X"):
        """
        Query the value of a cursor. The unit depends on the unit currently
        selected.
        """
        cursor_mode = self.get_cursor_mode()
        cursor_mode = cursor_mode.replace("\n","")
        assert cursor_mode in ["MAN", "TRAC", "XY"]
        assert cursor in ["A", "B"]
        assert axis in ["X", "Y"]
        return self._masked_float(
            self.open.query(":CURS:{0}:{1}{2}Value?".format(cursor_mode, cursor, axis))
        )

    def get_cursor_delta(self, axis="X"):
        """
        Query the difference between the values of cursor A and cursor B. The
        unit depends on the unit currently selected.
        """
        cursor_mode = self.get_cursor_mode()
        cursor_mode = cursor_mode.replace("\n","")
        assert cursor_mode in ["MAN", "TRAC"]
        assert axis in ["X", "Y"]
        return self._masked_float(
            self.open.query(":CURS:{0}:{1}DEL?".format(cursor_mode, axis))
        )

    def get_cursor_inverse_delta(self):
        """
        Query the reciprocal of the absolute value of the difference between the
        values of cursor A and cursor B. The unit depends on the unit currently
        selected.
        """
        cursor_mode = self.get_cursor_mode()
        cursor_mode = cursor_mode.replace("\n","")
        assert cursor_mode in ["MAN", "TRAC"]
        return self._masked_float(self.open.query(":CURS:{0}:IXDELta?".format(cursor_mode)))

    def get_cursor_auto_parameters(self):
        """
        Query the parameters currently measured by the auto cursor.
        """
        parameters = self.open.query(":CURS:AUTO:ITEM?")
        parameters = parameters.replace("\n","")
        assert parameters in ["ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5"]
        return parameters

    def set_cursor_auto_parameters(self, parameters="OFF"):
        """
        The auto cursor function can measure 24 waveform parameters. Using this
        command, you can select the parameters to be measured by the auto cursor
        from the five parameters enabled last.
        """
        assert parameters in ["OFF", "ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5"]
        self.open.write(":CURS:AUTO:ITEM {0}".format(parameters))

    def get_decoder_mode(self,decoder=1):
        """
        Query the current decoder mode
        The query returns PAR, UART, SPI or IIC.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:MODE?".format(decoder))

    def set_decoder_mode(self,decoder=1,mode="PAR"):
        """
        Set the decoder to respective type
        """
        decoder = self._interpret_decoder(decoder)
        assert mode in ["PAR","SPI", "UART", "IIC"]
        self.open.write("{0}:MODE {1}".format(decoder,mode))

    def get_decoder_status(self,decoder=1):
        """
        Query the status of decoder
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:DISP?".format(decoder))

    def set_decoder_status(self,decoder=1,display="OFF"):
        """
        Set the status of decoder (ON/OFF)
        """
        decoder = self._interpret_decoder(decoder)
        display = str(display)
        assert display in ["1","ON","0","OFF"]
        self.open.write("{0}:DISP {1}".format(decoder,display))

    def get_decoder_format(self,decoder=1):
        """
        Query the bus display format
        The query returns HEX, ASC, DEC, BIN or LINE
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:FORM?".format(decoder))
    
    def set_decoder_format(self,decoder=1,form="ASC"):
        """
        Set the bus display format
        {HEX|ASCii|DEC|BIN|LINE}
        """
        decoder = self._interpret_decoder(decoder)
        assert form in ["HEX","ASC","DEC","BIN","LINE"]
        self.open.write("{0}:FORM {1}".format(decoder,form))

    def get_decoder_position(self,decoder=1):
        """
        Query the vertical position of the bus on the screen
        The query returns an integer between 50 and 350
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:POS?".format(decoder))

    def set_decoder_position(self,decoder=1,position=350):
        """
        Set the vertical position of the bus on the screen
        The screen is divided into 400 parts vertically which are marked as 0 to 400 from top to bottom respectively. 
        The range of <pos> is from 50 to 350.
        """
        decoder = self._interpret_decoder(decoder)
        assert position >= 50 and position <=350
        self.open.write("{0}:POS {1}".format(decoder,position))

    def get_decoder_threshold(self,decoder=1,channel=1):
        """
        query the threshold level of the specified analog channel
        """
        decoder = self._interpret_decoder(decoder)
        channel = self._interpret_channel(channel)
        return self.open.query("{0}:THRE:{1}?".format(decoder,channel))

    def set_decoder_threshold(self,decoder=1,channel=1,threshold=0):
        """
        set the threshold level of the specified analog channel
        """
        decoder = self._interpret_decoder(decoder)
        channel = self._interpret_channel(channel)
        threshold = str(threshold)
        self.open.write("{0}:THRE:{1} {2}".format(decoder,channel,threshold))

    def get_decoder_threshold_auto(self,decoder=1):
        """
        query the status of the auto threshold function of the analog channels
        The query returns 1 or 0
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:THRE:AUTO?".format(decoder))

    def set_decoder_threshold_auto(self,decoder=1,auto="ON"):
        """
        Set the status of the auto threshold function of the analog channels
        The query returns 1 or 0
        """
        decoder = self._interpret_decoder(decoder)
        auto = str(auto)
        assert auto in ["0","1","ON","OFF"]
        self.open.write("{0}:THRE:AUTO {1}".format(decoder,auto))

    def get_decoder_config_label(self,decoder=1):
        """
        query the status of the label display function
        The query returns 1 or 0.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:CONF:LAB?".format(decoder))

    def set_decoder_config_label(self,decoder=1,label="ON"):
        """
        Turn on or off the label display function
        When this function is turned on, the bus label will be displayed at the 
        lower-upper side of the bus (when the bus display is turned on)
        """
        decoder = self._interpret_decoder(decoder)
        label = str(label)
        assert label in ["0","1","ON","OFF"]
        self.open.write("{0}:CONF:LAB {1}".format(decoder,label))

    def get_decoder_config_line(self,decoder=1):
        """
        query the status of the bus display function
        The query returns 1 or 0.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:CONF:LINE?".format(decoder))

    def set_decoder_config_line(self,decoder=1,line="ON"):
        """
        Turn on or off the label display function
        When this function is enabled, the bus will be displayed on the screen. 
        You can send the :DECoder<n>:POSition command to adjust the vertical display position of the bus.
        """
        decoder = self._interpret_decoder(decoder)
        line = str(line)
        assert line in ["0","1","ON","OFF"]
        self.open.write("{0}:CONF:LINE {1}".format(decoder,line))

    def get_decoder_config_format(self,decoder=1):
        """
        query the status of the format display function
        The query returns 1 or 0.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:CONF:FORM?".format(decoder))

    def set_decoder_config_format(self,decoder=1,form="ON"):
        """
        Turn on or off the format display function
        When this function is turned on, the current bus display format will be displayed 
        at the right of the label display (when the bus display is turned on). 
        You can send the :DECoder<n>:FORMat command to set the bus display format.
        """
        decoder = self._interpret_decoder(decoder)
        form = str(form)
        assert form in ["0","1","ON","OFF"]
        self.open.write("{0}:CONF:FORM {1}".format(decoder,form))
    
    def get_decoder_config_endian(self,decoder=1):
        """
        query the status of the endian display function in serial bus decoding
        The query returns 1 or 0.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:CONF:END?".format(decoder))

    def set_decoder_config_endian(self,decoder=1,endian="ON"):
        """
        Turn on or off the format display function
        This command is invalid in parallel decoding.
        When this function is enabled, the current bus endian will be 
        displayed at the right of the format display (when the bus display is turned on).
        """
        decoder = self._interpret_decoder(decoder)
        endian = str(endian)
        assert endian in ["0","1","ON","OFF"]
        self.open.write("{0}:CONF:END {1}".format(decoder,endian))

    def get_decoder_config_width(self,decoder=1):
        """
        query the status of the width display function
        The query returns 1 or 0.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:CONF:WID?".format(decoder))

    def set_decoder_config_width(self,decoder=1,width="ON"):
        """
        Turn on or off the width display function
        When this function is enabled, the width of each frame of data will be displayed 
        at the right of the endian display (when the bus display is turned on).   
        """
        decoder = self._interpret_decoder(decoder)
        width = str(width)
        assert width in ["0","1","ON","OFF"]
        self.open.write("{0}:CONF:WID {1}".format(decoder,width))

    def get_decoder_config_srate(self,decoder=1):
        """
        Query the current digital sample rate
        The query returns the digital sample rate in scientific notation
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:CONF:SRAT?".format(decoder))

    def get_decoder_uart_lines(self,decoder=1,line="TX"):
        """
        query the TX/RX channel source of RS232 decoding.
        The query returns D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, CHAN1, CHAN2, CHAN3, CHAN4 or OFF.
        """
        decoder = self._interpret_decoder(decoder)
        line = str(line)
        assert line in ["TX","RX"]
        return self.open.query("{0}:UART:{1}?".format(decoder,line))

    def set_decoder_uart_lines(self,decoder=1,line="TX",source="CHAN1"):
        """
        Set the TX/RX channel source of RS232 decoding.
        When OFF is selected, no TX/RX channel source will be set. 
        The RX channel source and TX channel source (:DECoder<n>:UART:TX) cannot be both set to OFF.
        """
        decoder = self._interpret_decoder(decoder)
        line = str(line)
        source = str(source)
        assert line in ["TX","RX"]
        assert source in ["D0","D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15", "CHAN1", "CHAN2", "CHAN3", "CHAN4", "OFF"]
        self.open.write("{0}:UART:{1} {2}".format(decoder,line,source))

    def get_decoder_uart_polarity(self,decoder=1):
        """
        query the polarity of RS232 decoding
        The query returns NEG or POS.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:UART:POL?".format(decoder))

    def set_decoder_uart_polarity(self,decoder=1,pol="POS"):
        """
        set the polarity of RS232 decoding
        NEGative: negative polarity, namely high level is 0 and low level is 1. The RS232 standard uses negative polarity.
        POSitive: positive polarity, namely high level is 1 and low level is 0.
        """
        decoder = self._interpret_decoder(decoder)
        pol = str(pol)
        assert pol in ["POS","NEG"]
        self.open.write("{0}:UART:POL {1}".format(decoder,pol))

    def get_decoder_uart_endian(self,decoder=1):
        """
        query the endian of RS232 decoding
        The query returns LSB or MSB.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:UART:END?".format(decoder))

    def set_decoder_uart_endian(self,decoder=1,endian="LSB"):
        """
        set the endian of RS232 decoding
        Seting it LSB or MSB.
        """
        decoder = self._interpret_decoder(decoder)
        endian = str(endian)
        assert endian in ["LSB","MSB"]
        self.open.write("{0}:UART:END {1}".format(decoder,endian))

    def get_decoder_uart_baud(self,decoder=1):
        """
        query the baud rate of RS232 decoding. The default unit is bps (baud per second).
        The query returns the current baud rate in integer.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:UART:BAUD?".format(decoder))       

    def set_decoder_uart_baud(self,decoder=1,baud=9600):
        """
        Set the buad rate of RS232 decoding. The default unit is bps (baud per second).
        Range from 110 to 20M
        """
        decoder = self._interpret_decoder(decoder)
        assert baud >= 110 and baud <= 20000000
        self.open.write("{0}:UART:BAUD {1}".format(decoder,baud))

    def get_decoder_uart_width(self,decoder=1):
        """
        query the width of each frame of data in RS232 decoding
        The query returns an integer between 5 and 8.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:UART:WIDT?".format(decoder))

    def set_decoder_uart_width(self,decoder=1,width=8):
        """
        Set the width of each frame of data in RS232 decoding.
        Width of integer between 5 and 8
        """
        decoder = self._interpret_decoder(decoder)
        assert width >= 5 and width <= 8
        self.open.write("{0}:UART:WIDT {1}".format(decoder,width))
        
    def get_decoder_uart_stopbit(self,decoder=1):
        """
        query the stop bit after each frame of data in RS232 decoding.
        The query returns 1, 1.5 or 2.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:UART:STOP?".format(decoder))

    def set_decoder_uart_stopbit(self,decoder=1,stopbit=1):
        """
        set the stop bit after each frame of data in RS232 decoding.
        The query returns 1, 1.5 or 2.
        """
        decoder = self._interpret_decoder(decoder)
        assert stopbit in [1,1.5,2]
        self.open.write("{0}:UART:STOP {1}".format(decoder,stopbit))

    def  get_decoder_uart_parity(self,decoder=1):
        """
        query the even-odd check mode of the data transmission in RS232 decoding.
        The query returns NONE, EVEN or ODD.    
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:UART:PAR?".format(decoder))

    def  set_decoder_uart_parity(self,decoder=1,parity="NONE"):
        """
        set the even-odd check mode of the data transmission in RS232 decoding.
        Set the values of {NONE|EVEN|ODD}    
        """
        decoder = self._interpret_decoder(decoder)
        assert parity in ["NONE","EVEN","ODD"]
        self.open.write("{0}:UART:PAR {1}".format(decoder,parity))

    def get_decoder_iic_lines(self,decoder=1,lines="CLK"):
        """
        query the signal source of the various channel in I2C decoding.
        The query returns D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, CHAN1, CHAN2, CHAN3 or CHAN4.
        """
        decoder = self._interpret_decoder(decoder)
        assert lines in ["CLK","DATA"]
        return self.open.query("{0}:IIC:{1}?".format(decoder,lines))

    def set_decoder_iic_lines(self,decoder=1,lines="CLK",source="CHAN1"):
        """
        set the signal source of the various channel in I2C decoding.
        The source can be D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, CHAN1, CHAN2, CHAN3 or CHAN4.
        """
        decoder = self._interpret_decoder(decoder)
        assert lines in ["CLK","DATA"]
        assert source in ["D0","D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15", "CHAN1", "CHAN2", "CHAN3", "CHAN4"]
        self.open.write("{0}:IIC:{1} {2}".format(decoder,lines,source))

    def get_decoder_iic_address(self,decoder=1):
        """
        query the address mode of I2C decoding.
        The query returns NORM or RW.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:IIC:ADDR?".format(decoder))

    def set_decoder_iic_address(self,decoder=1,addr="NORM"):
        """
        set the address mode of I2C decoding.
        Setting it to NORM or RW.
        NORMal: the address bits (:TRIGger:IIC:AWIDth) does not include the R/W bit.
        RW: the address bits (:TRIGger:IIC:AWIDth) includes the R/W bit.
        """
        decoder = self._interpret_decoder(decoder)
        assert addr in ["NORM","RW"]
        self.open.write("{0}:IIC:ADDR {1}".format(decoder,addr))

    def get_decoder_spi_lines(self,decoder=1,lines="CLK"):
        """
        query the signal source of the various channel in SPI decoding.
        The query returns D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, CHAN1, CHAN2, CHAN3 or CHAN4.
        """
        decoder = self._interpret_decoder(decoder)
        assert lines in ["CLK","MOSI","MISO","CS"]
        return self.open.query("{0}:SPI:{1}?".format(decoder,lines))

    def set_decoder_spi_lines(self,decoder=1,lines="CLK",source="CHAN1"):
        """
        set the signal source of the various channel in SPI decoding.
        The source can be D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, CHAN1, CHAN2, CHAN3 or CHAN4.
        """
        decoder = self._interpret_decoder(decoder)
        assert lines in ["CLK","MOSI","MISO","CS"]
        assert source in ["D0","D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15", "CHAN1", "CHAN2", "CHAN3", "CHAN4"]
        self.open.write("{0}:SPI:{1} {2}".format(decoder,lines,source))
    
    def get_decoder_spi_select(self,decoder=1):
        """
        query the CS polarity in SPI decoding
        The query returns NCS or CS.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:SPI:SEL?".format)

    def set_decoder_spi_select(self,decoder=1,select="NCS"):
        """
        set the CS polarity in SPI decoding
        Setting it to either NCS or CS.
        NCS: low level is valid (). The instrument starts transmitting data when the CS is low.
        CS: high level is valid (). The instrument starts transmitting data when the CS is high.
        This command is only valid in the CS mode (:DECoder<n>:SPI:MODE).
        """
        decoder = self._interpret_decoder(decoder)
        assert select in ["NCS","CS"]
        self.open.write("{0}:SPI:SEL {1}".format,select)        

    def get_decoder_spi_mode(self,decoder=1):
        """
        query the frame synchronization mode of SPI decoding
        The query returns CS or TIM.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:SPI:MODE?".format(decoder))

    def set_decoder_spi_mode(self,decoder=1,mode="TIM"):
        """
        set the frame synchronization mode of SPI decoding
        Setting it either CS or TIM.
        CS: it contains a chip select line (CS). You can perform frame synchronization according to CS. At this point, 
            you need to send the :DECoder<n>:SPI:CS and :DECoder<n>:SPI:SELect commands to set the CS channel source and polarity.
        TIMeout: you can perform frame synchronization according to the timeout time. At this point, you need
        """
        decoder = self._interpret_decoder(decoder)
        assert mode in ["TIM","CS"]
        self.open.write("{0}:SPI:MODE {1}".format(decoder,mode))

    def get_decoder_spi_timeout(self,decoder=1):
        """
        query the timeout time in the timeout mode of SPI decoding. The default unit is s.
        The query returns the timeout time in scientific notation.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:SPI:TIM?".format(decoder))
        
    def set_decoder_spi_timeout(self,decoder=1,timeout=0.000001):
        """
        set the timeout time in the timeout mode of SPI decoding. The default unit is s.
        The timeout time should be greater than the maximum pulse width of the clock and lower than the idle time between frames.
        This command is only valid in the timeout mode (:DECoder<n>:SPI:MODE).
        """
        decoder = self._interpret_decoder(decoder)
        self.open.write("{0}:SPI:TIM {1} ".format(decoder.timeout))
        
    def get_decoder_spi_polarity(self,decoder=1):
        """
        query the polarity of the SDA data line in SPI decoding.
        The query returns NEG or POS.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:SPI:POL?".format(decoder))
    
    def set_decoder_spi_polarity(self,decoder=1,polarity="POS"):
        """
        set the polarity of the SDA data line in SPI decoding.
        Setting it either NEG or POS.
        NEGative: . The low level is 1.
        POSitive: . The high level is 1.
        """
        decoder = self._interpret_decoder(decoder)
        assert polarity in ["POL"]
        self.open.write("{0}:SPI:POL {1}".format(decoder,polarity))    
        
    def get_decoder_spi_edge(self,decoder=1):
        """
        query the clock type when the instrument samples the data line in SPI decoding.
        The query returns RISE or FALL.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:SPI:EDGE?".format(decoder))
    
    def set_decoder_spi_edge(self,decoder=1,edge="RISE"):
        """
        set the clock type when the instrument samples the data line in SPI decoding.
        Setting it either RISE or FALL.
        """
        decoder = self._interpret_decoder(decoder)
        assert edge in ["RISE","FALL"]
        self.open.write("{0}:SPI:EDGE {1}".format(decoder,edge))
        
    def get_decoder_spi_endian(self,decoder=1):
        """
        query the endian of the SPI decoding data.
        The query returns LSB or MSB.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:SPI:END?".format(decoder))

    def set_decoder_spi_endian(self,decoder=1,endian="MSB"):
        """
        Set the endian of the SPI decoding data.
        Setting it either LSB or MSB.
        """
        decoder = self._interpret_decoder(decoder)
        assert endian in ["MSB","LSB"]
        self.open.write("{0}:SPI:END {1}".format(decoder,endian))

    def get_decoder_spi_width(self,decoder=1):
        """
        query the number of bits of each frame of data in SPI decoding.
        The query returns an integer between 8 and 32.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:SPI:WIDT?".format(decoder))

    def set_decoder_spi_width(self,decoder=1,width=8):
        """
        set the number of bits of each frame of data in SPI decoding.
        Setting an integer between 8 and 32.
        """
        decoder = self._interpret_decoder(decoder)
        assert width >= 8 and width <= 32
        self.open.write("{0}:SPI:WIDT {1}".format(decoder,width))

    def get_decoder_parallel_clk(self,decoder=1):
        """
        query the CLK channel source of parallel decoding.
        The query returns D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, CHAN1, CHAN2, CHAN3, CHAN4 or OFF.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:PAR:CLK?".format(decoder))

    def set_decoder_parallel_clk(self,decoder=1,clk="CHAN1"):
        """
        Set the CLK channel source of parallel decoding.
        The source can be D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, CHAN1, CHAN2, CHAN3, CHAN4 or OFF.
        """
        decoder = self._interpret_decoder(decoder)
        assert clk in ["D0","D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15", "CHAN1", "CHAN2", "CHAN3", "CHAN4","OFF"]
        self.open.write("{0}:PAR:CLK {1}".format(decoder,clk))

    def get_decoder_parallel_edge(self,decoder=1):
        """
        query the edge type of the clock channel when the instrument samples the data channel in parallel decoding.
        The query returns RISE, FALL or BOTH.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:PAR:EDGE?".format(decoder))

    def set_decoder_parallel_edge(self,decoder=1,edge="RISE"):
        """
        Set the edge type of the clock channel when the instrument samples the data channel in parallel decoding.
        Setting it either RISE, FALL or BOTH.
        """
        decoder = self._interpret_decoder(decoder)
        assert edge in ["RISE","FALL","BOTH"]
        self.open.write("{0}:PAR:EDGE {1}".format(decoder,edge))

    def get_decoder_parallel_width(self,decoder=1):
        """
        query the data width (namely the number of bits of each frame of data) of the parallel bus.
        The query returns an integer between 1 and 16.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:PAR:WIDT?".format(decoder))

    def set_decoder_parallel_width(self,decoder=1,width=8):
        """
        set the data width (namely the number of bits of each frame of data) of the parallel bus.
        Setting an integer between 1 and 16.
        After setting the data width using this command, send the 
        :DECoder<n>:PARallel:BITX and :DECoder<n>:PARallel:SOURce commands to select each bit and set the channel source for each bit respectively.
        """
        decoder = self._interpret_decoder(decoder)
        assert width >=1 and width <=16
        self.open.write("{0}:PAR:WIDT {1}".format(decoder))

    def get_decoder_parallel_bitx(self,decoder=1):
        """
        query the data bit that requires a channel source on the parallel bus.
        The query returns the current data bit in integer.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:PAR:BITX?".format(decoder))

    def set_decoder_parallel_bitx(self,decoder=1,bit=0):
        """
        set the data bit that requires a channel source on the parallel bus.
        Setting it to a value between 0 and (data width-1)
        Set the data width using the :DECoder<n>:PARallel:WIDTh command.
        After selecting the desired bit, send the :DECoder<n>:PARallel:SOURce command to set the channel source of this bit.
        """
        decoder = self._interpret_decoder(decoder)
        assert bit >= 0 and bit <=15
        self.open.write("{0}:PAR:BITX {1}".format(decoder,bit))  

    def get_decoder_parallel_source(self,decoder=1):
        """
        query the channel source of the data bit currently selected.
        The query returns D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, CHAN1, CHAN2, CHAN3 or CHAN4
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:PAR:SOUR?".format(decoder))

    def set_decoder_parallel_source(self,decoder=1,source=""):
        """
        set the channel source of the data bit currently selected.
        Setting either D0, D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, D15, CHAN1, CHAN2, CHAN3 or CHAN4
        Default depends on the bit selected
        """
        decoder = self._interpret_decoder(decoder)
        assert source in ["D0","D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15", "CHAN1", "CHAN2", "CHAN3", "CHAN4"]
        self.open.write("{0}:PAR:SOUR {1}".format(decoder,source))

    def get_decoder_parallel_polarity(self,decoder=1):
        """
        query the data polarity of parallel decoding.
        The query returns NEG or POS.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:PAR:POL?".format(decoder))

    def set_decoder_parallel_polarity(self,decoder=1,polarity="POS"):
        """
        set the data polarity of parallel decoding.
        Setting it either NEG or POS.
        NEGative: The low level is 1.
        POSitive: The high level is 1.
        """
        decoder = self._interpret_decoder(decoder)
        assert polarity in ["POS","NEG"]
        self.open.write("{0}:PAR:POL {1}".format(decoder,polarity))

    def get_decoder_parallel_nreject(self,decoder=1):
        """
        query the status of the noise rejection function of parallel decoding.
        The query returns 1 or 0.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:PAR:NREJ?".format(decoder))

    def set_decoder_parallel_nreject(self,decoder=1,nreject="OFF"):
        """
        Turn on or off the noise rejection function of parallel decoding,
        Noise rejection can remove the data without enough duration on the bus to eliminate the glitches of the actual circuit.
        When the noise rejection is turned on, sending the :DECoder<n>:PARallel:NRTime command can set the desired rejection time.
        """
        decoder = self._interpret_decoder(decoder)
        nreject = str(nreject)
        assert nreject in ["1","0","OFF","ON"]
        self.open.write("{0}:PAR:NREJ {1}".format(decoder,nreject))    

    def get_decoder_parallel_nrtime(self,decoder=1):
        """
        query the noise rejection time of parallel decoding. The default unit is s.
        The query returns the noise rejection time in scientific notation.  
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:PAR:NRT?".format(decoder))

    def set_decoder_parallel_nrtime(self,decoder=1,nrtime=0.00):
        """
        set the noise rejection time of parallel decoding. The default unit is s.
        Setting the nrtime between the range 0.00s to 100ms
        Before sending this command, send the :DECoder<n>:PARallel:NREJect command to turn on the noise rejection function.  
        """
        decoder = self._interpret_decoder(decoder)
        assert nrtime >= 0.00 and nrtime <=0.1
        self.open.write("{0}:PAR:NRT {1}".format(decoder,nrtime))   

    def get_decoder_parallel_clkcompensation(self,decoder=1):
        """
        query the clock compensation time of parallel decoding. The default unit is s.
        The query returns the compensation time in scientific notation.
        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:PAR:CCOM?".format(decoder))
    
    def set_decoder_parallel_clkcompensation(self,decoder=1,ccom=0.0):
        """
        set the clock compensation time of parallel decoding. The default unit is s.
        Setting clk compensation between the range -0.1s to 0.1s
        """
        decoder = self._interpret_decoder(decoder)
        assert ccom >=-0.1 and ccom <=0.1
        self.open.write("{0}:PAR:CCOM {1}".format(decoder,ccom))

    def get_decoder_parallel_plot(self,decoder=1):
        """
        query the status of the curve function of parallel decoding.
        The query returns 1 or 0.

        """
        decoder = self._interpret_decoder(decoder)
        return self.open.query("{0}:PAR:PLOT?".format(decoder))

    def set_decoder_parallel_plot(self,decoder=1,plot="OFF"):
        """
        Turn on or off the curve function of parallel decoding.
        When this function is turned on, the variation trend of the bus data is displayed in vector diagram form.

        """
        decoder = self._interpret_decoder(decoder)
        plot = str(plot)
        assert plot in ["1","0","OFF","ON"]
        self.open.write("{0}:PAR:PLOT {1}".format(decoder,plot))

    def take_screenshot(self):
        """
        Read the bitmap data stream of the image currently displayed.
        """
        self.open.write(":DISPlay:DATA? ON,OFF,PNG")
        buff = self.open.read_raw(99999999)
        n_header_bytes = int(chr(buff[1])) + 2
        n_data_bytes = int(buff[2:n_header_bytes].decode("ascii"))
        decoded_block = buff[n_header_bytes : n_header_bytes + n_data_bytes]
        im = Image.open(io.BytesIO(decoded_block))
        filename = time.strftime("%Y-%m-%d_%H-%M-%S.png", time.localtime())
        im.save(filename, format="png")
        return filename

    def get_display_type(self):
        """
        Query the display mode of the waveform on the screen.
        """
        return self.open.query(":DISP:TYPE?")

    def set_display_type(self, type="VECT"):
        """
        Set the display mode of the waveform on the screen.
        """
        assert type in ["VECT", "DOTS"]
        self.open.write(":DISP:TYPE {0}".format(type))

    def get_persistence_time(self):
        """
        Query the persistence time. The default unit is s.
        """
        persistence_time = self.open.query(":DISP:GRAD:TIME?")
        persistence_time = persistence_time.replace("\n","")
        if persistence_time in ["MIN", "INF"]:
            return persistence_time
        else:
            return self._masked_float(persistence_time)

    def set_persistence_time(self, persistence_time="MIN"):
        """
        Set the persistence time. The default unit is s.
        """
        assert persistence_time in ["MIN", 0.1, 0.2, 0.5, 1, 5, 10, "INF"]
        self.open.write(":DISP:GRAD:TIME {0}".format(persistence_time))

    def get_waveform_brightness(self):
        """
        Query the waveform brightness. The default unit is %.
        """
        return int(self.open.query(":DISP:WBR?"))

    def set_waveform_brightness(self, brightness=50):
        """
        Set the waveform brightness. The default unit is %.
        """
        assert brightness >= 0 and brightness <= 100
        self.open.write(":DISP:WBR {0}".format(brightness))

    def get_grid(self):
        """
        Query the grid type of screen display.
        """
        return self.open.query(":DISPlay:GRID?")

    def set_grid(self, grid="FULL"):
        """
        Set the grid type of screen display.
        """
        assert grid in ["FULL", "HALF", "NONE"]
        self.open.write(":DISP:GRID {0}".format(grid))

    def get_grid_brightness(self):
        """
        Query the brightness of the screen grid. The default unit is %.
        """
        return int(self.open.query(":DISP:GBR?"))

    def set_grid_brightness(self, brightness=50):
        """
        Set the brightness of the screen grid. The default unit is %.
        """
        assert brightness >= 0 and brightness <= 100
        self.open.write(":DISP:GBR {0}".format(brightness))

    def get_etable_display(self,etable=1):
        """
        query the status of the decoding event table.
        The query returns 1 or 0.
        """
        etable = self._interpret_etable(etable)
        return self.open.query("{0}:DISP?".format(etable))

    def set_etable_display(self,etable=1,display="OFF"):
        """
        Turn on or off the decoding event table.
        This command is only valid when the decoder is turned on (:DECoder<n>:DISPlay).
        """
        etable = self._interpret_etable(etable)
        display = str(display)
        assert display in ["ON","OFF","1","0"]
        self.open.write("{0}:DISP {1}".format(etable,display))       

    def get_etable_format(self,etable=1):
        """
        query the data display format of the event table.
        The query returns HEX, ASC or DEC.
        """
        etable = self._interpret_etable(etable)
        return self.open.query("{0}:FORM?".format(etable))

    def set_etable_format(self,etable=1,form="HEX"):
        """
        set the data display format of the event table.
        Setting it either HEX, ASC or DEC.
        """
        etable = self._interpret_etable(etable)
        assert form in ["HEX","ASC","DEC"]
        self.open.write("{0}:FORM {1}".format(etable,form))

    def get_etable_view(self,etable=1):
        """
        query the display mode of the event table.
        The query returns PACK, DET or PAYL.
        """
        etable = self._interpret_etable(etable)
        return self.open.query("{0}:VIEW?".format(etable))

    def set_etable_view(self,etable=1,view="PACK"):
        """
        set the display mode of the event table.
        Setting it between PACK, DET or PAYL.
        PACKage: the time and data are displayed in the event table.    
        DETail: the detailed data of the specified row is displayed in the event table. 
        PAYLoad: all data of the specified column is displayed in the event table.
        """
        etable = self._interpret_etable(etable)
        assert view in ["PACK","DET","PAYL"]
        self.open.write("{0}:VIEW {1}".format(etable,view))

    def get_etable_column(self,etable=1):
        """
        query the current column of the event table.
        The query returns DATA, TX, RX, MISO or MOSI.
        """
        etable = self._interpret_etable(etable)
        return self.open.query("{0}:COL?".format(etable))

    def set_etable_column(self,etable=1,column=""):
        """
        Set the current column of the event table.
        Setting it either DATA, TX, RX, MISO or MOSI depending on decoder mode
        When different decoder is selected (:DECoder<n>:MODE), the range of <col> differs.
        Parallel decoding: DATA
        RS232 decoding: TX|RX I2C decoding: DATA SPI decoding: MISO|MOSI
        If the TX or RX channel source in RS232 decoding or the MISO or MOSI channel source in SPI decoding is set to OFF, <col> cannot be set to the corresponding parameter.
        """
        etable = self._interpret_etable(etable)
        if column == "":
            return "Check Decoder Mode and input a valid column argument"
        assert column in ["DATA","TX","RX","MOSI","MISO"]
        self.open.write("{0}:COL {1}".format(etable,column))

    def get_etable_row(self,etable=1):
        """
        query the current row of the event table.
        The query returns the current row in integer. If the current even table is empty, the query returns 0.
        """
        etable = self._interpret_etable(etable)
        return self.open.query("{0}:ROW?".format(etable))

    def set_etable_row(self,etable=1,row=1):
        """
        set the current row of the event table.     
        """
        etable = self._interpret_etable(etable)
        self.open.write("{0}:ROW {1}".format(etable,row))

    def get_etable_sort(self,etable=1):
        """
        query the display type of the decoding results in the event table.
        The query returns ASC or DESC.
        """
        etable = self._interpret_etable(etable)
        return self.open.query("{0}SORT?".format(etable))

    def set_etable_sort(self,etable=1,sort="ASC"):
        """
        set the display type of the decoding results in the event table.
        Setting them either ASC or DESC.
        ASCend: the events are displayed in the order in which they occurred.
        DESCend: the events are displayed in the order reverse to the order in which they occurred.
        """
        etable = self._interpret_etable(etable)
        assert sort in ["ASC","DESC"]
        self.open.write("{0}:SORT {1}".format(etable,sort))

    def get_etable_data(self,etable=1):
        """
        Read the current event table data.
        """
        etable = self._interpret_etable(etable)
        return self.open.query("{0}:DATA?".format(etable))

    def get_waveform_record_end_frame(self):
        """
        query the end frame of waveform recording.
        The query returns the current end frame in integer.
        """
        return self.open.query("FUNC:WREC:FEND?")
    
    def set_waveform_record_end_frame(self,fend=5000):
        """
        set the end frame of waveform recording.
        Use the :FUNCtion:WRECord:FMAX? command to query the maximum number of frames can be recorded currently.
        """
        self.open.write("FUNC:WREC:FEND {0}".format(fend))      

    def get_waveform_record_max_frame(self):
        """
        Query the maximum number of frames can be recorded currently.
        The query returns the maximum number of frames can be recorded currently in integer.
        """
        return self.open.query("FUNC:WREC:MAX?")
    
    def get_waveform_record_frame_timeinterval(self):
        """
        query the time interval between frames in waveform recording. The default unit is s.
        The query returns the time interval currently set in scientific notation.
        """
        return self.open.query("FUNC:WREC:FINT?")

    def set_waveform_record_frame_timeinterval(self,interval=0.0000001):
        """
        set the time interval between frames in waveform recording. The default unit is s.
        setting a range of between 100ns to 10s
        """
        assert interval >= 0.0000001 and interval <= 10
        self.open.write("FUNC:WREC:FINT {0}".format(interval))

    def get_waveform_record_prompt(self):
        """
        query the status of the sound prompt when the recording finishes.
        The query returns 1 or 0.
        """
        return self.open.query("FUNC:WREC:PROM?")

    def set_waveform_record_prompt(self,prompt="ON"):
        """
        Turn on or off the sound prompt when the recording finishes
        When the sound prompt is turned on, the instrument exerts a sound prompt when the recording 
        finishes no matter whether the system sound (refer to :SYSTem:BEEPer) is turned on or not.
        """
        prompt = str(prompt)
        assert prompt in ["ON","OFF","1","0"]
        self.open.write("FUNC:WREC:PROM {0}".format(prompt))

    def get_waveform_record_operate(self):
        """
        query the status of the waveform recording.
        The query returns RUN or STOP.
        """
        return self.open.query("FUNC:WREC:OPER?")

    def set_waveform_record_operate(self,status):
        """
        Start or stop the waveform recording
        Before sending this command, send the :FUNCtion:WRECord:ENABle command to turn on the waveform recording function. Otherwise, this command is invalid.
        """
        assert status in ["RUN","STOP"]
        self.open.write("FUNC:WREC:OPER {0}".format(status))

    def get_waveform_record_enable(self):
        """
        query the status of the waveform recording function.
        The query returns 1 or 0.
        """
        return self.open.query("FUNC:WREC:ENAB?")

    def set_waveform_record_enable(self,enable="OFF"):
        """
        Turn on or off the waveform recording function
        The waveform recording function can only be enabled when the horizontal timebase mode is “YT” 
        and the horizontal timebase is lower than 200ms.
        After turning on the waveform recording function, RUN/STOP can be used to start or stop the waveform 
        recording. At this point, you can send the :FUNCtion:WRECord:OPERate command to start the recording.
        """
        enable = str(enable)
        assert enable in ["ON","OFF","1","0"]
        self.open.write("FUNC:WREC:ENAB {0}".format(enable))

    def get_waveform_replay_frame_start(self):
        """
        query the start frame of waveform playback.
        The query returns an integer.
        """
        return self.open.query("FUNC:WREP:FST?")

    def set_waveform_replay_frame_start(self,frame=1):
        """
        set the start frame of waveform playback.
        Sets an integer from 1 to the maximum number of frames recorded
        Use the :FUNCtion:WRECord:FEND command to set the maximum number of frames recorded.
        The start frame of waveform playback cannot be greater than the end frame of waveform playback (:FUNCtion:WREPlay:FEND).
        You can only set the start frame of waveform playback when a waveform is currently recorded.
        You cannot set the start frame of waveform playback during the waveform recording or playback process.
        """
        assert frame >= 1
        self.open.write("FUNC:WREP:FST {0}".format(frame))    

    def get_waveform_replay_frame_end(self):
        """
        query the end frame of waveform playback.
        The query returns an integer.
        """
        return self.open.query("FUNC:WREP:FEND?")

    def set_waveform_replay_frame_end(self,frame):
        """
        set the end frame of waveform playback.
        Sets an integer from 1 to the maximum number of frames recorded
        Use the :FUNCtion:WRECord:FEND command to set the maximum number of frames recorded.
        The end frame of waveform playback cannot be lower than the start frame of waveform playback (:FUNCtion:WREPlay:FSTart).
        You can only set the end frame of waveform playback when a waveform is currently recorded.
        You cannot set the end frame of waveform playback during the waveform recording or playback process.
        """
        self.open.write("FUNC:WREP:FEND {0}".format(frame))

    def get_waveform_replay_frame_max(self):
        """
        Query the maximum number of frames can be played, namely the maximum number of frames recorded.
        The query returns an integer.
        """
        return self.open.query("FUNC:WREP:FMAX?")

    def get_waveform_replay_frame_timeinterval(self):
        """
        query the time interval between frames in waveform playback. The default unit is s.
        The query returns the time interval currently set in scientific notation.
        """
        return self.open.query("FUNC:WREP:FINT?")

    def set_waveform_replay_frame_timeinterval(self,interval=0.0000001):
        """
        set the time interval between frames in waveform playback. The default unit is s.
        setting a range of between 100ns to 10s
        """
        assert interval >= 0.0000001 and interval <= 10
        self.open.write("FUNC:WREP:FINT {0}".format(interval))

    def get_waveform_replay_mode(self):
        """
        query the waveform playback mode.
        The query returns REP or SING.
        """
        return self.open.query("FUNC:WREP:MODE?")

    def set_waveform_replay_mode(self,mode="SING"):
        """
        Set the waveform playback mode.
        Setting it either REP or SING
        REPeat: cycle playback. Play from the start frame to the end frame and then repeat until you stop it manually.
        SINGle: single playback. Play from the start frame to the end frame and then stop.
        You can only set the waveform playback mode when a waveform is currently recorded.
        You cannot set the waveform playback mode during the waveform recording or playback process.
        """
        assert mode in ["SING","REP"]
        self.open.write("FUNC:WREP:MODE {0}".format(mode))

    def get_waveform_replay_direction(self):
        """
        query the waveform playback direction
        The query returns FORW or BACK.
        """
        return self.open.query("FUNC:WREP:DIR?")

    def set_waveform_replay_direction(self,direction="FORW"):
        """
        set the waveform playback direction
        Setting it either FORW or BACK.
        FORWard: positive direction. Play from the start frame to the end frame.
        BACKward: negative direction. Play from the end frame to the start frame.
        You can only set the waveform playback direction when a waveform is currently recorded.
        You cannot set the waveform playback direction during the waveform recording or playback process.
        """
        assert direction in ["FORW","BACK"]
        self.open.write("FUNC:WREP:DIR {0}".format(direction))

    def get_waveform_replay_operate(self):
        """
        query the status of the waveform playback.
        The query returns RUN, PAUS or STOP.
        """
        return self.open.query("FUNC:WREP:OPER?")

    def set_waveform_replay_operate(self,status="STOP"):
        """
        Start,pause or stop the waveform playback
        This command is only valid when waveform has already been recorded.
        """
        assert status in ["RUN","PAUS","STOP"]
        self.open.write("FUNC:WREP:OPER {0}".format(status))

    def get_waveform_replay_frame_current(self):
        """
        query the current frame in waveform playback.
        The query returns an integer.
        """
        return self.open.query("FUNC:WREP:FCUR?")

    def set_waveform_replay_frame_current(self,frame):
        """
        set the current frame in waveform playback.
        Setting it to an integer between 1 to the maximum number of frames recorded
        Use the :FUNCtion:WRECord:FEND command to set the maximum number of frames recorded.
        You can only set the current frame of waveform playback when a waveform is currently recorded.
        You cannot set the current frame of waveform playback during the waveform recording or playback process.
        """
        assert frame >= 1
        self.open.write("FUNC:WREP:FCUR {0}".format(frame))

    def get_event_status_enable(self):
        """
        Query the enable register for the standard event status register set.
        """
        return int(self.open.query("*ESE?"))

    def set_event_status_enable(self, data=0):
        """
        Set the enable register for the standard event status register set.
        """
        assert data >= 0 and data <= 255
        self.open.write("*ESE {0}".format(data))

    def get_event_status(self):
        """
        Query and clear the event register for the standard event status
        register.
        """
        return int(self.open.query("*ESR?"))

    def get_identification(self):
        """
        Query the ID string of the instrument.
        """
        return self.open.query("*IDN?")

    def get_vendor(self):
        return self.get_identification().split(",")[0]

    def get_product(self):
        return self.get_identification().split(",")[1]

    def get_serial_number(self):
        return self.get_identification().split(",")[2]

    def get_firmware(self):
        return self.get_identification().split(",")[3]

    def is_busy(self):
        """
        The *OPC? command is used to query whether the current operation is
        finished. The *OPC command is used to set the Operation Complete bit
        (bit 0) in the standard event status register to 1 after the current
        operation is finished.
        """
        return not bool(int(self.open.query("*OPC?")))

    def get_service_request_enable(self):
        """
        Query the enable register for the status byte register set.
        """
        return int(self.open.query("*SRE?"))

    def set_service_request_enable(self, data=0):
        """
        Set the enable register for the status byte register set.
        """
        assert data >= 0 and data <= 255
        self.open.write("*SRE {0}".format(data))

    def get_status_byte(self):
        """
        Query the event regester for the status byte register. The
        value of the status byte register is set to 0 after this
        command is executed.
        """
        return int(self.open.query("*STB?"))

    def self_test_is_passing(self):
        """
        Perform a self-test and then returns the self-test results.
        """
        return not bool(int(self.open.query("*TST?")))

    def wait(self):
        """
        Wait for the operation to finish.
        """
        self.open.write("*WAI")

    def math_is_shown(self):
        """
        Query the math operation status.
        """
        return bool(int(self.open.query(":MATH:DISP?")))

    def show_math(self):
        """
        Enable the math operation function.
        """
        self.open.write(":MATH:DISP 1")

    def hide_math(self):
        """
        Disable the math operation function.
        """
        self.open.write(":MATH:DISP 0")

    def get_math_operator(self):
        """
        Query the operator of the math operation.
        """
        return self.open.query(":MATH:OPER?")

    def set_math_operator(self, operator="ADD"):
        """
        Set the operator of the math operation.
        """
        assert operator in [
            "ADD",
            "SUBT",
            "MULT",
            "DIV",
            "AND",
            "OR",
            "XOR",
            "NOT",
            "FFT",
            "INTG",
            "DIFF",
            "SQRT",
            "LOG",
            "LN",
            "EXP",
            "ABS",
        ]
        self.open.write(":MATH:OPER {0}".format(operator))

    def get_math_source(self, source=1):
        """
        Query the source of the math operation.
        """
        source = self._interpret_source(source)
        assert source in ["SOUR1", "SOUR2"]
        return self.open.query(":MATH:{0}?".format(source))

    def set_math_source(self, channel=1, source=1):
        """
        Set the source of the math operation.
        """
        source = self._interpret_source(source)
        assert source in ["SOUR1", "SOUR2"]
        channel = self._interpret_channel(channel)
        assert channel in ["CHAN1", "CHAN2", "CHAN3", "CHAN4"]
        self.open.write(":MATH:{0} {1}".format(source, channel))

    def get_math_scale(self):
        """
        Query the vertical scale of the operation result. The unit depends on
        the operator currently selected and the unit of the source.
        """
        return self._masked_float(self.open.query(":MATH:SCAL?"))

    def set_math_scale(self, scale=1):
        """
        Set the vertical scale of the operation result. The unit depends on the
        operator currently selected and the unit of the source.
        """
        possible_scales = [
            base * 10 ** exp for base in [1, 2, 5] for exp in range(-12, 13)
        ]
        scale = min(possible_scales, key=lambda x: abs(x - scale))
        self.open.write(":MATH:SCAL {0}".format(scale))

    def get_math_offset(self):
        """
        Query the vertical offset of the operation result. The unit depends on
        the operator currently selected and the unit of the source.
        """
        return self._masked_float(self.open.query(":MATH:OFFS?"))

    def set_math_offset(self, offset=0):
        """
        Set the vertical offset of the operation result. The unit depends on
        the operator currently selected and the unit of the source.
        """
        math_scale = self.get_math_scale()
        offset = round(offset * 50 / math_scale, 0) * math_scale / 50.0
        assert abs(offset) <= 1000 * math_scale
        self.open.write(":MATH:OFFS {0}".format(offset))

    def math_is_inverted(self):
        """
        Query the inverted display mode status of the operation result.
        """
        return bool(int(self.open.query(":MATH:INV?")))

    def invert_math(self):
        """
        Enable the inverted display mode of the operation result.
        """
        self.open.write(":MATH:INV 1")

    def uninvert_math(self):
        """
        Disable the inverted display mode of the operation result.
        """
        self.open.write(":MATH:INV 0")

    def reset_math(self):
        """
        Sending this command, the instrument adjusts the vertical scale of the
        operation result to the most proper value according to the current
        operator and the horiontal timebase of the source.
        """
        self.open.write(":MATH:RES")

    def get_fft_window(self):
        """
        Query the window function of the FFT operation.
        """
        return self.open.query(":MATH:FFT:WIND?")

    def set_fft_window(self, window="RECT"):
        """
        Set the window function of the FFT operation.
        """
        assert window in ["RECT", "BLAC", "HANN", "HAMM", "FLAT", "TRI"]
        self.open.write(":MATH:FFT:WIND {0}".format(window))

    def fft_split_is_enabled(self):
        """
        Query the status of the half display mode of the FFT operation.
        """
        return bool(int(self.open.query(":MATH:FFT:SPL?")))

    def enable_fft_split(self):
        """
        Enable the half-screen display mode of the FFT operation.
        """
        self.open.write(":MATH:FFT:SPL 1")

    def disable_fft_split(self):
        """
        Disable the half-screen display mode of the FFT operation.
        """
        self.open.write(":MATH:FFT:SPL 0")

    def get_fft_unit(self):
        """
        Query the vertical unit of the FFT operation result.
        """
        return self.open.query(":MATH:FFT:UNIT?")

    def set_fft_unit(self, unit="DB"):
        """
        Set the vertical unit of the FFT operation result.
        """
        assert unit in ["VRMS", "DB"]
        self.open.write(":MATH:FFT:UNIT {0}".format(unit))

    def get_fft_horizontal_scale(self):
        """
        Query the horizontal scale of the FFT operation result. The default unit
        is Hz.
        """
        return self._masked_float(self.open.query(":MATH:FFT:HSC?"))

    def set_fft_horizontal_scale(self, scale=5e6):
        """
        Set the horizontal scale of the FFT operation result. The default unit
        is Hz.
        """
        possible_scales = [x / self.get_timebase_scale() for x in [5, 2.5, 1, 0.5]]
        scale = min(possible_scales, key=lambda x: abs(x - scale))
        self.open.write(":MATH:FFT:HSC {0}".format(scale))

    def get_fft_center_frequency(self):
        """
        Query the center frequency of the FFT operation result, namely the
        frequency relative to the horizontal center of the screen. The default
        unit is Hz.
        """
        return self._masked_float(self.open.query(":MATH:FFT:HCEN?"))

    def set_fft_center_frequency(self, frequency=5e6):
        """
        Set the center frequency of the FFT operation result, namely the
        frequency relative to the horizontal center of the screen. The default
        unit is Hz.
        """
        if self.get_timebase_scale() <= 1 / frequency / 10:
            self.set_timebase_scale(1 / frequency / 10)
        horizontal_scales = [x / self.get_timebase_scale() for x in [5, 2.5, 1, 0.5]]
        for horizontal_scale in horizontal_scales:
            self.set_fft_horizontal_scale(horizontal_scale)
            frequency = (
                round(frequency * 50 / self.get_fft_horizontal_scale(), 0)
                * self.get_fft_horizontal_scale()
                / 50
            )
            if frequency != 0:
                break
        assert frequency <= 40 / self.get_timebase_scale()
        self.open.write(":MATH:FFT:HCEN {0}".format(frequency))

    def get_math_start(self):
        """
        Query the start point of the waveform math operation.
        """
        return int(self.open.query(":MATH:OPT:STAR?"))

    def set_math_start(self, position=0):
        """
        Set the start point of the waveform math operation.
        """
        position = int(round(position))
        assert position >= 0 and position <= 1199
        self.open.write(":MATH:OPT:STAR {0}".format(position))

    def get_math_end(self):
        """
        Query the end point of the waveform math operation.
        """
        return int(self.open.query(":MATH:OPT:END?"))

    def set_math_end(self, position=1199):
        """
        Set the end point of the waveform math operation.
        """
        position = int(round(position))
        assert position > self.get_math_start() and position <= 1199
        self.open.write(":MATH:OPT:END {0}".format(position))

    def get_math_sensitivity(self):
        """
        Query the sensitivity of the logic operation. The default unit is div
        (namely the current vertical scale).
        """
        return self._masked_float(self.open.query(":MATH:OPT:SENS?"))

    def set_math_sensitivity(self, sensitivity=0):
        """
        Set the sensitivity of the logic operation. The default unit is div
        (namely the current vertical scale).
        """
        assert self.get_math_operator() in ["AND", "OR", "XOR", "NOT"]
        sensitivity = round(sensitivity * 12.5, 0) / 12.5
        assert sensitivity >= 0 and sensitivity <= 0.96
        self.open.write(":MATH:OPT:SENS {0}".format(sensitivity))

    def get_differential_smoothing_width(self):
        """
        Query the smoothing window width of the differential operation (diff).
        """
        return int(self.open.query(":MATH:OPT:DIS?"))

    def set_differential_smoothing_width(self, distance=3):
        """
        Set the smoothing window width of the differential operation (diff).
        """
        assert distance >= 3 and distance <= 201
        self.open.write(":MATH:OPT:DIS {0}".format(distance))

    def math_autoscale_is_enabled(self):
        """
        Query the status of the auto scale setting.
        """
        return bool(int(self.open.query(":MATH:OPT:ASC?")))

    def enable_math_autoscale(self):
        """
        Enable the auto scale setting of the operation result.
        """
        self.open.write(":MATH:OPT:ASC 1")

    def disable_math_autoscale(self):
        """
        Disable the auto scale setting of the operation result
        """
        self.open.write(":MATH:OPT:ASC 0")

    def get_math_threshold(self, source=1):
        """
        Query the threshold level of a source in the logic operation. The
        default unit is V.
        """
        assert source in [1, 2]
        return self._masked_float(self.open.query(":MATH:OPT:THR{0}?".format(source)))

    def set_math_threshold(self, threshold, source=1):
        """
        Set the threshold level of a source in the logic operation. The default
        unit is V.
        """
        assert source in [1, 2]
        math_operator = self.get_math_operator()
        math_operator = math_operator.replace("\n","")
        assert math_operator in ["AND", "OR", "XOR", "NOT"]
        possible_thresholds = [i * self.get_math_scale() / 25 for i in range(-100, 101)]
        threshold = min(possible_thresholds, key=lambda x: abs(x - threshold))
        self.open.write(":MATH:OPT:THR{0} {1}".format(source, threshold))

    def mask_is_enabled(self):
        """
        Query the status of the pass/fail test.
        """
        return bool(int(self.open.query(":MASK:ENAB?")))

    def enable_mask(self):
        """
        Enable the pass/fail test.
        """
        self.open.write(":MASK:ENAB 1")

    def disable_mask(self):
        """
        Disable the pass/fail test.
        """
        self.open.write(":MASK:ENAB 0")

    def get_mask_source(self):
        """
        Query the source of the pass/fail test.
        """
        return self.open.query(":MASK:SOUR?")

    def set_mask_source(self, channel=1):
        """
        Set the source of the pass/fail test.
        """
        channel = self._interpret_channel(channel)
        self.open.write(":MASK:SOUR {0}".format(channel))

    def mask_is_running(self):
        """
        Query the status of the pass/fail test.
        """
        resp = self.open.query(":MASK:OPER?")
        resp = resp.replace("\n","")
        return  resp == "RUN"

    def run_mask(self):
        """
        Run or stop the pass/fail test.
        """
        self.open.write(":MASK:OPER RUN")

    def stop_mask(self):
        """
        Run or stop the pass/fail test.
        """
        self.open.write(":MASK:OPER STOP")

    def mask_stats_is_shown(self):
        """
        Query the status of the statistic information.
        """
        return bool(int(self.open.query(":MASK:MDIS?")))

    def show_mask_stats(self):
        """
        Enable the statistic information when the pass/fail test is enabled.
        """
        self.open.write(":MASK:MDIS 1")

    def hide_mask_stats(self):
        """
        Enable the statistic information when the pass/fail test is enabled.
        """
        self.open.write(":MASK:MDIS 0")

    def mask_stop_on_fail_is_enabled(self):
        """
        Query the status of the "Stop on Fail" function.
        """
        return bool(int(self.open.query(":MASK:SOO?")))

    def enable_mask_stop_on_fail(self):
        """
        Turn the "Stop on Fail" function on.
        """
        self.open.write(":MASK:SOO 1")

    def disable_mask_stop_on_fail(self):
        """
        Turn the "Stop on Fail" function off.
        """
        self.open.write(":MASK:SOO 0")

    def mask_beeper_is_enabled(self):
        """
        Query the status of the sound prompt.
        """
        return bool(int(self.open.query(":MASK:OUTP?")))

    def enable_mask_beeper(self):
        """
        Enable the sound prompt when the failed waveforms are detected.
        """
        self.open.write(":MASK:OUTP 1")

    def disable_mask_beeper(self):
        """
        Disable the sound prompt when the failed waveforms are detected.
        """
        self.open.write(":MASK:OUTP 0")

    def get_mask_adjustment(self, axis):
        """
        Query the adjustment parameter in the pass/fail test mask.
        """
        return self._masked_float(self.open.query(":MASK:{0}?".format(axis)))

    def set_mask_adjustment(self, axis, adjustment=0.24):
        """
        Set the adjustment parameter in the pass/fail test mask.
        """
        possible_adjustments = [round(0.02 * x, 2) for x in range(201)]
        adjustment = min(possible_adjustments, key=lambda x: abs(x - adjustment))
        self.open.write(":MASK:{0} {1}".format(axis, adjustment))

    def create_mask(self):
        """
        Create the pass/fail test mark using the current horizontal adjustment
        parameter and vertical adjustment parameter.
        """
        assert self.mask_is_enabled()
        assert not self.mask_is_running()
        self.open.write(":MASK:CRE")

    def get_passed_mask_frames(self):
        """
        Query the number of passed frames in the pass/fail test.
        """
        return int(self.open.query(":MASK:PASS?"))

    def get_failed_mask_frames(self):
        """
        Query the number of failed frames in the pass/fail test.
        """
        return int(self.open.query(":MASK:FAIL?"))

    def get_total_mask_frames(self):
        """
        Query the total number of frames in the pass/fail test.
        """
        return int(self.open.query(":MASK:TOT?"))

    def reset_mask(self):
        """
        Reset the numbers of the passed frames and the failed frames as well as
        the total number of frames in the pass/fail test to 0.
        """
        return self.open.write(":MASK:RES")

    def get_measurement_source(self):
        """
        Query the source of the current measurement parameter.
        """
        return self.open.query(":MEAS:SOUR?")

    def set_measurement_source(self, channel=1):
        """
        Set the source of the current measurement parameter.
        """
        channel = self._interpret_channel(channel)
        self.open.write(":MEAS:SOUR {0}".format(channel))

    def get_counter_source(self):
        """
        Query the source of the frequency counter.
        """
        return self.open.query(":MEAS:COUN:SOUR?")

    def set_counter_source(self, channel):
        """
        Set the source of the frequency counter.
        """
        channel = self._interpret_channel(channel)
        self.open.write(":MEAS:COUN:SOUR {0}".format(channel))

    def get_counter_value(self):
        """
        Query the measurement result of the frequency counter. The default unit
        is Hz.
        """
        return self._masked_float(self.open.query(":MEAS:COUN:VAL?"))

    def clear_measurement(self, item="ALL"):
        """
        Clear one or all of the last five measurement items enabled.
        """
        item = self._interpret_item(item)
        assert item in ["ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ALL"]
        self.open.write(":MEAS:CLE {0}".format(item))

    def recover_measurement(self, item="ALL"):
        """
        Recover the measurement item which has been cleared.
        """
        item = self._interpret_item(item)
        assert item in ["ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ALL"]
        self.open.write(":MEAS:REC {0}".format(item))

    def all_measurements_is_shown(self):
        """
        Query the status of the all measurement function.
        """
        return bool(int(self.open.query("MEAS:ADIS?")))

    def show_all_measurements_display(self):
        """
        Enable the all measurement function.
        """
        self.open.write(":MEAS:ADIS 1")

    def hide_all_measurements_display(self):
        """
        Disable the all measurement function.
        """
        self.open.write(":MEAS:ADIS 0")

    def get_all_measurements_display_source(self):
        """
        Query the source of the all measurement function.
        """
        return self.open.query(":MEAS:AMS?")

    def set_all_measurements_display_source(self, channel=1):
        """
        Set the source of the all measurement function.
        """
        channel = self._interpret_channel(channel)
        self.open.write(":MEAS:AMS {0}".format(channel))

    def get_measure_threshold_max(self):
        """
        Query the upper limit of the threshold in the time, delay, and phase
        measurements. The default unit is %.
        """
        return int(self.open.query(":MEAS:SET:MAX?"))

    def set_measure_threshold_max(self, percent=90):
        """
        Set the upper limit of the threshold in the time, delay, and phase
        measurements. The default unit is %.
        """
        self.open.write(":MEAS:SET:MAX {0}".format(percent))

    def get_measure_threshold_mid(self):
        """
        Get the middle point of the threshold in the time, delay, and phase
        measurements. The default unit is %.
        """
        return int(self.open.query(":MEAS:SET:MID?"))

    def set_measure_threshold_mid(self, percent=50):
        """
        Set the middle point of the threshold in the time, delay, and phase
        measurements. The default unit is %.
        """
        self.open.write(":MEAS:SET:MID {0}".format(percent))

    def get_measure_threshold_min(self):
        """
        Query the lower limit of the threshold in the time, delay, and phase
        measurements. The default unit is %.
        """
        return int(self.open.query(":MEAS:SET:MIN?"))

    def set_measure_threshold_min(self, percent=10):
        """
        Set the lower limit of the threshold in the time, delay, and phase
        measurements. The default unit is %.
        """
        self.open.write(":MEAS:SET:MIN {0}".format(percent))

    def get_measure_phase_source(self, source="A"):
        """
        Query the source of the Phase 1 -> 2 rising and Phase 1 -> 2 falling
        measurements.
        """
        return self.open.query("MEAS:SET:PS{0}?".format(source))

    def set_measure_phase_source(self, channel, source="A"):
        """
        Set the source of the Phase 1 -> 2 rising and Phase 1 -> 2 falling
        measurements.
        """
        assert source in ["A", "B"]
        channel = self._interpret_channel(channel)
        self.open.write(":MEAS:SET:PS{0} {1}".format(source, channel))

    def get_measure_delay_source(self, source="A"):
        """
        Query the source of the Delay 1 -> rising and Delay 1 -> falling
        measurements.
        """
        assert source in ["A", "B"]
        return self.open.query(":MEAS:SET:DS{0}?".format(source))

    def set_measure_delay_source(self, channel, source="A"):
        """
        Set the source of the Delay 1 -> rising and Delay 1 -> falling
        measurements.
        """
        assert source in ["A", "B"]
        channel = self._interpret_channel(channel)
        self.open.write(":MEAS:SET:DS{0} {1}".format(source, channel))

    def statistic_is_shown(self):
        """
        Query the status of the statistic function
        """
        return bool(int(self.open.query(":MEAS:STAT:DISP?")))

    def show_statistics(self):
        """
        Enable the statistic function.
        """
        self.open.write(":MEAS:STAT:DISP 1")

    def hide_statistics(self):
        """
        Disable the statistic function.
        """
        self.open.write(":MEAS:STAT:DISP 0")

    def get_statistic_mode(self):
        """
        Query the statistic mode.
        """
        return self.open.query(":MEAS:STAT:MODE?")

    def set_statistic_mode(self, mode="EXTR"):
        """
        Set the statistic mode.
        """
        assert mode in ["DIFF", "EXTR"]
        self.open.write(":MEAS:STAT:MODE {0}".format(mode))

    def reset_statistic(self):
        """
        Clear the history data and make statistic again.
        """
        self.open.write(":MEAS:STAT:RES")

    def get_measurement(self, item, type="CURR", channel=1):
        """
        Query the statistic result of any waveform parameter of the specified
        source.
        """
        channel = self._interpret_channel(channel)
        assert type in ["MAX", "MIN", "CURR", "AVER", "DEV"]
        assert item in [
            "VMAX",
            "VMIN",
            "VPP",
            "VTOP",
            "VBAS",
            "VAMP",
            "VAVG",
            "VRMS",
            "OVER",
            "PRES",
            "MAR",
            "MPAR",
            "PER",
            "FREQ",
            "RTIM",
            "FTIM",
            "PWID",
            "NWID",
            "PDUT",
            "NDUT",
            "RDEL",
            "FDEL",
            "RPH",
            "FPH",
            "TVMAX",
            "TVMIN",
            "PSLEW",
            "NSLEW",
            "VUP",
            "VMID",
            "VLOW",
            "VARI",
            "PVRMS"
        ]
        return self._masked_float(
            self.open.query(":MEAS:STAT:ITEM? {0},{1},{2}".format(type, item, channel))
        )

    def show_measurement(self, item, channel=1):
        """
        Set the statistic result of any waveform parameter of the specified
        source.
        """
        channel = self._interpret_channel(channel)
        assert item in [
            "VMAX",
            "VMIN",
            "VPP",
            "VTOP",
            "VBAS",
            "VAMP",
            "VAVG",
            "VRMS",
            "OVER",
            "PRES",
            "MAR",
            "MPAR",
            "PER",
            "FREQ",
            "RTIM",
            "FTIM",
            "PWID",
            "NWID",
            "PDUT",
            "NDUT",
            "RDEL",
            "FDEL",
            "RPH",
            "FPH",
            "TVMAX",
            "TVMIN",
            "PSLEW",
            "NSLEW",
            "VUP",
            "VMID",
            "VLOW",
            "VARI",
            "PVRMS"
        ]
        self.open.write(":MEAS:STAT:ITEM {0},{1}".format(item, channel))

    def reference_is_shown(self):
        """
        Query the status of the REF function.
        """
        return bool(int(self.open.query(":REF:DISP?")))

    def show_reference(self):
        """
        Enable the REF function.
        """
        self.open.write(":REF:DISP 1")

    def hide_reference(self):
        """
        Disable the REF function.
        """
        self.open.write(":REF:DISP 0")

    def reference_is_enabled(self, reference=1):
        """
        Query the status of the REF function.
        """
        reference = self._interpret_reference(reference)
        return bool(int(self.open.query(":{0}:ENAB?".format(reference))))

    def enable_reference(self, reference=1):
        """
        Enable the ref function.
        """
        reference = self._interpret_reference(reference)
        self.open.write(":{0}:ENAB 1".format(reference))

    def disable_reference(self, reference=1):
        """
        Enable the ref function.
        """
        reference = self._interpret_reference(reference)
        self.open.write(":{0}:ENAB 0".format(reference))

    def get_reference_source(self, reference=1):
        """
        Query the source of the specified reference channel.
        """
        reference = self._interpret_reference(reference)
        return self.open.query(":{0}:SOUR?".format(reference))

    def set_reference_source(self, channel, reference=1):
        """
        Set the source of the specified reference channel.
        """
        channel = self._interpret_channel(channel)
        reference = self._interpret_reference(reference)
        assert self.channel_is_shown(channel)
        self.open.write(":{0}:SOUR {1}".format(reference, channel))

    def get_reference_scale(self, reference=1):
        """
        Query the vertical scale of the specified reference channel. The unit is
        the same as the unit of the source.
        """
        reference = self._interpret_reference(reference)
        return self._masked_float(self.open.query(":{0}:VSC?".format(reference)))

    def set_reference_scale(self, scale, reference=1):
        """
        Set the vertical scale of the specified reference channel. The unit is
        the same as the unit of the source.
        """
        assert (
            scale >= self.get_probe_ratio() * 1e-3
            and scale <= self.get_probe_ratio() * 10
        )
        reference = self._interpret_reference(reference)
        self.open.write(":{0}:VSC {1}".format(reference, scale))

    def get_reference_offset(self, reference=1):
        """
        Query the vertical offset of the specified reference channel. The unit
        is the same as the unit of the source.
        """
        reference = self._interpret_reference(reference)
        return self._masked_float(self.open.query(":{0}:VOFF?".format(reference)))

    def set_reference_offset(self, offset, reference=1):
        """
        Set the vertical offset of the specified reference channel. The unit is
        the same as the unit of the source.
        """
        reference = self._interpret_reference(reference)
        self.open.write(":{0}:VOFF {1}".format(reference, offset))

    def reset_reference(self, reference=1):
        """
        Reset the vertical scale and vertical offset of the specified reference
        channel to their default values.
        """
        reference = self._interpret_reference(reference)
        self.open.write(":{0}:RES".format(reference))

    def manual_autoscale_is_enabled(self):
        """
        Query the status of the auto key.
        """
        return bool(int(self.open.query(":SYST:AUT?")))

    def enable_manual_autoscale(self):
        """
        Enable the auto key at the front panel.
        """
        self.open.write(":SYST:AUT 1")

    def disable_manual_autoscale(self):
        """
        Disable the auto key at the front panel.
        """
        self.open.write(":SYST:AUT 0")

    def beeper_is_enabled(self):
        """
        Query the status of the beeper.
        """
        return bool(int(self.open.query(":SYST:BEEP?")))

    def enable_beeper(self):
        """
        Enable the beeper.
        """
        self.open.write(":SYST:BEEP 1")

    def disable_beeper(self):
        """
        Disable the beeper.
        """
        self.open.write(":SYST:BEEP 0")

    def get_error_message(self):
        """
        Query and delete the last system error message.
        """
        return self.open.query(":SYST:ERR?")

    def get_gpib(self):
        """
        Query the GPIB address.
        """
        return int(self.open.query(":SYST:GPIB?"))

    def set_gpib(self, address):
        """
        Set the GPIB address.
        """
        assert address in range(1, 31)
        self.open.write(":SYST:GPIB {0}".format(address))

    def get_language(self):
        """
        Query the system language.
        """
        return self.open.query(":SYST:LANG?")

    def set_language(self, language="ENGL"):
        """
        Set the system language.
        """
        assert language in ["SCH", "ENGL"]
        self.open.write(":SYST:LANG {0}".format(language))

    def keyboard_is_locked(self):
        """
        Query the status of the keyboard lock function.
        """
        return bool(int(self.open.query(":SYST:LOCK?")))

    def lock_keyboard(self):
        """
        Enable the keyboard lock function.
        """
        self.open.write(":SYST:LOCK 1")

    def unlock_keyboard(self):
        """
        Disable the keyboard lock function.
        """
        self.open.write(":SYST:LOCK 0")

    def recall_is_enabled(self):
        """
        Query the system configuration to be recalled when the oscilloscope is
        powered on again after power-off.
        """
        return any(i in self.open.query(":SYST:PON?") for i in "LAT")

    def enable_recall(self):
        """
        Set the system configuration to be recalled when the oscilloscope is
        powered on again after power-off.
        """
        self.open.write(":SYST:PON LAT")

    def disable_recall(self):
        """
        Set the system configuration to be recalled when the oscilloscope is
        powered on again after power-off.
        """
        self.open.write(":SYST:PON DEF")

    def install_option(self, license):
        """
        Install the option.
        """
        self.open.write(":SYST:OPT:INST {0}".format(license))

    def uninstall_option(self):
        """
        Uninstall the options installed.
        """
        self.open.write(":SYST:OPT:UNINST")

    def timebase_delay_is_enabled(self):
        """
        Query the status of the delayed sweep.
        """
        return bool(int(self.open.query(":TIM:DEL:ENAB?")))

    def enable_timebase_delay(self):
        """
        Enable the delayed sweep.
        """
        self.open.write(":TIM:DEL:ENAB 1")

    def disable_timebase_delay(self):
        """
        Disable the delayed sweep.
        """
        self.open.write(":TIM:DEL:ENAB 0")

    def get_timebase_delay_offset(self):
        """
        Query the delayed timebase offset.
        """
        return self._masked_float(self.open.query(":TIM:DEL:OFFS?"))

    def set_timebase_delay_offset(self, offset=0):
        """
        Set the delayed timebase offset.
        """
        timebase_scale = self.get_timebase_scale()
        timebase_offset = self.get_timebase_offset()
        delay_scale = self.get_timebase_delay_scale()
        assert offset >= -6 * (timebase_scale - delay_scale) + timebase_offset
        assert offset <= 6 * (timebase_scale - delay_scale) + timebase_offset
        self.open.write(":TIM:DEL:OFFS {0}".format(offset))

    def get_timebase_delay_scale(self):
        """
        Query the delayed timebase scale. The default unit is s/div.
        """
        return self._masked_float(self.open.query(":TIM:DEL:SCAL?"))

    def set_timebase_delay_scale(self, scale=500e-9):
        """
        Set the delayed timebase scale. The default unit is s/div.
        """
        sample_rate = self.get_sample_rate()
        timebase_scale = self.get_timebase_scale()
        possible_scales = [
            round(j * 10 ** i, 9)
            for i in range(-9, 1)
            for j in [1, 2, 5]
            if j * 10 ** i >= 2 / sample_rate and j * 10 ** i <= timebase_scale
        ]
        min(possible_scales, key=lambda x: abs(x - scale))
        self.open.write(":TIM:DEL:SCAL {0}".format(scale))

    def get_timebase_offset(self):
        """
        Query the delayed timebase offset. The default unit is s.
        """
        return self._masked_float(self.open.query(":TIMebase:MAIN:OFFSet?"))

    def set_timebase_offset(self, offset=0):
        """
        Set the delayed timebase offset. The default unit is s.
        """
        assert not (("ROLL" in self.get_timebase_mode()) and self.is_running())
        assert not (
            ("YT" in self.get_timebase_mode())
            and self.get_timebase_scale() == 20e-3
            and not self.is_running()
        )
        self.open.write(":TIMebase:MAIN:OFFSet {0}".format(offset))

    def get_timebase_scale(self):
        """
        Query the delayed timebase scale. The default unit is s/div.
        """
        return self._masked_float(self.open.query(":TIMebase:MAIN:SCALe?"))

    def set_timebase_scale(self, scale=1e-6):
        """
        Set the delayed timebase scale. The default unit is s/div.
        """
        timebase_mode = self.get_timebase_mode()
        timebase_mode = timebase_mode.replace("\n","")
        if timebase_mode == "MAIN":
            possible_scales = [
                base * 10 ** exp
                for base in [1, 2, 5]
                for exp in range(-9, 1)
                if base * 10 ** exp >= 5e-9
            ]
        elif timebase_mode == "ROLL":
            possible_scales = [
                base * 10 ** exp
                for base in [1, 2, 5]
                for exp in range(-9, 1)
                if base * 10 ** exp >= 200e-3
            ]
        scale = min(possible_scales, key=lambda x: abs(x - scale))
        self.open.write(":TIMebase:MAIN:SCALe {0}".format(scale))

    def get_timebase_mode(self):
        """
        Query the mode of the horizontal timebase.
        """
        return self.open.query(":TIM:MODE?")

    def set_timebase_mode(self, mode="MAIN"):
        """
        Set the mode of the horizontal timebase.
        """
        assert mode in ["MAIN", "XY", "ROLL"]
        self.open.write(":TIM:MODE {0}".format(mode))

    def get_trigger_mode(self):
        """
        Query the trigger type.
        """
        return self.open.query(":TRIG:MODE?")

    def set_trigger_mode(self, mode="EDGE"):
        """
        Set the trigger type.
        """
        assert mode in [
            "PULS",
            "RUNT",
            "WIND",
            "NEDG",
            "SLOP",
            "VID",
            "PATT",
            "DEL",
            "TIM",
            "DUR",
            "SHOL",
            "RS232",
            "IIC",
            "SPI",
            "EDGE",
        ]
        self.open.write(":TRIG:MODE {0}".format(mode))

    def get_trigger_coupling(self):
        """
        Query the trigger coupling type.
        """
        return self.open.query(":TRIG:COUP?")

    def set_trigger_coupling(self, coupling="DC"):
        """
        Set the trigger coupling type.
        """
        assert coupling in ["AC", "DC", "LFR", "HFR"]
        self.open.write(":TRIG:COUP {0}".format(coupling))

    def get_trigger_status(self):
        """
        Query the current trigger status.
        """
        return self.open.query(":TRIGger:STATus?")
    
    def is_running(self):
        return any(i in self.get_trigger_status() for i in ["TD", "WAIT", "RUN", "AUTO"])

    def force_trigger(self):
        """
        Generate a trigger signal forcefully. This command is only applicable to
        the normal and single trigger modes (see the :TRIGger:SWEep command) and
        is equivalent to pressing the FORCE key at the front panel.
        """
        trigger_sweep = self.get_trigger_sweep()
        assert any(i in trigger_sweep for i in ["NORM","SING"])
        self.open.write(":TFORce")

    def get_trigger_sweep(self):
        """
        Query the trigger mode.
        """
        return self.open.query(":TRIG:SWE?")

    def set_trigger_sweep(self, mode="AUTO"):
        """
        Set the trigger mode.
        """
        assert mode in ["AUTO", "NORM", "SING"]
        self.open.write(":TRIG:SWE {0}".format(mode))

    def get_trigger_holdoff(self):
        """
        Query the trigger holdoff time. The default unit is s.
        """
        return self._masked_float(self.open.query(":TRIG:HOLD?"))

    def set_trigger_holdoff(self, time=16e-9):
        """
        Set the trigger holdoff time. The default unit is s.
        """
        self.open.write(":TRIG:HOLD {0}".format(time))

    def trigger_noise_reject_is_enabled(self):
        """
        Query the status of the noise rejection.
        """
        return bool(int(self.open.query(":TRIG:NREJ?")))

    def enable_trigger_noise_reject(self):
        """
        Enable the noise rejection.
        """
        self.open.write(":TRIG:NREJ 1")

    def disable_trigger_noise_reject(self):
        """
        Disable the noise rejection.
        """
        self.open.write(":TRIG:NREJ 0")

    def get_trigger_source(self):
        """
        Query the trigger source in edge trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        assert trigger_mode in ["EDGE", "PULS", "SLOP", "VID", "DURAT"]
        return self.open.query(":TRIG:{0}:SOUR?".format(trigger_mode))

    def set_trigger_source(self, channel=1):
        """
        Set the trigger source in edge trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        assert trigger_mode in ["EDGE", "PULS", "SLOP", "VID", "DURAT"]
        channel = self._interpret_channel(channel)
        self.open.write(":TRIG:{0}:SOUR {1}".format(trigger_mode, channel))

    def get_trigger_direction(self):
        """
        Query the edge type in edge trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        if trigger_mode in ["EDGE"]:
            return self.open.query(":TRIG:{0}:SLOP?".format(trigger_mode))
        elif trigger_mode in ["VID"]:
            return self.open.query(":TRIG:{0}:POL?".format(trigger_mode))
        else:
            raise ValueError

    def set_trigger_direction(self, direction="POS"):
        """
        Set the edge type in edge trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        if trigger_mode in ["EDGE"]:
            assert direction in ["POS", "NEG", "RFAL"]
            self.open.write(":TRIG:{0}:SLOP {1}".format(trigger_mode, direction))
        elif trigger_mode in ["VID"]:
            assert direction in ["POS", "NEG"]
            self.open.write(":TRIG:{0}:POL {1}".format(trigger_mode, direction))
        else:
            raise ValueError

    def get_trigger_level(self, source=None):
        """
        Query the trigger level. The unit is the same as the current amplitude
        unit.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        if trigger_mode in ["EDGE", "PULS", "VID"]:
            return self._masked_float(self.open.query(":TRIG:{0}:LEV?".format(trigger_mode)))
        elif trigger_mode in ["PATT"]:
            channel = self._interpret_channel(source)
            assert channel in ["CHAN1", "CHAN2", "CHAN3", "CHAN4"]
            return self._masked_float(
                self.open.query(":TRIG:{0}:LEV? {1}".format(trigger_mode, channel))
            )
        elif trigger_mode in ["SLOP"]:
            assert source in ["A", "B"]
            return self._masked_float(
                self.open.query(":TRIG:{0}:{1}LEV?".format(trigger_mode, source))
            )
        else:
            raise ValueError

    def set_trigger_level(self, level, source=None):
        """
        Set the trigger level in edge trigger. The unit is the same as the
        current amplitude unit.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        channel_scale = self.get_channel_scale()
        channel_offset = self.get_channel_offset()
        assert abs(level) <= 5 * channel_scale - channel_offset
        if trigger_mode in ["EDGE", "PULS", "VID"]:
            self.open.write(":TRIG:{0}:LEV {1}".format(trigger_mode, level))
        elif trigger_mode in ["PATT"]:
            channel = self._interpret_channel(source)
            assert channel in ["CHAN1", "CHAN2", "CHAN3", "CHAN4"]
            self.open.write(":TRIG:{0}:LEV {1},{2}".format(trigger_mode, channel, level))
        elif trigger_mode in ["SLOP"]:
            assert source in ["A", "B"]
            self.open.write(":TRIG:{0}:{1}LEV {2}".format(trigger_mode, source, level))
        else:
            raise ValueError

    def get_trigger_condition(self):
        """
        Query the trigger condition in pulse width trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        assert trigger_mode in ["PULS", "SLOP", "DURAT"]
        return self.open.query(":TRIG:{0}:WHEN?".format(trigger_mode))

    def set_trigger_condition(self, condition):
        """
        Set the trigger condition in pulse width trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        if trigger_mode in ["PULS", "SLOP"]:
            assert condition in ["PGR", "PLES", "NGR", "NLES", "PGL", "NGL"]
            self.open.write(":TRIG:{0}:WHEN {1}".format(trigger_mode, condition))
        elif trigger_mode in ["DURAT"]:
            assert condition in ["GRE", "LESS", "GLES"]
            self.open.write(":TRIG:{0}:WHEN {1}".format(trigger_mode, condition))
        else:
            raise ValueError

    def get_trigger_width(self):
        """
        Query the pulse width in pulse width trigger. The default unit is s.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        if trigger_mode in ["SLOP"]:
            return self._masked_float(self.open.query(":TRIG:{0}:TIME?".format(trigger_mode)))
        elif trigger_mode in ["PULS"]:
            return self._masked_float(self.open.query(":TRIG:{0}:WIDT?".format(trigger_mode)))
        else:
            raise ValueError

    def set_trigger_width(self, width):
        """
        Set the pulse width in pulse width trigger. The default unit is s.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        if trigger_mode in ["SLOP"]:
            self.open.write(":TRIG:{0}:TIME {1}".format(trigger_mode, width))
        elif trigger_mode in ["PULS"]:
            self.open.write(":TRIG:{0}:WIDT {1}".format(trigger_mode, width))
        else:
            raise ValueError

    def get_trigger_upper_width(self):
        """
        Query the upper pulse width in pulse width trigger. The default unit is
        s.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        if trigger_mode in ["SLOP", "DURAT"]:
            return self._masked_float(self.open.query(":TRIG:{0}:TUPP?".format(trigger_mode)))
        elif trigger_mode in ["PULS"]:
            return self._masked_float(self.open.query(":TRIG:{0}:UWID?".format(trigger_mode)))
        else:
            raise ValueError

    def set_trigger_upper_width(self, width=1e-6):
        """
        Set the upper pulse width in pulse width trigger. The default unit is s.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        if trigger_mode in ["SLOP", "DURAT"]:
            self.open.write(":TRIG:{0}:TUPP {1}".format(trigger_mode, width))
        elif trigger_mode in ["PULS"]:
            self.open.write(":TRIG:{0}:UWID {1}".format(trigger_mode, width))
        else:
            raise ValueError

    def get_trigger_lower_width(self):
        """
        Query the lower pulse width in pulse width trigger. The default unit is
        s.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        if trigger_mode in ["SLOP", "DURAT"]:
            return self._masked_float(self.open.query(":TRIG:{0}:TLOW?".format(trigger_mode)))
        elif trigger_mode in ["PULS"]:
            return self._masked_float(self.open.query(":TRIG:{0}:LWID?".format(trigger_mode)))
        else:
            raise ValueError

    def set_trigger_lower_width(self, width=992e-9):
        """
        Set the lower pulse width in pulse width trigger. The default unit is s.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        trigger_condition = self.get_trigger_condition()
        trigger_condition = trigger_condition.replace("\n","")
        assert trigger_condition in ["PGL", "NGL"]
        if trigger_mode in ["SLOP", "DURAT"]:
            self.open.write(":TRIG:{0}:TLOW {1}".format(trigger_mode, width))
        elif trigger_mode in ["PULS"]:
            self.open.write(":TRIG:{0}:LWID {1}".format(trigger_mode, width))
        else:
            raise ValueError

    def get_trigger_window(self):
        """
        Query the vertical window type in slope trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        assert trigger_mode in ["SLOP"]
        return self.open.query(":TRIG:{0}:WIND?".format(trigger_mode))

    def set_trigger_window(self, window="TA"):
        """
        Set the vertical window type in slope trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        assert trigger_mode in ["SLOP"]
        self.open.write(":TRIG:{0}:WIND {1}".format(trigger_mode, window))

    def get_trigger_sync_type(self):
        """
        Query the sync type in video trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        assert trigger_mode in ["VID"]
        return self.open.query(":TRIG:{0}:MODE?".format(trigger_mode))

    def set_trigger_sync_type(self, mode="ALIN"):
        """
        Set the sync type in video trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        assert trigger_mode in ["VID"]
        assert mode in ["ODDF", "EVEN", "LINE", "ALIN"]
        self.open.write(":TRIG:{0}:MODE {1}".format(trigger_mode, mode))

    def get_trigger_line(self):
        """
        Query the line number when the sync type in video trigger is LINE.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        assert trigger_mode in ["VID"]
        return int(self.open.query(":TRIG:{0}:LINE?".format(trigger_mode)))

    def set_trigger_line(self, line=1):
        """
        Set the line number when the sync type in video trigger is LINE.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        assert trigger_mode in ["VID"]
        assert line >= 1 and line <= 625
        self.open.write(":TRIG:{0}:LINE {1}".format(trigger_mode, line))

    def get_trigger_standard(self):
        """
        Query the video standard in video trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        assert trigger_mode in ["VID"]
        return self.open.query(":TRIG:{0}:STAN?".format(trigger_mode))

    def set_trigger_standard(self, standard="NTSC"):
        """
        Set the video standard in video trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        assert trigger_mode in ["VID"]
        assert standard in ["PALS", "NTSC", "480P", "576P"]
        self.open.write(":TRIG:{0}:STAN {1}".format(trigger_mode, standard))

    def get_trigger_pattern(self):
        """
        Query the pattern of each channel in pattern trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        if trigger_mode in ["PATT"]:
            return self.open.query(":TRIG:{0}:PATT?".format(trigger_mode))
        elif trigger_mode in ["DUR"]:
            return self.open.query("TRIG:{0}:TYP?")

    def set_trigger_pattern(self, pattern="X,X,X,X"):
        """
        Set the pattern of each channel in pattern trigger.
        """
        trigger_mode = self.get_trigger_mode()
        trigger_mode = trigger_mode.replace("\n","")
        assert pattern.count(",") == 3
        if trigger_mode in ["PATT"]:
            assert all([x in ["H", "L", "X", "R", "F"] for x in pattern.split(",")])
            self.open.write(":TRIG:{0}:PATT {1}".format(trigger_mode, pattern))
        elif trigger_mode in ["DUR"]:
            assert all([x in ["H", "L", "X"] for x in pattern.split(",")])
            self.open.write(":TRIG:{0}:TYP {1}".format(trigger_mode, pattern))

    def get_waveform_source(self):
        """
        Query the channel of which the waveform data will be read.
        """
        return self.open.query(":WAV:SOUR?")

    def set_waveform_source(self, channel=1):
        """
        Set the channel of which the waveform data will be read.
        """
        channel = self._interpret_channel(channel)
        self.open.write(":WAV:SOUR {0}".format(channel))

    def get_waveform_mode(self):
        """
        Query the reading mode used by :WAVeform:DATA?.
        """
        return self.open.query(":WAV:MODE?")

    def set_waveform_mode(self, mode="NORM"):
        """
        Set the reading mode used by :WAVeform:DATA?.
        """
        assert mode in ["NORM", "MAX", "RAW"]
        self.open.write("WAVeform:MODE {0}".format(mode))

    def get_waveform_format(self):
        """
        Query the return format of the waveform data.
        """
        return self.open.query(":WAV:FORM?")

    def set_waveform_format(self, format="BYTE"):
        """
        Set the return format of the waveform data.
        """
        assert format in ["WORD", "BYTE", "ASC"]
        self.open.write(":WAV:FORM {0}".format(format))

    def get_waveform_data(self):
        """
        Read the waveform data.
        """
        self.open.write_raw(":WAV:DATA?".encode("utf-8"))
        return self.open.read_raw()

    def get_waveform_increment(self, axis="X"):
        """
        Query the time difference between two neighboring points of the
        specified channel source.
        """
        assert axis in ["X", "Y"]
        return self._masked_float(self.open.query(":WAV:{0}INC?".format(axis)))

    def get_waveform_origin(self, axis="X"):
        """
        Query the time from the trigger point to the reference time of the
        specified channel source.
        """
        assert axis in ["X", "Y"]
        return self._masked_float(self.open.query(":WAV:{0}OR?".format(axis)))

    def get_waveform_reference(self, axis="X"):
        """
        Query the reference time of the specified channel source.
        """
        assert axis in ["X", "Y"]
        return self._masked_float(self.open.query(":WAV:{0}REF?".format(axis)))

    def get_waveform_start(self):
        """
        Query the start position of internal memory waveform reading.
        """
        return int(self.open.query(":WAV:STAR?"))

    def set_waveform_start(self, start=1):
        """
        Set the start position of internal memory waveform reading.
        """
        self.open.write(":WAV:STAR {0}".format(start))

    def get_waveform_stop(self):
        """
        Query the stop position of internal memory waveform reading.
        """
        return int(self.open.query(":WAV:STOP?"))

    def set_waveform_stop(self, stop=1200):
        """
        Set the stop position of internal memory waveform reading.
        """
        self.open.write(":WAV:STOP {0}".format(stop))

    def get_waveform_preamble(self):
        """
        Query and return all the waveform parameters.
        """
        values = self.open.query(":WAV:PRE?")
        values = values.split(",")
        assert len(values) == 10
        format, type, points, count, x_reference, y_origin, y_reference = (
            int(val) for val in values[:4] + values[6:7] + values[8:10]
        )
        x_increment, x_origin, y_increment = (
            float(val) for val in values[4:6] + values[7:8]
        )
        return (
            format,
            type,
            points,
            count,
            x_increment,
            x_origin,
            x_reference,
            y_increment,
            y_origin,
            y_reference,
        )

    def get_waveform_samples(self, channel=1):
        """
        Adapted from https://github.com/pklaus/ds1054z
        """
        channel = self._interpret_channel(channel)
        self.set_waveform_source(channel)
        self.set_waveform_format("BYTE")
        (
            format,
            type,
            points,
            count,
            x_increment,
            x_origin,
            x_reference,
            y_increment,
            y_origin,
            y_reference,
        ) = self.get_waveform_preamble()
        self.set_waveform_start(1)
        self.set_waveform_stop(1200)
        tmp_buff = self.get_waveform_data()
        n_header_bytes = int(chr(tmp_buff[1])) + 2
        n_data_bytes = int(tmp_buff[2:n_header_bytes].decode("ascii"))
        buff = tmp_buff[n_header_bytes : n_header_bytes + n_data_bytes]
        assert len(buff) == points
        samples = list(struct.unpack(str(len(buff)) + "B", buff))
        samples = [
            (sample - y_origin - y_reference) * y_increment for sample in samples
        ]
        timebase_scale = self.get_timebase_scale()
        timebase_offset = self.get_timebase_offset()
        x_axis = [
            i * timebase_scale / 10.0 + timebase_offset
            for i in range(-len(samples) // 2, len(samples) // 2)
        ]
        return x_axis, samples