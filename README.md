# ASCII-Wires: The Direct-Stream Poem Project
## Bit-Paced Serial Transfer & Direct GPIO Inter-Device Signaling

A hands-on embedded-systems project that demonstrates **direct serial data ingest and hardware signaling between microcontrollers** using a Mac (PyCharm), an **Arduino Uno R3**, and a **BBC micro:bit V1/V2**.

## 📌 Project Overview

This project explores how a computer script can stream dynamically generated data into an entry-level microcontroller over standard serial protocols, and use hardware-level digital state changes to trigger multi-screen status indicators across platform families.

The system loops through four distinct stages:
1. **PyCharm (Mac):** Generates a grammatically aligned random poem and streams it character-by-character over a direct USB line.
2. **Arduino Uno R3 (The Core Receiver):** Collects the text into an isolation software ring buffer to completely bypass the 64-byte hardware limit, typing it out at a readable human pace on an I2C LCD screen.
3. **The Stop Marker (`#`):** Signals to the Arduino that transmission is complete.
4. **The micro:bit (Status Node):** Monitors a direct digital input pin from the Arduino. When the pin transitions to `HIGH`, the micro:bit swaps its waiting display to a giant checkmark (**Tick**).

The project is a practical demonstration of:
* Software-driven hardware buffer overflow management
* Multi-platform logic levels and shared ground references
* Continuous background loop sampling inside MakeCode JavaScript (JS)
* Grammatically constrained lexical matrix generators

## ⚙️ How It Works

```text
+-----------------------+              +-----------------------+              +-------------------+

|     Mac Laptop        |  USB Serial  |   Arduino Uno R3      |  Digital Pin |   BBC micro:bit   |
|   (PyCharm Python)    | ------------>| (Paced Typing Engine) | ------------>|    (Pin P0 Input) |
|  [Poem Generator Code]|  (9600 Baud) |  [Prints to I2C LCD]  |  (HIGH Signal)   | [Displays a Tick] |
+-----------------------+              +-----------------------+              +-------------------+
```

### 1. Pacing the Pipeline
Because the Arduino's hardware interface caps input arrays at **64 bytes**, the Python script paces its output stream by injecting a **25ms delay** between characters. This keeps the incoming buffer cleared while printing.

### 2. Typing Engine
The Arduino continuously sweeps characters out of the serial cache and feeds them into a 256-byte circular array. It applies a non-blocking `millis()` tracking window to step through the array indices every **150ms**, producing a sleek "typing" animation on the LCD without blocking the chip.

## 🔌 Hardware Connection & Pinout

```text
[Arduino Uno R3]                            [BBC micro:bit]
      5V  ------------------------------->    VCC / 3V Pad
     GND  ------------------------------->    GND Pad
  Pin D3  ------------------------------->    Pin P0 Pad

[Arduino Uno R3]                            [I2C LCD Display]
  Pin A4 (SDA) -------------------------->    SDA
  Pin A5 (SCL) -------------------------->    SCL
```

> ⚠️ **Important Wiring Note:** Connecting a common ground (`GND`) wire between all active platforms is absolutely mandatory to prevent floating logic states and noise disruption. 

## 📂 Project Structure

```text
├── arduino/
│   └── lcd_receiver.ino     # Non-blocking ring buffer typing engine
│
├── microbit/
│   └── tick_display.js      # MakeCode JavaScript pin monitoring script
│
├── python/
│   └── poem_sender.py       # Paced character stream generator
│
└── README.md
```

## 💻 Source Code

### 1. Python Sender Script (`python/poem_sender.py`)
Run this script locally on your machine inside **PyCharm**.

