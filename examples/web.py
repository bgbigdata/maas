# coding: utf-8
import os
import glob
import json
import re
from bottle import route, run, HTTPResponse, static_file, request, template
from datetime import datetime
import unicodedata
import nfc
import binascii
import time
import sys
from threading import Thread, Timer
import RPi.GPIO as GPIO
from time import sleep
from cli import CommandLineInterface

import nfc
import nfc.clf
import nfc.ndef

from sense_hat import SenseHat

sense = SenseHat()
R = [255, 0, 0]
G = [0, 255, 0]
O = [0, 0, 0]

green_check = [
O, O, O, O, O, O, O, G,
O, O, O, O, O, O, G, G,
O, O, O, O, O, G, G, O,
G, O, O, O, G, G, O, O,
G, G, O, G, G, O, O, O,
O, G, G, G, O, O, O, O,
O, O, G, O, O, O, O, O,
O, O, O, O, O, O, O, O
]
red_cross = [
R, O, O, O, O, O, O, R,
R, R, O, O, O, O, R, R,
O, R, R, O, O, R, R, O,
O, O, R, R, R, R, O, O,
O, O, O, R, R, O, O, O,
O, O, R, R, R, R, O, O,
O, R, R, O, O, R, R, O,
R, R, O, O, O, O, R, R
]
heart = [
O, R, O, O, O, O, R, O,
R, R, R, O, O, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
R, R, R, R, R, R, R, R,
O, R, R, R, R, R, R, O,
O, O, R, R, R, R, O, O,
O, O, O, R, R, O, O, O
]

hostname = "0.0.0.0"
port = 80

@route("/unlock")
def unlock():
    sense.set_pixels(green_check)

@route("/lock")
def lock():
    sense.set_pixels(red_cross)
    
@route("/heart")
def unlock():
    sense.set_pixels(heart)

'''
@route("/blink")
def blink():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

    while True:
        GPIO.output(8, GPIO.HIGH)
        sleep(1)
        GPIO.output(8, GPIO.LOW)
        sleep(1)
'''
run(host='localhost', port=80)
#run(host=hostname, port=int(os.environ.get("PORT", port)))