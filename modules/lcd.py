import board
import time
import adafruit_character_lcd.character_lcd_i2c as character_lcd

i2c = board.I2C()  # uses board.SCL and board.SDA

class LCDModule():

    def __init__(self):
        # Define LCD column and row size for 16x2 LCD.
        self.address = 0x21
        self.lcd_columns = 16
        self.lcd_rows = 2
        # Initialize the LCD using the pins
        self.lcd = character_lcd.Character_LCD_I2C(i2c, self.lcd_columns, self.lcd_rows, self.address)
        
    def turn_off(self):
        # Turn backlight off
        #self.lcd.set_backlight(1)
        self.lcd.backlight = False

    def turn_on(self):
        # Turn backlight on
        #self.lcd.set_backlight(0)
        self.lcd.backlight = True

    def clear(self):
        # clear the LCD screen
        self.lcd.clear()

    def write_lcd(self,text):
        # turn on LCD
        self.turn_on()
        # wait 0.1 seconds
        time.sleep(0.05)
        # Print a two line message
        self.clear()
        #self.lcd.message(text)
        self.lcd.message = text
        # wait 3 seconds
#         time.sleep(3)
        # clear screen
#         self.clear()
        # wait 0.1 seconds
#         time.sleep(0.1)
        # turn off LCD
#         self.turn_off()

#         time.sleep(1)
        # clear screen
#         self.clear()
        # wait 0.1 seconds
        time.sleep(0.05)
        # turn off LCD
#         self.turn_off()