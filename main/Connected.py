import requests
import browser_cookie3
import re

class Connected:

    def __init__(self):
        self.__session = requests.session()
        self.__name_task = ''
        self.__TRUE_CODE = 200
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
        Функция авторизации пользователя на сайте
    """
    def authorization(self):
        URL = 'https://leetcode.com/accounts/login/'
        self.__session.get(URL)
        csrftoken = self.getToken()
        login_data = dict(csrfmiddlewaretoken=csrftoken, login='test_lab_2', password='Lab2Test', next='/')
        response = self.__session.post(URL, data=login_data, headers=dict(Referer=URL))
        print("User Authorization Status:", response.status_code)

    """
        Функция возвращает cua - закодированное название клиента и браузера
    """
    def getCAU(self, URL):
        return self.__session.get(URL, cookies=browser_cookie3.chrome()).cookies.values()[0]

    """
        Функция возвращает куки
    """
    def getCookies(self, csrftoken):
        __cfduid = '__cfduid=' + self.__session.cookies.values()[1]
        token = 'csrftoken=' + csrftoken
        LEETCODE_SESSION = 'LEETCODE_SESSION=' + self.__session.cookies.values()[0]
        c_a_u = self.getCAU(str('https://leetcode.com/problems/'+self.__name_task+'/'))
        return str(__cfduid+'; '+token+'; '+LEETCODE_SESSION+'; '+c_a_u)

    """
        Функция возвращает хедер
    """
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

    """
        Функция узнает и возващает backend id задачи
    """
    def getQuestionId(self):
        req = {"operationName":"questionData","variables":{"titleSlug":self.__name_task},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    enableTestMode\n    envInfo\n    libraryUrl\n    __typename\n  }\n}\n"}
        response = self.__session.post("https://leetcode.com/graphql", json=req, headers=dict(Referer="https://leetcode.com/graphql"))
        if response.status_code != self.__TRUE_CODE: return
        return response.json()["data"]["question"]["questionId"]

    """
        Функция отправляет на сервер решенние в виде json и, если решение правильное,
        получает id ответа, через который достает с сервера информацию об ответе
    """
    def solve(self, decision_json, name_task):
        self.__name_task = name_task
        decision_json["question_id"] = self.getQuestionId()
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
