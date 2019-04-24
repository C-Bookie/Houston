#include <Ethernet.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192, 168, 1, 234);
IPAddress server(192, 168, 1, 233);
int port = 8089;

const int MAX_BUFFER = 256;
const int HEADER_SIZE = 4;  // 0 to disable header
unsigned char* headerBuffer;
unsigned char* packetBuffer = 0;
int packetIndex = 0;
int packetLen = 0;
int packetSize = 0;

EthernetClient client;

void resetBuffer(int length) {
  packetIndex = 0;
  packetLen = length;
  packetSize = packetLen * sizeof(char);
  if (packetBuffer != 0)
    packetBuffer = (unsigned char*) realloc(packetBuffer, packetSize);
  else
    packetBuffer = (unsigned char*) malloc(packetSize);
  memset(packetBuffer, 0, packetSize);

  int i = 0;
  while (i < HEADER_SIZE) {
    headerBuffer[i] = (packetLen >> (8 * (HEADER_SIZE-i-1))) & ((2<<8)-1);
    i++;
  }
}

void addToBuffer(char msg) {
  packetBuffer[packetIndex] = msg;
  packetIndex++;
}

void sendBuffer() {
  Serial.print("Sending: ");
  Serial.write(packetBuffer, packetSize);
  Serial.print("\n");
  client.write(headerBuffer, HEADER_SIZE);
  client.write(packetBuffer, packetSize);
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
  headerBuffer = (unsigned char*) malloc(HEADER_SIZE * sizeof(char));
  Ethernet.begin(mac, ip);
  //  Ethernet.begin(mac);
  Serial.begin(9600);
  delay(1000);
  Serial.setTimeout(10);
}

void connectionSanity() {
  while (!client.connected()) {
    Serial.println("Connecting...");
    if (client.connect(server, port)) {
      Serial.println("Connected");
      printStatus();
    }
    else
      Serial.println("Connecting timedout!");
  }
  client.setTimeout(100);
}

void loop() {
  connectionSanity();
  
  if (client.available()) {
    unsigned char size[HEADER_SIZE];
    client.read(size, HEADER_SIZE);
    char msg = client.read();
    Serial.println(msg);
  }
  
  if (Serial.available() > 0) {
    resetBuffer(Serial.available());
    while (Serial.available() > 0)
      addToBuffer(Serial.read());
    sendBuffer();
  }
  
}
