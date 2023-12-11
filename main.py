import numpy as np

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g = gcd(a, m)
    if g != 1:
        # Modular inverse does not exist
        return None
    else:
        # Extended Euclidean Algorithm to find the modular inverse
        _, x, _ = extended_gcd(a, m)
        return x % m

def matrix_modulo_inverse(matrix, modulus):
    det = int(np.linalg.det(matrix))
    det_inv = mod_inverse(det, modulus)

    if det_inv is None:
        print("Error: Modular inverse does not exist. Please choose a different key matrix.")
        return None

    adjugate = np.round(np.linalg.inv(matrix) * det).astype(int)
    inverse = (det_inv * adjugate) % modulus
    return inverse

def prepare_output(output, block_size, encrypt=True):
    output = "".join(output.split())
    if encrypt:
        output += "X" * (block_size - (len(output) % block_size))
    return output

def remove_padding(output):
    return output.rstrip('X')

def text_to_matrix(text, block_size):
    matrix = []
    for char in text:
        matrix.append(ord(char) - ord('A'))
        if len(matrix) == block_size:
            yield matrix
            matrix = []

def matrix_to_text(matrix):
    return "".join([chr(char[0] + ord('A')) for char in matrix])

def get_key_matrix():
    print("Enter the key matrix (each row on a new line, space-separated):")
    key = []
    for _ in range(block_size):
        row = list(map(int, input().split()))
        key.append(row)
    return key

def encrypt(output, key):
    block_size = len(key)
    output = prepare_output(output, block_size)
    key_matrix = np.array(key).reshape((block_size, block_size))

    ciphertext = ""
    for block in text_to_matrix(output, block_size):
        block = np.array(block).reshape((block_size, 1))
        encrypted_block = np.dot(key_matrix, block) % 26
        ciphertext += matrix_to_text(encrypted_block)

    return ciphertext

def decrypt(ciphertext, key):
    block_size = len(key)
    key_matrix = np.array(key).reshape((block_size, block_size))
    key_inverse = matrix_modulo_inverse(key_matrix, 26)

    if key_inverse is None:
        return "Decryption failed."

    output = ""
    for block in text_to_matrix(ciphertext, block_size):
        block = np.array(block).reshape((block_size, 1))
        decrypted_block = np.dot(key_inverse, block) % 26
        output += matrix_to_text(decrypted_block)

    return remove_padding(output)

# Read input text from a file
file_path = "output.txt"
with open(file_path, "r") as file:
    output = file.read().upper()  # Convert to uppercase for consistency

# Get the key matrix from the user
block_size = int(input("Enter the block size: "))
key = get_key_matrix()

encrypted_text = encrypt(output, key)
decrypted_text = decrypt(encrypted_text, key)

print("\noutput:", output)
print("Encrypted:", encrypted_text)
print("Decrypted:", decrypted_text)
