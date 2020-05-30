import requests
import json
from PIL import Image, ImageDraw
import numpy as np
import os
#import cv2
import psycopg2
import time

conn = psycopg2.connect(dbname="ddcdvtofrshbnj", user="ntvhhmrhgzdmqh", password="70f5719386ca8d7a4464e7ba903ff81ddbe1fe1d444071cc5ce4e1ad28059870",
                        host="ec2-54-247-89-181.eu-west-1.compute.amazonaws.com", port="5432")
cur = conn.cursor()


def execute_command(command):
    try:
        cur.execute(command)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return cur.fetchall()


def getcsvdataprocess():
    print(os.getcwd())
    print(os.listdir())
    now = time.strftime("%Y%m%d-%H%M%S")
    timeName = "img"+str(now)
    os.mkdir("fullimgs/"+timeName)
    os.mkdir("newimgs/"+timeName)
    rows = execute_command("SELECT * FROM data")
    for row in rows:
        name = "img"+str(row[0])
        file_name = "fullimgs/"+timeName+"/"+ name +".jpg"
        # row[0] is id: int
        # row[1] is url: str
        # row[2] is points: json

        img_data = requests.get(str(row[1])).content
        print("url: "+str(row[1]))
        with open(file_name, 'wb') as handler:
            handler.write(img_data)
            jsonData = str(row[2])
            jsonObj = json.loads(jsonData)
            print(jsonObj)
            objName = jsonObj["name"]
            yPoints = jsonObj["all_points_y"]
            xPoints = jsonObj["all_points_x"]

            yList = eval(str(yPoints))
            xList = eval(str(xPoints))

            if objName == "polyline":
                im = Image.open(file_name).convert("RGBA")
                imArray = np.asarray(im)
                polygon = [None] * len(yList)
                for z in range(len(yList)):
                    polygon[z] = (xList[z], yList[z])
                maskIm = Image.new(
                    'L', (imArray.shape[1], imArray.shape[0]), 0)
                ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
                mask = np.array(maskIm)
                newImArray = np.empty(imArray.shape, dtype='uint8')
                newImArray[:, :, :3] = imArray[:, :, :3]
                newImArray[:, :, 3] = mask*255
                newIm = Image.fromarray(newImArray, "RGBA")
                newIm.save("newimgs/"+timeName+"/"+name + ".png")
"""                 im = cv2.imread("newimgs/"+name+"/" +
                                name+".png", cv2.IMREAD_UNCHANGED)
                
                y, x = im[:, :, 3].nonzero()
                minx = np.min(x)
                miny = np.min(y)
                maxx = np.max(x)
                maxy = np.max(y)

                cropImg = im[miny:maxy, minx:maxx]
                whiteCellsMask = np.logical_and(cropImg[:, :, 0] == 255, np.logical_and(
                    cropImg[:, :, 1] == 255, cropImg[:, :, 2] == 255))
                cropImg[whiteCellsMask, :] = [255, 255, 255, 0]

                cv2.imwrite("newimgs/"+name+"/" +
                            name + ".png", cropImg)
                cv2.waitKey(0) """


getcsvdataprocess()
