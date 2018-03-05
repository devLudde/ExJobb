import picamera
import time

camera = picamera.PiCamera()
camera.vflip = True
camera.hflip = True

camera.start_preview()
time.sleep(5)
camera.capture('/home/pi/ExJobb/LaserCamera/ExJobb/Picture/LaserPic.jpg')
camera.stop_preview()

