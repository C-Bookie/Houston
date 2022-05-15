// if the following is seen
// rst:0xc (SW_CPU_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
// it is possible the ESP32 is starved of power when using the WI-FI radio


#include <Arduino.h>

#include <ArduinoJson.h>

#define WIFI true

#if WIFI
  #include "WiFi.h"

  // char ssid[] = "Party!"; //  your network SSID (name)

  // char ssid[] = "Cherry-Rose"; //  your network SSID (name)
  // char pass[] = "DuckandMook";    // your network password (use for WPA, or use as key for WEP)

  // char ssid[] = "BT-6FCJ6X"; //  your network SSID (name)
  // char pass[] = "mHfKDAeMfV74cQ";    // your network password (use for WPA, or use as key for WEP)

  char ssid[] = "VM3877152"; //  your network SSID (name)
  char pass[] = "s7kyTysrddbg";    // your network password (use for WPA, or use as key for WEP)

  int status = WL_IDLE_STATUS;
  WiFiClient client;
#else
  #include <Ethernet.h>
  //TODO: impliment https://arduinojson.org/v5/example/http-client/

  byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
  IPAddress ip(192, 168, 0, 25);

  EthernetClient client;
#endif

IPAddress server(192, 168, 0, 23);
int port = 8089;

#define USING_HEADER false

#if USING_HEADER
  const int HEADER_LEN = 4;
#else
  const int MAX_BUFFER = 3000;
  const unsigned char ETX = 0x03;  //end of transmission tag
#endif

struct Buffer {  // pass by reference
  unsigned char* packet;
  #if USING_HEADER
    unsigned char* header;
  #endif
  int len;
};

struct Buffer *bufferIn;
struct Buffer *bufferOut;

Buffer* newBuffer() {
  Buffer* buffer = (Buffer*)malloc(sizeof(Buffer));
  *buffer = Buffer {
    .packet = NULL,
    #if USING_HEADER
      .header = (unsigned char*)malloc(HEADER_LEN),
    #endif
    // .len = 0
  };
  return buffer;
}

void printBuffer(Buffer* buffer) {
  for (int i=0; i<buffer->len; i++){
    Serial.print("\\x");
    Serial.print(buffer->packet[i], DEC);
  }
  Serial.println();
}

void resizeBuffer(Buffer* buffer, int len) {
  buffer->len = len;
  #if USING_HEADER  // fixme unsure if this code is requiered when !USING_HEADER
    for (int i=0; i<HEADER_LEN; i++)
      buffer->header[i] = (buffer->len >> (8 * (HEADER_LEN-i-1))) & ((2<<8)-1);
  #endif

  int size = buffer->len * sizeof(char);
  // void* temp = realloc(buffer->packet, size);  //may need to cast to (unsigned char*)
  buffer->packet = (unsigned char*)realloc(buffer->packet, size);
  // memset(buffer->packet, 0, size);
}

void sendBuffer(Buffer* buffer) {
  Serial.print("Sending: ");
  Serial.write(buffer->packet, buffer->len);
  Serial.print("\n");

  #if USING_HEADER
    client.write(buffer->header, HEADER_LEN);
  #endif

  client.write(buffer->packet, buffer->len);

  #if !USING_HEADER
    client.write(&ETX, 1);
  #endif
}

void recieveBuffer(Buffer* buffer) {
  #if USING_HEADER
    client.read(buffer->header, HEADER_LEN);
    buffer->len = 0;
    for (int i=0; i<HEADER_LEN; i++){
      buffer->len |= buffer->header[i] >> (8 * (HEADER_LEN-i-1));
    }

    resizeBuffer(buffer, buffer->len);
    client.read(buffer->packet, buffer->len);
  #else
    resizeBuffer(buffer, MAX_BUFFER);
    unsigned int index = 0;

    uint8_t data = 0;
    while (true) {
      if (index > MAX_BUFFER) {
          Serial.print("ERROR: buffer went oversize:");
          Serial.println(MAX_BUFFER);
      }
      int res = client.read(&data, 1);

      if(res <= 0) {
          Serial.print("ERROR: bad response from client.read():");
          Serial.println(res);
          // raise Exeption // fixme
      }

      if (data == ETX)
        break;

      buffer->packet[index] = data;
      index++;
    }

    buffer->len = index;
  #endif

  // Serial.print("Recieved: ");
  // Serial.write(buffer->packet, buffer->len);
  // Serial.println();
}

void printStatus() {
  #if WIFI
    // print the SSID of the network you're attached to:
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());
    // print your WiFi shield's IP address:
    IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");
    Serial.println(ip);
    // print the received signal strength:
    long rssi = WiFi.RSSI();
    Serial.print("signal strength (RSSI):");
    Serial.print(rssi);
    Serial.println(" dBm");

  #else
    Serial.print("Local IP: \t");
    Serial.println(Ethernet.localIP());

    Serial.print("Gateway IP: \t");
    Serial.println(Ethernet.gatewayIP());

    Serial.print("DNS server IP: \t");
    Serial.println(Ethernet.dnsServerIP());

    Serial.print("Subnet mask: \t");
    Serial.println(Ethernet.subnetMask());

  #endif
}

