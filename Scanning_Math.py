from PIL import Image
import numpy as np
import math
import glob
import time


# Takes an image and make it to an np array
def getdata_as_np_array(image_file_name):
    with Image.open(image_file_name) as img:
        im_rgb = img.convert('RGB')
        width, height = img.size
        shape = (height, width)
    
        picture_list_only_r_band = list(im_rgb.getdata(0))
        data = np.array(picture_list_only_r_band)
        data.shape = shape
    return data
    
    
# Retunerar en lista med alla kompletta namn på bilderna i mappen Pictures
def get_all_image_as_list():
    image_list = []
    for filename in glob.glob('C:\Programmering\ExJobb\Pictures3/*.jpg'):
        image_list.append(filename)
    return image_list


def calc_z_string(arr, index, width):
    # Arr lista av lista, arr[0] = (y, x)
    # itr = iteration, 0-199
    # print(arr)
    laserAngle = 45
    pxpmmhor = 8  # 15 cm avstånd
    pxpmmver = 8  # 15 cm avstånd
    fi = float(index) * 1.8
    # width avstånd från kant till mitten av bilden
    for i in range(0, len(arr)):
        b = float((arr[i][1] - (width / 2)) / pxpmmhor)
        ro = float(b / math.sin(laserAngle))

        x = float(ro * math.cos(fi))
        y = float(ro * math.sin(fi))
        z = float(arr[i][0] / pxpmmver)
        s = ("%d, %d, %d\n" % (x, y, z))
        #file.write("%d, %d, %d\n" % (i[0], i[1], i[2]))
        return s
    # spara (x, y, z) till fil/array


def calc_z(arr, index, width):
    # Arr lista av lista, arr[0] = (y, x)
    # itr = iteration, 0-199
    # print(arr)
    laserAngle = 45
    pxpmmhor = 8  # 15 cm avstånd
    pxpmmver = 8  # 15 cm avstånd
    fi = float(index) * 1.8
    return_arr = []
    # width avstånd från kant till mitten av bilden
    for i in range(0, len(arr)):
        b = float((arr[i][1] - (width / 2)) / pxpmmhor)
        ro = float(b / math.sin(laserAngle))

        x = float(ro * math.cos(fi))
        y = float(ro * math.sin(fi))
        z = float(arr[i][0] / pxpmmver)
        t = [x, y, z]
        return_arr.append(t)
    return return_arr
    # spara (x, y, z) till fil/array


def savefile(filename, value):
    with open(filename, mode='at', encoding='utf-8') as file:  # mode='wt'
        for i in value:
            #file.write(value)
            file.write("%d, %d, %d\n" % (i[0], i[1], i[2]))


def find_laser(np_array_data, height, width):
    """
    Starta på 0 leta i x led tills slutet om man hittar höga R spara det och starta
    en rad ner på samma x värde som ovan och gå ett steg höger sedan ett steg vänster

    hittar man ingen på rad 1 starta på 0 i rad 2

    np_array_data[y][x]
    y ner
    x åt höger
    """
    LASERVALUE = 200
    laser_width = 0
    x_on_row_abow = 0
    start_x = math.floor(width * 0.35)  # x = 0
    x = start_x
    nuber_of_objekt = 0
    picture_list = []
    didnt_find_x_to_right = False
    ticks = time.time()
    for y in range(0, height):
        while x != width:
            # starta på ca 35% av width sedan gå åt höger
            # hittar man inget gå från vänster till 35%
            # hittar man inte laser där heller så sätter vi x = 35% igen
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
        if x_on_row_abow > (start_x * 0.9):
            x = int(x_on_row_abow * 0.9)
            x_on_row_abow = 0
        else:
            x = start_x
        # else:
        #    x = 0
        laser_width = 0
    print(nuber_of_objekt)
    ticks = time.time() - ticks
    print("new :", ticks)
    return picture_list


def get_file_number_as_index(filename):
    """
    IN:
    c:\Programmering\ExJobb\Pictures\123.jpg
    Takes an filepath

    OUT:
    returns number
    123
    """

    filename_list = filename.split("\\")
    number_list = filename_list[4].split(".")
    return number_list[0]


def main():
    image_list = get_all_image_as_list()
    for i in image_list:
        # i = complete file path for 1 picture
        with Image.open(i) as img:
            width, height = img.size
        index = get_file_number_as_index(i)
        data = getdata_as_np_array(i)
        found_laser_at_position = find_laser(data, height, width)
        print("Picture: %s" % index)
        three_d_arr = calc_z(found_laser_at_position, index, width)
        # name = ("threeDArrPicture%s.asc" % index)
        name = "scanned.asc"
        savefile(name, three_d_arr)


if __name__ == '__main__':
    main()

