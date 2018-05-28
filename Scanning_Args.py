from PIL import Image
import numpy as np
import math
import glob
import time
import os
import sys


# Takes an image and make it to an np array
def getdata_as_np_array(image_file_name):
    with Image.open(image_file_name) as img:
        im_rgb = img.convert('RGB')
        width, height = img.size
        shape = (height, width)
    
        picture_list_only_r_band = list(im_rgb.getdata(1))
        data = np.array(picture_list_only_r_band)
        data.shape = shape
    return data


def calc_z(arr, index, width, laserAngle):
    # Arr lista av lista, arr[0] = (y, x)
    # itr = iteration, 0-199
    # print(arr)
    #laserAngle = 45
    pxpmmhor = 8  # 15 cm avstånd
    pxpmmver = 8  # 15 cm avstånd
    fi = (float(index) * 1.8 * math.pi)/ 180 ###radianer???
    return_arr = []

    laserAngle = (laserAngle * math.pi) / 180
    
    # width avstånd från kant till mitten av bilden
    for i in range(0, len(arr)):
        b = float((arr[i][1] - (595)) / pxpmmhor)
            
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
            file.write("%f, %f, %f\n" % (i[0], i[1], i[2]))


def find_laser(np_array_data, height, width):
    """
    Starta på 0 leta i x led tills slutet om man hittar höga R spara det och starta
    en rad ner på samma x värde som ovan och gå ett steg höger sedan ett steg vänster

    hittar man ingen på rad 1 starta på 0 i rad 2

    np_array_data[y][x]
    y ner
    x åt höger
    """
    LASERVALUE = 230
    laser_width = 0
    x_on_row_abow = 0
    start_x = math.floor(width * 0.35)  # x = 0
    x = start_x
    nuber_of_objekt = 0
    picture_list = []
    didnt_find_x_to_right = False
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
    lastInList = len(filename_list) - 1
    number_list = filename_list[lastInList].split(".")
    return number_list[0]
    
 

def maps_to_scann_in(filePath):
    # C:\Programmering\ExJobb\Squarepyramid15x45
    # C:\Programmering\ExJobb\Pictures3
    # Hourglass15x45
    # c:\Programmering\ExJobb\Pictures\123.jpg
    # C:\\Users\\Tyysken\\Documents\\GitHub\\ExJobb\\Hourglass15x45/*.jpg
    # Object_Hourglass_15_45_/
    temp=[]
    for filename in glob.glob(filePath):
        #print(filename)
        temp.append(filename)
    return temp

    
def map_info(filePath):
    """
    tar namnet på mappen som bilderna ligger i och gör om
    dessa till: 
    namn på objekt
    avstånd
    vinkel
    """
    t = filePath.split('_')
    nameArr = [t[len(t)-4],int(t[len(t)-3]), int(t[len(t)-2])]
    return nameArr
    
    
def delete_old_scann_file(fileName):
    """
    Tar bort de gamla inskannade filerna innan den skannar 
    de nya värderna
    """
    if os.path.isfile(fileName):
        os.remove(fileName)
        print("\nOld %s file removed!" % fileName)
        time.sleep(1)
    else:
        print ("\n%s already deleted!" % fileName)
        time.sleep(1)


def printInfo(mapinfo, picture, totPicture, precentage, map_index, totMap):
    """
    Skriver ut info på skärmen 
    """
    print("-" * 50)
    print("Map\t\t\t: %s\n" % mapinfo[0])
    print("Angle\t\t\t: %i°\n" % mapinfo[2])
    print("Distance\t\t: %icm\n" % mapinfo[1])
    print("Picture\t\t\t: %i of %i\n" % (picture, totPicture))
    print("Total %% done\t\t: %0.2f%% \n" % precentage)
    print("Map\t\t\t: %i of %i " % ((map_index +1) , totMap))
    print("-" * 50)
    
def sys_argv():
    """
    Ser till att man skriver in de rätta argumenten vid start

    Försa arg:
    namnet på mappen där alla mappar med bilderna ligger


    Andra arg:
    L eller l för att köra från lasses dator med rätt sökväg till filerna
    J eller j för johans dator


    Tredje arg:
    antalet bilder som skall skannas in i varje map
    1-199
    A eller a skannar in samtliga 199 bilder i varje map
    """
    lasses_laptop_FilePath = "c:/Programmering/ExJobb/Object_*"
    johans_dator_FilePath = "C:\\Users\\Tyysken\\Documents\\GitHub\\ExJobb\\Object_Ball*"
    sysArg = sys.argv
    returnArr = []
    if len(sysArg) == 3:
        print("Correct number of arguments")
        if sysArg[1] == 'l' or sysArg[1] == 'L':
            print(lasses_laptop_FilePath)
            returnArr.append(lasses_laptop_FilePath)
        elif sysArg[1] == 'j' or sysArg[1] == 'J':
            print(johans_dator_FilePath)
            returnArr.append(johans_dator_FilePath)
        else:
            print("Error: Wrong second Argument")
        
        if sysArg[2] == 'a' or sysArg[2]=='A':
            print("199")
            returnArr.append(199)
        elif sysArg[2].isdigit() and int(sysArg[2])<200 and int(sysArg[2]) > 0:
            print("Scanning %s pictures" % sysArg[2])
            returnArr.append(sysArg[2])
        else: 
            print("\nError: No number or too high number!")
        
    else:
        print("Error, arguments isn't correct")
    return returnArr
    

def main():
    #system_arguments = sys_argv()
    system_arguments = []
    system_arguments.append("C:\\Users\\Tyysken\\Documents\\GitHub\\ExJobb\\Object_Ball*")
    system_arguments.append(199)
    if len(system_arguments) == 2:
        print("correct")
    else: 
        sys.exit()
    time.sleep(2)
    #maps_to_scann = maps_to_scann_in("c:/Programmering/ExJobb/Object_*")
    maps_to_scann = maps_to_scann_in(system_arguments[0])
    
    #print(maps_to_scann)
    picture_number = 0
    for y in maps_to_scann:
        #print(y)
    
   
        #path = maps_to_scann[y]
        path = y
        mapInfo = map_info(path)
    
        savePath = "Scanned\\" + mapInfo[0] + "_" + str(mapInfo[1]) + "x" + str(mapInfo[2]) +".asc"
        #print(savePath)
        
        delete_old_scann_file(savePath)

        #print(mapInfo)

    
    
        # main for loop for all pictures
        for i in range(1, int(system_arguments[1])+1):
            mainTime= time.time()
            picture_number +=1
            imagePath = path +"\\"+ str(i) + ".jpg"
            with Image.open(imagePath) as img:
                width, height = img.size
            data = getdata_as_np_array(imagePath)
            found_laser_at_position = find_laser(data, height, width)
            three_d_arr = calc_z(found_laser_at_position, i, width, mapInfo[2])
            savefile(savePath, three_d_arr)
            #os.system('cls')
            #procent = picture_number /(len(maps_to_scann)* int(system_arguments[1]))*100 #fixa denna så att den räknar ut totala %klar
            
            #printInfo(mapInfo, i, int(system_arguments[1]), procent, maps_to_scann.index(y), len(maps_to_scann))
    print("\n------------------3D scan done--------------------\n")
            

if __name__ == '__main__':
    print("\n\n-----Lasses och Johans Exjobb-----\n\n")
    time.sleep(1)
    main()
    
    
    
    
    #C:\\Users\\Tyysken\\Documents\\GitHub\\ExJobb\\Hourglass15x45/*.jpg'
