import json
import re
import requests
import socket
from requests_toolbelt.adapters import socket_options
from urllib.parse import urlunparse, urlparse

from tellyget.utils.authenticator import Authenticator


class Auth:
    def __init__(self, args):
        self.args = args
        self.session = None
        self.base_url = ''

    def authenticate(self):
        self.session = self.get_session()
        self.base_url = self.get_base_url()
        print('base_url: ' + self.base_url)
        self.login()

    def get_session(self):
        session = requests.Session()
        if self.args.interface is not None:
            options = [(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, self.args.interface.encode())]
            adapter = socket_options.SocketOptionsAdapter(socket_options=options)
            session.mount("http://", adapter)
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.0 (KHTML, like Gecko)',
        }
        return session

    def get_base_url(self):
        params = {'UserID': self.args.user, 'Action': 'Login'}
        response = self.session.get(self.args.authurl, params=params, allow_redirects=False)
        url = response.headers.get('Location')
        # noinspection PyProtectedMember
        return urlunparse(urlparse(url)._replace(path='', query=''))

    def login(self):
        token = self.get_token()
        authenticator = Authenticator(self.args.passwd).build(token, self.args.user, self.args.imei, self.args.address, self.args.mac)
        params = {
            'client_id': 'smcphone',
            'DeviceType': 'deviceType',
            'UserID': self.args.user,
            'DeviceVersion': 'deviceVersion',
            'userdomain': 2,
            'datadomain': 3,
            'accountType': 1,
            'authinfo': authenticator,
            'grant_type': 'EncryToken',
        }
        self.session.get(self.base_url + '/EPG/oauth/v2/token', params=params)

    def get_token(self):
        params = {
            'response_type': 'EncryToken',
            'client_id': 'smcphone',
            'userid': self.args.user,
        }
        response = self.session.get(f'{self.base_url}/EPG/oauth/v2/authorize', params=params)
        j = json.loads(response.text)
        return j['EncryToken']
