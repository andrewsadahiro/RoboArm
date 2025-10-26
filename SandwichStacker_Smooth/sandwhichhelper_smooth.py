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
#allow communication with Arduino
import serial
serial1 = serial.Serial('/dev/ttyUSB0', 9600)
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
#NOTE: Servo stuff in arduino file

def reset():
    serial1.write(b'base,90\n')
    time.sleep(0.5)
    serial1.write(b'elbow,90\n')
    time.sleep(0.5)
    serial1.write(b'shoulder,140\n')
    time.sleep(0.5)
    serial1.write(b'wrist,100\n')
    time.sleep(0.5)
    serial1.write(b'hand,180\n')
    print('reset done')

def pickup():
    reset()
    print("Picking up")
    #rotate elbow so arm pointing up
    serial1.write(b'elbow,30\n')
    time.sleep(1)
    #rotate base
    serial1.write(b'base,160\n')
    time.sleep(1)
    #open hand
    serial1.write(b'hand,00\n')
    time.sleep(1)
    #shoulder + elbow reach down
    serial1.write(b'elbow,40\n')
    time.sleep(1)
    serial1.write(b'shoulder,80\n')
    time.sleep(1)
    #rotate wrist
    serial1.write(b'wrist,30\n')
    time.sleep(1)
    #close hand
    serial1.write(b'hand,180\n')
    time.sleep(1)
    #shoulder/elbow lift up
    serial1.write(b'shoulder,140\n')
    time.sleep(1)
    serial1.write(b'elbow,30\n')
    time.sleep(1)
    #rotate base
    serial1.write(b'base,75\n')
    time.sleep(1)
    #reach back down
    serial1.write(b'elbow,40\n')
    time.sleep(1)
    serial1.write(b'shoulder,100\n')
    time.sleep(1)
    #open hand
    serial1.write(b'hand,0\n')
    time.sleep(1)
    print("Pickup complete")
    time.sleep(10)
    #reset
    reset()
    
def pushaway():
    reset()
    print("Pushing Away")
    #rotate elbow so arm pointing up
    serial1.write(b'elbow,30\n')
    time.sleep(1)
    #rotate base
    serial1.write(b'base,180\n')
    time.sleep(1)
    #shoulder + elbow reach down
    serial1.write(b'elbow,40\n')
    time.sleep(1)
    serial1.write(b'shoulder,80\n')
    time.sleep(1)
    #rotate wrist
    serial1.write(b'wrist,30\n')
    time.sleep(1)
    #rotate base
    serial1.write(b'base,75\n')
    time.sleep(1)
    print("Pushaway complete")
    time.sleep(10)
    #reset
    reset()


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
        
        