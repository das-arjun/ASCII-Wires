#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int signalPin = 2;

const unsigned long BIT_TIME = 50;
const unsigned long START_TIME = 150;

LiquidCrystal_I2C lcd(0x27, 16, 2);

int lcdColumn = 0;
int lcdRow = 0;

void setup() {
  pinMode(signalPin, INPUT);

  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("Waiting...");
}

void loop() {

  if (digitalRead(signalPin) == HIGH) {

    // Measure start pulse
    unsigned long t = millis();

    while (digitalRead(signalPin) == HIGH);

    unsigned long length = millis() - t;

    // Detect start pulse
    if (length > 100 && length < 250) {

      byte data = 0;

      // Move to middle of first bit
      delay(BIT_TIME);

      // Read 8 bits
      for (int i = 0; i < 8; i++) {

        data = data << 1;

        if (digitalRead(signalPin)) {
          data |= 1;
        }

        delay(BIT_TIME);
      }

      char c = (char)data;

      // Display printable characters only
      if (c >= 32 && c <= 126) {

        lcd.setCursor(lcdColumn, lcdRow);
        lcd.print(c);

        lcdColumn++;

        // Move to second row
        if (lcdColumn >= 16) {
          lcdColumn = 0;
          lcdRow++;
        }

        // Reset after full screen
        if (lcdRow >= 2) {
          lcd.clear();
          lcdColumn = 0;
          lcdRow = 0;
        }
      }
    }
  }
}
