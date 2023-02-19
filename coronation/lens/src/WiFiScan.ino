// if the following is seen
// rst:0xc (SW_CPU_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
// it is possible the ESP32 is starved of power when using the WI-FI radio


#include <Arduino.h>

#include <Base64.h>

#include "example.pb.h"

#include <pb_decode.h>
#include <pb_encode.h>

#define WIFI true
#define PRINT false


#if WIFI
  #include "WiFi.h"

  // char ssid[] = "Party!"; //  your network SSID (name)

  // char ssid[] = "Cherry-Rose"; //  your network SSID (name)
  // char pass[] = "DuckandMook";    // your network password (use for WPA, or use as key for WEP)

//   char ssid[] = "BT-6FCJ6X"; //  your network SSID (name)
//   char pass[] = "mHfKDAeMfV74cQ";    // your network password (use for WPA, or use as key for WEP)

  char ssid[] = "VM3877152"; //  your network SSID (name)
  char pass[] = "s7kyTysrddbg";    // your network password (use for WPA, or use as key for WEP)

  // char ssid[] = "leaf"; //  your network SSID (name)
  // char pass[] = "";    // your network password (use for WPA, or use as key for WEP)

  int status = WL_IDLE_STATUS;
  WiFiClient client;
#else
  #include <Ethernet.h>
  //TODO: impliment https://arduinojson.org/v5/example/http-client/

  byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
  IPAddress ip(192, 168, 0, 25);

  EthernetClient client;
#endif



// IPAddress server(192, 168, 5, 1);
IPAddress server(192, 168, 0, 18);
int port = 8089;

#define USING_HEADER true

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
    unsigned int byte_mask = ((1<<8)-1);
    for (int i=0; i<HEADER_LEN; i++)
//       buffer->header[i] = (buffer->len >> (8 * (HEADER_LEN-i-1))) & ((2<<8)-1);
      buffer->header[i] = (buffer->len >> (8 * (HEADER_LEN-i-1))) & byte_mask;
//       buffer->header[i] = (buffer->len >> (8 * i)) & byte_mask;
  #endif

  int size = buffer->len * sizeof(char);
  // void* temp = realloc(buffer->packet, size);  //may need to cast to (unsigned char*)
  buffer->packet = (unsigned char*)realloc(buffer->packet, size);
  // memset(buffer->packet, 0, size);
}

void sendBuffer(Buffer* buffer) {
//   Serial.print("Sending: ");
//   Serial.write(buffer->packet, buffer->len);
//   Serial.print("\n");

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
    unsigned int byte_mask = ((1<<8)-1);
    // fixme printing debugging header
    Serial.print("header: [");
    for (int i=0; i<HEADER_LEN; i++){
        if (i!=0)
            Serial.print(", ");

      Serial.print("0x");
      Serial.print(buffer->header[i], HEX);
      buffer->len |= buffer->header[i] >> (8 * (HEADER_LEN-i-1));
    }
    Serial.print("] translated: ");
    Serial.printf("%d", buffer->len);
    Serial.println();

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
    fill_strip(128, 128, 0);  // YELLOW

    #if WIFI
      while (status != WL_CONNECTED) {
        fill_strip(128, 0, 0);  // RED

        Serial.print("Attempting to connect to SSID: ");
        Serial.println(ssid);
        // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
        if (pass != "")
            WiFi.begin(ssid, pass);
        else
            WiFi.begin(ssid);
        status = WiFi.waitForConnectResult();
        if (status != WL_CONNECTED) {
          Serial.print("Connecting failed with status: ");
          if (status == WL_IDLE_STATUS)
              Serial.println("WL_IDLE_STATUS");
          else if (status == WL_NO_SSID_AVAIL)
              Serial.println("WL_NO_SSID_AVAIL");
          else if (status == WL_SCAN_COMPLETED)
              Serial.println("WL_SCAN_COMPLETED");
          else if (status == WL_CONNECT_FAILED)
              Serial.println("WL_CONNECT_FAILED");
          else if (status == WL_CONNECTION_LOST)
              Serial.println("WL_CONNECTION_LOST");
          else if (status == WL_DISCONNECTED)
              Serial.println("WL_DISCONNECTED");
          else
              Serial.println(WL_CONNECTED);
          listNetworks();
          // wait 1 second for connection:
          delay(1000);
        }
      }
    #endif

    Serial.print("Connecting to ");
    Serial.print(server);
    Serial.print(":");
    Serial.print(port);
    Serial.println("...");
    client.setTimeout(10000);
    if (client.connect(server, port)) {
      Serial.println("Connected");
      fill_strip(0, 128, 0);  // GREEN
      printStatus();

//       unsigned char message[] = "{\"type\": \"subscribe\", \"args\": [\"pitta\"]}";
//       resizeBuffer(bufferOut, 40);
//       memcpy(bufferOut->packet, message, bufferOut->len);
//       sendBuffer(bufferOut);

    } else {
      fill_strip(0, 0, 128);  //BLUE
      Serial.println("Connecting timedout!");
      // wait 1 second for connection:
      delay(1000);
    }
  }
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
    Serial.println(" dBm");
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
// const int BTN_PIN = 35;
const int POT_PIN = 35;

