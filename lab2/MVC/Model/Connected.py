import time

import requests
import browser_cookie3
import re
import bs4 as bs
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import qApp


class Connected:

    def __init__(self):
        self.__session = requests.session()
        self.__name_task = ''
        self.__TRUE_CODE = 200
        self.__state_id = ''
        self.__client_id = ''
        self.__authenticity_token = ''
        self.__ga_id = ''
        self.__webauthn_support = 'supported'
        self.__webauthn_iuvpaa_support = 'unsupported'
        self.__timestamp = ''
        self.__timestamp_secret = ''
        self.__git_login = "testGitLab2"
        self.__git_password = "Test2Lab"
        self.__URL_author = "https://leetcode.com/accounts/github/login/?next=%2F"
        self.__URL_header = "https://leetcode.com/graphql"
        self.__URL_git = ""
        self.__URL_git_session = "https://github.com/session"
        self.__URL_git_verification = ""
        return

    """
        Функция возвращает токен сессии
    """

    def getToken(self):
        if 'csrftoken' in self.__session.cookies:
            return self.__session.cookies['csrftoken']
        else:
            return self.__session.cookies['csrf']

    """
        Функция авторизации пользователя на сайте через авторизацию на GitHub.com
    """

    def authorization(self):
        response = self.__session.get(self.__URL_author, headers=dict(Refere=self.__URL_header))
        sauce = response.text
        soup = bs.BeautifulSoup(sauce, "html.parser")
        meta = soup.findAll('a')
        for element in meta:
            if element.get('data-hydro-click') != None:
                a = element.get('data-hydro-click').find('state%3D')
                b = element.get('data-hydro-click').find('","referrer"')
                self.__state_id = element.get('data-hydro-click')[a + 8:b]
                a = element.get('data-hydro-click').find('client_id%3D')
                b = element.get('data-hydro-click').find('%26redirect_uri%3D')
                self.__client_id = element.get('data-hydro-click')[a + 12:b]
                a = element.get('data-hydro-click').find('"originating_url":"')
                b = element.get('data-hydro-click').find('","referrer"')
                self.__URL_git = element.get('data-hydro-click')[a + 19:b]

        data = dict(client_id=self.__state_id,
                    return_to='/login/oauth/authorize?client_id=' + self.__state_id + '&redirect_uri=https%3A%2F%2Fleetcode.com%2Faccounts%2Fgithub%2Flogin%2Fcallback%2F&response_type=code&scope=user%3Aemail&state=' + self.__client_id)
        response = self.__session.get(self.__URL_git, headers=dict(Refere=self.__URL_header), data=data)
        print("User Authorization Git Status:", response.status_code)
        sauce = response.text
        soup = bs.BeautifulSoup(sauce, "html.parser")
        form = soup.find('form')
        inputs = form.find_all('input', type='hidden')
        for element in inputs:
            if element.get('name') == 'authenticity_token':
                self.__authenticity_token = element.get('value')
            elif element.get('name') == 'timestamp':
                self.__timestamp = element.get('value')
            elif element.get('name') == 'timestamp_secret':
                self.__timestamp_secret = element.get('value')
        meta = soup.findAll('meta')
        for element in meta:
            if element.get('name') == 'octolytics-dimension-visitor_id':
                self.__ga_id = element.get('content')
                break
        self.__ga_id = self.__ga_id[0:8] + '.' + self.__ga_id[8:19]

        data = {
            "commit": "Sign+in",
            "utf8": "✓",
            "authenticity_token": self.__authenticity_token,
            "ga_id": self.__ga_id,
            "login": self.__git_login,
            "password": self.__git_password,
            "webauthn-support": self.__webauthn_support,
            "webauthn-iuvpaa-support": self.__webauthn_iuvpaa_support,
            "required_field_cb11": "",
            "timestamp": self.__timestamp,
            "timestamp_secret": self.__timestamp_secret
        }
        response = self.__session.post(self.__URL_git_session, data=data, headers=dict(Refere=self.__URL_header))
        print("User Authorization LeetCode Status:", response.status_code)
        sauce = response.text
        soup = bs.BeautifulSoup(sauce, "html.parser")
        div = soup.find_all('div')
        incorrect = True
        verification = False
        for element in div:
            if element.get('class') is not None:
                if element.get('class')[0] == 'container':
                    if element.getText().find('Incorrect username or password.') > 0:
                        incorrect = False
                        break
                elif element.get('class')[0] == 'two-factor-help':
                    if element.getText().find('t*************@mail.ru') > 0:
                        verification = True
                        print(response.text)
                        break
        return response.status_code, incorrect, verification

    """
        Функция возвращает cua - закодированное название клиента и браузера
    """

    def getCAU(self, URL):
        return self.__session.get(URL, cookies=browser_cookie3.chrome()).cookies.values()[0]

    """
        Функция возвращает куки
    """

    def getCookies(self, csrftoken):
        __cfduid = '__cfduid=' + self.__session.cookies.values()[4]
        token = 'csrftoken=' + csrftoken
        LEETCODE_SESSION = 'LEETCODE_SESSION=' + self.__session.cookies.values()[3]
        c_a_u = self.getCAU(str('https://leetcode.com/problems/' + self.__name_task + '/'))
        return str(__cfduid + '; ' + token + '; ' + LEETCODE_SESSION + '; ' + c_a_u)

    """
        Функция возвращает хедер
    """

    def getHeaders(self):
        csrftoken = self.getToken()
        return {
            'authority': 'leetcode.com',
            'method': 'POST',
            'path': str('/problems/' + self.__name_task + '/submit/'),
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '220',
            'content-type': 'application/json',
            'cookie': self.getCookies(csrftoken),
            'origin': 'https://leetcode.com',
            'referer': str('https://leetcode.com/problems/' + self.__name_task + '/submissions/'),
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'x-csrftoken': csrftoken
        }

    """
        Функция узнает и возващает backend id задачи
    """

    def getQuestionId(self):
        req = {"operationName": "questionData", "variables": {"titleSlug": self.__name_task},
               "query": "query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}
        response = self.__session.post("https://leetcode.com/graphql", json=req,
                                       headers=dict(Referer="https://leetcode.com/graphql"))
        if response.status_code != self.__TRUE_CODE: return
        return response.json()["data"]["question"]["questionId"]

    """
        Функция отправляет на сервер решенние в виде json и, если решение правильное,
        получает id ответа, через который достает с сервера информацию об ответе
    """

    def solve(self, decision_json, name_task):
        self.pbar.setValue(0)
        self.progressBarWakeUp()
        self.__name_task = name_task
        decision_json["question_id"] = self.getQuestionId()
        response = self.__session.post(str('https://leetcode.com/problems/' + name_task + '/submit/'),
                                       json=decision_json, headers=self.getHeaders())
        print("\nTask", name_task, "Transfer Status:", response.status_code)
        self.progressBarWakeUp()
        if response.status_code != self.__TRUE_CODE:
            return 'Error'
        submit_id = re.search(': (.*?)}', response.text).group(1)
        self.progressBarWakeUp()
        while True:
            self.__session.get(str('https://leetcode.com/submissions/detail/' + submit_id + '/check'))
            response = self.__session.get(str('https://leetcode.com/submissions/detail/' + submit_id + '/check/'))
            if '{"state": "STARTED"}' != response.text and '{"state": "PENDING"}' != response.text:
                response_json = response.json()
                print(response_json)
                break
        self.progressBarWakeUp()
        solve_dict = dict()
        solve_dict['status_msg'] = response_json['status_msg']
        solve_dict['status_runtime'] = response_json['status_runtime']
        solve_dict['status_memory'] = response_json['status_memory']
        if response_json['status_msg'] == 'Wrong Answer':
            solve_dict['input'] = response_json['input']
            solve_dict['code_output'] = response_json['code_output']
            solve_dict['expected_output'] = response_json['expected_output']
        else:
            solve_dict['input'] = ''
            solve_dict['code_output'] = ''
            solve_dict['expected_output'] = ''
        if not response_json['run_success']:
            solve_dict['full_compile_error'] = response_json['full_compile_error']
        else:
            solve_dict['full_compile_error'] = ''
        self.progressBarWakeUp()
        QTimer.singleShot(0, self.startLoop2)
        qApp.processEvents()
        if self.pbar.value() == self.pbar.maximum():
            self.pbar.reset()
        return solve_dict

    def setPbar(self, pbar, pbar2, size):
        self.pbar = pbar
        self.pbar2 = pbar2
        self.size = 100 // size

    def startLoop(self):
        time.sleep(0.05)
        value = self.pbar.value() + 20
        self.pbar.setValue(value)

    def startLoop2(self):
        time.sleep(0.05)
        value = self.pbar2.value() + self.size
        self.pbar2.setValue(value)

    def progressBarWakeUp(self):
        QTimer.singleShot(0, self.startLoop)
        qApp.processEvents()
