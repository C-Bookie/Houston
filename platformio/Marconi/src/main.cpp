#include <Arduino.h>
#include <side.h>

int cycle = 0;

// const int LED_PIN = LED_BUILTIN;
const int LED_PIN = 2;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  bufferIn = newBuffer();
  bufferOut = newBuffer();

  #if WIFI
    // Set WiFi to station mode and disconnect from an AP if it was previously connected
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(100);

    if (WiFi.status() == WL_NO_SHIELD) {
      Serial.println("WiFi shield not present");
      // don't continue:
      while (true);
  }

    // String fv = WiFi.firmwareVersion();
    // if (fv != "1.1.0") {
    //   Serial.println("Please upgrade the firmware");
    // }

  #else
    //Ethernet.begin(mac, ip);
    Ethernet.begin(mac);
    delay(1000);
    // Serial.setTimeout(10);

  #endif
}

void loop() {
  connectionSanity();
//  Serial.print("Cycle: ");
//  Serial.println(cycle, DEC);
  digitalWrite(LED_PIN, cycle%2==0);
  
  if (client.available()) {
    recieveBuffer(bufferIn);
  }
  
  if (Serial.available() > 0) {
    int outLen = Serial.available();
    int newOutLen = 0;
    while (outLen != newOutLen) {  // todo wait for new line
      outLen = newOutLen;
      delay(10);
      newOutLen = Serial.available();
    }

    resizeBuffer(bufferOut, outLen);
    for (int i=0; i<outLen; i++)
      bufferOut->packet[i] = Serial.read();
    sendBuffer(bufferOut);
  }
  cycle++;  

  delay(2000);
}
