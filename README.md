<h1>42 Cybersecurity Projects</h1>

<h2>Arachnida</h2>

<p>This project consists of two distinct programs focused on image manipulation and metadata extraction:</p>

<h3>Spider</h3>
<p>A web crawler that recursively downloads images from a website. Features:</p>
<ul>
  <li>Image downloading from a specified URL</li>
  <li>Recursion depth limitation</li>
  <li>Restriction to specific domains</li>
  <li>Support for image formats: jpg, jpeg, png, gif, and bmp</li>
</ul>

<h4>How to Start:</h4>
<pre><code>
# Navigate to the project directory
cd arachnida

# Run Spider
python3 spider.py [options] [URL]
</code></pre>

<h3>Scorpion</h3>
<p>An image analysis tool that extracts and displays image file metadata. Features:</p>
<ul>
  <li>Reading EXIF data and other metadata</li>
  <li>Display of technical information (creation date, device used, etc.)</li>
  <li>Detection of potential sensitive information</li>
  <li>Support for the same formats as Spider</li>
</ul>

<h4>How to Start:</h4>
<pre><code>
# Navigate to the project directory
cd arachnida

# Run Scorpion
python3 scorpion.py [options] [image_file(s)]
</code></pre>

<h2>ft_otp</h2>

<p>Implementation of a Time-based One-Time Password (TOTP) generator compliant with RFC 6238. This program:</p>
<ul>
  <li>Generates time-based one-time passwords</li>
  <li>Uses a securely stored secret key</li>
  <li>Creates temporary codes compatible with standard authentication applications</li>
  <li>Provides reliable and secure two-factor authentication</li>
</ul>

<h4>How to Start:</h4>
<pre><code>

# Navigate to the project directory
cd ft_otp


# Generate a new key (adding -q for a qrcode)
python3 ft_otp.py -g [key_file] -q 

# Generate a TOTP code
python3 ft_otp.py -k [key_file]
</code></pre>

<h2>ft_onion</h2>

<p>Project for deploying a hidden service on the Tor network. Objectives:</p>
<ul>
  <li>Configuration of a website accessible only via the Tor network</li>
  <li>Setup of a minimalist web server</li>
  <li>Creation of an .onion address to access the service</li>
  <li>Implementation of security measures to protect the service's anonymity</li>
</ul>

<h4>How to Start:</h4>
<pre><code>

# Navigate to the project directory
cd ft_onion

# Launch the Docker


</code></pre>

<p>Each project explores different aspects of cybersecurity, from data analysis to online anonymity and secure authentication.</p>