// bool last_btn_state = false;
int last_dial_value = 0;

SensorLog sensor_log = SensorLog_init_zero;

void log_local_sensors() {
//   bool new_btn_state = digitalRead(BTN_PIN);
  int dial_value = analogRead(POT_PIN);

  if (dial_value != last_dial_value) {
        bufferOut->len = SensorLog_size;
        resizeBuffer(bufferOut, bufferOut->len);

//     pb_ostream_t stream = pb_ostream_from_buffer(bufferOut->packet, sizeof(buffer));
    pb_ostream_t stream = pb_ostream_from_buffer(bufferOut->packet, bufferOut->len);
    sensor_log.pot = dial_value;

    Serial.printf("Logging: %d\n", dial_value);


    status = pb_encode(&stream, SensorLog_fields, &sensor_log);
    bufferOut->len = stream.bytes_written;

    if (!status) {
        Serial.printf("Encoding failed: %s\n", PB_GET_ERROR(&stream));
//         return 1;
    } else {
//         sendBuffer(bufferOut);  # todo re-enable


        last_dial_value = dial_value;
    }
  }
}

int counter;

static bool rgb_decode(pb_istream_t *stream, const pb_field_t *field, void **arg) {
//     IntList * dest = (IntList*)(*arg);
    RGBValue rgb_value;


    while (stream->bytes_left)
    {
        status = pb_decode(stream, RGBValue_fields, &rgb_value);

        if (!status) {
            Serial.printf("Decoding failed: %s\n", PB_GET_ERROR(stream));
            return false;
        }
        Serial.printf("RGB %d: (%d, %d, %d)\n", counter, rgb_value.red, rgb_value.green, rgb_value.blue);
        leds[counter] = CRGB(rgb_value.red, rgb_value.green, rgb_value.blue);

        counter += 1;
    }

    return true;
}

LightRequest light_request = LightRequest_init_default;


