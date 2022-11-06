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
    @staticmethod
    def updatePigeonVelocities(x, y, z):
        if x != 0 or y != 0 or z != 0:
            pigeonVelocityCommand = PigeonDrone.pigeon.message_factory.set_position_target_local_ned_encode(0, 0, 0, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, 0b0000111111000111, 0, 0, 0, x*3, y*3, z*3, 0, 0, 0, 0, 0)
            PigeonDrone.pigeon.send_mavlink(pigeonVelocityCommand)
            PigeonDrone.pigeon.flush()
            
    @staticmethod
    def startPigeonKillSwitch():
        pigeonKillCommand = PigeonDrone.pigeon.message_factory.command_long_encode(0, 0, mavutil.mavlink.MAV_CMD_DO_FLIGHTTERMINATION, 0, 1, 0, 0, 0, 0, 0, 0)
        PigeonDrone.pigeon.send_mavlink(pigeonKillCommand)
        PigeonDrone.pigeon.flush()
        
    @staticmethod
    def updatePigeonYawHeading(relPigeonDegrees):
        pigeonYawCW = 1
        if (relPigeonDegrees < 0):
            pigeonYawCW = -1
        pigeonYawCommand = PigeonDrone.pigeon.message_factory.command_long_encode(0, 0, mavutil.mavlink.MAV_CMD_CONDITION_YAW, 0, abs(relPigeonDegrees), 0, pigeonYawCW, 1, 0, 0, 0)
        PigeonDrone.pigeon.send_mavlink(pigeonYawCommand)
        PigeonDrone.pigeon.flush()
        
#pigeon = startPigeonConnect()
#startMotors()
