from PIL import Image
import numpy as np
import time

def openImage():
    im = Image.open('image10.jpg')
    im_rgb = im.convert('RGB')

    picture_list = list(im_rgb.getdata())
    data = np.array( picture_list )
    
    width, height = im.size
    data.shape = ( height, width, 3 )

    return data

def createImage(listX, name):
    im = Image.open('image10.jpg')
    im_rgb = im.convert('RGB')

    picture_list = list(im_rgb.getdata())
    data = np.array( picture_list )
    
    width, height = im.size
    f = open("brightest_list.txt", "w")
    
    for y in range(0, height):
        for x in range(0, width):
            if x == listX[y]:
                f.write("(%d, %d) %d\n" % (y, x, (data[(((width)*y)+x)][0])))
                data[(((width)*y)+x)][0] = 255
                data[(((width)*y)+x)][1] = 255
                data[(((width)*y)+x)][2] = 255
            else:
                data[(((width)*y)+x)][0] = 0
                data[(((width)*y)+x)][1] = 0
                data[(((width)*y)+x)][2] = 0
                
    data = tuple(map(tuple, data))
    im2 = Image.new(im.mode, im.size)
    im2.putdata(data)
    im2.save(name)
    f.close()
    
    return

def findLaser(ar_data, y, x, direction):
    while 0 < x < len(ar_data[0]):
        if ar_data[y][x][0] > 40:
            return x

        if direction == 1:
            x += 1
        else:
            x -= 1
        
    return None

def recursiveFunction(ar_data, y, x, direction):
    if 0 < x < len(ar_data[0]):
        if ar_data[y][x][0] > 40:
            return x

        if direction == 1:
            x = recursiveFunction(ar_data, y, x+1, direction) 
        else:
            x = recursiveFunction(ar_data, y, x-1, direction)
            
        return x
    else:
        return None

    
#####################################
#                                   #
#       Start of Main program       #
#                                   #
#####################################
def main():
    ticks = time.clock()
    
    #Collect Image and its size
    ar_data = openImage()
    width = len(ar_data[0])
    height = len(ar_data)

    ###################################
    #Using for loop through all pixels#
    ###################################
    list_brightestX = []
    for y in range(0, height):
        brightest_point = 0
        for x in range(0, width):
            current_point = ar_data[y][x][0] + ar_data[y][x][1] + ar_data[y][x][2]
            if current_point > brightest_point:
                brightest_point = current_point
                max_val_x = x
                
        list_brightestX.append(max_val_x)
    print(time.clock() - ticks)
    createImage(list_brightestX, 'forloop.jpg')
    
    #########################################
    #Using recursive function to find pixels#
    #########################################
    ticks = time.clock()
    list_findX = []
    for y in range(0, height):
        if y == 0:
            x = recursiveFunction(ar_data, y, int(width/2), 0)
            if x == None:
                x = recursiveFunction(ar_data, y, int(width/2), 1)

            if x != None:
                list_findX.append(x)
            else:
                list_findX.append(None)
        else:
            if x == None:
                x = recursiveFunction(ar_data, y, int(width/2), 0)
                if x == None:
                    x = recursiveFunction(ar_data, y, int(width/2), 1)

                if x != None:
                    list_findX.append(x)
                else:
                    list_findX.append(None)
            else:
                x = recursiveFunction(ar_data, y, x, 0)
                if x == None:
                    x = recursiveFunction(ar_data, y, int(width/2), 1)

                if x != None:
                    list_findX.append(x)
                else:
                    list_findX.append(None)

    print(time.clock() - ticks)   
    createImage(list_findX, 'recursive.jpg')        
    

    #########################################
    #Using while function to find pixels#
    #########################################
    ticks = time.clock()
    list_findX = []
    for y in range(0, height):
        if y == 0:
            x = findLaser(ar_data, y, int(width/2), 0)
            if x == None:
                x = findLaser(ar_data, y, int(width/2), 1)

            if x != None:
                list_findX.append(x)
            else:
                list_findX.append(None)
        else:
            if x == None:
                x = findLaser(ar_data, y, int(width/2), 0)
                if x == None:
                    x = findLaser(ar_data, y, int(width/2), 1)

                if x != None:
                    list_findX.append(x)
                else:
                    list_findX.append(None)
            else:
                x = findLaser(ar_data, y, x, 0)
                if x == None:
                    x = findLaser(ar_data, y, int(width/2), 1)

                if x != None:
                    list_findX.append(x)
                else:
                    list_findX.append(None)

    print(time.clock() - ticks)    
    createImage(list_findX, 'while.jpg')


if __name__ == '__main__':
    main()
