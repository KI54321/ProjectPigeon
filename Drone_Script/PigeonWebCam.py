from flask import Flask, render_template, Response
import numpy
import cv2

    
app = Flask(__name__)
pigeonWebVideoCam = cv2.VideoCapture(0)

@app.route("/")
def pigeonWebCamFlask():
    return render_template("PigeonWebCam.html")

def pigeonWebCamGen():
    while True:
        pigeonSuccessful, pigeonWebFrame = pigeonWebVideoCam.read()
        if pigeonSuccessful:
            cv2.imwrite("pigeonFrame.jpg", pigeonWebFrame)
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + open("pigeonFrame.jpg", "rb").read() + b'\r\n')

@app.route("/pigeonVideoFeed")
def pigeonVideoFeed():
    return Response(pigeonWebCamGen(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="10.0.0.147")

