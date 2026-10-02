import random
import time
import serial
import pyttsx3
import multiprocessing

# ==================== MANUAL TUNING CONFIGURATION ====================
TALKING_SPEED = 80  # 👈 Adjust this up/down to match your LCD's print speed!
SERIAL_PORT = '/dev/cu.usbmodem14201'
BAUD_RATE = 9600


# =====================================================================

def generate_perfect_poem(subject="nature"):
    """Generates a grammatically correct poem by matching singular/plural contexts dynamically."""
    adjectives_vowel = ["ancient", "enchanted", "infinite", "emerald", "unfading"]
    adjectives_consonant = ["shimmering", "whispering", "golden", "serene", "mystic", "gentle", "bright", "silent",
                            "velvet"]
    singular_nouns = ["leaf", "star", "river", "mountain", "dream", "wind", "flower", "shadow", "spirit", "echo",
                      "heart", "melody"]
    plural_nouns = ["leaves", "stars", "rivers", "mountains", "dreams", "winds", "flowers", "shadows", "echoes",
                    "melodies"]
    verbs_singular_noun = ["dances", "sings", "dreams", "flows", "rises", "whispers", "glows", "sleeps", "awakens",
                           "blooms"]
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


def tts_process_worker(text, speed):
    """Runs inside an isolated OS process to bypass macOS threading bugs completely."""
    worker_engine = pyttsx3.init()
    worker_engine.setProperty('rate', speed)
    worker_engine.say(text)
    worker_engine.runAndWait()


def main():
    try:
        poem_output = generate_perfect_poem("sea")
        char_count = len(poem_output)
        byting = char_count.bit_length() / 8

        print("=== Grammatically Correct Poem ===")
        print(poem_output)
        print("==================================")
        if byting != 1:
            print(char_count, "characters in this poem.", char_count.bit_length(), "bits or", byting, "byte(s) needed.")
        else:
            print(char_count, "characters in this poem.", char_count.bit_length(), "bits or", int(byting),
                  "byte(s) needed.")

        # 1. Establish the serial connection
        print("Opening serial port...")
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

        # 2. Wait out the 2-second Arduino bootloader setup up front
        print("Waiting 2 seconds for hardware bootloader...")
        time.sleep(2)

        # 3. Create the isolated Process payload
        bg_voice_process = multiprocessing.Process(
            target=tts_process_worker,
            args=(poem_output, TALKING_SPEED)
        )

        payload = poem_output.strip() + "#"
        print("Streaming characters... Audio triggers immediately after the first character prints.")

        audio_started = False

        # 4. Stream character loop
        for char in payload:
            ser.write(char.encode('utf-8'))
            ser.flush()

            # Start isolated voice process ONLY after the very first character writes to hardware
            if not audio_started:
                bg_voice_process.start()
                audio_started = True

            time.sleep(0.025)  # Your steady 25ms physical pacing delay

        ser.close()
        print("Text streaming finished. Waiting safely for background speech process to conclude...")

        # 5. Keep main alive until the independent voice concludes cleanly
        bg_voice_process.join()
        print("\nSent and spoken successfully without interruption!")

    except Exception as e:
        print(f"Error executing transmission: {e}")


if __name__ == "__main__":
    # Required safely on macOS to prevent infinite process looping forks
    multiprocessing.freeze_support()
    main()
