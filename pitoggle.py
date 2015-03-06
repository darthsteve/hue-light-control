from time import sleep
import RPi.GPIO as GPIO
import time
import random
from phue import Bridge

#GPIO pins to align with function!
togglePin = 4
brightPin = 8
dimPin = 7
colorPin = 3
bridgeIP = '192.168.88.250'

GPIO.setmode(GPIO.BCM)
GPIO.setup(togglePin, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(brightPin, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(dimPin, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(colorPin, GPIO.IN, GPIO.PUD_UP)

#use the IP of your bridge
b = Bridge(bridgeIP)

def toggle_lights():
    lights = b.get_light_objects()
    on = False
    for light in lights:
        if light.on:
            on = True
            light.brightness=254
            #break
    if on:
        b.set_group(0,'on',False)
    else:
        b.set_group(0,'on',True)

def bright_up():
    lights = b.get_light_objects()
    for light in lights:
        if light.on and light.brightness<254:
           light.brightness+=40

def dim_down():
    lights = b.get_light_objects()
    for light in lights:
        if light.on and light.brightness>0:
            light.brightness-=40

def change_color():
    lights = b.get_light_objects()
    color1 = random.random()
    color2 = random.random()
    for light in lights:
        light.xy = [color1, color2]

while True:
    toggle = GPIO.input(togglePin)
    bright = GPIO.input(brightPin)
    dim = GPIO.input(dimPin)
    colors = GPIO.input(colorPin)
    if toggle == 0:
        print("toggling power!")
        toggle_lights()
    if dim == 0:
        print('moar dim')
        dim_down()
    if bright == 0:
        bright_up()
        print('moar brights')
    if colors == 0:
        print('new color')
        change_color()
    #pause to allow the switch to bounce back
    time.sleep(0.05)



