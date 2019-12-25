from PIL import Image as image
from PIL import ImageDraw as draw
from PIL import ImageFont
import sys
import numpy as np
import math
import os

color_scale = []
size = 0
pix_array = 0

def create_color_scale():
    for i in range(256):
        color_scale.append([255 - i, i, 0])

    for i in range(256):
        color_scale.append([0, 255 - i, i])

# in mm
def find_dist(x, y):
    return math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)


def main():
    create_color_scale()

    img = image.open("thing.png")
    global pix_array
    pix_array = np.asarray(img)
    pix_array.setflags(write=1)

    point1 = (400, 350)
    point2 = (400, 400)
    point3 = (400, 450)

    points = [(400, 300), (400, 350), (400, 400), (400, 450), (400, 500)]

    global size
    size = len(pix_array)

    # clear array
    for i, row in enumerate(pix_array):
        for j, pix in enumerate(row):
            pix_array[i][j] = [0, 0, 0]

    # pretty colors
    for j in range(len(pix_array[0])):
        for i in range(len(color_scale)):
            pix_array[j][i%size] = color_scale[i]

    freq_const = 20
    fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)


    counter = 0
    for phase in range(-15, 15):
        for time in range(20):
            for i in range(size):
                for j in range(size):
                    superposition = 0
                    for p, point in enumerate(points):
                        superposition += math.sin(find_dist((i, j), point)/freq_const + (time + (p-len(points))*phase)/10)

                    intensity = int(((superposition)/len(points))**2 * 512)
                    color = color_scale[intensity]
                    pix_array[i][j] = color

            img = image.fromarray(pix_array, 'RGB')
            d = draw.Draw(img)
            d.text((10,10), str(phase), font=fnt, fill=(255,255,255,255))
            img.save("total/" + str(counter) + ".jpg")
            counter += 1

        img.save("phases/" + str(phase) + ".jpg")




if __name__ == '__main__':
    main()