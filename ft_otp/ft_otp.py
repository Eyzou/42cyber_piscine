import json
import argparse
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)

def parse_args():
    parser = argparse.ArgumentParser(prog="ft_otp", description="Generate a 1-time password that expires after 30 secs from a 64 hex key")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-g",metavar="HEX_FILE",type=str,help="Generate a .key file from a 64 hex string file")
    parser.add_argument("-k", "--key",metavar="KEY_FILE",type=str,help="Key file to generate a new temporary password")
    group.require= True
    args = parser.parse_args()
    return args

def generate_key(key_file):
    try:
        with open(key_file,"r") as file:
            hex_key = file.read()
    except FileNotFoundError:
        print(f"File {key_file} not found")
        return 1

    if len(hex_key) != 64:
        print(f"Invalid hex key {hex_key}")
        return 1

    data = {"key":hex_key,"counter":0}
    json_data = json.dumps(data).encode()

    encrypted = fernet.encrypt(json_data)
    with open("ft_otp.key","wb") as file:
        file.write(encrypted)

    print("Key was successfully save in ftp_otp.key")
    return 0


def main():
    print("WELCOME TO FT_OTP")
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