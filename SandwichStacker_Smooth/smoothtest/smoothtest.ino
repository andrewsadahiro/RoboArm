#include <Servo.h>

// Servo objects
Servo baseservo;
Servo shoulderservo;
Servo elbowservo;
Servo wristservo;
Servo handservo;

// Servo pins
const int BASESERVOPIN = 2;
const int SHOULDERSERVOPIN = 3;
const int ELBOWSERVOPIN = 4;
const int WRISTSERVOPIN = 5;
const int HANDSERVOPIN = 6;

// Smoothness and speed
const int SMOOTHNESS = 1;     // Degrees per step
const int DELAY_MS = 15;      // Delay per step

// Store current angles
int baseAngle = 90;
int shoulderAngle = 140;
int elbowAngle = 90;
int wristAngle = 100;
int handAngle = 180;

void setup() {
  Serial.begin(9600);

  // Attach all servos
  baseservo.attach(BASESERVOPIN);
  shoulderservo.attach(SHOULDERSERVOPIN);
  elbowservo.attach(ELBOWSERVOPIN);
  wristservo.attach(WRISTSERVOPIN);
  handservo.attach(HANDSERVOPIN);

  // Move to initial positions
  baseservo.write(baseAngle);
  shoulderservo.write(shoulderAngle);
  elbowservo.write(elbowAngle);
  wristservo.write(wristAngle);
  handservo.write(handAngle);
}

// Function to smoothly move a servo
void moveServo(Servo& servo, int& currentAngle, const String& name, int targetAngle) {
  targetAngle = constrain(targetAngle, 0, 180);  // Keep angle in bounds

  Serial.print("Moving ");
  Serial.print(name);
  Serial.print(" from ");
  Serial.print(currentAngle);
  Serial.print(" to ");
  Serial.println(targetAngle);

  if (currentAngle < targetAngle) {
    for (int i = currentAngle; i <= targetAngle; i += SMOOTHNESS) {
      servo.write(i);
      Serial.print(name);
      Serial.print(": ");
      Serial.println(i);
      delay(DELAY_MS);
    }
  } else if (currentAngle > targetAngle) {
    for (int i = currentAngle; i >= targetAngle; i -= SMOOTHNESS) {
      servo.write(i);
      Serial.print(name);
      Serial.print(": ");
      Serial.println(i);
      delay(DELAY_MS);
    }
  }

  currentAngle = targetAngle; // Update current angle
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();  // Remove extra whitespace or newlines
    Serial.print("Received: ");
    Serial.println(data);

    int commaIndex = data.indexOf(',');
    if (commaIndex > 0) {
      String servoName = data.substring(0, commaIndex);
      int targetAngle = data.substring(commaIndex + 1).toInt();

      // Match servo name and move
      if (servoName == "base") {
        moveServo(baseservo, baseAngle, "base", targetAngle);
      } else if (servoName == "shoulder") {
        moveServo(shoulderservo, shoulderAngle, "shoulder", targetAngle);
      } else if (servoName == "elbow") {
        moveServo(elbowservo, elbowAngle, "elbow", targetAngle);
      } else if (servoName == "wrist") {
        moveServo(wristservo, wristAngle, "wrist", targetAngle);
      } else if (servoName == "hand") {
        moveServo(handservo, handAngle, "hand", targetAngle);
      } else {
        Serial.println("Error: Unknown servo name.");
      }
    } else {
      Serial.println("Error: Invalid command format.");
    }
  }
}
