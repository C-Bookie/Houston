#include <Ethernet.h>

byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
IPAddress ip(192,168,1,234); 
IPAddress server(192,168,1,233); 
int port = 8089;

EthernetClient client;

void setup() {
  Ethernet.begin(mac, ip);
//  Ethernet.begin(mac);
  Serial.begin(9600);
  delay(1000);
  Serial.println("Connecting...");

  if (client.connect(server, port)) {
    Serial.println("Connected");
  } 
  else {
    Serial.println("Connection failed!");
  }
}

void loop() {
  if (client.available()) {
    char c = client.read();
    Serial.print(c);
  }

  while (Serial.available() > 0) {
    char inChar = Serial.read();
    if (client.connected()) {
      client.print(inChar); 
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
