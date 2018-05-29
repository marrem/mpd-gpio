import RPi.GPIO as GPIO
import time
from mpd import MPDClient

client = MPDClient()
client.timeout = 10
client.connect ('localhost', 6600)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)
GPIO.setup(5, GPIO.IN)
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(3, GPIO.FALLING, bouncetime=200)
GPIO.add_event_detect(5, GPIO.FALLING, bouncetime=200)
GPIO.add_event_detect(35, GPIO.FALLING, bouncetime=200)
GPIO.add_event_detect(37, GPIO.FALLING, bouncetime=200)

volume = 50

def vol_down(channel):
        global volume
	print ("Volume naar beneden")
        volume -= 10
        client.setvol(volume)
        print(volume)


def vol_up(channel):
        global volume
	print ("Volume omhoog")
        volume += 10
        client.setvol(volume)
        print(volume)

def item_down(channel):
        print ("Item naar beneden")

def item_up(channel):
        print ("Item omhoog")


GPIO.add_event_callback(3, vol_down)
GPIO.add_event_callback(5, vol_up)
GPIO.add_event_callback(35, item_down)
GPIO.add_event_callback(37, item_up)


while 1:
    try:
	time.sleep(10)
    except KeyboardInterrupt:
        print ('Exiting...')
        quit()
