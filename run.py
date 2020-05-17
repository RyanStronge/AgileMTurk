from flask import Flask, render_template, redirect, url_for, request, Response, flash, send_file, Response, after_this_request, make_response
import requests
import csv
import json
import ast
from PIL import Image, ImageDraw
import numpy as np
import os
import cv2
import time


app = Flask(__name__)


@app.route("/via")
def index():
    return render_template("via_demo.html")


@app.route("/csv")
def getcsvdata():
    csvdata = request.args.get('csvdata')
    print("here")
    # returns
    # filename,file_size,file_attributes,region_count,region_id,region_shape_attributes,region_attributes,
    # https://api.jquery.com/jquery-wp-content/themes/jquery/content/donate.png,-1,"{}",1,0,"{""name"":""polyline"",""all_points_x"":[15,26,69,15],""all_points_y"":[14,64,18,15]}","{}"
    print(str(csvdata))
    print(type(csvdata))
    split = csvdata.split('\n')

    for i in range(len(split)):
        if(i > 0):
            now = time.strftime("%Y%m%d-%H%M%S")
            name = "img"+str(now)
            os.mkdir(name)
            file_name = "fullimgs/"+name+".jpg"

            print("\n"+split[1]+"\n")
            rowsplit = split[i].split(',')
            # rowsplit[0] is url
            # rowsplit[5] is points

            img_data = requests.get(split[i][0]).content
            with open(file_name, 'wb') as handler:
                handler.write(img_data)
            jsonData = split[i][5]
            jsonObj = json.loads(jsonData)
            print(jsonObj)
            name = jsonObj["name"]
            yPoints = jsonObj["all_points_y"]
            xPoints = jsonObj["all_points_x"]

            yList = eval(str(yPoints))
            xList = eval(str(xPoints))

            if name == "polyline":
                im = Image.open(file_name).convert("RGBA")
                imArray = np.asarray(im)
                polygon = [None] * len(yList)
                for z in range(len(yList)):
                    polygon[z] = (xList[z], yList[z])
                print(polygon)
                maskIm = Image.new(
                    'L', (imArray.shape[1], imArray.shape[0]), 0)
                ImageDraw.Draw(maskIm).polygon(polygon, outline=1, fill=1)
                mask = np.array(maskIm)
                newImArray = np.empty(imArray.shape, dtype='uint8')
                newImArray[:, :, :3] = imArray[:, :, :3]
                newImArray[:, :, 3] = mask*255
                newIm = Image.fromarray(newImArray, "RGBA")
                newIm.save("newimgs/"+name+".png")
        else:
            print("skipping header")
    print(split[1])
    return "OK"


if __name__ == "__main__":
    app.secret_key = 'w77pebv6'
    app.run(debug=True, host='0.0.0.0')
