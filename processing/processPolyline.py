import csv
import requests
import json
import ast
from PIL import Image, ImageDraw
import numpy as np
import os
import cv2

print(os.listdir())
results = []
with open("csv/export.csv") as csvfile:
    next(csvfile)
    reader = csv.reader(csvfile)
    for row in reader:
        results.append(row)

    #results[x][0] is url
    #results[x][5] is points

    length = len(results)

    for x in range(length):
        fileName = "fullimgs/image"+str(x)+".jpg"
        img_data = requests.get(results[x][0]).content
        with open(fileName, 'wb') as handler:
            handler.write(img_data)

        print(results[x][5])
        jsonData = results[x][5]
        jsonObj = json.loads(jsonData)
        print(jsonObj)
        name = jsonObj["name"]
        yPoints = jsonObj["all_points_y"]
        xPoints = jsonObj["all_points_x"]

        yList = eval(str(yPoints))
        xList = eval(str(xPoints))

        if name == "polyline":
            im = Image.open(fileName).convert("RGBA")
            imArray = np.asarray(im)
            polygon = [None] * len(yList)
            for z in range(len(yList)):
                polygon[z] = (xList[z], yList[z])
            print(polygon)
            maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
            ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
            mask = np.array(maskIm)
            newImArray = np.empty(imArray.shape, dtype='uint8')
            newImArray[:, :, :3] = imArray[:, :, :3]
            newImArray[:, :, 3] = mask*255
            newIm = Image.fromarray(newImArray, "RGBA")
            newIm.save("newimgs/image"+str(x)+".png")

            # cropping
            """ im = cv2.imread("AgileMTurk/processing/newimgs/image" +
                            str(x)+".png", cv2.IMREAD_UNCHANGED)
            y, x = im[:, :, 3].nonzero()
            minx = np.min(x)
            miny = np.min(y)
            maxx = np.max(x)
            maxy = np.max(y)

            cropImg = im[miny:maxy, minx:maxx]
            whiteCellsMask = np.logical_and(cropImg[:, :, 0] == 255, np.logical_and(
                cropImg[:, :, 1] == 255, cropImg[:, :, 2] == 255))
            cropImg[whiteCellsMask, :] = [255, 255, 255, 0]
            cv2.imwrite("AgileMTurk/processing/newimgs/image" +
                        str(x)+".png", cropImg)
            cv2.waitKey(0) """
        else:
            print("Not a polyline")
