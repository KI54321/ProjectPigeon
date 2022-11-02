from flask import Flask, render_template, Response
import numpy
import cv2

class PigeonWebCam:
    
    pigeonWebApp = Flask(__name__)
    pigeonWebVideoCam = cv2.VideoCapture(0)
    
    @app.route("/")
    def startPigeonWebCamFlask():
        return render_template("PigeonWebCam.html")
    
    def pigeonWebCamGen():
        while True:
            pigeonSuccessful, pigeonWebFrame = pigeonWebVideoCam.read()
            cv2.imwrite("pigeonFrame.png", pigeonWebFrame)
            yield(b'--frame\r\n'b'Content-Type: imaghe/jpeg\r\n\r\n' + open("pigeonFrame.png", "rb").read() + b'\r\n')
    
    @app.route("/pigeonVideoFeed")
    def pigeonVideoFeed():
        return Response(pigeonWebCamGen(), mimetype="multipart/x-mixed-replace; boundary=frame")
    
    if __name__ == "__main__":
        pigeonWebApp.run(host="0.0.0.0", debug=True)