from PIL import Image
import time
im = Image.open('Picture/image10.jpg')

#print(im.format, im.size, im.mode)

rgb_im = im.convert('RGB')

r, g, b = rgb_im.getpixel((1, 1))

#print(r, g, b)
ticks = time.time()
for y in range (0, 50):
    s1 = []
    for x in range (0, 1919):
        r, g, b = rgb_im.getpixel((x, y))
        if (r > 200):
            #print(x)
            s1.append(x)
            #print(x, y, r)
    #print(s1[int(len(s1)/2)])
ticks = time.time() - ticks
print(ticks)
