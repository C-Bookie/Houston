#define WIFI true

#if WIFI
  #include "WiFi.h"

  char ssid[] = "Cherry-Rose"; //  your network SSID (name)
  char pass[] = "DuckandMook";    // your network password (use for WPA, or use as key for WEP)

  int status = WL_IDLE_STATUS;
  WiFiClient client;
#else
  #include <Ethernet.h>
  //TODO: impliment https://arduinojson.org/v5/example/http-client/

  byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
  IPAddress ip(192, 168, 0, 25);

  EthernetClient client;
#endif

IPAddress server(192, 168, 1, 182);
int port = 8089;


#define USING_HEADER false

#if USING_HEADER
  const int HEADER_LEN = 4;
#else
  const int MAX_BUFFER = 256;
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

// Buffer* newBuffer();
// void printBuffer(Buffer* buffer);
// void resizeBuffer(Buffer* buffer, int len);

// void sendBuffer(Buffer* buffer);
// void recieveBuffer(Buffer* buffer);

// void printStatus();
// void connectionSanity();

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

  Serial.print("Recieved: ");
  Serial.write(buffer->packet, buffer->len);
  Serial.println();
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
  #if WIFI
    while (status != WL_CONNECTED) {
      Serial.print("Attempting to connect to SSID: ");
      Serial.println(ssid);
      // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
      status = WiFi.begin(ssid, pass);
      // wait 10 seconds for connection:
      delay(10000);
    }
  #endif

  while (!client.connected()) {
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