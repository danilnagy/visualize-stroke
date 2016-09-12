import math
import numpy as np
import matplotlib.pyplot as plt

def plotLine(x0,y0,x1,y1,output):
    #plots line to numpy array using Bresenham's Line Algorithm
    #https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm

    if x0 > x1:
        x_max = int(x0)
        y_max = int(y0)
        x_min = int(x1)
        y_min = int(y1)
    else:
        x_max = int(x1)
        y_max = int(y1)
        x_min = int(x0)
        y_min = int(y0)

    dx = x_max - x_min
    dy = y_max - y_min

    if dx == 0:
        #exception for vertical lines
        for y in range(y_min,y_max):
            output[y,x_min] = 1
    else:
        error = -1.0
        d_error = abs( float(dy)/float(dx) )
        y = y_min
        for x in range(x_min,x_max):
            if y >= height or y < 0:
                continue
            elif x >= width or x < 0:
                continue
            output[y,x] = 1
            error += d_error
            while error >= 0.0:
                if(dy > 0):
                    y += 1
                else:
                    y-= 1
                error -= 1.0
                output[y,x] = 1



    return output

#dimensions of output image
width = 240
height = 240
commands = 200

#numpy array "canvas"
canvas = np.zeros((height,width))

#generate random command type (G00 = move / G01 = paint)
stroke = np.round( np.random.random_sample(commands))
#generate random position coordinates (relative positioning 0.0 to 1.0)
posx = np.random.random_sample(commands)
posy = np.random.random_sample(commands)




#draw commands sequentially
#commands assume starting point to be final point of last command
lastx = posx[0]
lasty = posy[0]
for i in range(1,len(posx)-1):
    nextx = posx[i]
    nexty = posy[i]

    print "G%02d X%.3f Y%.3f" %(stroke[i], nextx * width, nexty * height)

    #if command is G01 - draw line
    if( stroke[i] == 1):
        #print "drawing line from (%f, %f) to (%f,%f)" %(lastx*width, lasty*height, nextx*width, nexty*height)
        canvas = plotLine( lastx*width, lasty*height, nextx*width, nexty*height, canvas)
    lastx = nextx
    lasty = nexty

#display output
plt.axis('off')
plt.imshow(canvas,cmap='Greys',interpolation='bicubic')
plt.savefig('blkwht.png',bbox_inches='tight')


#plt.show()
