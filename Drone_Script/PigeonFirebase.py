import firebase_admin
from firebase_admin import credentials, db
import PigeonDrone
from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import _thread
import datetime, time

class PigeonFirebase:
    
    pigeonDatabaseControls = None
    pigeonDatabaseLogs = None
    
    @staticmethod
    def pigeonAuth():
        pigeonFirebaseCred = credentials.Certificate("/home/pigeon/Desktop/ProjectPigeon/Drone_Script/projectpigeon-firebase-adminsdk-ycgqq-fa6ff827eb.json")
        firebase_admin.initialize_app(pigeonFirebaseCred, {"databaseURL": "https://projectpigeon-default-rtdb.firebaseio.com/"})
        
        PigeonFirebase.pigeonDatabaseControls = db.reference("controls")
        PigeonFirebase.pigeonDatabaseLogs = db.reference("logs")

        PigeonDrone.PigeonDrone.pigeon.parameters.add_attribute_listener("*", PigeonFirebase.startPigeonLogs)
        #PigeonFirebase.pigoneDatabaseControls.update({"altitude": PigeonDrone.PigeonDrone.pigeon.location.global_relative_frame.alt})
        
        _thread.start_new_thread(PigeonFirebase.handlePigeonMovements, ())
        print("WrotePigeon Monitering Database")
        
    @staticmethod
    def handlePigeonMovements():
        while True:
            pigeonValues = PigeonFirebase.pigeonDatabaseControls.get()

            if (pigeonValues.get("action")) == "Takeoff":
                PigeonDrone.PigeonDrone.pigeon.armed = True
                PigeonDrone.PigeonDrone.pigeon.mode = VehicleMode("GUIDED")
                PigeonDrone.PigeonDrone.pigeon.simple_takeoff(2)
                PigeonFirebase.pigeonDatabaseControls.update({"action": ""})

                print("HELLO")
            elif (pigeonValues.get("action")) == "Land":
                print("HELLO")
                PigeonDrone.PigeonDrone.pigeon.mode = VehicleMode("LAND")
                PigeonFirebase.pigeonDatabaseControls.update({"action": ""})

            elif  (pigeonValues.get("action")) == "Return to Home":
                PigeonDrone.PigeonDrone.pigeon.mode = VehicleMode("RTL")
                PigeonFirebase.pigeonDatabaseControls.update({"action": ""})

                print("Boom")
            elif (pigeonValues.get("action")) == "Kill":
                PigeonDrone.PigeonDrone.updatePigeonVelocities(0, 0, 0)
                PigeonFirebase.pigeonDatabaseControls.update({"action": ""})

            else:
                PigeonDrone.PigeonDrone.updatePigeonYawHeading(pigeonValues.get("yaw"))
                PigeonDrone.PigeonDrone.updatePigeonVelocities(pigeonValues.get("x_vel"), pigeonValues.get("y_vel"), pigeonValues.get("z_vel"))
                    
                print("Read Values")
            time.sleep(0.5)

    def startPigeonLogs(self, pigeonParamName, pigeonParamValue):
        
        pigeonLocData = PigeonDrone.PigeonDrone.pigeon.location.global_relative_frame
        print(PigeonDrone.PigeonDrone.pigeon.attitude)
        PigeonFirebase.pigeonDatabaseLogs.update({"lastUpdateDate": str(datetime.datetime.now()), "mode": PigeonDrone.PigeonDrone.pigeon.mode.name, "pitch": PigeonDrone.PigeonDrone.pigeon.attitude.pitch, "yaw": PigeonDrone.PigeonDrone.pigeon.attitude.yaw, "roll": PigeonDrone.PigeonDrone.pigeon.attitude.roll, "airspeed": PigeonDrone.PigeonDrone.pigeon.airspeed, "groundspeed": PigeonDrone.PigeonDrone.pigeon.groundspeed, "lastLink": PigeonDrone.PigeonDrone.pigeon.last_heartbeat, "altitude": pigeonLocData.alt, "lat": pigeonLocData.lat, "long": pigeonLocData.lon, "battery": PigeonDrone.PigeonDrone.pigeon.battery.level, "velocity": PigeonDrone.PigeonDrone.pigeon.velocity})