```python
import random
import time
import serial

def generate_perfect_poem(subject="nature"):
    adjectives_vowel = ["ancient", "enchanted", "infinite", "emerald", "unfading"]
    adjectives_consonant = ["shimmering", "whispering", "golden", "serene", "mystic", "gentle", "bright", "silent", "velvet"]
    singular_nouns = ["leaf", "star", "river", "mountain", "dream", "wind", "flower", "shadow", "spirit", "echo", "heart", "melody"]
    plural_nouns = ["leaves", "stars", "rivers", "mountains", "dreams", "winds", "flowers", "shadows", "echoes", "melodies"]
    verbs_plural_noun = ["dance", "sing", "dream", "flow", "rise", "whisper", "glow", "sleep", "awaken", "bloom"]
    verbs_active = ["takes flight", "drifts away", "unfurls", "soars high", "watches close"]

    adj1 = random.choice(adjectives_vowel + adjectives_consonant)
    line1 = f"Oh {adj1} {subject.lower()} so grand,"

    p_noun = random.choice(plural_nouns)
    p_verb = random.choice(verbs_plural_noun)
    line2 = f"Where {p_noun} {p_verb} in the breeze,"

    adj2_vowel = random.choice(adjectives_vowel)
    adj2_consonant = random.choice(adjectives_consonant)
    s_noun = random.choice(singular_nouns)
    v_active = random.choice(verbs_active)
    
    if random.choice([True, False]):
        line3 = f"An {adj2_vowel} {s_noun} {v_active},"
    else:
        line3 = f"A {adj2_consonant} {s_noun} {v_active},"

    p_noun2 = random.choice(plural_nouns)
    line4 = f"Secrets that the {p_noun2} keep."

    return f"{line1} {line2} {line3} {line4}"

SERIAL_PORT = '/dev/cu.usbmodem14201'  # Mac port assignment
BAUD_RATE = 9600      

try:
    poem_output = generate_perfect_poem("ocean")
    print(f"Generated text:\n{poem_output}\n")
    
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # Give the bootloader time to pass control
    
    payload = poem_output.strip() + "#"
    print("Pacing transmission over USB link to prevent buffer overflow...")
    
    for char in payload:
        ser.write(char.encode('utf-8'))
        ser.flush()
        time.sleep(0.025) # 25ms delay
        
    ser.close()
    print("Sent successfully!")
except Exception as e:
    print(f"Error: {e}")
```

### 2. Arduino Core Engine (`arduino/lcd_receiver.ino`)
Upload this code to your **Arduino Uno R3**.

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

const int triggerPin = 3; 
LiquidCrystal_I2C lcd(0x27, 16, 2);

char textBuffer[256];
int writeIndex = 0;
int readIndex = 0;

int lcdColumn = 0;
int lcdRow = 0;
bool isPrintingPoem = false;

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
  while (Serial.available() > 0) {
    char c = Serial.read();
    textBuffer[writeIndex] = c;
    writeIndex = (writeIndex + 1) % 256; 
  }

  if (readIndex != writeIndex) {
    if (millis() - lastPrintTime >= printInterval) {
      lastPrintTime = millis(); 

      char nextChar = textBuffer[readIndex];
      readIndex = (readIndex + 1) % 256; 

      if (!isPrintingPoem) {
        lcd.clear();
        lcdColumn = 0;
        lcdRow = 0;
        isPrintingPoem = true;
        digitalWrite(triggerPin, LOW); 
      }

      if (nextChar == '#') {
        digitalWrite(triggerPin, HIGH); 
        isPrintingPoem = false;         
      } 
      else if (nextChar >= 32 && nextChar <= 126) {
        lcd.setCursor(lcdColumn, lcdRow);
        lcd.print(nextChar);
        lcdColumn++;

        if (lcdColumn >= 16) {
          lcdColumn = 0;
          lcdRow++;
        }

        if (lcdRow >= 2) {
          lcd.clear();
          lcdColumn = 0;
          lcdRow = 0;
        }
      }
    }
  }
}
```

### 3. micro:bit Script (`microbit/tick_display.js`)
Paste this code inside the **JavaScript tab** of the MakeCode editor.

```typescript
basic.showIcon(IconNames.Square) // Square = Waiting for data stream

basic.forever(function () {
    // Poll input status on Pin 0
    if (pins.digitalReadPin(DigitalPin.P0) == 1) {
        basic.showIcon(IconNames.Yes) // Message complete. Flash the Tick!
    } else {
        basic.showIcon(IconNames.Square)
    }
    basic.pause(100) 
})
```

## 🦾 Requirements & Cross-Platform Hardware Support
* **micro:bit:** V1 or V2 matching configurations.
* **I2C LCD Display:** Based on MCP23008/PCF8574 chip lines at address `0x27` (16x2 grid configuration).
* **Alligator Clips & Jumpers**
* **Supported Core Devices:** 
  * Arduino Uno R3, Nano V3, Pro Mini, Elegoo Clone Uno R3 boards, SparkFun RedBoard lines, and Adafruit Metro 328 arrays.

## 📄 Personal Project Notes

This repository was put together for learning, fun, and optimization **by an 11-year-old developer.** No beef with the [ESP-32 storyteller project](https://github.com/slvDev/esp32-ai)—this is just the foundational stage of a much larger vision!

### 🗺️ The Project Road Map
* **Step 1:** Transfer raw binary ASCII values across physical terminal lines. (**Done**)
* **Step 2:** Construct an autonomous language model generator template block. (**Done**)
* **Step 3:** Figure out how to sync cloud code streams straight into a local micro:bit loop. (**Done**)
* **Step 4:** Build a fully independent desktop Poem Matrix generator system! (**Done**)

I specifically opted to build this using an ATMega328P profile platform paired with basic C++ interfaces, instead of scaling up to massive Linux-based processing engines like a Raspberry Pi 5 or an AI HAT+ expansion shield. Stripping down the architecture makes it significantly more challenging—and much more rewarding when the full string processes flawlessly!

