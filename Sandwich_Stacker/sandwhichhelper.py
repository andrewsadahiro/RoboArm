#This program uses a Lynxmotion AL5A arm, webcam, and ultrasonic sensor
#to assist in the creation of a sandwich. Place potential ingredients
#in the designated area, and the program will determine if its a
#sandwich ingredient or not, and then move the object to a specified location

#to detect when an potential ingredient is placed infront of the camera
from gpiozero import DistanceSensor
#to control the arm's servos
from gpiozero import AngularServo
#smoothing out motion
from time import sleep
#to identify objects, and optionally display what the camera is seeing
import cv2
import numpy as np
import tensorflow as tf

object_in_range = False
identified_object = ""

#the list of accepted sandwich ingredients
sandwich_list = ['bagel']

#ultrasonic sensor distance cutoff
MAX_SENSOR_DISTANCE = 0.13

#initialize distance sensor
TRIG_PIN = 17
ECHO_PIN = 27
distancesensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)

#initialize servos
HAND_PIN = 18
WRIST_PIN = 19
ELBOW_PIN = 20
SHOULDER_PIN = 21
BASE_PIN = 16
MIN_ANGLE = 0
MAX_ANGLE = 270
MIN_PULSE_WIDTH = 0.0005
MAX_PULSE_WIDTH = 0.0025
handservo = AngularServo(HAND_PIN,
                         min_angle = MIN_ANGLE,
                         max_angle = MAX_ANGLE,
                         min_pulse_width = MIN_PULSE_WIDTH,
                         max_pulse_width = MAX_PULSE_WIDTH)
wristservo = AngularServo(WRIST_PIN,
                         min_angle = MIN_ANGLE,
                         max_angle = MAX_ANGLE,
                         min_pulse_width = MIN_PULSE_WIDTH,
                         max_pulse_width = MAX_PULSE_WIDTH)
elbowservo = AngularServo(ELBOW_PIN,
                         min_angle = MIN_ANGLE,
                         max_angle = MAX_ANGLE,
                         min_pulse_width = MIN_PULSE_WIDTH,
                         max_pulse_width = MAX_PULSE_WIDTH)
shoulderservo = AngularServo(SHOULDER_PIN,
                         min_angle = MIN_ANGLE,
                         max_angle = MAX_ANGLE,
                         min_pulse_width = MIN_PULSE_WIDTH,
                         max_pulse_width = MAX_PULSE_WIDTH)
baseservo = AngularServo(BASE_PIN,
                         min_angle = MIN_ANGLE,
                         max_angle = MAX_ANGLE,
                         min_pulse_width = MIN_PULSE_WIDTH,
                         max_pulse_width = MAX_PULSE_WIDTH)

#attempts to slow down servo movement (currently twitchy)
def smooth_move(servo, start, end):
    DELAY = 0.1
    #clamp values to between 0, 270
    start = max(0, min(270, start))
    end = max(0, min(270, end))
    #ensure start on start value
    step = 5 if start <= end else -5
    
    servo_map = {
        'base':baseservo,
        'shoulder':shoulderservo,
        'elbow':elbowservo,
        'wrist':wristservo,
        'hand':handservo
        }
    if servo not in servo_map:
        raise ValueError(f"Unknown servo name: {servo}")
    
    target_servo = servo_map[servo]
    
    for i in range(start, end + step, step):
        target_servo.angle = i
        sleep(DELAY)
    
#Reset arm position inbetween actions
        #run on startup to prevent arm suicide
def pos_reset():
    print("Reseting Position")
    baseservo.angle = 145
    sleep(1)
    shoulderservo.angle = 250
    sleep(1)
    elbowservo.angle = 200
    sleep(1)
    wristservo.angle = 145
    sleep(1)
    handservo.angle = 180
    print("Reset complete")
pos_reset()

#moves arm to pickup object in specified location upon ingredient recognition
def pickup():
    pos_reset()
    print("Picking up")
    #rotate elbow so arm pointing up
    smooth_move('elbow', 200, 90)
    sleep(3)
    #rotate base
    baseservo.angle = 240
    sleep(3)
    #open hand
    handservo.angle = 0
    sleep(3)
    #shoulder + elbow reach down
    smooth_move('shoulder', 250, 180)
    sleep(3)
    smooth_move('elbow', 90, 110)
    sleep(3)
    #rotate wrist
    wristservo.angle = 0
    sleep(3)
    #close hand
    handservo.angle = 270
    sleep(3)
    #shoulder/elbow lift up
    smooth_move('shoulder', 180, 180)
    smooth_move('elbow', 110, 80)
    sleep(3)
    #rotate base
    baseservo.angle = 80
    sleep(3)
    #open hand
    handservo.angle = 0
    sleep(3)
    print("Pickup complete")
    #reset
    pos_reset()

#pushes away non-sandiwch ingredient
def pushaway():
    pos_reset()
    print("Pushing away")
    #rotate elbow so arm pointing up
    smooth_move('elbow', 200, 90)
    sleep(3)
    #rotate base
    baseservo.angle = 200
    sleep(3)
    #shoulder + elbow reach down
    smooth_move('shoulder', 250, 180)
    smooth_move('elbow', 90, 150)
    sleep(3)   
    #rotate wrist
    wristservo.angle = 50
    sleep(1)
    #rotate base
    baseservo.angle = 270
    sleep(1)
    print("Push complete")
    #reset position for next action
    pos_reset()
        

#load labels
with open("ImageNetLabels.txt","r") as f:
    labels = [line.strip() for line in f.readlines()]
    #labels from https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt

#load TFlite model
interpreter = tf.lite.Interpreter(model_path="MobileNet-v2.tflite")
    #model from https://huggingface.co/qualcomm/MobileNet-v2/blob/main/MobileNet-v2.tflite
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#preprocess function
def preprocess_image(image):
    image = cv2.resize(image, (224, 224))
    image = image.astype(np.float32)/255.0
    image = np.expand_dims(image, axis = 0)
    return image

def start_image_rec():
    global object_in_range
    global identified_object
    global sandwich_list
    
    #open camera
    cap = cv2.VideoCapture(0)

    #start object detection
    while object_in_range == False:
            sleep(1)
            #detect object in proximity
            print(f"distance: {distancesensor.distance * 100:.1f} cm")
            
            #cap 13cm
            if distancesensor.distance <= MAX_SENSOR_DISTANCE:
                print("object in range")
                object_in_range = True
                
    if object_in_range == True:

        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            
        
        #preprocess and run inference
        input_data = preprocess_image(frame)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        predicted_class = np.argmax(output_data[0])
        
        #shift index
        label_index = predicted_class + 1
        
        #protect against out of range index
        if label_index <len(labels):
            label = labels[label_index]
        else:
            label = "unknown"
            
        #display results
        #cv2.putText(frame, label, (10,30),
        #            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        #cv2.imshow("Real-time Classificaiton", frame)
        
        print(f"Predicted class: {label}")
        identified_object = label
        
        if identified_object in sandwich_list:
            print("Sandwich Ingredient Detected")
            pickup()
        else:
            print("Non-sandwich Object Detected")
            pushaway()
        cap.release()
        #cv2.destroyAllWindows()

start_image_rec()
#pickup()
        
        