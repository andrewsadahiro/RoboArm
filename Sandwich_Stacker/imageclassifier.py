import cv2
import numpy as np
import tensorflow as tf

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

print("Starting real-time classificaiton. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break
    
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
    cv2.imshow("Real-time Classificaiton", frame)
    
    print(f"Predicted class: {label}")
    
    #quit on q
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()