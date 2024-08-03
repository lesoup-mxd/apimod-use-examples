#include <Arduino.h>

void setup() {
  Serial.begin(9600);
  pinMode(11, OUTPUT); // Set PWM pin as output
}

void loop() {
  if (Serial.available()) { // Check if data is available to read
    String input = Serial.readStringUntil('\n'); // Read until newline character
    int value;
    
    if (input.length() == 1) {
      value = input.toInt(); // Convert single digit string to integer
    } else if (input.length() == 2) {
      value = input.toInt(); // Convert double digit string to integer
    } else if (input.length() == 3) {
      value = input.toInt(); // Convert triple digit string to integer
    } else {
      return; // Ignore if input length is not 1, 2, or 3
    }
    
    Serial.print("Setting PWM to: ");
    Serial.println(value); // Output the value being set
    
    analogWrite(11, value); // Set PWM value
  }
}
