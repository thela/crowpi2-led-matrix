
import time
import math
import random
import RPi.GPIO as GPIO

import board

import spidev
from modules.lcd import LCDModule
from modules.led_matrix import strip, set_block_to_random_colour, dim_colours, set_block_to_colour, Color
from modules.button_matrix import ButtonMatrix
#from modules.segment import Segment

shake_pin = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(shake_pin, GPIO.OUT)

i2c = board.I2C()  # uses board.SCL and board.SDA

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz=1000000

strip.begin()
dim_colours(strip)
lcd_screen = LCDModule(i2c=i2c)
lcd_screen.turn_on()
buttons = ButtonMatrix(spi)


class Moles:
    def new_mole(self):
        if (time.process_time() - self.time_last_mole) > self.delay_between_moles:
            self.time_last_mole = time.process_time()
            
            if self.indices_no_moles:
                random_pixel = random.sample(self.indices_no_moles, 1)[0]
                
                self.indices_no_moles.remove(random_pixel)
                set_block_to_random_colour(strip, random_pixel)
                #lcd_screen.write_lcd("a mole appears\n at {0}!!1!".format(random_pixel))
                #time.sleep(
                #    1/ (math.ceil(self.moles_wacked/10) if self.moles_wacked > 0 else 1)
                #)
            else:
                self.playing = False
                GPIO.output(shake_pin,GPIO.HIGH)
                time.sleep(.1)
                GPIO.output(shake_pin,GPIO.LOW)
                time.sleep(.1)
                GPIO.output(shake_pin,GPIO.HIGH)
                time.sleep(.1)
                GPIO.output(shake_pin,GPIO.LOW)
                time.sleep(.1)
                GPIO.output(shake_pin,GPIO.HIGH)
                time.sleep(.2)
                GPIO.output(shake_pin,GPIO.LOW)
                #lcd_screen.write_lcd("Screen full!")
            
                
    def manage_levels(self):
        if not self.moles_wacked % 10:
            self.delay_between_moles = 1 / math.ceil(self.moles_wacked/10)
            print(self.delay_between_moles)
    
    def wack(self, key):
        if key not in self.indices_no_moles:
            GPIO.output(shake_pin,GPIO.HIGH)
            set_block_to_colour(strip, key, Color(0, 0, 0))
            strip.show()
            self.moles_wacked += 1
            self.manage_levels()
            lcd_screen.write_lcd("you wacked {0}\n moles!!1!".format(self.moles_wacked))
            #time.sleep(.1)
            GPIO.output(shake_pin,GPIO.LOW)
            self.indices_no_moles.append(key)
            
            
    def __init__(self):
        self.playing = True
        self.internal_timer = 0
        self.delay_between_moles = .5
 5 0       self.time_last_mole = 0
        
        self.level = 1
        self.moles_wacked = 0
        
        self.indices_no_moles = list(range(16))


moles = Moles()

if __name__ == "__main__":
    try:
        while moles.playing:            
            adc_key_value = buttons.GetAdcValue()
            key = buttons.GetKeyNum(adc_key_value)
            if key != buttons.oldkey:
                moles.wack(key)
            moles.new_mole()
    except KeyboardInterrupt:
        lcd_screen.clear()
        lcd_screen.turn_off()
        GPIO.cleanup()
