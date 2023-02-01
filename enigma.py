# Enigma Machine in Python
alphabet = "abcdefghijklmnopqrstuvwxyz"
rotorL = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
rotorM = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotorR = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"

lOffset = 0
mOffset = 0
rOffset = 0

plugboard = {
    "a": "b",
    "b" : "a"
}

input_text = input("Enter text to encrypt: ")
output_text = ""

for char in input_text:
    if char in plugboard:
        char = plugboard[char]

    # Step rotors
    rOffset = (rOffset + 1) % 26
    if rOffset == 0:
        mOffset = (mOffset + 1) % 26 # Full revolution of first rotor
        if mOffset == 0:
            lOffset = (lOffset + 1) % 26 # Full revolution of second rotor
            if lOffset == 0:
                mOffset = 0 # Full revolution of third rotor also resets second rotor

    # Pass char through rotors
    
    output_text += char

print(output_text)
