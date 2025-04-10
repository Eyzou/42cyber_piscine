FROM alpine:latest

RUN apk update && apk add --no-cache \
    nginx \
    tor \
    openssh \
    && rm -rf /var/cache/apk/*

COPY nginx.conf /etc/nginx/nginx.conf
COPY torrc /etc/tor/torrc
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80 4242

COPY send_config /send_config
RUN chmod +x /send_config

CMD ["/send_config"]