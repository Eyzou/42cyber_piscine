FROM debian:buster

# Install packages in one RUN layer (reduces image size)
RUN apt-get update && \
    apt-get install -y \
    nginx \
    curl \
    openssh-server \
    tor \
    && rm -rf /var/lib/apt/lists/*

# Configure SSH
RUN useradd -m -s /bin/bash ehamm
RUN echo 'ehamm:ehamm' | chpasswd
RUN mkdir -p /home/ehamm/.ssh && \
    chmod 700 /home/ehamm/.ssh

# Generate SSH keys
RUN ssh-keygen -A && \
    ssh-keygen -t ed25519 -f /home/ehamm/.ssh/id_ed25519 -N "" && \
    cp /home/ehamm/.ssh/id_ed25519.pub /home/ehamm/.ssh/authorized_keys && \
    chown -R ehamm:ehamm /home/ehamm/.ssh && \
    chmod 600 /home/ehamm/.ssh/authorized_keys

# Copy config files
COPY nginx.conf /etc/nginx/nginx.conf
COPY index.html /var/www/html
COPY torrc /etc/tor/torrc
COPY sshd_config /etc/ssh/sshd_config

# Startup script
COPY start_services.sh /start_services.sh
RUN chmod +x /start_services.sh

EXPOSE 80 4242

CMD ["/start_services.sh"]

