int In1 = 8;
int In2 = 9;
int En1 = 5;

int In4 = 10;
int In3 = 11;
int En2 = 6;

//const int LED_BUILTIN = 13;
int cycle = 0;

String val1 = "";
String val2 = "";

int x = 0;
int y = 0;


void setup() {  
  pinMode(En1,OUTPUT);
  pinMode(In1,OUTPUT);
  pinMode(In2,OUTPUT);
  pinMode(En2,OUTPUT);
  pinMode(In3,OUTPUT);
  pinMode(In4,OUTPUT);
  
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    val1 = Serial.readStringUntil('|');
    Serial.read(); 
    val2 = Serial.readStringUntil('\n'); 
    Serial.println(val1 + '|' + val2);

    x = val1.toInt();
    y = val2.toInt();

    digitalWrite(In1, x > 0);
    digitalWrite(In2, x < 0);
    analogWrite(En1, abs(x));

    digitalWrite(In3, y > 0);
    digitalWrite(In4, y < 0);
    analogWrite(En2, abs(y));

    cycle++;
    digitalWrite(LED_BUILTIN, cycle%2==0);
  }
}
