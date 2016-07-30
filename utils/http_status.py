# -*- coding: utf-8 -*-

# Http status information
# Created: 2016-7-22
# Copyright: (c)<smileboywtu@gmail.com>

import json

class Status(object):
    """customer status code"""

    # 状态信息
    success = 'ok'
    failure = 'error'

    # 状态码
    code = {
        'ok': 0,                    # 成功返回
        'err': -1,                  # 标准错误
        'unknown': 1,               # 位置错误
        'params_type_err': 72201,   # 参数类型错误
        'params_less_err': 72202,   # 参数缺失

        'db_field_err': 72203,      # 参数长度不符合要求
        'db_integrity_err': 72204,  # 破坏数据的完整性
        'db_nexist_err': 72205,     # 指定对象不存在

        'db_referenced_err': 72206  # 数据库有依赖，禁止删除
    }


# customer class json serializable
# http://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
class GeneralResponse(object):
    """customer general http response"""

    def __init__(self, code, errmsg, message, **kwargs):
        self.errcode = code
        self.errmsg = errmsg
        self.help = message
        self.general = kwargs

    def __dict__(self):
        self.general.update({
            'errcode': self.errcode,
            'errmsg': self.errmsg,
            'help': self.help,
        })
        return self.general

    def __repr__(self):
        return json.dumps(self.__dict__())


class ResponseFactory(object):
    """create reponse"""
    @staticmethod
    def create(errtype, message='', **kwargs):
        """construct response"""
        code = Status.code.get(errtype, 'unknown')
        errmsg = Status.success if code == 0 else Status.failure
        return GeneralResponse(code, errmsg, message, **kwargs)

    @staticmethod
    def ok_resp(message, **kwargs):
        return ResponseFactory.create(
            'ok',
            message=message,
            **kwargs
        )

    @staticmethod
    def params_type_err_resp(message):
        return ResponseFactory.create(
            'params_type_err',
            message=message
        )

    @staticmethod
    def params_less_err_resp(param):
        return ResponseFactory.create(
            'params_less_err',
            message= 'need param: {0}'.format(param)
        )

    @staticmethod
    def db_field_err_resp(exception):
        return ResponseFactory.create(
            'db_field_err',
            exception=exception
        )

    @staticmethod
    def db_integrity_err_resp(message):
        return ResponseFactory.create(
            'db_integrity_err',
            message=message
        )

    @staticmethod
    def db_nexist_err_resp(exception):
        return ResponseFactory.create(
            'db_nexist_err',
            message='choose another id.',
            exception=exception
        )

    @staticmethod
    def db_referenced_err_resp(id):
        return ResponseFactory.create(
            'db_referenced_err',
            message="module id {0} is referenced by others, you can't delete".format(id)
        )


if __name__ == '__main__':
    resp = ResponseFactory.create('params_type_err', message='need to integer type', exception='ValueError')
    print resp
