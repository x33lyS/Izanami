import time
import board
import neopixel
import json

import config
import profiles


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 150

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)


curprofile = profiles.Profile(pixels)

while True:
    try:
        f = open('curprof.json')
        myresult = json.load(f)

  
        if curprofile.name!=myresult["profile"]:
            curprofile = profiles.Factory(myresult['profile'])(pixels)
            print(curprofile)
    except:
        print('error retrieving profile')
    
    curprofile.display()
