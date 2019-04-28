#include <Ethernet.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192, 168, 1, 234);
IPAddress server(192, 168, 1, 233);
int port = 8089;

const int MAX_BUFFER = 256;
const int HEADER_SIZE = 4;  // 0 to disable header

unsigned char* inHeaderBuffer = 0;
unsigned char* inPacketBuffer = 0;
int inLen = 0;
int inSize = 0;

unsigned char* outHeaderBuffer = 0;
unsigned char* outPacketBuffer = 0;
int outLen = 0;
int outSize = 0;

// const int LED_BUILTIN = 13;
int cycle = 0;

EthernetClient client;

void makeBuffer(unsigned char* buffer, int len) {
  int size = len * sizeof(char);
  if (buffer == 0)
    buffer = (unsigned char*) malloc(size);
  else
    buffer = (unsigned char*) realloc(buffer, size);
  memset(buffer, 0, size);
}

void encodeHeader(unsigned char* headerBuffer, int len) {
  for (int i=0; i<HEADER_SIZE; i++)
    headerBuffer[i] = (len >> (8 * (HEADER_SIZE-i-1))) & ((2<<8)-1);
}

int decodeHeader(unsigned char* headerBuffer) {
  int size = 0;
  for (int i=0; i<HEADER_SIZE; i++) {
    Serial.println((8 * (HEADER_SIZE-i-1)));
    Serial.println(headerBuffer[i]);
    size |= headerBuffer[i] >> (8 * (HEADER_SIZE-i-1));
  }
  return size;
}

void sendPacket(unsigned char* packetBuffer, unsigned char* headerBuffer, int len) {
  Serial.print("Sending: ");
  Serial.write(packetBuffer, len);
  Serial.print("\n");

  encodeHeader(headerBuffer, len);
  client.write(headerBuffer, HEADER_SIZE);
  client.write(packetBuffer, len);
}

int recievePacket(unsigned char* packetBuffer, unsigned char* headerBuffer) {
  client.read(headerBuffer, HEADER_SIZE);
  int len = decodeHeader(headerBuffer);
  makeBuffer(packetBuffer, len);
  client.read(packetBuffer, len);
  return len;
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

void connectionSanity() {
  while (!client.connected()) {
    Serial.println("Connecting...");
    if (client.connect(server, port))
      printStatus();
    else
      Serial.println("Connecting timedout!");
  }
  client.setTimeout(100);
}


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  makeBuffer(inHeaderBuffer, HEADER_SIZE);
  makeBuffer(outHeaderBuffer, HEADER_SIZE);
  Ethernet.begin(mac, ip);
  //  Ethernet.begin(mac);
  Serial.begin(9600);
  delay(1000);
  // Serial.setTimeout(10);
}

void loop() {
  Serial.print("Cycle: ");
  Serial.println(cycle, DEC);
  digitalWrite(LED_BUILTIN, cycle%2==0);
  connectionSanity();
  
  if (client.available()) {
    inLen = recievePacket(inPacketBuffer, inHeaderBuffer);
    Serial.write(inPacketBuffer, inLen);
  }
  
  if (Serial.available() > 0) {
    outLen = Serial.available();
    makeBuffer(outPacketBuffer, outLen);
    Serial.println(outPacketBuffer[0], DEC);
    for (int i=0; i<outLen; i++)
      outPacketBuffer[i] = Serial.read();
    sendPacket(outPacketBuffer, outHeaderBuffer, outLen);
  }
  cycle++;  
}
