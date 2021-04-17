from flask import Flask, render_template
import cv2
from PIL import Image

import time


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/t')
def superimpose_image():
    # im1 = Image.open("014.jpg")
    # im2 = Image.open("018.jpg")
    # im3 = Image.open("007.jpg")
    # newim = Image.blend(im1, im2, alpha=1)
    # newim.save("static/result.jpg")

    im1 = cv2.imread("014.jpg")
    im2 = cv2.imread("018.jpg")
    im3 = cv2.imread("007.jpg")
    dst = cv2.addWeighted(im1, 0.5, im2, 0.5, 0.5)
    dstt = cv2.addWeighted(dst, 0.5, im3, 0.5, 0.5)
    cv2.imwrite("static/result.jpg", dstt)
    return render_template('event.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run(debug=True)

