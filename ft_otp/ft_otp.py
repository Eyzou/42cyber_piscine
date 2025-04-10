import json
import argparse
import string
import hashlib
import hmac
from cryptography.fernet import Fernet

FERNET_KEY = b'5FDxpglPAIJiDlz3AcOF9R13ukLe70V7QfZZ0IHjuuA='
fernet = Fernet(FERNET_KEY)

def parse_args():
    parser = argparse.ArgumentParser(prog="ft_otp", description="Generate a 1-time password that expires after 30 secs from a 64 hex key")
    parser.add_argument("-g",metavar="HEX_FILE",type=str,help="Generate a .key file from a 64 hex string file")
    parser.add_argument("-k", "--key",metavar="KEY_FILE",type=str,help="Key file to generate a new temporary password")
    args = parser.parse_args()
    return args

def generate_key(key_file):
    try:
        with open(key_file,"r") as file:
            hex_key = file.read()
    except FileNotFoundError:
        print(f"File {key_file} not found")
        return 1

    if len(hex_key) != 64 or not all(c in string.hexdigits for c in hex_key):
        print(f"python3 ft_otp.py error: key must be 64 hexadecimal characters.")
        return 1

    data = {"key":hex_key.lower(),"counter":0}
    json_data = json.dumps(data).encode()

    encrypted = fernet.encrypt(json_data)
    with open("ft_otp.key","wb") as file:
        file.write(encrypted)

    print("Key was successfully saved in ftp_otp.key.")
    return 0

# make sure to open with read and bytes
def generate_otp(key_file):
    try:
        with open(key_file,"rb") as file:
            encrypted_data = file.read()
    except FileNotFoundError:
        print(f"File {key_file} not found")
        return 1

    try:
        json_data = fernet.decrypt(encrypted_data).decode()
        data = json.loads(json_data) # load transform json en dict
    except Exception as e:
        print(f"Decryption/JSON error: {e}")
        return 1

    with open("check.txt","w") as file:
        file.write(json_data)
    hex_key = data["key"]
    current_counter = data["counter"]

    key_bytes = bytes.fromhex(hex_key)
    counter_bytes = current_counter.to_bytes(8,"big")
    digest = hmac.new(key_bytes,counter_bytes,hashlib.sha1).digest()

    otp = int.from_bytes(digest,"big") % 10**6
    print(f"{otp}")

    data["counter"] += 1
    new_json_data = json.dumps(data).encode()
    new_encrypted_data = fernet.encrypt(new_json_data)
    with open("ft_otp.key","wb") as file:
        file.write(new_encrypted_data)

def main():
    args = parse_args()
    if args.g:
        return generate_key(args.g)
    elif args.key:
        return generate_otp(args.key)
    else:
        print("Usage: python3 ft_otp.py [-g] [-k]")
        return 1

if __name__ == '__main__':
   main()