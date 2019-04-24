#include <Ethernet.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192, 168, 1, 234);
IPAddress server(192, 168, 1, 233);
int port = 8089;

const int MAX_BUFFER = 256;
const int HEADER_SIZE = 4;  // 0 to disable header
unsigned char* packetBuffer = 0;
int packetIndex = 0;
int packetLen = 0;
int packetSize = 0;

EthernetClient client;

void makeBuffer(int length) {
  packetLen = length + 256;
  Serial.print("Packet Length: \t");
  Serial.println(packetLen);
  packetSize = (packetLen * sizeof(char)) + HEADER_SIZE;
  if (packetBuffer != 0)
    packetBuffer = (unsigned char*) realloc(packetBuffer, packetSize);
  else
    packetBuffer = (unsigned char*) malloc(packetSize);
  Serial.println(String(sizeof(packetBuffer)));
  Serial.println(String(packetSize));
  memset(packetBuffer, 0, packetSize);
  packetIndex = 0;
  while (packetIndex < HEADER_SIZE)
    addToBuffer((packetLen >> (8 * (HEADER_SIZE-packetIndex-1))) & ((2<<8)-1));
}

void addToBuffer(char msg) {
//  Serial.print("Before: ");
//  Serial.println(packetBuffer);
  Serial.print("Char: ");
  Serial.println(String(msg, HEX));
  packetBuffer[packetIndex] = msg;
  packetIndex++;
//  Serial.print("After: ");
//  Serial.println(packetBuffer);
  Serial.print("Length: ");
  Serial.println(String(sizeof(packetBuffer)));
}

void sendBuffer() {
  Serial.print("Sending: ");
  Serial.write(packetBuffer, packetSize);
  client.write(packetBuffer, packetSize);  // fixme: spcify length
}

void printStatus() {
  Serial.print("Local IP: \t");
  Serial.println(Ethernet.localIP());

  Serial.print("Gateway IP: \t");
  Serial.println(Ethernet.gatewayIP());

  Serial.print("DNS server IP: \t");
  Serial.println(Ethernet.dnsServerIP());

  Serial.print("Subnet mask: \t");
  Serial.println(Ethernet.subnetMask());
}


void setup() {
  Ethernet.begin(mac, ip);
  //  Ethernet.begin(mac);
  Serial.begin(9600);
  delay(1000);
  Serial.println("Connecting...");

  if (client.connect(server, port)) {
    Serial.println("Connected");
    printStatus();
  }
  else
    Serial.println("Connection failed!");
}

void loop() {
  if (client.available()) {
    unsigned char size[4];
    client.read(size, 4);
    char msg = client.read();
    Serial.println(msg);
  }

  if (Serial.available() > 0) {
    if (client.connected()) {
      makeBuffer(Serial.available());
      while (Serial.available() > 0)
        addToBuffer(Serial.read());
      sendBuffer();
    }
    else {
      Serial.println("Error!");
    }
  }

  if (!client.connected()) {
    Serial.println();
    Serial.println("Disconnecting");
    client.stop();
    Serial.println("Disconnected");
    while (true);
  }
}
