from PIL import Image
import numpy as np
import time
im = Image.open('image10.jpg')

#print(im.format, im.size, im.mode)

im_rgb = im.convert('RGB')
width, height = im.size
picture_list = list(im_rgb.getdata(0))
#r, g, b = rgb_im.getpixel((1, 1))

shape = ( height, width )
data = np.array( picture_list )

f = open("s1.txt", "w")
data.shape = shape
s1 = [[0 for x in range(1920)] for y in range (1080)]
#print(r, g, b)
ticks = time.time()
for y in range (0, 1080):
    
    for x in range (0, 1920):
        #r, g, b = rgb_im.getpixel((x, y))
        #print(data[y][x])
        if (data[y][x] > 200):
            
            s1[y][x] = data[y][x]
            #print(s1[y][x])
            f.write("%d, %d, %d\n" % (y, x, s1[y][x]))
            #s1.append(x)
            #print(x, y, r)
        
    #print(s1[int(len(s1)/2)])
ticks = time.time() - ticks
print(ticks)
f.close()