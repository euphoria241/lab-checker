import requests
import browser_cookie3
import re

class Connected:

    def __init__(self):
        self.__session = requests.session()
        self.__name_task = ''
        self.__TRUE_CODE = 200
        return

    def getToken(self):
        if 'csrftoken' in self.__session.cookies:
            return self.__session.cookies['csrftoken']
        else:
            return self.__session.cookies['csrf']

    def authorization(self):
        URL = 'https://leetcode.com/accounts/login/'
        self.__session.get(URL)
        csrftoken = self.getToken()
        login_data = dict(csrfmiddlewaretoken=csrftoken, login='test_lab_2', password='Lab2Test', next='/')
        response = self.__session.post(URL, data=login_data, headers=dict(Referer=URL))
        print("User Authorization Status:", response.status_code)

    def getCAU(self, URL):
        return self.__session.get(URL, cookies=browser_cookie3.chrome()).cookies.values()[0]

    def getCookies(self, csrftoken):
        __cfduid = '__cfduid=' + self.__session.cookies.values()[1]
        token = 'csrftoken=' + csrftoken
        LEETCODE_SESSION = 'LEETCODE_SESSION=' + self.__session.cookies.values()[0]
        c_a_u = self.getCAU(str('https://leetcode.com/problems/'+self.__name_task+'/'))
        return str(__cfduid+'; '+token+'; '+LEETCODE_SESSION+'; '+c_a_u)

    def getHeaders(self):
        csrftoken = self.getToken()
        return {
                'authority': 'leetcode.com',
                'method': 'POST',
                'path': str('/problems/'+self.__name_task+'/submit/'),
                'scheme': 'https',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'content-length': '220',
                'content-type': 'application/json',
                'cookie': self.getCookies(csrftoken),
                'origin': 'https://leetcode.com',
                'referer': str('https://leetcode.com/problems/'+self.__name_task+'/submissions/'),
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
                'x-csrftoken': csrftoken
        }

    def solve(self, decision_json, name_task):
        self.__name_task = name_task
        response = self.__session.post(str('https://leetcode.com/problems/'+name_task+'/submit/'), json=decision_json, headers=self.getHeaders())
        print("\nTask", name_task, "Transfer Status:", response.status_code)
        if response.status_code != self.__TRUE_CODE: return
        submit_id = re.search(': (.*?)}', response.text).group(1)
        while True:
            self.__session.get(str('https://leetcode.com/submissions/detail/' + submit_id + '/check'))
            response = self.__session.get(str('https://leetcode.com/submissions/detail/' + submit_id + '/check/'))
            if '{"state": "STARTED"}' != response.text and '{"state": "PENDING"}' != response.text:
                print(response.json())
                break
