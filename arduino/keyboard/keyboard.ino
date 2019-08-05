#include <Keypad.h>
#include <Wire.h>

const int PRESSED_OFFSET = 100;
const int NOT_PRESSED_OFFSET = 0;

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

#define SLAVE_ADDRESS 0x04
int state = 0;
int number = 0;
char keyVal = 0;
int currentPressedOffset = 0;

void setup() {
  pinMode(10, OUTPUT);

  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(sendData);

  Serial.begin(9600);
  loopCount = 0;
  startTime = millis();
  msg = "";
}

void sendData() {
  Wire.write(keyVal);
}

void loop() {
  loopCount++;
  if ( (millis() - startTime) > 5000 ) {
    Serial.print("Average loops per second = ");
    Serial.println(loopCount / 5);
    startTime = millis();
    loopCount = 0;
  }

  // Fills kpd.key[ ] array with up-to 10 active keys.
  // Returns true if there are ANY active keys.
  if (kpd.getKeys())
  {
    for (int i = 0; i < LIST_MAX; i++) // Scan the whole key list.
    {
      if ( kpd.key[i].stateChanged )   // Only find keys that have changed state.
      {
        switch (kpd.key[i].kstate) {
          case PRESSED:
            msg = " PRESSED.";
            currentPressedOffset = PRESSED_OFFSET;
            break;
          case RELEASED:
            msg = " RELEASED.";
            currentPressedOffset = NOT_PRESSED_OFFSET;
            break;
          default:
            continue;
        }

        Serial.print(kpd.key[i].kchar);
        Serial.println(msg);

        keyVal = kpd.key[i].kchar + currentPressedOffset;


        digitalWrite(10, LOW);
        delay(5);
        digitalWrite(10, HIGH);
      }
    }
  }
}
