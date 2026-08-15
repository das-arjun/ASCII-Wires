import random
import serial
import time


def generate_simple_poem(subject="nature"):
    adjectives = ["shimmering", "whispering", "ancient", "golden", "serene", "verdant", "bright", "silent"]
    nouns = ["leaves", "stars", "rivers", "mountains", "dreams", "winds", "flowers", "light"]
    verbs = ["dance", "sing", "dream", "flow", "rise", "whisper", "glow", "bloom"]

    line1 = f"Oh {random.choice(adjectives)} {subject.lower()} so grand,"
    line2 = f"Where {random.choice(nouns)} {random.choice(verbs)} in the breeze,"
    line3 = f"A {random.choice(adjectives)} {random.choice(nouns)} takes flight,"
    line4 = f"Secrets that the {random.choice(nouns)} keep."

    # Keep text flat on a single space-separated line
    return f"{line1} {line2} {line3} {line4}"


# Update to your working Micro:bit COM port number
SERIAL_PORT = '/dev/cu.usbmodem14202'
BAUD_RATE = 115200

try:
    poem_output = generate_simple_poem("ocean")
    print(f"Generated Text:\n{poem_output}\n")

    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(3)  # Give Micro:bit 3 full seconds to initialize serial channels

    # Append the termination symbol '#'
    payload = poem_output.strip() + "#"

    print("Streaming bytes to micro:bit...")
    ser.write(payload.encode('ascii'))
    ser.flush()

    ser.close()
    print("Sent successfully!")

except Exception as e:
    print(f"Error: {e}")
