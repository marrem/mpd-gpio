#!/usr/bin/python

import RPi.GPIO as GPIO
import time
# from mpd import MPDClient
# import alsaaudio
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                            format='(%(threadName)-10s) %(message)s',
                                                )

# mixer = alsaaudio.Mixer(control = 'PCM')
# 
# client = MPDClient()
# client.timeout = 10
# client.connect ('localhost', 6600)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)
GPIO.setup(5, GPIO.IN)
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(3, GPIO.FALLING, bouncetime=200)
GPIO.add_event_detect(5, GPIO.FALLING, bouncetime=200)
GPIO.add_event_detect(35, GPIO.FALLING, bouncetime=200)
GPIO.add_event_detect(37, GPIO.FALLING, bouncetime=200)

def omlaag(stopEvent):
    logging.debug('started')
    while True:
        print "volume omlaag"
        time.sleep(5)
        if stopEvent.isSet():
            logging.debug('Stop event received')
            return


logging.debug('Starting main loop')
while True:
    if GPIO.event_detected(3) :
        logging.debug('knop wordt ingedrukt')
        logging.debug('creating worker thread')
        stop = threading.Event()
        down = threading.Thread(name='omlaag', target=omlaag, args=(stop,))
        logging.debug('starting worker thread')
        down.start()
        GPIO.wait_for_edge(3, GPIO.RISING, bouncetime=200)
        stop.set()
        down.join()
        GPIO.remove_event_detect(3)
        GPIO.add_event_detect(3, GPIO.FALLING, bouncetime=200)
