import random, json, time

# Resources used:
# https://en.wikipedia.org/wiki/Enigma_machine
# https://www.youtube.com/watch?v=G2_Q9FoD-oQ
# https://www.youtube.com/watch?v=ybkkiGtJmkM
# https://www.youtube.com/watch?v=mcX7iO_XCFA

# Enigma Machine in Python
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ,.!?- " # Encryption input and decryption output alphabet
rotorL = "BDFHJLCPRTXVZNYEIWGAKMUSQO,.!?- "
rotorM = "AJDKSIRUXBLHWTMCQGZNPYFVOE,.!?- "
rotorR = "EKMFLGDQVZNTOWYHXUSPAIBRCJ,.!?- "
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT,.!?- "

# Rotor offsets - change the starting position of the rotors
lOffset = 4
mOffset = 12
rOffset = 20
startOffsets = [int(lOffset), int(mOffset), int(rOffset)]

# Ring offsets - change the internal wiring of the rotors
lRingOffset = 2
mRingOffset = 8
rRingOffset = 16

def ListToString(list):
    return "".join(list)

def Scramble():
    global rotorL, rotorM, rotorR, reflector, lOffset, mOffset, rOffset, lRingOffset, mRingOffset, rRingOffset

    # Convert rotors to lists to allow shuffling
    rotorL = list(alphabet)
    rotorM = list(alphabet)
    rotorR = list(alphabet)
    reflector = list(alphabet)

    # Shuffle each rotor and reflector
    random.shuffle(rotorL)
    random.shuffle(rotorM)
    random.shuffle(rotorR)
    random.shuffle(reflector)

    # Convert back to string
    rotorL = ListToString(rotorL)
    rotorM = ListToString(rotorM)
    rotorR = ListToString(rotorR)
    reflector = ListToString(reflector)

    lOffset = random.randint(0, len(rotorL) - 1)
    mOffset = random.randint(0, len(rotorM) - 1)
    rOffset = random.randint(0, len(rotorR) - 1)

    lRingOffset = random.randint(0, len(rotorL) - 1)
    mRingOffset = random.randint(0, len(rotorM) - 1)
    rRingOffset = random.randint(0, len(rotorR) - 1)

def ExportSettings():
    global rotorL, rotorM, rotorR, reflector, plugboard, lOffset, mOffset, rOffset, lRingOffset, mRingOffset, rRingOffset

    # Export rotors and reflector to a file
    with open("settings.txt", "w") as file:
        file.write(
            f"""{rotorL}\n{rotorM}\n{rotorR}\n{reflector}\n{json.dumps(plugboard)}\n{json.dumps(startOffsets)}\n{lRingOffset}\n{mRingOffset}\n{rRingOffset}""")
        file.close()

def ImportSettings():
    global rotorL, rotorM, rotorR, reflector, plugboard, lOffset, mOffset, rOffset, lRingOffset, mRingOffset, rRingOffset

    # Import rotors and reflector from a file
    with open("settings.txt", "r") as file:
        try:
            rotorL = file.readline().strip()
            rotorM = file.readline().strip()
            rotorR = file.readline().strip()
            reflector = file.readline().strip()
            plugboard = json.loads(file.readline().strip())
            startOffsets = json.loads(file.readline().strip())
            lOffset = int(startOffsets[0])
            mOffset = int(startOffsets[1])
            rOffset = int(startOffsets[2])
            lRingOffset = int(file.readline().strip())
            mRingOffset = int(file.readline().strip())
            rRingOffset = int(file.readline().strip())
            file.close()
        except Exception as e:
            print(e)
            file.close()
            Scramble()

# The plugboard swaps characters that are connected together
plugboard = {
    "A" : "B",
    "B" : "A",
    "F" : "P",
    "P" : "F",
    "G" : "V",
    "V" : "G",
    "Q" : "M",
    "M" : "Q",
}

ImportSettings()

while True:
    menu_input = input("\n1. Encrypt/Decrypt\n2. Scramble\n3. Exit\n\nU: ")

    # Encrypt/Decrypt
    if menu_input == "1":
        input_text = input("Enter text to encrypt/decrypt: ").upper()
        output_text = ""

        lOffset = startOffsets[0]
        mOffset = startOffsets[1]
        rOffset = startOffsets[2]

        print(f"Starting offsets: {lOffset}, {mOffset}, {rOffset}")

        # Remove any characters that are not in the alphabet
        for char in input_text:
            if char not in alphabet:
                input_text = input_text.replace(char, "")

        # Encrypt or decrypt input text - enigma works the same both ways
        for char in input_text:
            # Pass char through plugboard
            if char in plugboard:
                char = plugboard[char]

            # Step rotors before connection
            rOffset = (rOffset + 1) % len(rotorR)
            if rOffset == 0:
                mOffset = (mOffset + 1) % len(rotorM) # Full revolution of first rotor
                if mOffset == 0:
                    lOffset = (lOffset + 1) % len(rotorL) # Full revolution of second rotor
                    if lOffset == 0:
                        mOffset = 0 # Full revolution of third rotor also resets second rotor

            # Pass char through rotors
            char = rotorR[abs(alphabet.index(char) + rOffset + rRingOffset) % len(rotorR)] # Right rotor
            char = rotorM[abs(alphabet.index(char) + mOffset + mRingOffset) % len(rotorM)] # Middle rotor
            char = rotorL[abs(alphabet.index(char) + lOffset + lRingOffset) % len(rotorL)] # Left rotor

            # Pass char through reflector
            char = reflector[alphabet.index(char)]

            # Pass char through rotors in reverse
            char = alphabet[abs(rotorL.index(char) - lOffset + lRingOffset) % len(alphabet)] # Left rotor
            char = alphabet[abs(rotorM.index(char) - mOffset + mRingOffset) % len(alphabet)] # Middle rotor
            char = alphabet[abs(rotorR.index(char) - rOffset + rRingOffset) % len(alphabet)] # Right rotor

            # Pass char through plugboard in reverse
            if char in plugboard:
                char = plugboard[char]

            output_text += char

        print(f"\nYour coded text is: \n{output_text}")
        ExportSettings()

        time.sleep(1)
    
    # Scramble settings
    elif menu_input == "2":
        Scramble()
        print("Settings scrambled.\n")

    # Exit
    elif menu_input == "3":
        break