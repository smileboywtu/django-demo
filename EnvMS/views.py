# -*- coding: utf-8 -*-

# 环境管理视图，管理环境和环境中的模块
# Created: 2016-7-22
# Copyright: (c) 2016<smileboywtu@gmail.com>


# TODO(chenbo) 由于使用了SQLite3作为后端的数据存储，当出现字段超出限制的情况，不会报错
# TODO(chenbo) 使用PUT和DELETE方法的时候，需要自己从body中提取参数
# TODO(chenbo) Django ORM 中外键的约束需要手动get

# 2016/7/23: 成功创建对象返回对象的详细信息, 修改对象后返回修改后的信息

import json

from models import EnvList, EnvModule
from BasicMMS.models import BasicModule
from utils.http_status import ResponseFactory
from utils.http_response import safe_response, process_frame, split_page


#####################################################
# 环境管理
#####################################################
def get_environs(request):
    """
    获取所有的环境列表

    :param request: object, http request
    :return: json
    """
    @process_frame(request, 'GET')
    @safe_response
    def func():
        env_list = []
        limit = int(request.GET['pageSize'])
        index = int(request.GET['currentPage']) - 1
        offset = index * limit
        env_objects = EnvList.objects.order_by('-id')[offset:offset + limit]
        for obj in env_objects:
            env_list.append(
                {
                    'id': obj.id,
                    'name': obj.name,
                    'description': obj.description
                }
            )
        # reverse
        total = EnvList.objects.count()
        return json.dumps({'datalist': env_list, 'total': total})

    return func()


def get_env(request):
    """
    获取环境的详情，返回当前环境的模块情况

    :param request:
    :return:
    """
    @process_frame(request, 'GET')
    @safe_response
    def func():
        env_id = int(request.GET['id'])
        index = int(request.GET['currentPage']) - 1
        limit = int(request.GET['pageSize'])
        # 通过环境的ID查找到所有的与之关联的环境模块
        module_list = []
        offset = index * limit
        envmodule = EnvList.objects.get(id=env_id)
        modules = EnvModule.objects.filter(envID=envmodule).order_by('-id')[offset:offset + limit]
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
        total = EnvModule.objects.filter(envID=envmodule).count()
        return json.dumps({'total': total, 'datalist': module_list})

    return func()


def add_env(requst):
    """
    添加新的环境
    处理的异常：
        参数不全，缺少名称或者描述
        环境命名冲突
        参数超过数据库表的限制

    :param requst: object, http request
    :return: status information
    """
    @process_frame(requst, 'POST')
    @safe_response
    def func():
        env_name = requst.POST['name']
        env_description = requst.POST['description']
        new_env = EnvList(name=env_name, description=env_description)
        new_env.save()
        resp = {
            'id': new_env.id,
            'name': env_name,
            'description': env_description
        }
        return ResponseFactory.ok_resp(
            'new environment add successfully.',
            **resp
        )

    return func()


def update_env(request):
    """
    修改环境信息
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
        env_id = int(request.POST['id'])
        env = EnvList.objects.get(id=env_id)
        env.name = request.POST.get('name', env.name)
        env.description = request.POST.get('description', env.description)
        env.save()
        resp = {
            'id': env.id,
            'name': env.name,
            'description': env.description
        }
        return ResponseFactory.ok_resp(
            'environment {0} update successfully.'.format(env_id),
            **resp
        )

    return func()


def delete_env(request):
    """
    删除一个环境
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
        env_id = int(request.POST['id'])
        env = EnvList.objects.get(id=env_id)
        env.delete()
        return ResponseFactory.ok_resp(
            'environment {0} remove successfully.'.format(env_id)
        )

    return func()


#####################################################
# 环境模块管理
#####################################################
def add_env_module(request):
    """
    获取环境模块的详细信息

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
        env_id = int(request.POST['eid'])
        module_id = int(request.POST['mid'])
        envmodule = EnvList.objects.get(id=env_id)
        basicmodule = BasicModule.objects.get(id=module_id)
        envmodule_name = request.POST['name']
        envmodule_conf = request.POST['config']
        new_envmodule = EnvModule(
            name=envmodule_name,
            envID=envmodule,
            moduleID=basicmodule,
            config=json.dumps(envmodule_conf)
        )
        new_envmodule.save()
        resp = {
            'id': new_envmodule.id,
            'name': envmodule_name,
            'envID': envmodule.id,
            'moduleID': basicmodule.id,
            'config': envmodule_conf
        }
        return ResponseFactory.ok_resp(
            'add new environment module successfully.',
            **resp
        )

    return func()


def update_env_module(request):
    """
    修改已经存在的模块
    需要处理的异常:
        完整性约束
        参数完整性
        参数类型合法
        数据模型要求合法
        指定环境模块不存在

    :param request: object, http request
    :return: json string
    """
    @process_frame(request, 'POST')
    @safe_response
    def func():
        envmodule_id = int(request.POST['id'])
        basicmodule_id = int(request.POST['mid'])
        basicmodule = BasicModule.objects.get(id=basicmodule_id)
        # 修改已经存在的环境module信息
        module = EnvModule.objects.get(id=envmodule_id)
        module.moduleID = basicmodule
        module.name = request.POST.get('name', module.name)
        module.config = json.dumps(request.POST['config'])
        module.save()
        resp = {
            'id': module.id,
            'name': module.name,
            'envID': module.envID.id,
            'moduleID': module.moduleID.id,
            'config': module.config
        }
        return ResponseFactory.ok_resp(
            'update environment module information successfully.',
            **resp
        )

    return func()


def delete_env_module(request):
    """
    删除一个环境模块
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
        envmodule_id = int(request.POST['id'])
        module = EnvModule.objects.get(id=envmodule_id)
        module.delete()
        return ResponseFactory.ok_resp(
            'environment module {0} remove successfully.'.format(envmodule_id)
        )

    return func()
