#!/usr/bin/python3

from ad9833 import AD9833

# device and spi_ch
spi_ch = 0
wave = AD9833(0, spi_ch)

# Input waveform and frequency
def generate(shape = 'sine',freq = 1000):

    if shape == 'triangle':
      wave.set_shape('triangle')
    elif shape == 'square':
      wave.set_shape('square')
    elif shape == 'pause':
      wave.set_shape('pause')
    else:
      wave.set_shape('sine')

    wave.set_freq(freq)

    wave.send()
    
def print_output():
    print('DAC output')
    print('Shape: ',wave.shape)
    print('Frequency: ',wave.freq)
    

generate()
