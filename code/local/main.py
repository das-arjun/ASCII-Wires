import random
import time
import serial


def generate_perfect_poem(subject="nature"):
    """Generates a grammatically correct poem by matching singular/plural contexts dynamically."""

    # 1. Grammar-Segregated Word Pools
    adjectives_vowel = ["ancient", "enchanted", "infinite", "emerald", "unfading"]
    adjectives_consonant = ["shimmering", "whispering", "golden", "serene", "mystic", "gentle", "bright", "silent",
                            "velvet"]

    singular_nouns = ["leaf", "star", "river", "mountain", "dream", "wind", "flower", "shadow", "spirit", "echo",
                      "heart", "melody"]
    plural_nouns = ["leaves", "stars", "rivers", "mountains", "dreams", "winds", "flowers", "shadows", "echoes",
                    "melodies"]

    # Verbs split by grammar conjugation
    verbs_singular_noun = ["dances", "sings", "dreams", "flows", "rises", "whispers", "glows", "sleeps", "awakens",
                           "blooms"]
    verbs_plural_noun = ["dance", "sing", "dream", "flow", "rise", "whisper", "glow", "sleep", "awaken", "bloom"]

    # General active base verbs
    verbs_active = ["takes flight", "drifts away", "unfurls", "soars high", "watches close"]

    # 2. Dynamic Line Building with Structural Alignment

    # Line 1: Main Subject Line
    adj1 = random.choice(adjectives_vowel + adjectives_consonant)
    line1 = f"Oh {adj1} {subject.lower()} so grand,"

    # Line 2: Plural Subject Alignment ("Where [Plural Nouns] [Plural Verb]...")
    p_noun = random.choice(plural_nouns)
    p_verb = random.choice(verbs_plural_noun)
    line2 = f"Where {p_noun} {p_verb} in the breeze,"

    # Line 3: Singular Determiner Alignment ("A" vs "An")
    adj2_vowel = random.choice(adjectives_vowel)
    adj2_consonant = random.choice(adjectives_consonant)
    s_noun = random.choice(singular_nouns)
    v_active = random.choice(verbs_active)

    # Flip a coin for a vowel or consonant adjective phrase to ensure proper grammar
    if random.choice([True, False]):
        line3 = f"An {adj2_vowel} {s_noun} {v_active},"
    else:
        line3 = f"A {adj2_consonant} {s_noun} {v_active},"

    # Line 4: Final Closing Line
    p_noun2 = random.choice(plural_nouns)
    line4 = f"Secrets that the {p_noun2} keep."

    # Return as a flat continuous text block
    return f"{line1} {line2} {line3} {line4}"


# --- SYSTEM CONFIGURATION ---
SERIAL_PORT = '/dev/cu.usbmodem14201'  # Keep your verified Mac port
BAUD_RATE = 9600


def main():
    try:
        # Generate the smart poem payload
        poem_output = generate_perfect_poem("sea")
        char = len(poem_output)
        byting = len(poem_output).bit_length() / 8
        print("=== Grammatically Correct Poem ===")
        print(poem_output)
        print("==================================")
        if byting < 1 or byting > 1:
            print(char, "characters in this poem.", char.bit_length(), "bits or", byting, "byte(s) needed.")
        elif byting == 1:
            print(char, "characters in this poem.", char.bit_length(), "bits or", int(byting), "byte(s) needed.")

        # Connect to your original Arduino Omega
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Bootloader delay

        # Structure terminal payload marker
        payload = poem_output.strip() + "#"
        print("Streaming paced characters over USB connection...")

        # Paced byte writer to prevent 64-byte hardware overflows
        for char in payload:
            ser.write(char.encode('utf-8'))
            ser.flush()
            time.sleep(0.025)  # 25ms hardware safety pacing

        ser.close()
        print("\nSent successfully!")

    except Exception as e:
        print(f"Error executing transmission: {e}")


if __name__ == "__main__":
    main()
