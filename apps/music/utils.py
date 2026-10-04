import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad


KEY = b"38346591"


def decrypt(ciphertext_base64):
    # Decode Base64
    encrypted_data = base64.b64decode(ciphertext_base64)

    # DES ECB mode
    cipher = DES.new(KEY, DES.MODE_ECB)

    # Decrypt
    decrypted_data = cipher.decrypt(encrypted_data)

    # Remove PKCS5/PKCS7 padding
    decrypted_data = unpad(decrypted_data, DES.block_size)

    return decrypted_data.decode("utf-8")


if __name__ == "__main__":
    while True:
        encrypted_input = input("Enter Base64 encrypted text: ")

        try:
            decrypted = decrypt(encrypted_input)
            print("Decrypted:", decrypted)
        except Exception as e:
            print("Decryption failed:", e)