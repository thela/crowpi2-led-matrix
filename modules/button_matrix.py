
import time

import RPi.GPIO as GPIO
if not 'spi' in locals():
    import spidev
    # Open SPI bus
    spi = spidev.SpiDev()
    spi.open(0,1)
    spi.max_speed_hz=1000000


class ButtonMatrix():

    def __init__(self):

        self.calculated = ""

        GPIO.setmode(GPIO.BCM)

        # Define key channels
        self.key_channel = 4
        self.delay = 0.1

        self.adc_key_val = [30,90,160,230,280,330,400,470,530,590,650,720,780,840,890,960]
        self.key = -1
        self.oldkey = -1
        self.num_keys = 16

        self.indexes = {
            12:1,
            13:2,
            14:3,
            15:4,
            10:5,
            9:6,
            8:7,
            11:8,
            4:9,
            5:10,
            6:11,
            7:12,
            0:13,
            1:14,
            2:15,
            3:16
        }

    def ReadChannel(self,channel):
        # Function to read SPI data from MCP3008 chip
        # Channel must be an integer 0-7
        adc = spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data
    
    def GetAdcValue(self):
        adc_key_value = self.ReadChannel(self.key_channel)
        return adc_key_value

    def GetKeyNum(self,adc_key_value):
        for num in range(0,16):
            if adc_key_value < self.adc_key_val[num]:
                return num
        if adc_key_value >= self.num_keys:
            num = -1
            return num

    def activateButton(self, btnIndex):
        # get the index from SPI
        btnIndex = int(btnIndex)
        # correct the index to better format
        btnIndex = self.indexes[btnIndex]
        # run calculator function
        self.calculate(btnIndex)
        print("button %s pressed" % btnIndex)
        # prevent button presses too close together
        time.sleep(.3)
        return self.calculated

