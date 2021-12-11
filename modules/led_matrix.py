from rpi_ws281x import PixelStrip, Color
import random

# LED strip configuration:
LED_COUNT = 64        # Number of LED pixels.
LED_PIN = 12          # GPIO pin connected to the pixels (18 uses $
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800$
LED_DMA = 10          # DMA channel to use for generating signal ($
LED_BRIGHTNESS = 50  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN $
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
row_size_from = 4
row_size_to = 8

def dim_color_to_RGB(color, dim_coeff=.99):
        return [int(dim_coeff * (color >> 16 & 0xff)), int(dim_coeff * (color >> 8  & 0xff)), int(dim_coeff * (color    & 0xff))]

def dim_colours(strip):
    for pixel_i in range(64):
        old_colour = strip.getPixelColor(pixel_i)
        if old_colour:
            strip.setPixelColorRGB(
                pixel_i,
                *dim_color_to_RGB(old_colour)
            )
    strip.show()
    

def set_strip_to_random_colour(strip, key):
    #rand_col = int(155*random.random())int((key)/row_size_from)*row_size_to+ (key % row_size)*int(row_size_to/row_size_from)
    # ribaltamento destra - sinistra
    key = row_size_from - (key % row_size_from + 1) + int(key/row_size_from) * row_size_from
    # ribaltamento alto - basso
    key = 16 - key - 1
    pixel_corner = int((key)/row_size_from)*row_size_to*2 + \
        (key % row_size_from) *  int(row_size_to/row_size_from)
    pixel_is = [ pixel_corner, pixel_corner + 1, pixel_corner + row_size_to, pixel_corner + row_size_to +1
    ]
    
    colour = [int(255*random.random()), int(255*random.random()), int(255*random.random())]
    for pixel_i in pixel_is:
        strip.setPixelColorRGB(pixel_i, *colour)
        #strip.setPixelColor(pixel_i, colour)
    strip.show()
