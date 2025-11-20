# RoboArm
AL5A Lynxmotion Arm with Botboarduino
Video Demo: https://youtu.be/LPjmW3BnntI

The general idea of this project, the sandwich helper, is to use the robot arm alongside some various other bits to help users build a sandwich. There are several subsections to this project, Manual Control, Sandwich Stacker, and Sandwich Stacker (smooth), as well as an extra, Laser Wave.

Manual Control + Laser Wave
This section is in C++ instead of python and designed to run on an Arduino instead of a raspberry Pi. The Laser Wave code is an expansion on Manual Control, so they are very similar. They function primarily with a joystick and a few potentiometers (or just a bunch of potentiometers and no joystick), and the Laser Wave also uses an Elegoo laser pointer and PIR sensor. The potentiometers and/or joystick are wired up to the Arduino alongside the option Laser Wave components. The laser module is taped to the side of the hand, and the PIR sensor is taped to a corner of the board the arm is screwed to. With either program, simple manual control is possible. The joystick controls the elbow and shoulder servos, extra potentiometers control the base and wrist, and a button (intended to be the joystick button, but the onboard Arduino button) controls the closing of the hand. When the PIR sensor senses motion, manual control will be paused, and the arm will make a sweeping motion with the laser on, scanning where the sensor is pointing. Afterwards, the arm will resume its previous position, and manual control will work as normal.

Sandwich Stacker + Smooth ver.
This section of the project uses a Raspberry Pi 5, ultrasonic sensor, webcam (and Arduino for smooth) to automatically assist in sandwich creation.
When everything is set up, you can place a potential ingredient in a specified location so that the ultrasonic sensor will trigger the camera to start image recognition. If the object placed is on the list of sandwich ingredients, the arm will place it (or at least do its best to) place the ingredient in a designated location. If the object is not on the list, the arm will push it away.

The code can be broken up into 3 major parts. The ultrasonic sensor, the camera and AI image recognition, and the servo control. All the code is currently run on a Raspberry Pi 5 (the smooth version also uses an Arduino)

The ultrasonic sensor uses the gpiozero DistanceSensor library to detect when an object is placed in front of the camera, and in the designated location that the arm is calibrated to move to. The ultrasonic sensor acts as the initial trigger for the entire program. It should be noted that the sensor can struggle with rounder shapes, due to it needing to be able to bounce a signal off a relatively flat surface to gauge distance.

The camera is operated primarily through the cv2 library, while the AI image recognition is done by the tensorflow library. numpy is also included so that the image can be displayed on a screen connected to the Raspberry Pi 5. The datasets for image recognition were found online and linked below. The chunk of the code that involves the camera and AI checks what has been placed in front of the distance sensor, checks if that object is on the sandwich ingredient list, and then directs the arm to react appropriately.

https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt
https://huggingface.co/qualcomm/MobileNet-v2/blob/main/MobileNet-v2.tflite

Last but certainly not least, is the servo control. It is done with the gpiozero AngularServo library. The AL5A Lynxmotion arm is made up of 5 servo motors, corresponding to the major joints on a person's arm. Theres a servo that opens and closes the hand, rotates the wrist, bends the elbow, bends the shoulder, and rotates the shoulder. By using all these motors in tandem, a wide range of motion can be achieved. With just the Raspberry Pi (like in the base Sandwich Stacker), you will experience severe twitching of the servos, due to the Pi’s lack of compatibility with the necessary libraries. To fix this issue, I used an Arduino to control the servos, and a wire to allow the Pi to use the Serial library to send the angles for each servo to the Arduino, which will then move them accordingly. In the Sandwich Stacker Smooth folder, there’s an extra folder that contains the Arduino code. 

My setup for this project is as follows. My Raspberry Pi 5 is connected to a specialized touchscreen monitor for easy use, along with a mouse and keyboard. The arm itself is screwed into an old wooden cutting board for stability, alongside the attached Arduino (that is currently only being used to supply power) and a small breadboard for sorting out wires. Each of the servos are connected to that breadboard and consequentially connected to power and grounded (to both the Arduino and RP5). The inputs of each servo are isolated by a mess of wires on the breadboard and connected to the RP5. The ultrasonic sensor is on its own breadboard for stability, and connected by several wires chained together, to ensure it can be oriented correctly. And finally, the camera is connected by a USB cable.
For the Smooth version, wire the arm to an Arduino instead, and use a USB cable to connect the Arduino to the Pi.

My RP5 only has 4 PCM pins that would allow for higher accuracy, so I prioritized the servos that need more accuracy, such as the shoulder and elbow, over other things like the base.
