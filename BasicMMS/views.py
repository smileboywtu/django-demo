# -*- coding: utf-8 -*-

# 基础模块管理视图
# Created: 2016-7-22
# Copyright: (c) 2016<smileboywtu@gmail.com>


# TODO(chenbo) 由于使用了SQLite3作为后端的数据存储，当出现字段超出限制的情况，不会报错
# TODO(chenbo) 使用PUT和DELETE方法的时候，需要自己从body中提取参数
# TODO(chenbo) 异常处理的详情在utils中


# 2016/7/23: 成功创建对象返回对象的详细信息, 修改对象后返回修改后的信息

import json

from models import BasicModule
from VerMS.models import VerModule
from EnvMS.models import EnvModule
from utils.http_status import ResponseFactory
from utils.http_response import safe_response, process_frame, split_page


def get_basic_modules(request):
    """
    获取所有的基础模块信息，包括基础模块的名称和描述

    :param request: object, http request
    :return: json
    """
    # 实际的业务逻辑
    @process_frame(request, 'GET')
    @safe_response
    def func():
        """

        :return: response string
        """
        module_list = []
        # get limit information
        full = int(request.GET.get('full', 0))
        if full:
            module_objects = BasicModule.objects.order_by('-id')
        else:
            limit = int(request.GET['pageSize'])
            index = int(request.GET['currentPage']) - 1
            offset = index * limit
            module_objects = BasicModule.objects.order_by('-id')[offset:offset+limit]
        for obj in module_objects:
            # 判断这个基础模块是否能够被删掉
            item = {
                'id': obj.id,
                'name': obj.name,
                'description': obj.description,
            }
            if not full:
                rely =  0 if len(EnvModule.objects.filter(moduleID=obj)[:1]) == 0 and \
                             len(VerModule.objects.filter(moduleID=obj)[:1]) == 0 else 1
                item.update({'rely': rely})
            module_list.append(item)
        if full:
            return json.dumps(module_list)
        else:
            total = BasicModule.objects.count()
            return json.dumps({'array': module_list, 'total': total})

    return func()


def add_basic_module(requst):
    """
    添加新的基础模块
    处理的异常：
        参数不全，缺少名称或者描述
        模块命名冲突
        参数超过数据库表的限制

    :param requst: object, http request
    :return: status information
    """
    # 实际添加业务逻辑流程
    @process_frame(requst, 'POST')
    @safe_response
    def func():
        """

        :return: response string
        """
        module_name = requst.POST['name']
        module_description = requst.POST['description']
        new_module = BasicModule(name=module_name, description=module_description)
        new_module.save()
        # 返回更多有用的信息
        resp = {
            'id': new_module.id,
            'name': module_name,
            'description': module_description
        }
        return ResponseFactory.ok_resp(
            message='new basic module add successfully.',
            **resp
        )

    return func()


def update_basic_module(request):
    """
    修改基础模块信息
    处理的异常：
        id类型错误
        指定ID不存在
        参数不合法
        完整性约束

    :param request: object, http request information
    :return: status information
    """
    @process_frame(request, 'POST')
    @safe_response
    def func():
        """

        :return: reaponse string
        """
        module_id = int(request.POST['id'])
        module = BasicModule.objects.get(id=module_id)
        module.name = request.POST.get('name', module.name)
        module.description = request.POST.get('description', module.description)
        module.save()
        resp = {
            'id': module.id,
            'name': module.name,
            'description': module.description
        }
        return ResponseFactory.ok_resp(
            message='basic module {0} update successfully.'.format(module_id),
            **resp
        )

    return func()


def delete_basic_module(request):
    """
    删除一个基础模块
    处理的异常：
        id类型错误
        缺少参数
        指定id不存在

    :param request: object, http request
    :param module_id: module id
    :return: status information
    """
    @process_frame(request, 'POST')
    @safe_response
    def func():
        """

        :return: response string
        """
        module_id = int(request.POST['id'])
        module = BasicModule.objects.get(id=module_id)
        rely =  0 if len(EnvModule.objects.filter(moduleID=module)[:1]) == 0 and \
                     len(VerModule.objects.filter(moduleID=module)[:1]) == 0 else 1
        if rely:
            return ResponseFactory.db_referenced_err_resp(module_id)
        module.delete()
        return ResponseFactory.ok_resp(
            'basic module {0} remove successfully.'.format(module_id)
        )

    return func()
