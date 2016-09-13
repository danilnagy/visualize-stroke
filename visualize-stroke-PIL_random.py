import math
import numpy as np
from PIL import Image, ImageFilter

def drawCanvas(w, h, g_, x_, y_):

    if len(g_) != len(x_) or len(g_) != len(y_) or len(x_) != len(y_):
        print "ERROR: INPUT ARRAYS MUST BE EQUAL LENGTH"
        return
    #numpy array "canvas"
    canvas = np.zeros((h,w))
    #draw commands sequentially
    #commands assume starting point to be final point of last command
    lastx = x_[0]
    lasty = y_[0]
    for i in range(1,len(x_)-1):
        nextx = x_[i]
        nexty = y_[i]

        print "G%02d X%.3f Y%.3f" %(stroke[i], nextx * w, nexty * h)

        #if command is G01 - draw line
        if( g_[i] == 1):
            canvas = plotLine( lastx*w, lasty*h, nextx*w, nexty*h, canvas)
        lastx = nextx
        lasty = nexty
    return canvas

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

    w = output.shape[1]
    h = output.shape[0]

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
            if y >= h or y < 0:
                continue
            elif x >= w or x < 0:
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

def renderCanvas( fp, source, blur ):
    #generate image from data array
    img = Image.fromarray( abs(canvas-1)*255 )
    #convert image to RGB for filtering & exporting
    if img.mode != 'RGB':
        img = img.convert('RGB')

    #apply blurring
    img = img.filter(ImageFilter.GaussianBlur(radius=blur)).filter(ImageFilter.EDGE_ENHANCE_MORE)
    #save image to file
    img.save(fp)


###
#RANDOM INPUTS FOR DEMO PURPOSES
###
commands = 200
#generate random command type (G00 = move / G01 = paint)
stroke = np.round( np.random.random_sample(commands))
#generate random position coordinates (relative positioning 0.0 to 1.0)
posx = np.random.random_sample(commands)
posy = np.random.random_sample(commands)


#generate "canvas" from sequential series of commands
canvas = drawCanvas(240,240,stroke,posx,posy)
#render canvas with blurring to a file
renderCanvas("pil-out-blur0.png",canvas,0)
renderCanvas("pil-out-blur1.png",canvas,1)
renderCanvas("pil-out-blur2.png",canvas,2)
renderCanvas("pil-out-blur3.png",canvas,3)
renderCanvas("pil-out-blur4.png",canvas,4)
renderCanvas("pil-out-blur5.png",canvas,5)
