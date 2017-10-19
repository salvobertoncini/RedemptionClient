import requests
import json

class Request:

    url = "http://127.0.0.1:4200"
    headers = {'Content-type': 'application/json'}
    data = {}

    def __init__(self, url, data, headers):
        self.url = url
        self.data = data
        self.headers = headers

    def getUrl(self):
        return self.url

    def getDatas(self):
        return self.data

    def getHeaders(self):
        return self.headers

    def setUrl(self, url):
        self.url = url

    def setData(self, data):
        self.data = data

    def setHeaders(self, headers):
        self.headers = headers

    def CustomPostRequest(self, ReqObj):
        return requests.post(ReqObj.getUrl(), json=json.dumps(ReqObj.getData()), headers=ReqObj.getHeaders())
