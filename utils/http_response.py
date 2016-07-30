# -*- coding: utf-8 -*-

# 处理HTTP返回信息， 包括状态信息和错误信息，辅助信息
# Created: 2016-7-23
# Copyright: (c)<smileboywtu@gmail.com>

import logging
import traceback

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.exceptions import FieldError, ObjectDoesNotExist

from http_status import ResponseFactory


def safe_response(func):
    """保证需要处理的错误可以被捕获并且正确返回辅助信息"""

    def __wrapper__(*args, **kwargs):
        """wrapper for func"""
        try:
            resp = func(*args, **kwargs)
        except KeyError as e:
            resp = ResponseFactory.params_less_err_resp(e.args)
        except ValueError as e:
            resp = ResponseFactory.params_type_err_resp(e.message)
        except IntegrityError as e:
            resp = ResponseFactory.db_integrity_err_resp(str(e))
        except FieldError as e:
            resp = ResponseFactory.db_field_err_resp(str(e))
        except ObjectDoesNotExist as e:
            resp = ResponseFactory.db_nexist_err_resp(str(e))
        except:
            logging.getLogger('root').error('unknown internal error happens: {0}'.format(traceback.format_exc()))
            resp = ResponseFactory.create('unknow', 'internal error.')
        return resp
    return __wrapper__


def process_frame(request, method):
    """
    判断是否满足HTTP方法体要求, 提供请求级别的包装
    :param request: 请求对象
    :param method: 支持的请求方法
    """
    def _decorator(func):
        def __wrapper__(*args, **kwargs):
            if request.method == method:
                resp = func(*args, **kwargs)
                return HttpResponse(resp)
            return HttpResponseNotAllowed([method])
        return __wrapper__
    return _decorator


def split_page(array, limit, index):
    """
    按限制要求分割数组，返回下标所指向的页面

    :param array: 需要分割的数组
    :param limit: 每个数组的大小
    :param index: 需要返回的分割后的数组
    :return: 数组
    """
    end = index * limit
    start = end - limit
    return array[start:end]
