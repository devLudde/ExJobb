from picamera import PiCamera

from time import sleep

camera = PiCamera()

camera.hflip=True
camera.vflip=True

#camera.rotation =180
camera.start_preview()
sleep(10)
camera.stop_preview()
