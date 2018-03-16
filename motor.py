from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO



camera = PiCamera()
camera.vflip = True
camera.hflip = True

DIR = 20 #Direction Pin
STEP = 21 #Step Pin
CW = 1 #Clockwise Rotation
CCW = 0 #CounterClockWise Rotation
SPR = 200 #Steps/varv 360/200 = 1,8

GPIO.setmode(GPIO.BCM) #bradcome memory
GPIO.setup(DIR, GPIO.OUT)#Puts DIR (20) Pin to OUT
GPIO.setup(STEP, GPIO.OUT)#Puts STEP (21) Pin to OUT

step_count = SPR
delay = 0.0003


def RotateAndCapture(steps, diraction):
   #Rotate and diraction to rotate at
   GPIO.output(DIR, diraction) # clockwise CW or counterclockwise CCW
   camera.start_preview()
   sleep(2)
   camera.stop_preview()
   micro_step_16=0
   pic_prefix = 0
   for i in range(steps):
#      sleep(0.2)
#      TakePictures((i+1))
      if(micro_step_16>=16):
         pic_prefix +=1
         TakePictures((pic_prefix))
         micro_step_16 = 0
      micro_step_16+=1
      GPIO.output(STEP, GPIO.HIGH)
      sleep(delay)
      GPIO.output(STEP, GPIO.LOW)
      sleep(delay)
   return

def TakePictures(prefix):
   camera.capture('/home/pi/ExJobb/LaserCamera/ExJobb/Picture/image%s.jpg' % prefix)

def set_up(steps):
   GPIO.output(DIR,CCW)
   for i in range(int(steps)):
      GPIO.output(STEP, GPIO.HIGH)
      sleep(0.01)
      GPIO.output(STEP, GPIO.LOW)
      sleep(0.01)
   return

def rotate_deg(deg):
   one_lap = 3200
   microstep = (one_lap)/(360/deg)
   set_up(microstep)

def main():
   rotate_deg(45)
   RotateAndCapture(3200,cw)
   GPIO.cleanup()
   


if __name__ == '__main__':
   main()

