import random, json, time

# Resources used:
# https://en.wikipedia.org/wiki/Enigma_machine
# https://www.youtube.com/watch?v=G2_Q9FoD-oQ
# https://www.youtube.com/watch?v=ybkkiGtJmkM
# https://www.youtube.com/watch?v=mcX7iO_XCFA

# Enigma Machine in Python
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # Encryption input and decryption output alphabet
rotorL = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
rotorM = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotorR = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# Rotor offsets - change the starting position of the rotors
lOffset = 4
mOffset = 12
rOffset = 20
startOffsets = [int(lOffset), int(mOffset), int(rOffset)]

# Ring offsets - change the internal wiring of the rotors
lRingOffset = 4
mRingOffset = 8
rRingOffset = 12

# The plugboard swaps characters that are connected together
plugboard = {
    "A": "B",
    "B": "A",
    "F": "P",
    "P": "F",
    "G": "V",
    "V": "G",
    "Q": "M",
    "M": "Q",
}

def ListToString(list):
    return "".join(list)

def Scramble():
    global rotorL, rotorM, rotorR, reflector, lOffset, mOffset, rOffset, lRingOffset, mRingOffset, rRingOffset, startOffsets

    # # Convert rotors to lists to allow shuffling
    # rotorL = list(alphabet)
    # rotorM = list(alphabet)
    # rotorR = list(alphabet)
    # reflector = list(alphabet)

    # # Shuffle each rotor and reflector
    # random.shuffle(rotorL)
    # random.shuffle(rotorM)
    # random.shuffle(rotorR)
    # random.shuffle(reflector)

    # # Convert back to string
    # rotorL = ListToString(rotorL)
    # rotorM = ListToString(rotorM)
    # rotorR = ListToString(rotorR)
    # reflector = ListToString(reflector)

    # Randomize rotors
    lOffset = random.randint(0, len(rotorL) - 1)
    mOffset = random.randint(0, len(rotorM) - 1)
    rOffset = random.randint(0, len(rotorR) - 1)
    startOffsets = [int(lOffset), int(mOffset), int(rOffset)]

    # Randomize rings
    lRingOffset = random.randint(0, len(rotorL) - 1)
    mRingOffset = random.randint(0, len(rotorM) - 1)
    rRingOffset = random.randint(0, len(rotorR) - 1)

def ExportSettings():
    global rotorL, rotorM, rotorR, reflector, plugboard, startOffsets, lRingOffset, mRingOffset, rRingOffset

    settings = {
        "rotorL" : rotorL,
        "rotorM" : rotorM,
        "rotorR" : rotorR,
        "reflector" : reflector,
        "plugboard" : plugboard,
        "offsets" : startOffsets,
        "ringOffsets" : [lRingOffset, mRingOffset, rRingOffset]
    }

    # Export rotors and reflector to a file
    with open("settings.json", "w") as file:
        file.write(json.dumps(settings, indent=4))
        file.close()

def ImportSettings():
    global rotorL, rotorM, rotorR, reflector, plugboard, lOffset, mOffset, rOffset, lRingOffset, mRingOffset, rRingOffset, startOffsets

    # Import rotors and reflector from a file
    try:
        with open("settings.json", "r") as file:
            try:
                settings = json.loads(file.read())

                rotorL = settings["rotorL"]
                rotorM = settings["rotorM"]
                rotorR = settings["rotorR"]
                reflector = settings["reflector"]
                plugboard = settings["plugboard"]
                startOffsets = settings["offsets"]
                lOffset = int(startOffsets[0])
                mOffset = int(startOffsets[1])
                rOffset = int(startOffsets[2])
                ringOffsets = settings["ringOffsets"]
                lRingOffset = int(ringOffsets[0])
                mRingOffset = int(ringOffsets[1])
                rRingOffset = int(ringOffsets[2])

                file.close()

            except Exception as e:
                print(e)
                file.close()
                Scramble()
                ExportSettings()

    except FileNotFoundError:
        print('\nCreating settings file.\n')
        Scramble()
        ExportSettings()

ImportSettings()

def Encode(char):
    global alphabet, plugboard, rotorR, rotorM, rotorL, rOffset, mOffset, lOffset, rRingOffset, mRingOffset, lRingOffset
    
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
    char = rotorR[(alphabet.index(char) + rOffset + rRingOffset) % len(rotorR)] # Right rotor
    char = rotorM[(alphabet.index(char) + mOffset + mRingOffset) % len(rotorM)] # Middle rotor
    char = rotorL[(alphabet.index(char) + lOffset + lRingOffset) % len(rotorL)] # Left rotor

    # Pass char through reflector
    char = reflector[alphabet.index(char)]

    # Pass char through rotors in reverse
    char = alphabet[(rotorL.index(char) - lOffset - lRingOffset) % len(alphabet)] # Left rotor
    char = alphabet[(rotorM.index(char) - mOffset - mRingOffset) % len(alphabet)] # Middle rotor
    char = alphabet[(rotorR.index(char) - rOffset - rRingOffset) % len(alphabet)] # Right rotor

    # Pass char through plugboard in reverse
    if char in plugboard:
        char = plugboard[char]

    return char

while True:
    menu_input = input("\nEnigma Machine\n1. Encrypt/Decrypt\n2. Scramble\n3. Settings\n4. Exit\n\nU: ").lower()

    # Encrypt/Decrypt
    if menu_input == "1" or menu_input == "encrypt" or menu_input == "decrypt":
        input_text = input("Enter text to encrypt/decrypt: ").upper()
        output_text = ""

        lOffset = startOffsets[0]
        mOffset = startOffsets[1]
        rOffset = startOffsets[2]

        print(f"Offsets - Left: {lOffset}, Middle: {mOffset}, Right: {rOffset}\nRings - Left: {lRingOffset}, Middle: {mRingOffset}, Right: {rRingOffset}")

        # Remove any characters that are not in the alphabet
        for char in input_text:
            if char not in alphabet:
                input_text = input_text.replace(char, "")

        # Encrypt or decrypt input text - enigma works the same both ways
        for char in input_text:
            output_text += Encode(char)
            #print(f"Current offsets: {lOffset}, {mOffset}, {rOffset}")

        print(f"\nYour coded text is: \n{output_text}")
        ExportSettings()

        time.sleep(1)
    
    # Scramble settings
    elif menu_input == "2" or menu_input == "scramble":
        Scramble()
        ExportSettings()
        print("Settings scrambled.\n")

    elif menu_input == "3" or menu_input == "settings":
        try:
            lOffset = int(input("Enter left rotor: "))
            mOffset = int(input("Enter middle rotor: "))
            rOffset = int(input("Enter right rotor: "))
            startOffsets = [lOffset, mOffset, rOffset]

            lRingOffset = int(input("Enter left ring offset: "))
            mRingOffset = int(input("Enter middle ring offset: "))
            rRingOffset = int(input("Enter right ring offset: "))

            ExportSettings()
            print("Settings saved.\n")
        except ValueError:
            print("Invalid input.")

    # Exit
    elif menu_input == "4" or menu_input == "exit":
        break