from flask import Flask, render_template, redirect, url_for, request, Response, flash, send_file, Response, after_this_request, make_response
import requests

app = Flask(__name__)


@app.route("/via")
def index():
    imageUrl = request.args.get('image')
    print(imageUrl)
    return render_template("via_demo.html")


if __name__ == "__main__":
    app.secret_key = 'w77pebv6'
    app.run(debug=True, host='0.0.0.0')
