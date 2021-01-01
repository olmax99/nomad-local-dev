#!/usr/bin/env sh
set -e

echo "[+] Install ansible-galaxy roles .."
if [ -f ~/requirements.yml ]; then
    ansible-galaxy install --roles-path /etc/ansible/roles -r ~/requirements.yml
else
  echo "[-] requirements.yml is missing.."
fi

# Verify insecure_key is loaded
if [ -f /tmp/insecure_key ]; then 
  cp /tmp/insecure_key ~/.ssh/id_rsa
  cmp /tmp/insecure_key ~/.ssh/id_rsa || cp /tmp/insecure_key ~/.ssh/id_rsa
else
  echo "[-] insecure_key is missing.."
fi

exec "$@"
