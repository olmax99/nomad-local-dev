#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# NOTE: This file is from https://github.com/alibaba/ansible-provider-docs/blob/master/contrib/vault/vault-keyring-client.py
#
# IT IS BEING ADJUSTED TO WORK WITH PASS https://www.passwordstore.org/
# ==============================================================================
# (c) 2014, Matt Martz <matt@sivel.net>
# (c) 2016, Justin Mayer <https://justinmayer.com/>
# This file is part of Ansible.
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
# =============================================================================
#
# This script is to be used with ansible-vault's --vault-id arg
# to retrieve the vault password via your local password-store.
#
# https://www.passwordstore.org/
#
# This file *MUST* be saved with executable permissions. Otherwise, Ansible
# will try to parse as a password file and display: "ERROR! Decryption failed"
#
# The `qpass` Python module is required: https://pypi.org/project/keyring/
#
# By default, this script will restore the specified password from the
# password-store, whose location is indicated in ansible.cfg. Example:
#
# [vault]
# storedir = ~/.password-store
#
# In useage like:
#
#    ansible-vault --vault-id keyring_id@contrib/vault/vault-keyring-client.py view some_encrypted_file
#
#  --vault-id will call this script like:
#
#     contrib/vault/vault-keyring-client.py --vault-id keyring_id
#
# That will retrieve the password from password-store for the
# key 'keyring_id'. The equilivent of:
#
#      keyring_id = keyprefix + keyname
#
# If no vault-id name is specified to ansible command line, the vault-keyring-client.py
# script will be called without a '--vault-id' and will default to the keyring_id 'ansible-vault'
#
# You can configure the `vault_password_file` option in ansible.cfg:
#
# [defaults]
# ...
# vault_password_file = /path/to/vault-keyring-client.py
# ...
#
# To set your password, `cd` to your project directory and run:
#
#   # will use default keyring service / vault-id of 'ansible'
#   #/path/to/vault-keyring-client.py --set
#
#   pass init "Ansible Controller Password Storage Key"
#   pass insert ansible-vault
#
#
# If you choose not to configure the path to `vault_password_file` in
# ansible.cfg, your `ansible-playbook` command might look like:
#
# ansible-playbook --vault-id=keyring_id@/path/to/vault-keyring-client.py site.yml

ANSIBLE_METADATA = {
    "status": ["preview"],
    "supported_by": "community",
    "version": "1.0",
}

import argparse
import sys
import getpass
import qpass

from ansible.config.manager import ConfigManager

KEYNAME_UNKNOWN_RC = 2


def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Get a vault password from user keyring"
    )

    parser.add_argument(
        "--vault-id",
        action="store",
        default=None,
        dest="vault_id",
        help="name of the vault secret to get from keyring",
    )
    parser.add_argument(
        "--username",
        action="store",
        default=None,
        help="the username whose keyring is queried",
    )
    parser.add_argument(
        "--set",
        action="store_true",
        default=False,
        dest="set_password",
        help="set the password instead of getting it",
    )
    return parser


def main():
    config_manager = ConfigManager()
    username = config_manager.data.get_setting("vault.storedir")
    if not username:
        username = "~/.password-store"

    keyprefix = config_manager.data.get_setting("vault.keyprefix")
    if not keyprefix:
        keyprefix = None

    keyname = config_manager.data.get_setting("vault.keyname")
    if not keyname:
        keyname = "dev"

    key = keyprefix + keyname if keyprefix else keyname

    arg_parser = build_arg_parser()
    args = arg_parser.parse_args()

    username = args.username or username
    keyname = args.vault_id or key

    print("username: %s keyname: %s" % (username, key))

    if args.set_password:
        # intro = 'Storing password in "{}" user keyring using key name: {}\n'
        # sys.stdout.write(intro.format(username, key))
        # password = getpass.getpass()
        # confirm = getpass.getpass("Confirm password: ")
        # if password == confirm:
        #     keyring.set_password(key, username, password)
        # else:
        sys.stderr.write("Storing Passwords is not supported with 'pass'\n")
        sys.exit(1)
    else:
        qpass.DEFAULT_DIRECTORY = username
        s = qpass.PasswordStore()
        e = qpass.PasswordEntry(store=s, name=key)
        secret = e.text
        if secret is None:
            sys.stderr.write(
                'vault-keyring-client could not find key="%s" for user="%s" via backend="%s"\n'
                % (keyname, username, s.repr())
            )
            sys.exit(KEYNAME_UNKNOWN_RC)

        # print('secret: %s' % secret)
        sys.stdout.write("%s\n" % secret)

    sys.exit(0)


if __name__ == "__main__":
    main()
