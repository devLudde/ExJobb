from PIL import Image
import numpy as np
import math
import glob
import time
import unittest


def build_array(data , index):

    multy_arr = [[0 for x in range(720)] for y in range(480)]
    filename = ("multyarr%d.txt" % index)
    file_for_array = open("multy_arr.txt", "w")
    file_for_array.write("Y  ,  X  ,  Value\n")
    ticks = time.time()
    for y in range(0, 480):
        for x in range(0, 720):
            if data[y][x] > 40:
                multy_arr[y][x] = data[y][x]
                file_for_array.write("%d, %d, %d\n" % (y, x, multy_arr[y][x]))
            
    ticks = time.time() - ticks
    print(ticks)
    file_for_array.write("Y  ,  X  ,  Value\n")
    file_for_array.close()
    return multy_arr

    
# Takes an image and make it to an np array
def getdata_as_np_array(image_file_name):
    im = Image.open(image_file_name)
    im_rgb = im.convert('RGB')
    width, height = im.size
    shape = (height, width)
    
    picture_list_only_r_band = list(im_rgb.getdata(0))
    data = np.array( picture_list_only_r_band )
    data.shape = shape
    return data
    
    
# Retunerar en lista med alla kompletta namn på bilderna i mappen Pictures
def get_all_image_as_list():
    image_list = []
    for filename in glob.glob('C:\Programmering\ExJobb\Pictures/*.jpg'):
        image_list.append(filename)
    return image_list
    

def calcZ(arr , itr):
    print(arr)


def saveArrToFile(filename, value, y, x):
    with open(filename, mode='wt', encoding='utf-8') as file:
        file.write("%d, %d, %d\n" % (y, x, value))


def find_laser(np_array_data, height, width):
    """
    Starta på 0 leta i x led tills slutet om man hittar höga R spara det och starta
    en rad ner på samma x värde som ovan och gå ett steg höger sedan ett steg vänster

    hittar man ingen på rad 1 starta på 0 i rad 2

    np_array_data[y][x]
    y ner
    x åt höger
    """
    LASERVALUE = 40
    laser_width = 0
    x_on_row_abow = 0
    x = 0
    nuber_of_objekt = 0
    picture_list = []
    t=0
    ticks = time.time()
    for y in range(0, height):
        while x != width:
            # om vi hittat lasern och har gått förbi den
            # så lägger vi till det mittersta värdet på x som värdet där vi har lasern
            if laser_width > 1 and np_array_data[y][x] < LASERVALUE:
                x -= (laser_width/2)
                x = math.floor(x)
                x_on_row_abow = x
                nuber_of_objekt += 1
                value_list = [y, x]
                picture_list.append(value_list)
                break
            if np_array_data[y][x] > LASERVALUE:
                # om vi hittat lasern räkna hur bred den är
                laser_width += 1
            x += 1
            # file_for_array.write("%d, %d, %d\n" % (y, x, np_array_data[y][x]))
        if x_on_row_abow > 30:
            x = int(x_on_row_abow * 0.9)
            x_on_row_abow = 0
        else:
            x = 0
        laser_width = 0
    print(nuber_of_objekt)
    ticks = time.time() - ticks
    print("new :", ticks)
    return picture_list
    

def main():
    image_list = get_all_image_as_list()
    for i in image_list:
        print(i)
        #print(str(image_list[0]))
    data = getdata_as_np_array(image_list[1])
    print(data)
    laser = find_laser(data, 480, 720)
    # calcZ(laser)


class FindLaserTest(unittest.TestCase):
    """Test find_laser function"""

    def test_function_run(self):
        data = [[50, 50, 50], [51, 51, 30]]
        print(data)
        find_laser(data, 2, 2)


if __name__ == '__main__':
    main()
    unittest.main()

