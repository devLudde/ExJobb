from PIL import Image
import numpy as np
import glob
import time

def build_array(data , index):

    multy_arr = [[0 for x in range(1920)] for y in range (1080)]
    filename = ("multyarr%d.txt" % index)
    file_for_array = open("multy_arr.txt", "w")
    file_for_array.write("Y  ,  X  ,  Value\n")
    ticks = time.time()
    for y in range (0, 1080):    
        for x in range (0, 1920):
            if (data[y][x] > 200):
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
    for filename in glob.glob('C:\Programmering\ExJobb\Picture/*.jpg'):
        im = Image.open(filename)
        image_list.append(filename)
   
    return image_list
    
def main():
    
    image_list = get_all_image_as_list()
    print(image_list)
    print(len(image_list))
    print(str(image_list[1]))
    np_array_data = getdata_as_np_array(image_list[1])
    arr = build_array(np_array_data,2)
    

if __name__ == '__main__':
    main()





