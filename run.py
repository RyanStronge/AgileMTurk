from flask import Flask, render_template, redirect, url_for, request, Response, flash, send_file, Response, after_this_request, make_response
import requests
import csv
import json
import ast
from PIL import Image, ImageDraw
import numpy as np
import os
import cv2
from datetime import datetime


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
    # split[i][0] is url
    # split[i][5] is points

    for i in range(len(split)):
        if(i > 0):
            now = datetime.now()
            name = "img"+now
            os.mkdir(name)
            fileName = "fullimgs/image"+str(i)+".jpg"
            img_data = requests.get(split[i][0]).content
            with open(fileName, 'wb') as handler:
                handler.write(img_data)
        else:
            print("skipping header")

    print(split[1])
    return "OK"


if __name__ == "__main__":
    app.secret_key = 'w77pebv6'
    app.run(debug=True, host='0.0.0.0')
