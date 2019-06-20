import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
f=21
r=20
GPIO.setup(f, GPIO.IN)
GPIO.setup(r, GPIO.IN)
    
def f_e(f):
    print("tick_l")
	
def r_e(r):
    print("tick_r")
    
GPIO.add_event_detect(f, GPIO.FALLING, callback=f_e)
GPIO.add_event_detect(r, GPIO.FALLING, callback=r_e)

while(True):
	continue
