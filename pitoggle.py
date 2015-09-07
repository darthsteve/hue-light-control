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
lights = b.get_light_objects()

def toggle_lights():
    on = False
    for light in lights:
        if light.on:
            on = True
    if on:
        b.set_group(0,'on',False)
    else:
        b.set_group(0,'on',True)

def bright_up():
    time.sleep(0.3)
    bright = GPIO.input(brightPin)
    if bright == 0:
        for light in lights:
            light.brightness=254
    else:
        for light in lights:
            if light.on and light.brightness<254:
                light.brightness+=40

def dim_down():
    time.sleep(0.3)
    dim = GPIO.input(dimPin)
    if dim == 0:
        for light in lights:
            light.brightness=10
    else:
        for light in lights:
            if light.on and light.brightness<254:
                light.brightness+=40

def change_color():
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



