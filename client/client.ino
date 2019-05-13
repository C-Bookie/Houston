#include <Ethernet.h>
//TODO: impliment https://arduinojson.org/v5/example/http-client/

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192, 168, 1, 235);
IPAddress server(192, 168, 1, 233);
int port = 8089;

const int MAX_BUFFER = 256;

const int HEADER_LEN = 4 * sizeof(char);  // 0 to disable header
const int HEADER_SIZE = HEADER_LEN * sizeof(char);

struct Buffer {  // pass by reference
  unsigned char* packet;
  unsigned char* header;
  int len;
};

struct Buffer *bufferIn;
struct Buffer *bufferOut;

// const int LED_BUILTIN = 13;
int cycle = 0;

EthernetClient client;


Buffer* newBuffer() {
  Buffer* buffer = (Buffer*)malloc(sizeof(Buffer));
  *buffer = Buffer {
    .packet = NULL,
    .header = (unsigned char*)malloc(HEADER_SIZE),
    .len = 0
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
  for (int i=0; i<HEADER_LEN; i++)
    buffer->header[i] = (buffer->len >> (8 * (HEADER_LEN-i-1))) & ((2<<8)-1);

  int size = buffer->len * sizeof(char);
  void* temp = realloc(buffer->packet, size);  //may need to cast to (unsigned char*)
  buffer->packet = (unsigned char*)realloc(buffer->packet, size);
  // memset(buffer->packet, 0, size);
}

void sendBuffer(Buffer* buffer) {
  Serial.print("Sending: ");
  Serial.write(buffer->packet, buffer->len);
  Serial.print("\n");

  client.write(buffer->header, HEADER_LEN);
  client.write(buffer->packet, buffer->len);
}

void recieveBuffer(Buffer* buffer) {
  client.read(buffer->header, HEADER_LEN);
  buffer->len = 0;
  for (int i=0; i<HEADER_LEN; i++){
    buffer->len |= buffer->header[i] >> (8 * (HEADER_LEN-i-1));
  }

  resizeBuffer(buffer, buffer->len);
  client.read(buffer->packet, buffer->len);

  Serial.print("Recieved: ");
  Serial.write(buffer->packet, buffer->len);
  Serial.println();
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
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  bufferIn = newBuffer();
  bufferOut = newBuffer();

  Ethernet.begin(mac, ip);
  //  Ethernet.begin(mac);
  delay(1000);
  // Serial.setTimeout(10);
}

void loop() {
  connectionSanity();
//  Serial.print("Cycle: ");
//  Serial.println(cycle, DEC);
  digitalWrite(LED_BUILTIN, cycle%2==0);
  
  if (client.available()) {
    recieveBuffer(bufferIn);
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
  cycle++;  
}
