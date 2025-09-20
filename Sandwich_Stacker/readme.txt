The general idea of this project, the sandwich helper, is to use the robot arm
alongside some AI image recognition to help users build a sandwich.

When everything is set up, you can place a potential ingredient in a specified location
so that the ultrasonic sensor will trigger to camera to start image recognition. If the
object placed is in the list ofo sandwich ingredients, the arm will place it (or atleast
do its best to) place the ingredient in a designated location. If the object is not in 
the list, the arm will push it away.

The code can be broken up into 3 major parts. The ultrasonic sensor, the camera and AI
image recognition, and the servo control. All the code is currently run on a Raspberry
Pi 5

The ultrasonic sensor uses the gpiozero DistanceSensor library to detect when an object
is placed infront of the camera, and in the designated location that the arm is 
calibrated to move to. The ultrasonic sensor acts as the initial trigger for the entire
program. It should be noted that the sensor can struggle with rounder shapes, due to it
needing to be able to bounce a signal off a relatively flat surface to gauge distance.

The camera is operated primarily through the cv2 library, while the AI image recognition
is done by the tensorflow library. numpy is also included so that the image can be
displayed on a screen connected to the Raspberry Pi 5. The datasets for the image recognition
were found online, and linked below. The chunk of the code that involves the camera and
AI check what has been placed infron of the distance sensor, check if that object is
on the sandwich ingredient list, and then direct the arm to react appropriately.

https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt
https://huggingface.co/qualcomm/MobileNet-v2/blob/main/MobileNet-v2.tflite

Last but certainly not least, is the servo control. It is done with the gpiozero AngularServo
library. The AL5A Lynxmotion arm is made up of 5 servo motors, corresponding to the major
joints on a person's arm. Theres a servo that opens and closes the hand, rotates the wrist, 
bends the elbow, bends the shoulder, and rotates the shoulder. By using all these motors
in tandem, a wide range of motion can be achieved. However, in the current state of this
project, using gpiozero on the Raspberry Pi 5, the servos jitter and twitch, due to 
the proper servo control libraries not being compatible with the RP5. To fix this issue,
an intermediary controller chip (or hopefully arduino) can be used.

I should also mention that I am using a virtual environment to run my code, primarily due
to some complicatations with other servo control libraries. I am not certain this is
neccessary, but it isn't too much trouble to set up.


My setup for this project is as follows. My Raspberry Pi 5 is connected to a specialized
touch-screen monitor for easy use, along with a mouse and keyboard. The arm itself is
screwed to an old wooden cutting board for stability, alongside the attached arduino
(that is currently only being used to supply power) and a small breadboard for sorting
out wires. Each of the servos are connected to that breadboard, and consequentially 
connected to power and grounded (to both the arduino and RP5). The inputs of each servo
are isolated by a mess of wires on the breadboard, and connected to the RP5. 
The ultrasonic sensor is on its own breadboard for stability, and connected by several wires
chained together, to ensure it can be oriented correctly. And finally, the camera is 
connected by a USB cable.

My RP5 only has 4 PCM pins that would allow for higher accuracy, so I prioritized the 
servos that need more accuracy, such as the shoulder and elbow, over other things like
the base.

















