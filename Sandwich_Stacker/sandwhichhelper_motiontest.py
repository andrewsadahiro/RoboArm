from gpiozero import AngularServo
from time import sleep

#initialize servos
handservo = AngularServo(18,
                         min_angle = 0,
                         max_angle = 270,
                         min_pulse_width = 0.0005,
                         max_pulse_width = 0.0025)
wristservo = AngularServo(19,
                         min_angle = 0,
                         max_angle = 270,
                         min_pulse_width = 0.0005,
                         max_pulse_width = 0.0025)
elbowservo = AngularServo(20,
                         min_angle = 0,
                         max_angle = 270,
                         min_pulse_width = 0.0005,
                         max_pulse_width = 0.0025)
shoulderservo = AngularServo(21,
                         min_angle = 0,
                         max_angle = 270,
                         min_pulse_width = 0.0005,
                         max_pulse_width = 0.0025)
baseservo = AngularServo(16,
                         min_angle = 0,
                         max_angle = 270,
                         min_pulse_width = 0.0005,
                         max_pulse_width = 0.0025)




def pos_reset():
    print("Reseting Position")
    baseservo.angle = -90
    sleep(1)
    shoulderservo.angle = 90
    sleep(1)
    elbowservo.angle = 60
    sleep(1)
    wristservo.angle = 0
    sleep(1)
    handservo.angle = 90
    sleep(1)
    print("Reset complete")
    
def pickup():
    pos_reset()
    print("Picking up")
    #rotate shoulder so arm pointing up
    elbowservo.angle = -90
    sleep(1)
    #rotate base
    baseservo.angle = 90
    sleep(1)
    #open hand
    handservo.angle = -90
    sleep(1)
    #shoulder + elbow reach down
    shoulderservo.angle = 0
    sleep(1)
    elbowservo.angle = -90
    sleep(1)
    #rotate wrist
    wristservo.angle = -90
    sleep(1)
    #close hand
    handservo.angle = 90
    sleep(1)
    #shoulder/elbow lift up
    shoulderservo.angle = 0
    sleep(1)
    #rotate base
    baseservo.angle = 0
    sleep(1)
    #open hand
    handservo.angle = -90
    sleep(1)
    print("Pickup complete")
    #reset
    pos_reset()

def pushaway():
    pos_reset()
    print("Pushing away")
    #rotate shoulder so arm pointing up
    elbowservo.angle = -90
    sleep(1)
    #rotate base
    baseservo.angle = 90
    sleep(1)
    #shoulder + elbow reach down
    shoulderservo.angle = 0
    sleep(1)
    elbowservo.angle = -90
    sleep(1)
    #rotate wrist
    wristservo.angle = -90
    sleep(1)
    #rotate base
    baseservo.angle = -90
    sleep(1)
    print("Push complete")
    pos_reset()
    
#     
# identified_object = "cucumber"
# sandwich_list = ['cucumber', 'bagel']
# 
# if identified_object in sandwich_list:
#     print("Sandwich Ingredient Detected")
#     pickup()
# else:
#     print("Non-sandwich Object Detected")
#     pushaway()

baseservo.angle = 145
shoulderservo.angle = 120
elbowservo.angle = 80
