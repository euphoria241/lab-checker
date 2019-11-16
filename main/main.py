from Connected import Connected
import time

connected = Connected()
connected.authorization()

decision_json = {"question_id": "258",
                  "lang": "python3",
                  "typed_code": "class Solution:\n    def addDigits(self, num: int) -> int:        \n        res = num % 9\n        if res == 0 and num != 0:\n            return 9\n        return res"}
connected.solve(decision_json, 'add-digits')

time.sleep(3)

decision_json = {"question_id":"1205",
                 "lang":"python3",
                 "typed_code":"class Solution:\n    def defangIPaddr(self, address: str) -> str:\n        return address.replace('.','[.]')\n        "}
connected.solve(decision_json, 'defanging-an-ip-address')

time.sleep(3)

decision_json = {"question_id":"742",
                 "lang":"python3",
                 "typed_code":"class Solution:\n    def toLowerCase(self, str: str) -> str:\n        return str.lower();"}
connected.solve(decision_json, 'to-lower-case')