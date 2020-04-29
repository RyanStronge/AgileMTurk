import csv
import requests
import json
import ast
from PIL import Image, ImageDraw
import numpy as np

results = []
with open("processing/csv/export.csv") as csvfile:
    next(csvfile)
    reader = csv.reader(csvfile)
    for row in reader:
        results.append(row)

    #results[x][0] is url
    #results[x][5] is points

    length = len(results)

    for x in range(length):
        fileName = "processing/fullimgs/image"+str(x)+".jpg"
        img_data = requests.get(results[x][0]).content
        with open(fileName, 'wb') as handler:
            handler.write(img_data)

        print(results[x][5])
        jsonData = results[x][5]
        jsonObj = json.loads(jsonData)
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
            newIm.save("processing/newimgs/image"+str(x)+".png")
        else:
            print("Not a polyline")
