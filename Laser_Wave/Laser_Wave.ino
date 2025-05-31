// This code is used to manually control a Lynxmotion AL5A arm with an elegoo joystick, 2 potentiometers, and a button on the board, 
// as well as a Botborduino, or Arduino Duemilanove or Diecimila.
// This code also uses an elegoo laser module, and PIR sensor
// The AL5A arm is made up of 5 servos, representing different parts of an arm.
// This code also has a function that makes the arm wave and shine a laser when motion is detected.
// https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/ses-v1/ses-v1-robots/ses-v1-arms/al5a/#HUserGuide



#include <Servo.h>
// initialize servos
  Servo baseservo;
  Servo shoulderservo;
  Servo elbowservo;
  Servo wristservo;
  Servo handservo;

// toggle print servo inputs/outputs
  bool debug = false;

// set base servo values
  int base0 = 90;
  int shoulder0 = 160;
  int elbow0 = 100;
  int wrist0 = 50;
  int hand0 = 90;

  // send hand parameters
  int handOpen = hand0 - 90;
  int handClosed = hand0 + 40;
  int currentHandPos = handClosed;

// initialize pot/button vals
  int ShoulderSensor = 0;  
  int ElbowSensor = 0; 
  int BaseSensor = 0;  
  int WristSensor = 0; 
  int buttonState = 0; 

// preset/intialize servo coords
  int shoulderval = 0;
  int elbowval = 0;
  int baseval = 0;
  int wristval = 0;

  int shoulderpos = shoulder0;
  int elbowpos = elbow0;
  int basepos = 0;
  int wristpos = 0;

// PIR setup
  // we start, assuming no motion detected
  int pirState = LOW;
  // variable for reading the pin status
  int PIRval = 0;


// sweep pos placeholder
  int pos = 0;

// cooldown
  unsigned long lastSweepTime = 0;
  const unsigned long cooldown = 10000; // 10 seconds

// set pins
  // control pins
  int ShoulderPin = A0;   
  int ElbowPin = A1;
  int BasePin = A2;
  int WristPin = A4;
  int buttonPin = 6;

  // module pins
  int PIRPin = 2;
  int LaserPin = 3;

  // servo pins
  const int BASESERVOPIN = 5;
  const int SHOULDERSERVOPIN = 6;
  const int ELBOWSERVOPIN = 10;
  const int WRISTSERVOPIN = 11;
  const int HANDSERVOPIN = 12;

// runs when motion detected
// sets servos to base position, turns on laser, sweeps, resumes previous state
void sweep_sequence(){
  // set arm to ready position
    shoulderservo.write(shoulder0);
    elbowservo.write(elbow0);
    wristservo.write(wrist0);
    baseservo.write(base0);
  // laser on
    analogWrite(LaserPin,200);
  // sweep
    for (pos = base0; pos <= base0+90; pos += 1) {
      baseservo.write(pos);            
      delay(45);                       
    }
  // laser off
    analogWrite(LaserPin,0);
  // return to rest or resume manual control
}

// runs once when power on
void setup() {
  // set servo pins
  baseservo.attach(BASESERVOPIN);
  shoulderservo.attach(SHOULDERSERVOPIN);
  elbowservo.attach(ELBOWSERVOPIN);
  wristservo.attach(WRISTSERVOPIN);
  handservo.attach(HANDSERVOPIN);

  Serial.begin(9600);

  // set pin mode for hand button
  pinMode(buttonPin, INPUT_PULLUP);
  handservo.write(currentHandPos); // Start in closed position
  //PIR pin setup
  pinMode(PIRPin, INPUT);

  //laser pin setup
  pinMode (LaserPin,OUTPUT);
  analogWrite(LaserPin,0);

  // TODO: 1 min timer

}

void loop() {
  // manual movement
    // read sensors
    ShoulderSensor = analogRead(ShoulderPin);
    ElbowSensor = analogRead(ElbowPin);
    buttonState = digitalRead(buttonPin);

    BaseSensor = analogRead(BasePin);
    WristSensor = analogRead(WristPin);

    shoulderval = map(ShoulderSensor, 0, 1023, -2, 2);
    shoulderval ++;
    elbowval = map(ElbowSensor, 0, 1023, -2, 2);

    baseval = map(BaseSensor, 0, 1023, 0, 180);
    wristval = map(WristSensor, 0, 1023, 0, 180);  

    shoulderpos += shoulderval;
    shoulderpos = constrain(shoulderpos, 0, 180);
    elbowpos += elbowval;
    elbowpos = constrain(elbowpos, 0, 180);
    basepos = constrain(baseval, 0, 180);
    // wristpos = constrain(wristval, 0, 180);

    // set servos
    shoulderservo.write(shoulderpos);
    elbowservo.write(elbowpos);
    wristservo.write(wristval);
    delay(100);
    baseservo.write(basepos);

    // only prints servo inputs/outputs in debug mode
    if (debug){
      Serial.print("shoulder in = ");
      Serial.println(shoulderval);
      Serial.print("shoulder out = ");
      Serial.println(shoulderpos);

      Serial.print("elbow in = ");
      Serial.println(elbowval);
      Serial.print("elbow out = ");
      Serial.println(elbowpos);

      Serial.print("base in = ");
      Serial.println(baseval);
      Serial.print("base out = ");
      Serial.println(basepos);

      Serial.print("wrist in = ");
      Serial.println(wristval);
      Serial.print("wrist out = ");
      Serial.println(wristpos);
    }

    // Hand logic
    if (buttonState == LOW) {
      // Button pressed - open hand
      if (currentHandPos > handOpen) {
        currentHandPos--;
        handservo.write(currentHandPos);
        Serial.println("Opening");
        Serial.println(currentHandPos);
      }
    } else {
      // Button not pressed - close hand
      if (currentHandPos < handClosed) {
        currentHandPos++;
        handservo.write(currentHandPos);
        Serial.println("Closing");
        Serial.println(currentHandPos);
      }
    }


  //check for PIR movement
  PIRval = digitalRead(PIRPin);
  if (PIRval == HIGH && pirState == LOW) {
    unsigned long currentTime = millis();
    if (currentTime - lastSweepTime > cooldown) {
      Serial.println("Motion Detected");
      sweep_sequence();
      lastSweepTime = currentTime;
      pirState = HIGH;
    }
  } else if (PIRval == LOW && pirState == HIGH) {
    Serial.println("Motion Ended");
    pirState = LOW;
  }




delay(100); // small delay for smoothness
}
