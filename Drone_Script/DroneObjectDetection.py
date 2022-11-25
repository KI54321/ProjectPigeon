import os
import random
import tensorflow
import keras.applications
import sklearn
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import *
import imutils

def trainDroneObjectDetectionModel():
    droneOutputCSV = open("./ObjectionDataset/Train/CSV/output.csv").read().strip().split("\n")

    droneImageData = []
    droneCoords = []
    droneImageFilenames = []

    for oneObjectRow in droneOutputCSV:
        print(oneObjectRow)
        (droneImageFileName, droneStartX, droneStartY, droneEndX, droneEndY) = oneObjectRow.split(",")
        imageDronePath = os.path.sep.join(["./ObjectionDataset/Train/Images/" + str(droneImageFileName)])
        droneImage = cv2.imread(imageDronePath)
        (droneHeight, droneWidth) = droneImage.shape[:2]

        droneStartX = float(droneStartX) / droneWidth
        droneStartY = float(droneStartY) / droneHeight
        droneEndX = float(droneEndX) / droneWidth
        droneEndY = float(droneEndY) / droneHeight

        droneImage = tensorflow.keras.preprocessing.image.load_img(imageDronePath, target_size=(224, 224))
        droneImage = tensorflow.keras.preprocessing.image.img_to_array(droneImage)

        droneImageData.append(droneImage)
        droneCoords.append((droneStartX, droneStartY, droneEndX, droneEndY))
        droneImageFilenames.append(droneImageFileName)

    droneImageDataNumpy = np.array(droneImageData, dtype="float32") / 255.0
    droneCoordsNumpy = np.array(droneCoords, dtype="float32")


    droneDataSplit = train_test_split(droneImageDataNumpy, droneCoordsNumpy, droneImageFilenames, test_size=0.25, random_state=random.randint(0, 100))


    (trainDroneImages, testDroneImages) = droneDataSplit[:2]
    (trainDroneCoords, testDroneCoords) = droneDataSplit[2:4]
    (trainDronFilenames, testDroneFilenames) = droneDataSplit[4:]

    droneVGG16 = tensorflow.keras.applications.VGG16(weights="imagenet", include_top=False, input_tensor=Input(shape=(224, 224, 3)))
    droneVGG16.trainable = False

    droneFlattenLayer = Flatten()(droneVGG16.output)
    droneCoord1 = Dense(128, activation="relu")(droneFlattenLayer)
    droneCoord2 = Dense(64, activation="relu")(droneCoord1)
    droneCoord3 = Dense(32, activation="relu")(droneCoord2)
    droneCoord4 = Dense(4, activation="sigmoid")(droneCoord3)

    droneObjectDectionModel = tensorflow.keras.models.Model(inputs=droneVGG16.input, outputs=droneCoord4)
    droneObjectDectionModel.compile(loss="mse", optimizer=Adam(lr="1e-4"))
    droneObjectDectionModel.summary()
    droneObjectDectionModel.fit(trainDroneImages, trainDroneCoords, validation_data=(testDroneImages, testDroneCoords), batch_size=32, epochs=25, verbose=1)

    droneObjectDectionModel.save("./DroneModelObjectDetectionVersions/DroneObjectDetectionV3.h5")

droneVideoCam = cv2.VideoCapture(0)

def loadDroneVideoCam():
    loadedDroneModel = tensorflow.keras.models.load_model("./DroneModelObjectDetectionVersions/DroneObjectDetectionV2.h5")

    while True:

        success, droneImage = droneVideoCam.read()

        if success:
            cv2.imwrite("./ObjectionDataset/Test/LiveFeed.jpg", droneImage)
            testImage = tensorflow.keras.preprocessing.image.load_img("./ObjectionDataset/Test/LiveFeed.jpg",
                                                                      target_size=(224, 224))

            testImage = tensorflow.keras.preprocessing.image.img_to_array(testImage) / 255.0

            testImage = np.expand_dims(testImage, axis=0)

            (xmin, ymin, xmax, ymax) = loadedDroneModel.predict(testImage)[0]


            testImage = imutils.resize(droneImage, width=2000)
            (droneH, droneW) = testImage.shape[:2]

            xmin = int(xmin * droneW)
            ymin = int(ymin * droneH)

            xmax = int(xmax * droneW)
            ymax = int(ymax * droneH)

            cv2.rectangle(testImage, (xmin, ymin), (xmax, ymax), (0, 255, 0), 10)

            cv2.imshow("frame", testImage)
            cv2.waitKey(1)

def loadDroneObjectDetectionModel():
    loadedDroneModel = tensorflow.keras.models.load_model("./DroneModelObjectDetectionVersions/DroneObjectDetectionV2.h5")

    testImage = tensorflow.keras.preprocessing.image.load_img("./ObjectionDataset/Test/2.jpg", target_size=(224, 224))

    testImage = tensorflow.keras.preprocessing.image.img_to_array(testImage) / 255.0

    testImage = np.expand_dims(testImage, axis=0)

    (xmin, ymin, xmax, ymax) = loadedDroneModel.predict(testImage)[0]

    testImage = cv2.imread("./ObjectionDataset/Test/2.jpg")
    testImage = imutils.resize(testImage, width=800)
    (droneH, droneW) = testImage.shape[:2]

    xmin = int(xmin*droneW)
    ymin = int(ymin*droneH)

    xmax = int(xmax*droneW)
    ymax = int(ymax*droneH)


    cv2.rectangle(testImage, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    cv2.imshow("Output", testImage)
    cv2.waitKey(0)

loadDroneVideoCam()