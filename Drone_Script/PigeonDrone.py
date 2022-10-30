from dronekit import connect, VehicleMode, LocationGlobalRelative, APIException
import time, socket, math
from pymavlink import mavutil
import PigeonFirebase

class PigeonDrone:
    
    pigeon = None
    
    @staticmethod
    def startPigeonConnect():
        
        PigeonDrone.pigeon = connect("/dev/ttyAMA0", baud=57600, wait_ready=True)
        print("Pigeon is armed")
        PigeonDrone.pigeon.mode = VehicleMode("GUIDED")
        
        PigeonFirebase.PigeonFirebase.pigeonAuth()
        

    @staticmethod
    def setPigeonAlt(y):
        PigeonDrone.pigeon.simple_goto(LocationGlobalRelative(PigeonDrone.PigeonDrone.pigeon.location.lat, PigeonDrone.PigeonDrone.pigeon.location.long), y)
        print("Created Pigeon Command")
        
       
        #PigeonDrone.pigeon.send_mavlink(pigeonVelocityCommand)
        #PigeonDrone.pigeon.flush()
        
    def updatePigeonVelocities(x, y, z):
        if x != 0 or y != 0 or z != 0:
            pigeonVelocityCommand = PigeonDrone.pigeon.message_factory.set_position_target_local_ned_encode(0, 0, 0, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 0b0000111111000111, 0, 0, 0, x*3, y*3, z*3, 0, 0, 0, 0, 0)
            PigeonDrone.pigeon.send_mavlink(pigeonVelocityCommand)
            PigeonDrone.pigeon.flush()
        
#pigeon = startPigeonConnect()
#startMotors()
