/*
 * Blink
 * Turns on an LED on for one second,
 * then off for one second, repeatedly.
 */

#include <Arduino.h>

// Set LED_BUILTIN if it is not defined by Arduino framework
// #define LED_BUILTIN 2

int delay_time = 100;

int LED_PIN = LED_BUILTIN;




void setup()
{
  // initialize LED digital pin as an output.
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
}

void loop()
{
  // Serial.println("Goodnight moon!");
  // Serial.println(String(LED_PIN));
  // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_PIN, HIGH);
  // wait for a second
  delay(delay_time);
  // turn the LED off by making the voltage LOW
  digitalWrite(LED_PIN, LOW);
   // wait for a second
  delay(delay_time);

  if (Serial.available() > 0) {
    Serial.println(Serial.available());
    Serial.flush();
  }

}
