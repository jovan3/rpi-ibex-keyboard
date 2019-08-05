#include <Keypad.h>
#include <Wire.h>

const byte ROWS = 2; //four rows
const byte COLS = 5; //three columns
char keys[ROWS][COLS] = {
  {'1', '2', '3', '4', '5'},
  {'6', '7', '8', '9', '0'}
};
byte rowPins[ROWS] = {0, A0}; //connect to the row pinouts of the kpd
byte colPins[COLS] = {2, 3, 4, 5, 6}; //connect to the column pinouts of the kpd

Keypad kpd = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

unsigned long loopCount;
unsigned long startTime;
String msg;
String wireMsg;

#define SLAVE_ADDRESS 0x04
int state = 0;
int number = 0;
char keyVal = 0;


void setup() {
  pinMode(10, OUTPUT);

  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(sendData1);
  //  Wire.onReceive(receiveData);
  Wire.onReceive(receiveEvent);

  Serial.begin(9600);
  loopCount = 0;
  startTime = millis();
  msg = "";
}

volatile byte buf [32];
char transmitBuf[32];


// called by interrupt service routine when incoming data arrives
void receiveEvent (int howMany)
{
  for (byte i = 0; i < howMany; i++)
  {
    buf [i] = Wire.read();
  }  // end of for loop
}  // end of receiveEvent

void sendData1() {
  Wire.write(keyVal);
}

void loop() {
  loopCount++;
  if ( (millis() - startTime) > 5000 ) {
    Serial.print("Average loops per second = ");
    Serial.println(loopCount / 5);
    startTime = millis();
    loopCount = 0;

    for (int i = 0; i < 32; i++) {
      Serial.print(buf[i]);
    }
    Serial.println();
  }

  // Fills kpd.key[ ] array with up-to 10 active keys.
  // Returns true if there are ANY active keys.
  if (kpd.getKeys())
  {
    for (int i = 0; i < LIST_MAX; i++) // Scan the whole key list.
    {
      if ( kpd.key[i].stateChanged )   // Only find keys that have changed state.
      {
        switch (kpd.key[i].kstate) {  // Report active key state : IDLE, PRESSED, HOLD, or RELEASED
          case PRESSED:
            msg = " PRESSED.";
            break;
          case HOLD:
            msg = " HOLD.";
            break;
          case RELEASED:
            msg = " RELEASED.";
            break;
          case IDLE:
            msg = " IDLE.";
        }

        wireMsg = kpd.key[i].kchar + " " + msg;
        wireMsg.toCharArray(transmitBuf, wireMsg.length());

        keyVal = kpd.key[i].kchar;
      }
    }

    digitalWrite(10, HIGH);
    digitalWrite(10, LOW);
    digitalWrite(10, HIGH);
  }
}  // End loop
