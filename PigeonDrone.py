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
        
        PigeonDrone.startMotors()
        
    @staticmethod
    def startMotors():
    #     while pigeon.is_armable==False:
    #          time.sleep(1)
        print("Pigeon is armed")
        
        PigeonDrone.pigeon.armed=True
        PigeonDrone.pigeon.simple_takeoff(0.5)
        #setPigeonVelocity(10, 10, 10, 1)
        
        #pigeon.mode = VehicleMode("LAND")
      #  while True:
            
        #pigeon.close()
    @staticmethod
    def stopMotors():
        PigeonDrone.pigeon.armed=False

    @staticmethod
    def setPigeonAlt(y):
        PigeonDrone.pigeon.simple_goto(LocationGlobalRelative(PigeonDrone.PigeonDrone.pigeon.location.lat, PigeonDrone.PigeonDrone.pigeon.location.long), y)
        #pigeonVelocityCommand = pigeon.message_factory.set_position_target_local_ned_encode(0, 0, 0, mavutil.mavlink.MAV_FRAME_BODY_NED, 0b0000111111000111, 0, 0, 0, x, y, z, 0, 0, 0, 0, 0)
        print("Created Pigeon Command")
        
       
        #PigeonDrone.pigeon.send_mavlink(pigeonVelocityCommand)
        #PigeonDrone.pigeon.flush()
            

#pigeon = startPigeonConnect()
#startMotors()
