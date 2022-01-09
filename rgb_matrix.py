
import time
import RPi.GPIO as GPIO

from modules.lcd import LCDModule
from modules.led_matrix import strip, set_strip_to_random_colour, dim_colours
from modules.button_matrix import ButtonMatrix


strip.begin()
lcd_screen = LCDModule()
lcd_screen.turn_on()
buttons = ButtonMatrix()

if __name__ == "__main__":

    try:
        while True:
            # get buttons press from SPI
            adc_key_value = buttons.GetAdcValue()
            key = buttons.GetKeyNum(adc_key_value)
            
            dim_colours(strip)
            if key != buttons.oldkey:
                time.sleep(0.05)
                adc_key_value = buttons.GetAdcValue()
                key = buttons.GetKeyNum(adc_key_value)
                if key != buttons.oldkey:
                    oldkey = key
                    if key >= 0:
                        # button pressed, activate it
                            set_block_to_random_colour(strip, key)
                            lcd_screen.write_lcd("pressed -> {0}".format(key))
            time.sleep(buttons.delay)

    except KeyboardInterrupt:
        lcd_screen.clear()
        lcd_screen.turn_off()
        GPIO.cleanup()
