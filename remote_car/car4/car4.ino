// #include "SerialDebug.h"


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

//const int LED_BUILTIN = 13;
int cycle = 0;


// RC-Values
int In1 = 2;
int In2 = 3;
int En1 = 5;

int In4 = 8;
int In3 = 9;
int En2 = 6;

String val1 = "";
String val2 = "";

int left = 0;
int right = 0;


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


void setup() {
  Serial.begin(115200);

  pinMode(LED_BUILTIN, OUTPUT);

  //RC-setup
  pinMode(En1,OUTPUT);
  pinMode(In1,OUTPUT);
  pinMode(In2,OUTPUT);
  pinMode(En2,OUTPUT);
  pinMode(In3,OUTPUT);
  pinMode(In4,OUTPUT);

  bufferIn = newBuffer();
  bufferOut = newBuffer();

  delay(1000);
  // Serial.setTimeout(10);
}


void loop() {
//  Serial.print("Cycle: ");
//  Serial.println(cycle, DEC);
  digitalWrite(LED_BUILTIN, cycle%2==0);


  if (Serial.available() > 0) {
    int outLen = Serial.available();
    int newOutLen = 0;
    while (outLen != newOutLen) {
      outLen = newOutLen;
      delay(10);
      newOutLen = Serial.available();
    }

    resizeBuffer(bufferIn, outLen);
    for (int i=0; i<outLen; i++)
      bufferIn->packet[i] = Serial.read();

//    Serial.write(bufferIn->packet, bufferIn->len);

    val1 = "";
    val2 = "";

    bool first = true;
    for (int i = 0; i < bufferIn->len-1; ++i) {
      if (bufferIn->packet[i] != '"') {
        if (bufferIn->packet[i] == '|')
          first = false;
        else {
          if (first)
            val1 += bufferIn->packet[i];
          else
            val2 += bufferIn->packet[i];
        }
      }
    }
    left = val1.toInt();
    right = val2.toInt();

    digitalWrite(In1, left > 0);
    digitalWrite(In2, left < 0);
    analogWrite(En1, abs(left));

    digitalWrite(In3, right > 0);
    digitalWrite(In4, right < 0);
    analogWrite(En2, abs(right));
  }

  cycle++;  
}
