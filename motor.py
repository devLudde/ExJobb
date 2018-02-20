from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO

camera = PiCamera()
camera.vflip = True

DIR = 20 #Direction Pin
STEP = 21 #Step Pin
CW = 1 #Clockwise Rotation
CCW = 0 #CounterClockWise Rotation
SPR = 200 #Steps/varv 360/200 = 1,8

GPIO.setmode(GPIO.BCM) #bradcome memory
GPIO.setup(DIR, GPIO.OUT)#Puts DIR (20) Pin to OUT
GPIO.setup(STEP, GPIO.OUT)#Puts STEP (21) Pin to OUT

step_count = SPR
delay = 0.005


def rotate(steps, diraction):
   #Rotate and diraction to rotate at
   GPIO.output(DIR, diraction) # clockwise CW or counterclockwise CCW
   for i in range(steps):
      sleep(2)
      camera.capture('/Picture/image%s.jpg' % i)
      GPIO.output(STEP, GPIO.HIGH)
      sleep(delay)
      GPIO.output(STEP, GPIO.LOW)
      sleep(delay)
   GPIO.cleanup()
   return

#rotate(SPR, CW)
#sleep(0.5)
#rotate(SPR, CCW)
camera.start_preview()
sleep(5)
rotate(3,CW)
camera.stop_preview()

GPIO.cleanup()
