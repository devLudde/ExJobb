from PIL import Image
import numpy as np
import glob
import time

def build_array(data , index):

    multy_arr = [[0 for x in range(720)] for y in range (480)]
    filename = ("multyarr%d.txt" % index)
    file_for_array = open("multy_arr.txt", "w")
    file_for_array.write("Y  ,  X  ,  Value\n")
    ticks = time.time()
    for y in range (0, 480):    
        for x in range (0, 720):
            if (data[y][x] > 40):
                multy_arr[y][x] = data[y][x]
                file_for_array.write("%d, %d, %d\n" % (y, x, multy_arr[y][x]))
            
    ticks = time.time() - ticks
    print(ticks)
    file_for_array.write("Y  ,  X  ,  Value\n")
    file_for_array.close()
    return multy_arr

    
#Takes an image and make it to an np array
def getdata_as_np_array(image_file_name):
    im = Image.open(image_file_name)
    im_rgb = im.convert('RGB')
    width, height = im.size
    shape = ( height, width )
    
    picture_list_only_r_band = list(im_rgb.getdata(0))
    data = np.array( picture_list_only_r_band )
    data.shape = shape
    return data
    
    
#lista med alla bilder i i mappen Pictures
def get_all_image_as_list():
    image_list = []
    for filename in glob.glob('C:\Programmering\ExJobb\Pictures/*.jpg'):
        im = Image.open(filename)
        image_list.append(filename)
   
    return image_list
    


def find_laser(np_array_data, height, width):
    """
    Starta på 0 leta i x led tills slutet om man hittar höga R spara det och starta
    en rad ner på samma x värde som ovan och gå ett steg höger sedan ett steg vänster

    hittar man ingen på rad 1 starta på 0 i rad 2
    
    np_array_data[y][x]
    y ner 
    x åt höger
    """    
    laser_width = 0
    x_on_row_abow = 0
    x=0
    nuber_of_objekt=0
    file_for_array = open("recursive_multy_arr.txt", "w")
    ticks = time.time()
    for y in range(0,height):
        #print("for: ",y)
        while(x!=width):
            if(np_array_data[y][x]>40):
                file_for_array.write("%d, %d, %d\n" % (y, x, np_array_data[y][x]))
                laser_width+=1
                x_on_row_abow=x
                #print("%d, %d, %d, %d" %(laser_width, y, x, np_array_data[y][x]))
                nuber_of_objekt+=1
                if(laser_width>4):
                    #print("end at: ",x)
                    break
            x+=1
            #file_for_array.write("%d, %d, %d\n" % (y, x, np_array_data[y][x]))
        if(x_on_row_abow>30):
            x=int(x_on_row_abow*0.9)
            x_on_row_abow=0
        else:
            x=0
        laser_width=0
        #print(x)
    file_for_array.close()
    print(nuber_of_objekt)
    ticks = time.time() - ticks
    print("new :", ticks)
    
    
    
def main():
    
    image_list = get_all_image_as_list()
    #print(image_list)
    #print(len(image_list))
    print(str(image_list[0]))
    
    
    np_array_data = getdata_as_np_array(image_list[0])
    arr = find_laser(np_array_data,480,719)
    #print(np_array_data[80])
    arr = build_array(np_array_data,2)
    

if __name__ == '__main__':
    main()





