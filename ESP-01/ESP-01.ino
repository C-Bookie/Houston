/*
    This sketch establishes a TCP connection to a "quote of the day" service.
    It sends a "hello" message, and then prints received data.
*/

#include <ESP8266WiFi.h>

#ifndef STASSID
#define STASSID "EE-Hub-76hH-2.4ghz"
#define STAPSK  "jig-SIFT-lunar"
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

const char* host = "2.28.174.66";
const uint16_t port = 8089;



const int MAX_BUFFER = 256;

const int HEADER_LEN = 4 * sizeof(char);  
const int HEADER_SIZE = HEADER_LEN * sizeof(char);

struct Buffer {  // pass by reference
  char* packet;
  char* header;
  int len;
};

struct Buffer *bufferIn;
struct Buffer *bufferOut;

WiFiClient client;

//const int LED_BUILTIN = 13;
int cycle = 0;


Buffer* newBuffer() {
  Buffer* buffer = (Buffer*)malloc(sizeof(Buffer));
  *buffer = Buffer {
    .packet = (char*)malloc(MAX_BUFFER),
    .header = (char*)malloc(HEADER_LEN),
    .len = 0
  };
  return buffer;
}

void printBuffer(Buffer* buffer) {
  Serial.print("Buffer: ");
  for (int i=0; i<buffer->len; i++){
    Serial.print("\\");
    Serial.print(buffer->packet[i], DEC);
  }
  Serial.println();
}

void resizeBuffer(Buffer* buffer, int len) {
  buffer->len = len;
  for (int i=0; i<HEADER_LEN; i++)
    buffer->header[i] = (buffer->len >> (8 * i)) & ((1<<8)-1);

  if (len >= MAX_BUFFER)
    Serial.println("WARRNING BUFFER TOO SMALL");
}

void sendBuffer(Buffer* buffer) {
  Serial.print("Sending: ");
  Serial.write(buffer->packet, buffer->len);
  Serial.print("\n");

  client.write(buffer->header, HEADER_LEN);
  client.write(buffer->packet, buffer->len);
}

void send_msg(char* msg) {
  int outLen = strlen(msg);
  resizeBuffer(bufferOut, outLen);
  bufferOut->packet = msg;
  sendBuffer(bufferOut);
}

void recieveBuffer(Buffer* buffer) {
  client.read((uint8_t*)buffer->header, HEADER_LEN);
  buffer->len = 0;
  for (int i=0; i<HEADER_LEN; i++){
    buffer->len |= buffer->header[i] >> (8 * i);
  }
  
  resizeBuffer(buffer, buffer->len);
  client.read((uint8_t*)buffer->packet, buffer->len);

  // Serial.print("Recieved: ");
  // Serial.write(buffer->packet, buffer->len);
  // Serial.println();
}


void printStatus() {
  Serial.print("Local IP: \t");
  Serial.println(WiFi.localIP());

  Serial.print("Gateway IP: \t");
  Serial.println(WiFi.gatewayIP());

  Serial.print("DNS IP: \t");
  Serial.println(WiFi.dnsIP());

  Serial.print("Subnet mask: \t");
  Serial.println(WiFi.subnetMask());
}


void connectionSanity() {
  while (!client.connected()) {
    Serial.println("Connecting...");
    if (client.connect(host, port)) {
      printStatus();
      send_msg("{\"type\": \"move_session\", \"args\": [2077]}");
      send_msg("{\"type\": \"rename_node\", \"args\": [\"rc_car\"]}");
      client.setTimeout(100);
    }
    else
      Serial.println("Connecting timedout!");
  }
}

void setup() {
  Serial.begin(115200);

  bufferIn = newBuffer();
  bufferOut = newBuffer();

  /* Explicitly set the ESP8266 to be a WiFi-client, otherwise, it by default,
     would try to act as both a client and an access-point and could cause
     network-issues with your other WiFi-devices on your WiFi-network. */
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
}



void loop() {
  connectionSanity();

  if (client.available()) {
    recieveBuffer(bufferIn);
    Serial.write(bufferIn->packet, bufferIn->len);
  }
  
  if (Serial.available() > 0) {
    int outLen = Serial.available();
    int newOutLen = 0;
    while (outLen != newOutLen) {
      outLen = newOutLen;
      delay(10);
      newOutLen = Serial.available();
    }

    resizeBuffer(bufferOut, outLen);
    for (int i=0; i<outLen; i++)
      bufferOut->packet[i] = Serial.read();
    sendBuffer(bufferOut);
  }

}
