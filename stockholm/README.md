# Stockholm - Educational Ransomware Simulator

Educational project for 42 Cybersecurity Piscine. Simulates ransomware behavior by encrypting files with Wannacry-targeted extensions using AES encryption (Fernet).

## Installation & Testing

# 1. Build and Run
make && make exec

# 2. Inside Container - Encryption Test

Check test files exist
ls -la ~/infection

Run encryption (files will be encrypted with .ft extension)
python3 /app/stockholm.py

Verify files are encrypted
ls -la ~/infection
cat ~/infection/test.txt.ft  # Should show encrypted content

# 3. Decryption Test

Decrypt using the key from previous step
python3 /app/stockholm.py --reverse YOUR_KEY_HERE

Verify files are restored
ls -la ~/infection
cat ~/infection/test.txt  # Should show original content

# Usage: 

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