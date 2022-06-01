import datetime
import sys
import hashlib

from tellyget.utils.cipher import Cipher


def usage():
    print('Usage:')
    print('\t\ttellyget-decrypt -h')
    print('\t\ttellyget-decrypt <authenticator> [--all]')


def find_encryption_keys(authenticator, passwd, find_all=False, debug=False):
    key = hashlib.md5(passwd.encode()).hexdigest()[:24].upper()
    plain_text = Cipher(key).decrypt(authenticator)
    return key
