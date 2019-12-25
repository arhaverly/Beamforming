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

# each pixel is 0.1mm
pix_dist = 1
wave_speed = 299792458

def create_color_scale():
    for i in range(256):
        color_scale.append([255 - i, i, 0])

    for i in range(256):
        color_scale.append([0, 255 - i, i])

# in mm
def find_dist(x, y):
    return math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2) * pix_dist


def get_points(file):
    '''
    read the places from the file of places to visit
    '''
    points = []
    with open(file) as f:
        line = f.readline()
        while line:
            x, y = line.split(" ")
            y = y[:-1]
            points.append((int(x), int(y)))
            line = f.readline()

    return points


def main():
    create_color_scale()

    img = image.open("thing.png")
    global pix_array
    pix_array = np.asarray(img)
    pix_array.setflags(write=1)

    points = get_points(sys.argv[1])

    global size
    size = len(pix_array)

    # clear array
    for i, row in enumerate(pix_array):
        for j, pix in enumerate(row):
            pix_array[i][j] = [0, 0, 0]

    # # pretty colors
    # for j in range(len(pix_array[0])):
    #     for i in range(len(color_scale)):
    #         pix_array[j][i%size] = color_scale[i]

    fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)

    wavelength = 80
    best = 0

    for time in range(20):
        time_inc = 0.05
        amp = 1
        for i in range(size):
            for j in range(size):
                superposition = 0
                for p, point in enumerate(points):
                    distance = find_dist((i, j), point)
                    if distance == 0:
                        continue

                    superposition += (amp*math.sin(2*math.pi*(distance - wave_speed*time*time_inc + 50*math.pi/180*p)/wavelength) / distance**2)
                    # if superposition > best:
                    #     best = superposition
                    #     print(best)

                intensity = int(((superposition)/len(points)) * 512)

                color = color_scale[intensity]
                pix_array[i][j] = color

        # for point in points:
        #     for k in range(20):
        #         for l in range(20):
        #             pix_array[point[0] - 10 + k][point[1] - 10 + l] = 0

        img = image.fromarray(pix_array, 'RGB')
        # img.save("amp.jpg")
        # img.show()
        img.save("images/" + str(time) + ".jpg")











    # counter = 0
    # for phase in range(-15, 15):
    #     for time in range(20):
    #         for i in range(size):
    #             for j in range(size):
    #                 superposition = 0
    #                 for p, point in enumerate(points):
    #                     superposition += math.sin(2*math.pi*(find_dist((i, j), point) - wave_speed*time)/wavelength)

    #                 intensity = int(((superposition)/len(points))**2 * 512)
    #                 color = color_scale[intensity]
    #                 pix_array[i][j] = color

    #         img = image.fromarray(pix_array, 'RGB')
    #         d = draw.Draw(img)
    #         d.text((10,10), str(phase), font=fnt, fill=(255,255,255,255))
    #         img.save("total/" + str(counter) + ".jpg")
    #         counter += 1

    #     img.save("phases/" + str(phase) + ".jpg")





if __name__ == '__main__':
    main()