import requests
import browser_cookie3
import re

URL = 'https://leetcode.com/accounts/login/'
client = requests.session()
client.get(URL)
if 'csrftoken' in client.cookies:
    csrftoken = client.cookies['csrftoken']
else:
    csrftoken = client.cookies['csrf']

login_data = dict(csrfmiddlewaretoken=csrftoken, login='test_lab_2', password='Lab2Test', next='/')
response = client.post(URL, data=login_data, headers=dict(Referer=URL))
print("User Authorization Status:", response)

print("\nTask Add Digits")
URL2 = 'https://leetcode.com/problems/add-digits/'

cj = browser_cookie3.chrome()
r = client.get(URL2, cookies=cj)
c_a_u = r.cookies.values()[0]
# print(c_a_u)

URL3 = 'https://leetcode.com/problems/add-digits/submit/'

if 'csrftoken' in client.cookies:
    csrftoken = client.cookies['csrftoken']
else:
    csrftoken = client.cookies['csrf']

problems_login = {"question_id": "258",
                  "lang": "python3",
                  "typed_code": "class Solution:\n    def addDigits(self, num: int) -> int:        \n        res = num % 9\n        if res == 0 and num != 0:\n            return 9\n        return res"}

cookie = client.cookies

__cfduid = '__cfduid='+cookie.values()[1]
token = 'csrftoken='+csrftoken
LEETCODE_SESSION = 'LEETCODE_SESSION='+cookie.values()[0]
l = str(__cfduid+'; '+token+'; '+LEETCODE_SESSION+'; '+c_a_u)
# print(l)

s = {
    'authority': 'leetcode.com',
    'method': 'POST',
    'path': '/problems/add-digits/submit/',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-length': '220',
    'content-type': 'application/json',
    'cookie': l,
    'origin': 'https://leetcode.com',
    'referer': 'https://leetcode.com/problems/add-digits/submissions/',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'x-csrftoken': csrftoken
}

response = client.post(URL3,  json=problems_login, headers=s)
print("Task Transfer Status:", response)
# print(response.text)
submit_id = re.search(': (.*?)}', response.text).group(1)
# print(submit_id)


URL4 = str('https://leetcode.com/submissions/detail/'+submit_id+'/check/')
URL5 = str('https://leetcode.com/submissions/detail/'+submit_id+'/check')

while True:
    client.get(URL5)
    h = client.get(URL4)
    if '{"state": "STARTED"}' != h.text and '{"state": "PENDING"}' != h.text:
        print("Information:", "\n\tTask completed correctly:", h.json()["run_success"], "\n\tRuntime:", h.json()["status_runtime"], "\n\tMemory:", h.json()["memory"])
        break


print("\nTask Defanging An Ip Address")

URL6 = 'https://leetcode.com/problems/defanging-an-ip-address/'

cj = browser_cookie3.chrome()
r = client.get(URL6, cookies=cj)
c_a_u = r.cookies.values()[0]

URL7 = 'https://leetcode.com/problems/defanging-an-ip-address/submit/'

if 'csrftoken' in client.cookies:
    csrftoken = client.cookies['csrftoken']
else:
    csrftoken = client.cookies['csrf']

problems_login = {"question_id":"1205",
                  "lang":"python3",
                  "typed_code":"class Solution:\n    def defangIPaddr(self, address: str) -> str:\n        "}

cookie = client.cookies

__cfduid = '__cfduid='+cookie.values()[1]
token = 'csrftoken='+csrftoken
LEETCODE_SESSION = 'LEETCODE_SESSION='+cookie.values()[0]
l = str(__cfduid+'; '+token+'; '+LEETCODE_SESSION+'; '+c_a_u)
# print(l)

s = {
    'authority': 'leetcode.com',
    'method': 'POST',
    'path': '/problems/defanging-an-ip-address/submit/',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-length': '130',
    'content-type': 'application/json',
    'cookie': l,
    'origin': 'https://leetcode.com',
    'referer': 'https://leetcode.com/problems/defanging-an-ip-address/submissions/',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    'x-csrftoken': csrftoken
}

response = client.post(URL7,  json=problems_login, headers=s)
print("Task Transfer Status:", response)
# print(response.text)
submit_id = re.search(': (.*?)}', response.text).group(1)
# print(submit_id)

while True:
    client.get(URL5)
    h = client.get(URL4)
    if '{"state": "STARTED"}' != h.text and '{"state": "PENDING"}' != h.text:
        print("Information:", "\n\tTask completed correctly:", h.json()["run_success"], "\n\tRuntime:", h.json()["status_runtime"], "\n\tMemory:", h.json()["memory"])
        break