void parse_command(Buffer* command) {
//   Serial.print("Recieved: ");
//   Serial.write(command->packet, command->len);
//   Serial.println();


//     IntList decodedData = { 0 };
//     light_request.value_array.arg = &decodedData;
    light_request.value_array.funcs.decode = rgb_decode;
//     light_request.value_array.funcs.args = light_request.  // todo
    counter = 0;

    /* Create a stream that reads from the buffer. */
    pb_istream_t stream = pb_istream_from_buffer(command->packet, command->len);

    /* Now we are ready to decode the message. */
    status = pb_decode(&stream, LightRequest_fields, &light_request);

    /* Check for errors... */
    if (!status) {
        Serial.printf("Decoding failed: %s\n", PB_GET_ERROR(&stream));
    }
    else{

    //         Serial.printf("RGB %d: (%d, %d, %d)\n", counter, rgb_value.red, rgb_value.green, rgb_value.blue);
//         leds[counter] = CRGB(rgb_value.red, rgb_value.green, rgb_value.blue);

    FastLED.show();
//         Serial.printf("LightRequest(value_array=[\n");
//         for (size_t i = 0; i < message.lights; i++) {
//           Serial.printf(
//               "  RGBValue(red=%d, green=%d, blue=%d)\n",
//               message.value_array[i].red,
//               message.value_array[i].green,
//               message.value_array[i].blue
//           );
//         }
//         Serial.printf("])\n");
        /* Print the data contained in the message. */
//         Serial.printf("Recieved: %d\n", (int)message.value);
//         for (size_t i = 0; i < message.value_array.size; i++) {
//             // Access the current value using the array index
//             int value = message.value_array.values[i];
//
//             // Use the value as needed
//             Serial.printf("%d,", value);
//         }
//         Serial.printf("\n");
    }

//   // maybe use JsonVariant
//   DynamicJsonDocument doc(2560);  // may be an inappropriate use of MAX_BUFFER
//   DeserializationError error = deserializeJson(doc, command->packet);
//
//   if (error) {
//     Serial.print(F("deserializeJson() failed: "));
//     Serial.println(error.f_str());
//     return;
//   }
//
//   // Serial.println("Parsing command:");
//   // serializeJsonPretty(doc, Serial);
//
//   // Serial.println("Keys:");
//   // for (JsonPair keyValue : doc) {
//   //   Serial.println(keyValue.key().c_str());
//   // }
//
//   const char* type = doc["type"];
//
//   if (String("light") == type) {  // may need to use String.equals()
//     bool light = doc["args"][0];  // light
//     digitalWrite(RED_LED_PIN, light);
//   } else if (String("fast_light") == type) {
//     int size = doc["args"][0]["size"];
//     int offset = doc["args"][0]["offset"];
//
//     for (int i=0; i<size; i++) {
//       char inputString[4];
//       for (int n=0; n<4; n++) {
//           Serial.println((i*4)+n);
//           inputString[n] = doc["args"][0]["values"][(i*4)+n];
//       }
//       char decodedString[3];
//
//       Base64.decode(decodedString, inputString, size*4);
//       leds[i+offset] = CRGB(decodedString[0], decodedString[1], decodedString[2]);  // fixme
//
// //       int r = doc["args"][0]["values"][i][0];
// //       int g = doc["args"][0]["values"][i][1];
// //       int b = doc["args"][0]["values"][i][2];
// //       leds[i+offset] = CRGB(r, g, b);  // fixme
//     }
//     FastLED.show();
//
// //     delete values;
// //     delete inputString;
// //     delete decodedString;
//   }else {
//     Serial.print("Unregognised type: ");
//     Serial.println(type);
//   }
}

void fill_strip(int r, int g, int b) {
  for (int i=0; i<NUM_LEDS; i++) {
    if (i < 10)
        leds[i] = CRGB(r, g, b);
    else
        leds[i] = CRGB(0, 0, 0);
  }
  FastLED.show();
}

void setup() {
  Serial.begin(115200);
  Serial.println("Setting up...");

  FastLED.addLeds<WS2812, LED_STRIP_PIN, GRB>(leds, NUM_LEDS);

  fill_strip(0, 128, 128);  // CYAN

  pinMode(LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
//   pinMode(BTN_PIN, INPUT);
  pinMode(POT_PIN, INPUT);

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

  fill_strip(128, 128, 0);  // YELLOW

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
  
//   if (Serial.available() > 0) {
//     int outLen = Serial.available();
//     int newOutLen = 0;
//     while (outLen != newOutLen) {  // todo wait for new line
//       outLen = newOutLen;
//       delay(10);
//       newOutLen = Serial.available();
//     }
//
//     resizeBuffer(bufferOut, outLen);
//     for (int i=0; i<outLen; i++)
//       bufferOut->packet[i] = Serial.read();
//     sendBuffer(bufferOut);
//   }

  log_local_sensors();

  cycle++;
  delay(10);
}
