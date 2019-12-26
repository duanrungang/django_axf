from rest_framework.exceptions import APIException

from utils import errors


class ParamError(APIException):
    """ http参数错误
    """

    def __init__(self, err=errors.ERR_MSG_INVALID):
        self.detail = err

    def __str__(self):
        return self.msg