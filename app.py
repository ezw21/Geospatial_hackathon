from flask import Flask, render_template, request
import cv2
from PIL import Image
import glob
import json
import time

global images

app = Flask(__name__)



def readImages(images_folder):
    global images
    filenames = glob.glob(images_folder + "/*.png" )
    images = []
    for i in range(0, len(filenames)):
        filename = filenames[i].split("\\")[-1]
        images.append((filename, cv2.imread(filenames[i])))
    return images


def loadReport(json_file):
    with open(json_file) as json_file:
        data = json.load(json_file)
        report = []
        for key in data.keys():
            report.append((key, data[key]))
        return report




@app.route('/')
def home():
    global images
    images = readImages("static")
    report = loadReport("json/e_set.txt")
    return render_template("index.html", images=images, report=report)


@app.route('/overlay_image', methods=["POST"])
def overlay_image():
    global images
    images = readImages("static")
    report = loadReport("json/e_set.txt")
    for filename, image in images:
        value = request.form.get(filename)
        print(value)
        if value:
            im1 = cv2.imread("static/" + filename)
            cv2.imwrite("static/result.jpg", im1)
            return render_template("index.html", result=True, images=images, report=report)
    return render_template("index.html", result=None, images=images, report=report)
    

@app.route('/t')
def superimpose_image(image):
    # im1 = Image.open("014.jpg")
    # im2 = Image.open("018.jpg")
    # im3 = Image.open("007.jpg")
    # newim = Image.blend(im1, im2, alpha=1)
    # newim.save("static/result.jpg")

    im1 = cv2.imread("drunk_duan.jpg")
    dst = cv2.addWeighted(im1, 0.5, image, 0.5, 0.5)
    cv2.imwrite("static/result.jpg", dst)


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

