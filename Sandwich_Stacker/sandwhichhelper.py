from gpiozero import DistanceSensor
from gpiozero import AngularServo
from time import sleep
import cv2
import numpy as np
import tensorflow as tf

object_in_range = False
identified_object = ""
sandwich_list = ['cucumber', 'dumbbell', 'punching bag']

#initialize distance sensor
TRIG_PIN = 17
ECHO_PIN = 27
distancesensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)

#initialize servos
handservo = AngularServo(18)
wristservo = AngularServo(19)
elbowservo = AngularServo(20)
shoulderservo = AngularServo(21)
baseservo = AngularServo(16)


def pos_reset():
    print("Reseting Position")
    baseservo.angle = 0
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
pos_reset()
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

    

#load labels
with open("ImageNetLabels.txt","r") as f:
    labels = [line.strip() for line in f.readlines()]

#load TFlite model
interpreter = tf.lite.Interpreter(model_path="MobileNet-v2.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#preprocess function
def preprocess_image(image):
    image = cv2.resize(image, (224, 224))
    image = image.astype(np.float32)/255.0
    image = np.expand_dims(image, axis = 0)
    return image

#open camera
cap = cv2.VideoCapture(0)

#start object detection
while object_in_range == False:
        sleep(1)
        #detect object in proximity
        print(f"distance: {distancesensor.distance * 100:.1f} cm")
        
        #cap 13cm
        if distancesensor.distance <= 0.13:
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
    cv2.putText(frame, label, (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
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
        
        