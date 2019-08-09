#include <Keypad.h>
#include <Wire.h>

const int PRESSED_OFFSET = 100;
const int NOT_PRESSED_OFFSET = 0;
const int INT_GPIO = 13;

const byte ROWS = 5; //four rows
const byte COLS = 10; //three columns
char keys[ROWS][COLS] = {
  {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
  {11, 12, 13, 14, 15, 16, 17, 18, 19, 20},
  {21, 22, 23, 24, 25, 26, 27, 28, 29, 30},
  {31, 32, 33, 34, 35, 36, 37, 38, 39, 40},
  {41, 42, 43, 44, 45, 46, 47, 48, 49, 50},
};
byte rowPins[ROWS] = {A0, A1, A2, A3, 0}; //connect to the row pinouts of the kpd
byte colPins[COLS] = {11, 10, 9, 8, 7, 6, 5, 4, 3, 2}; //connect to the column pinouts of the kpd

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
  pinMode(INT_GPIO, OUTPUT);

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


        digitalWrite(INT_GPIO, LOW);
        delay(5);
        digitalWrite(INT_GPIO, HIGH);
      }
    }
  }
}
