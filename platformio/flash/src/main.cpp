
//todo
//  serial 


#include <Arduino.h>
#include <FastLED.h> 

const int DIAL_PIN = 36;

const int LED_STRIP_PIN = 27;
const int NUM_LEDS = 150;
CRGB leds[NUM_LEDS];

const int LEDS_USED = 10;

float col[3];

// https://gist.github.com/postspectacular/2a4a8db092011c6743a7

// HSV->RGB conversion based on GLSL version
// expects hsv channels defined in 0.0 .. 1.0 interval
float fract(float x) { return x - int(x); }

float mix(float a, float b, float t) { return a + (b - a) * t; }

float* hsv2rgb(float h, float s, float b, float* rgb) {
  rgb[0] = b * mix(1.0, constrain(abs(fract(h + 1.0) * 6.0 - 3.0) - 1.0, 0.0, 1.0), s);
  rgb[1] = b * mix(1.0, constrain(abs(fract(h + (2.0/3)) * 6.0 - 3.0) - 1.0, 0.0, 1.0), s);
  rgb[2] = b * mix(1.0, constrain(abs(fract(h + (1.0/3)) * 6.0 - 3.0) - 1.0, 0.0, 1.0), s);
  return rgb;
}

float float_mod(float a, int b) {
  return a - (int)(a / b) * b;
}

int cycle = 0;

float bpm = 120;
float beats = 4;
float bpm_fps = 60 / bpm;
float min_fps = 30;
unsigned long last_time = 0;
unsigned long start = 0;
// float gap = (bpm / ((int)(bpm / min_fps) + 1)) * 1000;
float gap = 50;


void setup() {
  Serial.begin(115200);
  FastLED.addLeds<WS2812, LED_STRIP_PIN, GRB>(leds, NUM_LEDS);

  for (int i=0; i<NUM_LEDS; i++) {
    leds[i] = CRGB(0, 0, 0);
  }
  FastLED.show();

  
  pinMode(DIAL_PIN, INPUT);
  
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  
  digitalWrite(LED_BUILTIN, HIGH);
  delay(200);

  start = millis();
}

void loop() {
  digitalWrite(LED_BUILTIN, cycle % 2);

  Serial.println("Moo2");


  // if (Serial.available() > 0) {
  //   int outLen = Serial.available();
  //   int newOutLen = 0;
  //   while (outLen != newOutLen) {  // todo wait for new line
  //     outLen = newOutLen;
  //     delay(10);
  //     newOutLen = Serial.available();
  //   }
  // }

  int dial_value = analogRead(DIAL_PIN);
  Serial.println(dial_value);

  // Update lights
  unsigned long now = millis();

  for (int i=0; i<LEDS_USED; i++) {
    // float beat_fraction = float_mod(now / (1000. / (bpm / 60.)), 1);
    float beat_fraction = float_mod(now / (1000. / ((bpm/beats) / 60.)), 1);
    float id = beat_fraction + ((float)i / LEDS_USED);

    // double h = float_mod(id, LEDS_USED) / (float)LEDS_USED;
    double h = id;


    // double s = 0.607;
    double s = float(dial_value) / (1<<12);
    double l = 0.1;// - (beat_fraction/64.);

    // double l = sin(((beat_fraction)-0.5) / 2);

    hsv2rgb(h, s, l, col);

    uint8_t r = (int)((col[0]) * 255);
    uint8_t g = (int)((col[1]) * 255);
    uint8_t b = (int)((col[2]) * 255);

    // uint8_t r = (int)((id % 20)*255 / 20);
    // uint8_t g = (int)((id % 30)*255 / 30);
    // uint8_t b = (int)((id % 50)*255 / 50);

    leds[i] = CRGB(r, g, b);
  }
  FastLED.show();
 
  unsigned long time_now = millis();
  float wait = last_time + gap - time_now;
  last_time = time_now;
  if (wait > 0)
    delay(wait);

  cycle++;

}