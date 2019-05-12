#include <Ethernet.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192, 168, 1, 235);
IPAddress server(192, 168, 1, 233);
int port = 8089;

const int MAX_BUFFER = 256;
const int HEADER_SIZE = 4;  // 0 to disable header

struct Buffer {  // pass by reference
  unsigned char* packet;
  unsigned char* header;
  int length;
  int size;
}

Buffer bufferIn = Buffer{NULL, NULL, 0, 0};
Buffer bufferOut = Buffer{NULL, NULL, 0, 0};

// const int LED_BUILTIN = 13;
int cycle = 0;

EthernetClient client;

void buildBuffer(Buffer* buffer, int len) {
  buffer->len = len;
  for (int i=0; i<HEADER_SIZE; i++)
    buffer->header[i] = (buffer->len >> (8 * (HEADER_SIZE-i-1))) & ((2<<8)-1);

  int size = buffer->len * sizeof(char)
  buffer = realloc(buffer->packet, size);  //may need to cast to (unsigned char*)
  // memset(buffer->packet, 0, size);
}

void sendBuffer(Buffer* buffer) {
  Serial.print("Sending: ");
  Serial.write(buffer->packet, buffer->len);
  Serial.print("\n");

  client.write(buffer->header, HEADER_SIZE);
  client.write(buffer->packet, buffer->len);
}

void recievePacket(Buffer* buffer) {
  client.read(buffer->header, HEADER_SIZE);
  for (int i=0; i<HEADER_SIZE; i++)
    buffer->len |= buffer->header[i] >> (8 * (HEADER_SIZE-i-1));

  packetBuffer = makeBuffer(buffer->packet, buffer->len);
  client.read(buffer->packet, buffer->len);

  Serial.print("Recieved: ");
  Serial.write(buffer->packet, buffer->len);
  Serial.print("\n");
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
  bufferIn.header = memalloc(HEADER_SIZE);
  bufferOut.header = memalloc(HEADER_SIZE);

  Ethernet.begin(mac, ip);
  //  Ethernet.begin(mac);
  Serial.begin(9600);
  delay(1000);
  // Serial.setTimeout(10);
}

void loop() {
  connectionSanity();
//  Serial.print("Cycle: ");
//  Serial.println(cycle, DEC);
  digitalWrite(LED_BUILTIN, cycle%2==0);
  
  if (client.available()) {
    recievePacket(bufferIn);
    Serial.write(bufferIn.packet, bufferIn.len);
  }
  
  if (Serial.available() > 0) {
    outLen = Serial.available();
    int newOutLen = 0;
    while (outLen != newOutLen) {
      outLen = newOutLen;
      delay(10);
      newOutLen = Serial.available();
    }

    buildBuffer(bufferOut, outLen);
    for (int i=0; i<outLen; i++)
      bufferOut.packet[i] = Serial.read();
    sendPacket(bufferOut);
  }
  cycle++;  
}
