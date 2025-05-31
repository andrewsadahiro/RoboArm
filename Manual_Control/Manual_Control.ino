// This code is used to manually control a Lynxmotion AL5A arm with an elegoo joystick, 2 potentiometers, and a button on the board, 
// as well as a Botborduino, or Arduino Duemilanove or Diecimila.
// The AL5A arm is made up of 5 servos, representing different parts of an arm.
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

// base positions for servos
int base0 = 90;
int shoulder0 = 160;
int elbow0 = 100;
int wrist0 = 50;
int hand0 = 90;

// set positons limits for hand
int handOpen = hand0 - 90;
int handClosed = hand0 + 40;
// start hand closed
int currentHandPos = handClosed;

// joystick/potentiometer/button pins
int ShoulderPin = A0;   
int EblowPin = A1;
int BasePotPin = A2;
int WristPotPin = A4;
int HandButtonPin = 7;
// TODO: integrate FSR
//int fsrPin = A3;

// servo pins
const int BASESERVOPIN = 5;
const int SHOULDERSERVOPIN = 6;
const int ELBOWSERVOPIN = 10;
const int WRISTSERVOPIN = 11;
const int HANDSERVOPIN = 12;


// initialize control output variables
int ShoulderSensor = 0;  
int ElbowSensor = 0; 
int BaseSensor = 0;  
int WristSensor = 0; 
int buttonState = 0; 
// initialize servo input variables
int shoulderval = 0;
int elbowval = 0;
int baseval = 0;
int wristval = 0;
// set starting positions
int shoulderpos = shoulder0;
int elbowpos = elbow0;
int basepos = 0;
int wristpos = 0;

// the first function that runs once on power on
void setup() {
  // set servo pins
  baseservo.attach(BASESERVOPIN);
  shoulderservo.attach(SHOULDERSERVOPIN);
  elbowservo.attach(ELBOWSERVOPIN);
  wristservo.attach(WRISTSERVOPIN);
  handservo.attach(HANDSERVOPIN);

  Serial.begin(9600);
  // set pinmode for hand button
  pinMode(HandButtonPin, INPUT_PULLUP);
  // stard hand closed
  handservo.write(currentHandPos);

}

// constantly runs forever after the setup function
void loop() {
  // TODO: setup FSR
  // int analogReading = analogRead(fsrPin);
  
  // reading joystick values
  ShoulderSensor = analogRead(ShoulderPin);
  ElbowSensor = analogRead(EblowPin);
  // reading button value
  buttonState = digitalRead(HandButtonPin);
  // reading potentiometer values
  BaseSensor = analogRead(BasePotPin);
  WristSensor = analogRead(WristPotPin);

  // map sensor values to servo input constraints
  shoulderval = map(ShoulderSensor, 0, 1023, -2, 2);
  shoulderval ++;
  elbowval = map(ElbowSensor, 0, 1023, -2, 2);

  baseval = map(BaseSensor, 0, 1023, 0, 180);
  wristval = map(WristSensor, 0, 1023, 0, 180);

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

// add input variables to output, to make it so you don't have to keep the joystick in a position to keep the arm there
  shoulderpos += shoulderval;
  shoulderpos = constrain(shoulderpos, 0, 180);
  elbowpos += elbowval;
  elbowpos = constrain(elbowpos, 0, 180);

  // doesn't add, just sets position to potentiometer value
  basepos = constrain(baseval, 0, 180);
  wristpos = constrain(wristval, 0, 180);

  // set servos
  shoulderservo.write(shoulderpos);
  elbowservo.write(elbowpos);
  wristservo.write(wristpos);
  baseservo.write(basepos);

  // TODO: Integrate FSR
  // //fsr code
  // Serial.print("Force sensor reading = ");
  // Serial.print(analogReading); // print the raw analog reading

  // if (analogReading < 10)       // from 0 to 9
  //   Serial.println(" -> no pressure");
  // else if (analogReading < 200) // from 10 to 199
  //   Serial.println(" -> light touch");
  // else if (analogReading < 500) // from 200 to 499
  //   Serial.println(" -> light squeeze");
  // else if (analogReading < 800) // from 500 to 799
  //   Serial.println(" -> medium squeeze");
  // else // from 800 to 1023
  //   Serial.println(" -> big squeeze");
  

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

  delay(30); // small delay for smoothness
}