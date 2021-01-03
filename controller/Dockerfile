FROM debian:buster-slim


RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y python3-pip bash tree sshpass git openssh-client pass unzip && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean
    
RUN pip3 install --upgrade pip cffi && \
    pip install ansible==2.10.3 && \
    pip install mitogen ansible-lint jmespath && \
    pip install --upgrade pywinrm \
    pip install netaddr \
    pip install keyring \
    pip install qpass

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
