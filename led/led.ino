#include <FastLED.h>

#define LED_PIN     7
#define NUM_LEDS    30

CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  
}

float fract(float x) { return x - int(x); }

float mix(float a, float b, float t) { return a + (b - a) * t; }

float step(float e, float x) { return x < e ? 0.0 : 1.0; }

float* hsv2rgb(float h, float self, float b, float* rgb) {
  rgb[0] = b * mix(1.0, constrain(abs(fract(h + 1.0) * 6.0 - 3.0) - 1.0, 0.0, 1.0), self);
  rgb[1] = b * mix(1.0, constrain(abs(fract(h + 0.6666666) * 6.0 - 3.0) - 1.0, 0.0, 1.0), self);
  rgb[2] = b * mix(1.0, constrain(abs(fract(h + 0.3333333) * 6.0 - 3.0) - 1.0, 0.0, 1.0), self);
  return rgb;
}

int i = 0;
float* rgb;
float h;

void loop() {
  h = ((float)i / 100.0) - (i / 100);
  Serial.println(h);
  rgb = hsv2rgb(h, 1, 0.1, rgb);
  for (int n = 0; n < NUM_LEDS; ++n) {
    // leds[n] = CRGB((int)(rgb[0]*255), (int)(rgb[1]*255), (int)(rgb[2]*255));
    leds[n] = CRGB((int)(h*255), 0, 0);
  }
  FastLED.show();
  delay(50);
  i++;
}