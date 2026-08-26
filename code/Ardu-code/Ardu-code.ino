#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int triggerPin = 3; // Connect this physically to Micro:bit Pin P0
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Secure 256-byte software queue structure
char textBuffer[256];
int writeIndex = 0;
int readIndex = 0;

int lcdColumn = 0;
int lcdRow = 0;
bool isPrintingPoem = false;

// Timing metrics for readable layout presentation (150ms)
unsigned long lastPrintTime = 0;
const unsigned long printInterval = 150; 

void setup() {
  Serial.begin(9600); 
  pinMode(triggerPin, OUTPUT);
  digitalWrite(triggerPin, LOW);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Waiting...");
}

void loop() {
  // Gather incoming paced text immediately from USB
  while (Serial.available() > 0) {
    char c = Serial.read();
    textBuffer[writeIndex] = c;
    writeIndex = (writeIndex + 1) % 256; 
  }

  // Presentation Typing Engine
  if (readIndex != writeIndex) {
    if (millis() - lastPrintTime >= printInterval) {
      lastPrintTime = millis(); 

      char nextChar = textBuffer[readIndex];
      readIndex = (readIndex + 1) % 256; 

      // Wipe screen on a brand new data arrival strike
      if (!isPrintingPoem) {
        lcd.clear();
        lcdColumn = 0;
        lcdRow = 0;
        isPrintingPoem = true;
        digitalWrite(triggerPin, LOW); // Drop old checkmark state
      }

      // Check for our custom end-of-message flag
      if (nextChar == '#') {
        digitalWrite(triggerPin, HIGH); // Signal Micro:bit Pin P0!
        isPrintingPoem = false;         // Reset loop tracker for next execution
      } 
      // Handle standard readable text characters
      else if (nextChar >= 32 && nextChar <= 126) {
        lcd.setCursor(lcdColumn, lcdRow);
        lcd.print(nextChar);
        lcdColumn++;

        // Row wrapping logic
        if (lcdColumn >= 16) {
          lcdColumn = 0;
          lcdRow++;
        }

        // Screen overflow clearing logic
        if (lcdRow >= 2) {
          lcd.clear();
          lcdColumn = 0;
          lcdRow = 0;
        }
      }
    }
  }
}
