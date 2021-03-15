#!/usr/bin/python3
import spidev

SPI_SPEED = 1000000

SHAPE_ID = {
    'square': 0x2020,
    'triangle': 0x0002,
    'sine': 0x2000,
    'sleep': 0x0040
}
# Chip Clock Frequency
ClockFreq = 25000000

class AD9833(object):
    
    def __init__(self,bus,device):
        """Inits AD9833

        :param bus: Bus
        :type bus: 
        :param device: SPI bus
        :type device: 
        """
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000

    def set_shape(self, shape):
        """Sets shape of waveform\n
        Options : "sine","triangle","square","sleep"\n
        sleep puts the IC into sleep mode, setting any other waveform will wake the IC.

        :param shape: Shape
        :type shape: str
        """
        self.shape = shape if shape in SHAPE_ID else 'sine'

    def set_freq(self, freq):
        """ Sets freuqncy from 0 to 12500000 Hz

        :param Frequency: Frequency range from 0 to 12500000 Hz
        :type Frequency: int
        """
        self.freq = freq
    
    def reset(self):
        """ Resets IC
        """
        self.spi.xfer2([0x01,0x00])

    def send(self):
        """ Sends the serial data after setting shape and frequency
                
        """
        # Calculate frequency word to send
        pulse = self.freq if self.shape is not 'square' else self.freq * 2
        word = round((pulse*2**28)/ClockFreq)

        #print(hex(word))
        # split frequency word into two 14-bit parts as MSB and LSB.
        freq_msb = (word & 0xFFFC000) >> 14
        freq_lsb = (word & 0x3FFF)
        # bit-or freq register 0 select (DB15 = 0, DB14 = 1)
        freq_lsb |= 0x4000
        freq_msb |= 0x4000
        
        freq_lsb = freq_lsb.to_bytes(2,'big')
        freq_msb = freq_msb.to_bytes(2,'big')
        tx_freq = freq_lsb+freq_msb
        

        """ Construct the control register contents per existing local parameters
            then send the new control register word to the waveform generator.
        """
        control_reg = 0x2000  # default control register skeleton value (sine wave mode)
        #control_reg |= 0x0100  # reset bit
        #if self._pause : control_reg |= 0x0080  # disable master clock bit
        control_reg |= 0 << 11  # freq register select bit
        control_reg |= 0 << 10 # phase register select bit

        if self.shape == 'sine':
            control_reg |= SHAPE_ID[self.shape]  # sine mode
        if self.shape == 'triangle':
            control_reg |= SHAPE_ID[self.shape]  # triangle mode
        if self.shape == 'square':
            control_reg |= SHAPE_ID[self.shape]  # square mode
        if self.shape == 'pause':
            control_reg |= SHAPE_ID[self.shape]  # pause mode

        #print(hex(control_reg))
        tx_lsb = control_reg >> 8
        tx_msb = control_reg & 0xFF
    
        
        #1. Control register write with reset 0x2100
        control_reset = 0x2100
        control_reset = control_reset.to_bytes(2,'big')
        
        self.spi.xfer2(control_reset)
        #2. Write to frequency and phase registers, B28 = 1 (2x16 bits write)
        self.spi.xfer2(tx_freq)
        
        #3. Control register write, Set reset = 0, select control and phase register
        self.spi.xfer2([tx_lsb,tx_msb])
        

        #example successful write sequence
        #xfer = [byte for word in (0x2100, lsb, msb, SHAPE_ID[self.shape]) for byte in word.to_bytes(2, 'big')]
        #e.g. 0x21 0x0 0x69 0xf1 0x40 0x0 0x20 0x0
        #[33, 0, 105, 241, 64, 0, 32, 0]
        
           
       

        
        
        
