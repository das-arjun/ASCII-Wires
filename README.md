# ASCII-Wires: The Direct-Stream Poem Project
## Bit-Paced Serial Transfer & Non-Blocking LCD Buffer Management

A hands-on embedded-systems project that demonstrates **direct serial data ingest and non-blocking hardware presentation** using a Mac (PyCharm) and an **Arduino Uno R3** driving an I2C LCD screen.

## 📌 Project Overview

This project explores how a computer script can stream dynamically generated data into an entry-level microcontroller over standard serial protocols without relying on massive computing platforms.

The system loops through three distinct stages:
1. **PyCharm (Mac):** Generates a grammatically aligned random poem and streams it character-by-character over a direct USB line.
2. **Arduino Uno R3 (The Core Receiver):** Collects the incoming text into an isolation software ring buffer to completely bypass the default 64-byte hardware limit.
3. **The Paced Typing Engine:** Sweeps letters out of the buffer using non-blocking clock loops to type out the poem at a readable human pace on a 16x2 LCD screen.

The project is a practical demonstration of:
* Software-driven hardware buffer overflow management
* Non-blocking clock timing cycles using `millis()` instead of thread-killing delays
* Grammatically constrained lexical matrix generators
* Direct desktop-to-microcontroller interface controls

## ⚙️ How It Works

```text
+-----------------------+              +-----------------------+

|     Mac Laptop        |  USB Serial  |   Arduino Uno R3      |
|   (PyCharm Python)    | ------------>| (Paced Typing Engine) | ----> [Prints to I2C LCD]
|  [Poem Generator Code]|  (9600 Baud) |  [256-Byte Ring Buf]  |
+-----------------------+              +-----------------------+
```

### 1. Pacing the Pipeline
Because the Arduino's internal hardware interface caps input streams at **64 bytes**, the Python script paces its output data. It injects a **25ms delay** between characters, ensuring the incoming link stays clear while printing.

### 2. Typing Engine
The Arduino sweeps characters out of the serial cache and stores them inside an expanded 256-character software array. It checks a non-blocking `millis()` tracking window to step through the array index every **150ms**, producing a sleek "typing" animation across the LCD lines without freezing the chip.

## 🔌 Hardware Connection & Pinout

```text
[Arduino Uno R3]                            [I2C LCD Display]
          5V  -------------------------->    VCC
         GND  -------------------------->    GND
     Pin A4   -------------------------->    SDA (Serial Data Line)
     Pin A5   -------------------------->    SCL (Serial Clock Line)
```

## 📂 Project Structure

```text
├── arduino/
│   └── lcd_receiver.ino     # Non-blocking ring buffer typing engine
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

def main():
    try:
        poem_output = generate_perfect_poem("ocean")
        print(f"Generated text:\n{poem_output}\n")
        
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2) # Give the bootloader time to pass control
        
        payload = poem_output.strip() + "#"
        print("Streaming paced characters over USB link to prevent buffer overflow...")
        
        for char in payload:
            ser.write(char.encode('utf-8'))
            ser.flush()
            time.sleep(0.025) # 25ms delay
            
        ser.close()
        print("Sent successfully!")
except Exception as e:
    print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### 2. Arduino Core Engine (`arduino/lcd_receiver.ino`)
Upload this code to your **Arduino Uno R3**.

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

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

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Waiting...");
}

void loop() {
  // 1. Gather all incoming data immediately to bypass the 64-byte limit
  while (Serial.available() > 0) {
    char c = Serial.read();
    textBuffer[writeIndex] = c;
    writeIndex = (writeIndex + 1) % 256; 
  }

  // 2. Typing pacing loop running on non-blocking intervals
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
      }

      if (nextChar == '#') {
        isPrintingPoem = false; // Poem finished processing        
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

## 🦾 Requirements & Cross-Platform Hardware Support
* **I2C LCD Display:** Based on MCP23008/PCF8574 chip line expansions at address `0x27` (16x2 grid configuration).
* **Jumper Cables**
* **Supported Core Devices:** 
  * Arduino Uno R3, Nano V3, Pro Mini, Elegoo Clone Uno R3 boards, SparkFun RedBoard lines, and Adafruit Metro 328 arrays.

## 📄 Personal Project Notes

This repository was put together for learning, fun, and optimization **by an 11-year-old developer.** No beef with the [ESP-32 storyteller project](https://github.com)—this is just the foundational stage of a much larger vision!

### 🗺️ The Project Road Map
* **Step 1:** Transfer raw binary ASCII values across physical terminal lines. (**Done**)
* **Step 2:** Construct an autonomous language model generator template block. (**Done**)
* **Step 3:** Figure out how to sync computer data streams straight into a local screen pipeline. (**Done**)
* **Step 4:** Build a fully independent desktop Poem Matrix generator system! (**Done**)
* **Step 5:** Add text to speech and speech to text. (**Done!**)

I specifically opted to build this using an ATMega328P profile platform paired with basic C++ interfaces, instead of scaling up to massive Linux-based processing engines like a Raspberry Pi 5. Stripping down the architecture makes it significantly more challenging—and much more rewarding when the full string processes flawlessly!

You are free to fork this project, modify the text pools, or tweak the non-blocking array sizing configurations under the rules of the **Apache 2.0 License** included in the repository. Enjoy exploring the hardware loops!

### After over a month since August 28th, the TTS service is finally here, woohoo! 📢🥳
I was procrastinating till about Mid-September, then I was having a hard time finding the right TTS; it seemed like every TTS service had a catch, like an paid API key, or just a week's trial, then pay up! But then, I came across pyttsx3, the mega-cum-free-cum-python library that saved my father's money. I would highly recommend pyttsx3 for beginners. Also I was having trouble syncing everything but i also added multiproccesing and that seemed to work.
I know the TTS is slow, but I'm too lazy to provide a ratio to correlate Words per second to the Characters per second, so deal with it.
