from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO



camera = PiCamera()
camera.vflip = True
camera.hflip = True

DIR = 26 #Direction Pin
STEP = 19 #Step Pin
CW = 1 #Clockwise Rotation
CCW = 0 #CounterClockWise Rotation
SPR = 200 #Steps/varv 360/200 = 1,8

GPIO.setmode(GPIO.BCM) #bradcome memory
GPIO.setup(DIR, GPIO.OUT)#Puts DIR (26) Pin to OUT
GPIO.setup(STEP, GPIO.OUT)#Puts STEP (19) Pin to OUT

step_count = SPR
delay = 0.005


def RotateAndCapture(steps, diraction):
   #Rotate and diraction to rotate at
   GPIO.output(DIR, diraction) # clockwise CW or counterclockwise CCW
   camera.start_preview()
   sleep(2)
   camera.stop_preview()
   for i in range(steps):
      sleep(0.2)
      TakePictures((i+1))
      GPIO.output(STEP, GPIO.HIGH)
      sleep(delay)
      GPIO.output(STEP, GPIO.LOW)
      sleep(delay)
   return

def TakePictures(prefix):
   camera.capture('/home/pi/ExJobb/LaserCamera/ExJobb/Picture/image%s.jpg' % prefix)




RotateAndCapture(200,CW)
GPIO.cleanup()

