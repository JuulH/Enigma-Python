# Enigma Machine in Python
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ,.!?- " # Encryption input and decryption output alphabet
rotorL = "BDFHJLCPRTXVZNYEIWGAKMUSQO,.!?- "
rotorM = "AJDKSIRUXBLHWTMCQGZNPYFVOE,.!?- "
rotorR = "EKMFLGDQVZNTOWYHXUSPAIBRCJ,.!?- "
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT,.!?- "

# Rotor offsets
lOffset = 4
mOffset = 12
rOffset = 20

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

input_text = input("Enter text to encrypt: ").upper()
output_text = ""

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
    rOffset = (rOffset + 1) % 26
    if rOffset == 0:
        mOffset = (mOffset + 1) % 26 # Full revolution of first rotor
        if mOffset == 0:
            lOffset = (lOffset + 1) % 26 # Full revolution of second rotor
            if lOffset == 0:
                mOffset = 0 # Full revolution of third rotor also resets second rotor

    # Pass char through rotors
    char = rotorR[(alphabet.index(char) + rOffset) % len(alphabet)] # Right rotor
    char = rotorM[(alphabet.index(char) + mOffset) % len(alphabet)] # Middle rotor
    char = rotorL[(alphabet.index(char) + lOffset) % len(alphabet)] # Left rotor

    # Pass char through reflector
    char = reflector[alphabet.index(char)]

    # Pass char through rotors in reverse
    char = alphabet[(rotorL.index(char) - lOffset) % len(alphabet)] # Left rotor
    char = alphabet[(rotorM.index(char) - mOffset) % len(alphabet)] # Middle rotor
    char = alphabet[(rotorR.index(char) - rOffset) % len(alphabet)] # Right rotor

    # Pass char through plugboard in reverse
    if char in plugboard:
        char = plugboard[char]

    output_text += char

print(f"\nYour coded text is: \n{output_text}\n")