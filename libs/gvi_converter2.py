import os
import cv2
import sys
import glob
import numpy as np

def convert_to_gvi(input_folder):
    w = 1
    r0 = 30
    g0 = 50
    b0 = 0

    # Saves local dir
    owd = os.getcwd()
    print(owd)

    # Iterates over files Found
    for file in glob.glob("{}/**.*".format(input_folder)):
        print("Processing {}...".format(file))
        img = cv2.imread(file)

        gvi_output = np.empty([img.shape[0], img.shape[1]])
        vvi_output = np.empty([img.shape[0], img.shape[1]])

        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                r = img[x][y][0]
                g = img[x][y][1]
                b = img[x][y][2]
                # GVI calc here
                #gvi_output[x][y] = (2*g-r-b)/(2*g+r+b)
                # VVI calc
                vvi_output[x][y] = ( (1-abs((r-r0)/(r+r0))) * (1-abs((g-g0)/(g+g0))) * (1-abs((r-r0)/(r+r0))))**1/w

        output_filename = "{}/out/{}".format(input_folder, file.split("/").pop())
        vvi_output += vvi_output.min()
        vvi_output *= (255.0/vvi_output.max())

        cv2.imwrite(output_filename, (vvi_output*512))

print(sys.argv[1])
convert_to_gvi(sys.argv[1])

def plotvvi(img, r0, g0, b0, w):
    print("Processing {}...".format(img))
    img = cv2.imread(img)
    vvi_output = np.empty([img.shape[0], img.shape[1]])
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            r = img[x][y][0] +1
            g = img[x][y][1] +1
            b = img[x][y][2] +1
            vvi_output[x][y] = ( (1-abs((r-r0)/(r+r0))) * (1-abs((g-g0)/(g+g0))) * (1-abs((r-r0)/(r+r0))))**1/w
    cv2.imshow('plot', vvi_output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
