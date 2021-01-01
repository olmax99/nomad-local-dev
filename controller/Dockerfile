FROM alpine:latest

# Install dependencies
RUN apk update && \
    apk upgrade &&  \
    apk add --no-cache --update ansible bash libffi-dev py-netaddr openssh sshpass zip python3 py3-pip

WORKDIR /etc/ansible

# Initialize
RUN mkdir -p /etc/ansible && mkdir /root/.ssh

COPY requirements.yml /root/requirements.yml
COPY ansible.cfg /root/ansible.cfg

COPY insecure_key /tmp/insecure_key

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
# RUN
CMD ["/bin/sh"]
