
# ASCII-Wires
## Bit Transfer Between Arduino Uno R3 and micro:bit V2

A simple embedded-systems project that demonstrates **transferring digital bits between two different microcontrollers** using physical wires: an **Arduino Uno R3** and a **BBC micro:bit V2**.

## 📌 Project Overview

This project explores how two microcontrollers can communicate at the bit level without relying on higher-level communication protocols such as UART, I²C, or SPI.

The Arduino Uno R3 and micro:bit V2 exchange binary data through GPIO pins connected with wires. Individual bits are represented using digital **HIGH** and **LOW** signals, allowing one microcontroller to transmit a sequence of bits while the other receives and reconstructs the data.

The project is intended as a hands-on demonstration of:

* Digital signals and binary data
* GPIO input and output
* Bit-level communication
* Timing and synchronization
* Serial data transmission
* Communication between different microcontroller platforms

## 🔧 Hardware

* Arduino Uno R3
* BBC micro:bit V2
* Jumper wires
* Breadboard (optional)
* USB cables for programming and power

## ⚙️ How It Works

The transmitter converts data into a sequence of binary bits. Each bit is represented by the voltage level on a GPIO wire:

* **HIGH** → `1`
* **LOW** → `0`

The receiving microcontroller samples the signal at the appropriate time and stores the received bits. After enough bits have been collected, they can be combined to reconstruct the original byte or message.

For example:

```text
Data:       10110010

Bit stream:
1 → 0 → 1 → 1 → 0 → 0 → 1 → 0
```

The project therefore demonstrates the fundamental idea behind digital communication: **information can be represented and transferred using changes in electrical signals.**

## 🔌 Connection

A GPIO pin on the Arduino is connected to a GPIO pin on the micro:bit.

A **common GND connection is required** so that both microcontrollers share the same voltage reference.

> ⚠️ Always verify the voltage levels and pin configuration before connecting the boards. The micro:bit uses 3.3 V GPIO logic, while the Arduino Uno R3 uses 5 V logic.

## 🚀 Goals

The main goals of this project are to:

1. Understand how individual bits can be transmitted through a wire.
2. Learn how microcontrollers generate and read digital signals.
3. Implement basic synchronization between a transmitter and receiver.
4. Transfer bytes or messages between an Arduino and micro:bit.
5. Explore the principles behind more advanced digital communication protocols.

## 📂 Project Structure

```text
├── arduino/
│   └── transmitter.ino
│
├── microbit/
│   └── receiver.py
│
└── README.md
```

The exact structure may vary depending on the programming environment used for the micro:bit.

## 🧪 Example

If the Arduino wants to transmit the byte:

```text
01001000
```

it sends each bit sequentially through the GPIO connection. The micro:bit reads the signal, records the bits, and reconstructs:

```text
01001000
```

which corresponds to the ASCII character:

```text
H
```

## 📚 What This Project Demonstrates

This project provides a practical introduction to the concepts that form the foundation of computer and embedded communication:

**Binary data → Digital signals → Electrical pulses → GPIO → Reconstructed data**

Although the implementation is intentionally simple, the same fundamental concepts are used in communication systems ranging from simple serial links to complex networking hardware.

## 🔮 Future Improvements

Possible extensions include:

* Two-way communication
* Start and stop bits
* Clock/synchronization signal
* Checksum or parity for error detection
* Multi-byte messages
* Bidirectional communication
* Custom communication protocol
* Data transmission testing and error-rate measurement
* Visualizing transmitted bits using LEDs or a logic analyzer
## Requirements and pinout
micro:bit v2+\
I2C LCD (MCP23008, 0x27, 16 by 2 display)\
Alligator clips\
Arduino Uno R3 (or R4 Minima/Minima WiFi/ WiFi Rev2), though it also works on the following:\

Arduino Nano V3\
Arduino Pro Mini (5V / 16MHz)\
Arduino Uno Mini Limited Edition\
SparkFun RedBoard\
SparkFun RedBoard Edge\
Adafruit Metro 328
DFRobot DFRduino Uno R3\
Seeeduino V4.2\
All generic or third-party Clone Uno R3 boards (Elegoo, Inland, etc.)
### With change of pins

Arduino Mega 2560 / Mega ADK (Move LCD to pins 20 and 21)\
Arduino Nano Every (Move LCD to pins A4 and A5)\
Arduino Micro (Move LCD to pins 2 and 3; change signal pin to avoid conflict)\
LilyPad Arduino Main Board (Move LCD to pins A4 and A5)
### With code change

Arduino Leonardo\
Arduino MicroPro Micro (5V or 3.3V)\
Required Code Modification:\
You must change your input pin variable from Pin 2 to any available digital pin (like Pin 4 or Pin 7).

```const int signalPin = 4; // Moved from 2 to avoid I2C conflict```

ESP32 Development Boards (ESP32-WROOM, ESP32-S3)\
NodeMCU / D1 Mini (ESP8266)\
Raspberry Pi Pico / Pico 2 (RP2040 / RP2350)\
You must pass your custom SDA and SCL pins directly into the Wire.begin() function inside setup(). For example, on a standard ESP32:
```
void setup() {
  pinMode(signalPin, INPUT);
  
  // Explicitly assign I2C pins (e.g., SDA = 21, SCL = 22 for ESP32)
  Wire.begin(21, 22); 

  lcd.init();
  lcd.backlight();
  // ... rest of setup
}
```
Arduino Uno R4 Minima / WiFi (Renesas RA4M1 architecture)\
Arduino Zero / Nano 33 IoT (SAMD21 ARM Cortex-M0+ architecture)\
Adafruit Metro M0 / M4 Express (ARM Cortex architecture)\
Teensy 4.0 / 4.1 (ARM Cortex-M7 architecture)
```
// Replace old AVR register code with native 32-bit hardware timers:
#include <TimerInterrupt.h> // Example for 32-bit boards
```
### Pinout
Pin D2 arduino --- P0 micro:bit\
SDA and SCL --- (ditto on the MCP-based I²C LCD)
## 📄 Notes

This project is intended for educational and experimental purposes.\
I have no grudges or copyright for ASCII, Arduino, nor microbit and solemnly agree to all rules and regulations.\
This repo was made for fun, by an 11 yr old. No beef with the [ESP-32 storyteller](https://github.com/slvDev/esp32-ai); although this is the first part of a big project.\
Step 1: Send binary ASCII through wires. (Done)\
Step 2: Make a LM (Either LLM or SLM) (Done, it wasn't even a LM!)\
Step 3: Figure out how to get that info to the micro:bit.\
Step 4: We have a Poem Generator!\
I specifically made this with a microcontroller with ATMega32p stats and a basic C++ interface, Arduino Uno R3; and a basic SLM handler, micro:bit, which can use SLMs to do basic stuff, and is programmable with JS, Python, Scratch and its lookalikes whether in the Gandi family or not; because I think it would honestly be more impressive if I did it that way, than to use complex microcontroller/Linux PC beasts, like the Raspberry Pi 5/ AI HAT+ /AI HAT+ 2 or an ESP-32 based controller like the Arduino Mini/Nano. But that is for you, dear viewer, to think about and decide.\
You are allowed to fork it and tweak the code as long as you comply to the Apache 2.0 License in the project. Take inspiration!
We all can make mistakes so tell me if there's any. We all are people after all.
