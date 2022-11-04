from flask import Flask, render_template, Response
import numpy
import cv2

    
pigeonWebApp = Flask(__name__)
pigeonWebVideoCam = cv2.VideoCapture("https://pigeon-webcam-drone-local.herokuapp.com")

@pigeonWebApp.route("/")
def pigeonWebCamFlask():
    return render_template("PigeonWebCam.html")

def pigeonWebCamGen():
    while True:
        pigeonSuccessful, pigeonWebFrame = pigeonWebVideoCam.read()
        cv2.imwrite("pigeonFrame.jpg", pigeonWebFrame)
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + open("pigeonFrame.jpg", "rb").read() + b'\r\n')

@pigeonWebApp.route("/pigeonVideoFeed")
def pigeonVideoFeed():
    return Response(pigeonWebCamGen(), mimetype="multipart/x-mixed-replace; boundary=frame")

def startPigeonWebCam():
    pigeonWebApp.run(host="10.0.0.147", use_reloader=False)
    
startPigeonWebCam()
