from picamera import PiCamera
from time import sleep
from PIL import Image
import io
import RPi.GPIO as GPIO
import numpy as np




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
         #TakePictures((pic_prefix))
         ProcessImage(pic_prefix)
         micro_step_16 = 0
      micro_step_16+=1
      GPIO.output(STEP, GPIO.HIGH)
      sleep(delay)
      GPIO.output(STEP, GPIO.LOW)
      sleep(delay)
   return

def TakePictures(prefix):
   camera.capture('/home/pi/ExJobb/LaserCamera/ExJobb/Pictures/image%s.jpg' % prefix)

def ProcessImage(prefix):
   camera.capture('/home/pi/ExJobb/LaserCamera/ExJobb/Pictures/image%s.jpg' % prefix)
   ar_data = openImage(prefix)

   ẃidth = len(ar_data[0])
   height = len(ar_data)

   pxpmmhor = 8
   pxpmmver = 8

   filename = 'coordinates.asc'

   if os.path.exists(filename):
      append_write = 'a'
   else:
      append_write = 'w'
   ascfile = open(filename, append_write)

   for y in range (0, height):
      if (y == 0):
         x = findLaser(ar_data, y, 0, width)
         preX = x
      else:
         if preX != None:
               if preX > 100:
                  x = findLaser(ar_data, y, preX-40, width)

                  if x == None:
                     x = findLaser(ar_data, y, 0, preX-39)
               else:
                  x = findLaser(ar_data, y, 0, width)
      if x != None:
         preX = x
         b = ((x + 1 - y * width) - width72) / pxpmmhor

         ro = (b / math.sin((45*math.pi)/180))

         ascfile.write(str(ro * math.cos(1.8 * prefix)) + "," +
                       str(ro * math.sin(1.8 * prefix)) + "," +
                       str(y / pxpmmver) + "\n")
   ascfile.close()
   return

   

def openImage(prefix):
   im = Image.open('/home/pi/ExJobb/LaserCamera/ExJobb/Pictures/image%s.jpg' % prefix)
   im_rgb = im.convert('RGB')

   picture_list = list(im.rgb.getdata(0))
   data = np.array(picture_list)

   width, height = im.size

   data.shape = (height, width)

   return data

def findLaser(ar_data, x, y, stop):
   while (x < stop):
      if (ar_data[y][x] > 25:
         return x
      x += 1
   return None
          
   

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
#   rotate_deg(45)
   stream = io.BytesIO()
   RotateAndCapture(3200,CW)
   GPIO.cleanup()
   


if __name__ == '__main__':
   main()

