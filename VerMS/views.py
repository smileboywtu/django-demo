
# -*- coding: utf-8 -*-

# 版本管理视图，管理版本和版本中的模块
# Created: 2016-7-22
# Copyright: (c) 2016<smileboywtu@gmail.com>


# TODO(chenbo) 由于使用了SQLite3作为后端的数据存储，当出现字段超出限制的情况，不会报错
# TODO(chenbo) 使用PUT和DELETE方法的时候，需要自己从body中提取参数
# TODO(chenbo) Django ORM 中外键的约束需要手动get

# 2016/7/23: 成功创建对象返回对象的详细信息, 修改对象后返回修改后的信息

import json

from models import VerList, VerModule
from BasicMMS.models import BasicModule
from utils.http_status import ResponseFactory
from utils.http_response import safe_response, process_frame, split_page


#####################################################
# 版本管理
#####################################################
def get_versions(request):
    """
    获取所有的版本列表

    :param request: object, http request
    :return: json
    """
    @process_frame(request, 'GET')
    @safe_response
    def func():
        ver_list = []
        index = int(request.GET['currentPage']) - 1
        limit = int(request.GET['pageSize'])
        offset = index * limit
        ver_objects = VerList.objects.order_by('-id')[offset:limit+offset]
        for obj in ver_objects:
            ver_list.append(
                {
                    'id': obj.id,
                    'name': obj.name,
                    'description': obj.description
                }
            )
        # 分页处理
        total = VerList.objects.count()
        return json.dumps({'datalist': ver_list, 'total': total})

    return func()


def get_ver(request):
    """
    获取版本的详情，返回当前版本的模块情况

    :param request:
    :return:
    """
    @process_frame(request, 'GET')
    @safe_response
    def func():
        ver_id = int(request.GET['id'])
        index = int(request.GET['currentPage']) - 1
        limit = int(request.GET['pageSize'])
        # 通过版本的ID查找到所有的与之关联的版本模块
        module_list = []
        offset = index * limit
        vermodule = VerList.objects.get(id=ver_id)
        modules = VerModule.objects.filter(verID=vermodule).order_by('-id')[offset:limit+offset]
        for module in modules:
            module_list.append(
                {
                    'id': module.id,
                    'name': module.name,
                    'module': {
                        'id': module.moduleID.id,
                        'name': module.moduleID.name,
                        'description': module.moduleID.description
                    },
                    'config': json.loads(module.config)
                }
            )
        # reverse
        total = VerModule.objects.filter(verID=vermodule).count()
        return json.dumps({'datalist': module_list, 'total': total})

    return func()


def add_ver(requst):
    """
    添加新的版本
    处理的异常：
        参数不全，缺少名称或者描述
        版本命名冲突
        参数超过数据库表的限制

    :param requst: object, http request
    :return: status information
    """
    @process_frame(requst, 'POST')
    @safe_response
    def func():
        ver_name = requst.POST['name']
        ver_description = requst.POST['description']
        new_ver = VerList(name=ver_name, description=ver_description)
        new_ver.save()
        resp = {
            'id': new_ver.id,
            'name': ver_name,
            'description': ver_description
        }
        return ResponseFactory.ok_resp(
            'new version add successfully.',
            **resp
        )

    return func()


def update_ver(request):
    """
    修改版本信息
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
        ver_id = int(request.POST['id'])
        ver = VerList.objects.get(id=ver_id)
        ver.name = request.POST.get('name', ver.name)
        ver.description = request.POST.get('description', ver.description)
        ver.save()
        resp = {
            'id': ver.id,
            'name': ver.name,
            'description': ver.description
        }
        return ResponseFactory.ok_resp(
            'version {0} update successfully.'.format(ver_id),
            **resp
        )

    return func()


def delete_ver(request):
    """
    删除一个版本
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
        ver_id = int(request.POST['id'])
        ver = VerList.objects.get(id=ver_id)
        ver.delete()
        return ResponseFactory.ok_resp(
            'version {0} remove successfully.'.format(ver_id)
        )

    return func()


#####################################################
# 版本模块管理
#####################################################
def add_ver_module(request):
    """
    获取版本模块的详细信息

    需要处理的异常：
        完整性约束，不允许出现未知参考
        参数需要完整
        参数类型需要正确
        外键参考完整性手动监测

    :param request: object, http request
    :return: json string
    """
    @process_frame(request, 'POST')
    @safe_response
    def func():
        ver_id = int(request.POST['vid'])
        module_id = int(request.POST['mid'])
        vermodule = VerList.objects.get(id=ver_id)
        basicmodule = BasicModule.objects.get(id=module_id)
        vermodule_name = request.POST['name']
        vermodule_conf = request.POST['config']
        new_vermodule = VerModule(
            name=vermodule_name,
            verID=vermodule,
            moduleID=basicmodule,
            config=json.dumps(vermodule_conf)
        )
        new_vermodule.save()
        resp = {
            'id': new_vermodule.id,
            'name': vermodule_name,
            'verID': vermodule.id,
            'moduleID': basicmodule.id,
            'config': vermodule_conf
        }
        return ResponseFactory.ok_resp(
            'add new version module successfully.',
            **resp
        )

    return func()


def update_ver_module(request):
    """
    修改已经存在的模块
    需要处理的异常:
        完整性约束
        参数完整性
        参数类型合法
        数据模型要求合法
        指定版本模块不存在

    :param request: object, http request
    :return: json string
    """
    @process_frame(request, 'POST')
    @safe_response
    def func():
        vermodule_id = int(request.POST['id'])
        basicmodule_id = int(request.POST['mid'])
        basicmodule = BasicModule.objects.get(id=basicmodule_id)
        # 修改已经存在的版本module信息
        module = VerModule.objects.get(id=vermodule_id)
        module.moduleID = basicmodule
        module.name = request.POST.get('name', module.name)
        module.config = json.dumps(request.POST['config'])
        module.save()
        resp = {
            'id': module.id,
            'name': module.name,
            'verID': module.verID.id,
            'moduleID': module.moduleID.id,
            'config': module.config
        }
        return ResponseFactory.ok_resp(
            'update version module information successfully.',
            **resp
        )

    return func()


def delete_ver_module(request):
    """
    删除一个版本模块
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
        vermodule_id = int(request.POST['id'])
        module = VerModule.objects.get(id=vermodule_id)
        module.delete()
        return ResponseFactory.ok_resp(
            'version module {0} remove successfully.'.format(vermodule_id)
        )

    return func()
