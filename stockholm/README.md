# Stockholm - Educational Ransomware Simulator

Educational project for 42 Cybersecurity Piscine. Simulates ransomware behavior by encrypting files with Wannacry-targeted extensions using AES encryption (Fernet).

## ⚠️ Warning

**This is for educational purposes only.** Only use in isolated environments (Docker/VM). Never use on production systems or important files.

## Requirements
- Docker
- Make

## Installation & Testing

# 1. Build and Run
Build Docker image and start container
make
make exec

# 2. Inside Container - Encryption Test

Check test files exist
ls -la ~/infection

Run encryption (files will be encrypted with .ft extension)
python3 /app/stockholm.py

#erify files are encrypted
ls -la ~/infection
cat ~/infection/test.txt.ft  # Should show encrypted content

# 3. Decryption Test

Decrypt using the key from previous step
python3 /app/stockholm.py --reverse YOUR_KEY_HERE

Verify files are restored
ls -la ~/infection
cat ~/infection/test.txt  # Should show original content

# Usage: 
Show help
python3 /app/stockholm.py --help

Show version
python3 /app/stockholm.py --version

Encrypt files (verbose)
python3 /app/stockholm.py

Encrypt files (silent mode)
python3 /app/stockholm.py --silent

Decrypt files
python3 /app/stockholm.py --reverse YOUR_ENCRYPTION_KEY

Decrypt silently
python3 /app/stockholm.py -r YOUR_KEY -s

### How It Works

Encryption: Generates a random Fernet key, encrypts all files in ~/infection with Wannacry extensions, renames them with .ft
Key Storage: Saves encryption key to ~/.stockholm_key
Decryption: Uses provided key to decrypt .ft files and restore original names

### Technical Details

Algorithm: AES-128 (Fernet from cryptography library)
Target: Only files in ~/infection directory
Extensions: 176 Wannacry-targeted file extensions
Language: Python 3.9