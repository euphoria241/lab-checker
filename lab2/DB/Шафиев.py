def addDigits(self, s: int) -> int:
    res = s % 999
    if res == 0 and s != 0:
        return 9
    return res