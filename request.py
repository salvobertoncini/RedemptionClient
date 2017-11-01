import requests
import json

class Request:

    url = ""
    headers = {'Content-type': 'application/json'}
    data = {}

    def __init__(self, data):
        self.url = "http://127.0.0.1:8000/"
        self.headers = {'Content-type': 'application/json'}
        self.data = data

    def getUrl(self):
        return self.url

    def getData(self):
        return self.data

    def getHeaders(self):
        return self.headers

    def setUrl(self, url):
        self.url = url

    def setData(self, data):
        self.data = data

    def setHeaders(self, headers):
        self.headers = headers

    def CustomPostRequest(self, data, url, header):
        r = requests.post(url=url, json=data, headers=header)
        return r.json()
