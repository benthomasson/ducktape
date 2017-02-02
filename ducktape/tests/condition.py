
class TestCondition(object):
    def __init__(self, status):
        self._status = str(status).lower()

    def __eq__(self, other):
        return str(self).lower() == str(other).lower()

    def __str__(self):
        return self._status

    def to_json(self):
        return str(self).upper()

ON_FAIL = TestCondition("on fail")
ON_PASS = TestCondition("on pass")


