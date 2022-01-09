
import time
from adafruit_ht16k33 import segments

class Segment():
    def __init__(self, i2c):
        # Define LCD column and row size for 16x2 LCD.
        self.address = 0x70
        self.lcd_columns = 16
        self.lcd_rows = 2
        # Initialize the LCD using the pins
        self.display = segments.Seg7x4(i2c, address=self.address)