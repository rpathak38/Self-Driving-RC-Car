#include <Arduino.h>
#include <Servo.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

#define DC_PIN 3
#define SERVO_PIN 11

void setMotors(void); //set both servo and dc motors based on global variables
Servo myServo;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial);

  myServo.attach(SERVO_PIN);
  pinMode(DC_PIN, OUTPUT);

  myServo.write(90);
  analogWrite(DC_PIN, 0);
  
  Serial.println("Welcome to Command Mode Driving");
  Serial.println("Type Engage to start");
  Serial.println();
}

char buffer[50];
int i = 0;
bool strComplete = false;
int motorSpeed = 0;
int servoPos = 90;
bool engage = false;

void loop() {
  if (Serial.available() > 0) {
    char temp = Serial.read();
    if (temp == '\n') {
      buffer[i] = '\0';
      Serial.println(buffer);
      i = 0;
      strComplete = true;
    } else {
      buffer[i] = temp;
      i++;
    }
  }

  if (strComplete && !engage) {
    if (strcasestr(buffer, "engage")) {
      engage = true;
      strComplete = false;
      Serial.println("Engaged");
      Serial.println();
    }
  }

  // Command Mode Piloting
  if (strComplete && engage) {
    // dc case
    if (strcasestr(buffer, "dc")) {
      // case in which a + sign is present, signaling to simply increase
      // the value of the motor
      if (char *start = strcasestr(buffer, "+")) {
        char **garbage;
        motorSpeed = motorSpeed + strtol(start, garbage, 10);
      }

      // case in which a - sign is present, signaling to decrease the
      // value of the motor
      else if (char *start = strcasestr(buffer, "-")) {
        char **garbage;
        motorSpeed = motorSpeed + strtol(start, garbage, 10);
      }

      else {
        char *current = buffer;
        while (*current) {
          if (isdigit(*current)) {
            motorSpeed = strtol(current, &current, 10);
            break;
          }
          current++;
        }
      }

      if (motorSpeed > 255) {
        motorSpeed = 255;
      } else if (motorSpeed < 0) {
        motorSpeed = 0;
      }
    }

    // servo case
    else if (strcasestr(buffer, "servo")) {
      // case in which a + sign is present, signaling to simply increase
      // the value of the motor
      if (char *start = strcasestr(buffer, "+")) {
        char **garbage;
        servoPos = servoPos + strtol(start, garbage, 10);
      }

      // case in which a - sign is present, signaling to decrease the
      // value of the motor
      else if (char *start = strcasestr(buffer, "-")) {
        char **garbage;
        servoPos = servoPos + strtol(start, garbage, 10);
      }

      else {
        char *current = buffer;
        while (*current) {
          if (isdigit(*current)) {
            servoPos = strtol(current, &current, 10);
            break;
          }
          current++;
        }
      }

      if (servoPos > 135) {
        servoPos = 135;
      } else if (servoPos < 45) {
        servoPos = 45;
      }
    }

    else if (strcasestr(buffer, "status")) {
      char temp[50];
      sprintf(temp, "SERVO MOTOR POSITION: %d", servoPos);
      Serial.println(temp);
      sprintf(temp, "DC MOTOR: %d", motorSpeed);
      Serial.println(temp);
    }

    else if (strcasestr(buffer, "reset")) {
      motorSpeed = 0;
      servoPos = 90;
      Serial.println("System Returned to Default State");
    }

    // Garbage Statement case
    else {
      Serial.println("Unable to Parse Command");
    }

    strComplete = false;
    setMotors();
    Serial.println();
  }
}

void setMotors(void) {
  myServo.write(servoPos);
  analogWrite(DC_PIN, motorSpeed);   
}