void connectionSanity() {
  while (!client.connected()) {
    #if WIFI
      while (status != WL_CONNECTED) {
        Serial.print("Attempting to connect to SSID: ");
        Serial.println(ssid);
        // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
        status = WiFi.begin(ssid, pass);
        // status = WiFi.begin(ssid);
        if (status != WL_CONNECTED)
          listNetworks();
        // wait 10 seconds for connection:
        delay(10000);
      }
    #endif

    Serial.println("Connecting...");
    if (client.connect(server, port)) {
      Serial.println("Connected");
      printStatus();

      unsigned char message[] = "{\"type\": \"subscribe\", \"args\": [\"pitta\"]}";
      resizeBuffer(bufferOut, 40);
      memcpy(bufferOut->packet, message, bufferOut->len);
      sendBuffer(bufferOut);

    } else
      Serial.println("Connecting timedout!");
  }
  client.setTimeout(100);
}


void listNetworks() {
  //https://docs.arduino.cc/library-examples/wifi-library/ScanNetworks
  // scan for nearby networks:
  Serial.println("** Scan Networks **");
  int numSsid = WiFi.scanNetworks();
  if (numSsid == -1) {
    Serial.println("Couldn't get a wifi connection");
    while (true);
  }

  // print the list of networks seen:
  Serial.print("number of available networks:");
  Serial.println(numSsid);

  // print the network number and name for each network found:
  for (int thisNet = 0; thisNet < numSsid; thisNet++) {
    Serial.print(thisNet);
    Serial.print(") ");
    Serial.print(WiFi.SSID(thisNet));
    Serial.print("\tSignal: ");
    Serial.print(WiFi.RSSI(thisNet));
    Serial.print(" dBm");
  }
}




#include <FastLED.h>

const int LED_STRIP_PIN = 27;

#define NUM_LEDS    150
CRGB leds[NUM_LEDS];

int cycle = 0;

// const int LED_PIN = LED_BUILTIN;
const int LED_PIN = 2;
const int RED_LED_PIN = 32;
const int BTN_PIN = 35;

bool last_btn_state = false;

void log_local_sensors() {
  bool new_btn_state = digitalRead(BTN_PIN);

  if (new_btn_state != last_btn_state) {    
    //todo send 
    DynamicJsonDocument doc(1024);

    // {'type': 'broadcast', 'args': [{'type': 'mail', 'args': ['turn on']}, 'pitta']}

    doc["type"] = "broadcast";
    doc["args"][1] = "pizza";

    doc["args"][0]["type"] = "report";
    doc["args"][0]["args"][0] = new_btn_state;  // button

    bufferOut->len = measureJson(doc);
    resizeBuffer(bufferOut, bufferOut->len);
    serializeJson(doc, bufferOut->packet, bufferOut->len);
    sendBuffer(bufferOut);
  
    last_btn_state = new_btn_state;
  }  
}

void parse_command(Buffer* command) {
  // maybe use JsonVariant
  DynamicJsonDocument doc(2560);  // may be an inappropriate use of MAX_BUFFER
  DeserializationError error = deserializeJson(doc, command->packet);

  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.f_str());
    return;
  }

  // Serial.println("Parsing command:");
  // serializeJsonPretty(doc, Serial);

  // Serial.println("Keys:");
  // for (JsonPair keyValue : doc) {
  //   Serial.println(keyValue.key().c_str());
  // }

  const char* type = doc["type"];

  if (String("light") == type) {  // may need to use String.equals()
    bool light = doc["args"][0];  // light
    digitalWrite(RED_LED_PIN, light);
  } else if (String("fast_light") == type) {
    int size = doc["args"][0]["size"];
    int offset = doc["args"][0]["offset"];
    for (int i=0; i<size; i++) {
      int r = doc["args"][0]["values"][i][0];
      int g = doc["args"][0]["values"][i][1];
      int b = doc["args"][0]["values"][i][2];
      leds[i+offset] = CRGB(r, g, b);  // fixme
    }
    FastLED.show();
  }else {
    Serial.print("Unregognised type: ");
    Serial.println(type);
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("Setting up...");
  pinMode(LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(BTN_PIN, INPUT);

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

  FastLED.addLeds<WS2812, LED_STRIP_PIN, GRB>(leds, NUM_LEDS);
  for (int i=0; i<NUM_LEDS; i++) {
    leds[i] = CRGB(0, 128, 0);
  }
  FastLED.show();

  Serial.println("Setup complete");
}

void loop() {
  connectionSanity();
//  Serial.print("Cycle: ");
//  Serial.println(cycle, DEC);
  digitalWrite(LED_PIN, cycle%2==0);
  
  if (client.available()) {
    recieveBuffer(bufferIn);
    parse_command(bufferIn);
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

  log_local_sensors();

  cycle++;
  delay(10);
}
