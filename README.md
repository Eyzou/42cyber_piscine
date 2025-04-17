# 42 Cybersecurity Projects

I've mainly used Python for this piscine.

## Arachnida
This project consists of two distinct programs focused on image manipulation and metadata extraction:

#### Spider
A web crawler that recursively downloads images from a website. Features:

- Image downloading from a specified URL  
- Recursion depth limitation  
- Restriction to specific domains  
- Support for image formats: jpg, jpeg, png, gif, and bmp  

#### How to Start:

```bash
# Navigate to the project directory
cd arachnida
# Run Spider
python3 spider.py [options] [URL]
```

#### Scorpion
An image analysis tool that extracts and displays image file metadata. Features:

- Reading EXIF data and other metadata  
- Display of technical information (creation date, device used, etc.)  
- Detection of potential sensitive information  
- Support for the same formats as Spider  

#### How to Start:
```bash
# Navigate to the project directory
cd arachnida
# Run Scorpion
python3 scorpion.py [options] [image_file(s)]
```

## ft_otp

Implementation of a Time-based One-Time Password (TOTP) generator compliant with RFC 6238. This program:

- Generates time-based one-time passwords  
- Uses a securely stored secret key  
- Creates temporary codes compatible with standard authentication applications  
- Provides reliable and secure two-factor authentication  

#### How to Start:

```bash
# Navigate to the project directory
cd ft_otp
# Generate a new key (adding -q for a qrcode)
python3 ft_otp.py -g [key_file] -q 
# Generate a TOTP code
python3 ft_otp.py -k [key_file]
```

## ft_onion

Project for deploying a hidden service on the Tor network. Objectives:

- Configuration of a website accessible only via the Tor network  
- Setup of a minimalist web server  
- Creation of an .onion address to access the service 
- Implementation of security measures to protect the service's anonymity  - ssh 

#### How to Start:

```bash
# Navigate to the project directory
cd ft_onion
# Launch the Docker
make build
make run
#into the container to enter the Tor website via ssh
torsocks ssh -i /home/ehamm/.ssh/id_ed25519 -p 4242 ehamm@xxx.onion
#into the container to enter the localhost  via ssh
ssh -i /home/ehamm/.ssh/id_ed25519 -p 4242 localhost

```

## reverse_me

See the README.ms into the folder!


