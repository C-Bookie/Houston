#include <Ethernet.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress server(192,168,1,233); 
int port = 8089;

EthernetClient client;

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
//  Ethernet.begin(mac, ip);
  Ethernet.begin(mac);
  Serial.begin(9600);
  delay(1000);
  Serial.println("Connecting...");

  if (client.connect(server, port)) {
    Serial.println("Connected");
    printStatus();
  } 
  else {
    Serial.println("Connection failed!");
  }
}

void sendChar(char msg) {
  Serial.print("Sending: ");
  Serial.println(String(msg));
  client.print(msg);
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
      int size = Serial.available();
      int i = 0;
      while (i < 4) {
        Serial.println(String((size >> (8 ^ i)) % 8, HEX));
        sendChar((size >> (8 * i)) % 8);
        i++;
      }
      while (Serial.available() > 0) {
        sendChar(Serial.read());
      }
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
    while(true);
  }
}
