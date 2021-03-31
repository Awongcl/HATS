#!/usr/bin/python3
import time
from ad9833_driver import AD9833

# device and spi_ch
spi_ch = 0
wave = AD9833(0, spi_ch)

# Input waveform and frequency
def generate(shape = 'sine',freq = 1000):
    # Set frequency
    if shape == 'triangle':
      wave.set_shape('triangle')
    elif shape == 'square':
      wave.set_shape('square')
    elif shape == 'sleep':
      wave.set_shape('sleep')
    elif shape == 'sine':
      wave.set_shape('sine')
    else:
      return 'fail'

    if freq not in range(0,12500000):
      return 'fail'
    wave.set_freq(freq)
    wave.send()
    print_output()
    return 'success'

  # establish initial parameters
def sweep(shape='sine',begin_freq=20,end_freq=5000,inc_freq=10):
  # sine, triangle, or square waveform
    if shape == 'triangle':
      wave.set_shape('triangle')
    elif shape == 'square':
      wave.set_shape('square')
    elif shape == 'sleep':
      wave.set_shape('sleep')
    elif shape == 'sine':
      wave.set_shape('sine')
    else:
      return 'fail'
    
    while True:
        # sweep from begin_freq to end_freq in inc_freq steps
        for i in range(begin_freq, end_freq, inc_freq):
            wave.set_freq(i)
            wave.send()  # load the next frequency value
            time.sleep(0.010)

        time.sleep(1)  # wait a second then do it all over again
def reset():
    wave.reset()

def print_output():
    print('DAC output')
    print('Shape: ',wave.shape)
    print('Frequency: ',wave.freq)





