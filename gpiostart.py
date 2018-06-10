import RPi.GPIO as GPIO
import time
from mpd import MPDClient
import alsaaudio

mixer = alsaaudio.Mixer(control = 'PCM')

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


def change_vol(vol_change):
        current_vol = mixer.getvolume()
        new_vol = current_vol[0] + vol_change
        if (new_vol < 0 or new_vol > 100): 
            return
        mixer.setvolume(new_vol)

def vol_down(channel):
    	print ("Volume naar beneden")
        change_vol(-4)

def vol_up(channel):
        global volume
	print ("Volume omhoog")
        change_vol(4)

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
