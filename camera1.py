import picamera
import time

camera = picamera.PiCamera()
camera.vflip = True

camera.start_preview()
time.sleep(5)
camera.capture('LaserPic.jpg')
camera.stop_preview()

