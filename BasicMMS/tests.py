# -*- coding: utf-8 -*-

# 基础模块自动化测试
# Created: 2016-7-23
# Copyright: (c)<smileboywtu@gmail.com>


import json
import time
import random
from unittest import skipIf
from django.test import TestCase
from django.conf import settings


import views as BasicMMS


class DummyData(object):
    """存储用于测试的虚拟数据"""

    # 模块名称
    name = (
        'basic_module_01',
        'basic_module_02',
        'basic_module_03',
        'basic_module_04',
        'basic_module_05',

        '基础模块01',
        '基础模块02',
        '基础模块03',
        '基础模块04',
        '基础模块05',
        '基础模块06',
    )

    update = (
        ('basic01', 'demo description01'),
        ('basic02', 'demo description02')
    )

    # 模块描述
    description = (
        'demo description for basic module',
        '基础模块描述示例'
    )


class Request(object):

    def __init__(self, method, data):
        self.method = method
        self.POST = data


class BasicModuleTestCase(TestCase):

    def setUp(self):
        # write data to the database
        random.seed(time.time())
        for name in DummyData.name:
            request = Request('POST', {
                'name': name,
                'description': random.choice(DummyData.description)
            })
            resp = BasicMMS.add_basic_module(request)
            resp = json.loads(resp.getvalue())
            self.assertEquals(resp['errcode'], 0)
            self.assertEquals(resp['name'].encode('utf-8'), name)

    def test_read_module_list(self):
        request = Request('GET', {})
        resp = BasicMMS.get_basic_modules(request)
        resp = json.loads(resp.getvalue())
        self.assertEquals(len(resp), len(DummyData.name))

    def test_update_module(self):
        id = random.randrange(len(DummyData.name))
        data = random.choice(DummyData.update)
        request = Request('POST', {
            'id': id,
            'name': data[0],
            'description': data[1]
        })
        resp = BasicMMS.update_basic_module(request)
        resp = json.loads(resp.getvalue())
        self.assertEquals(resp['errcode'], 0)
        self.assertEquals(resp['id'], id)
        self.assertEquals(resp['name'].encode('utf-8'), data[0])
        # how to deal with code charset
        # http://wklken.me/posts/2013/08/31/python-extra-coding-intro.html
        self.assertEquals(resp['description'].encode('utf-8'), data[1])

    def test_delete_module(self):
        id = random.randrange(len(DummyData.name))
        request = Request('POST', {
            'id': id
        })
        resp = BasicMMS.delete_basic_module(request)
        resp = json.loads(resp.getvalue())
        self.assertEquals(resp['errcode'], 0)

    # code = {
    #     'ok': 0,                    # 成功返回
    #     'err': -1,                  # 标准错误
    #     'unknown': 1,               # 位置错误
    #     'params_type_err': 72201,   # 参数类型错误
    #     'params_less_err': 72202,   # 参数缺失
    #
    #     'db_field_err': 72203,      # 参数长度不符合要求
    #     'db_integrity_err': 72204,  # 破坏数据的完整性
    #     'db_nexist_err': 72205      # 指定对象不存在
    # }

    def test_id_type_error(self):
        """
        should get the error code:
            72201
        :return:
        """
        id = 'a'
        request = Request('POST', {
            'id': id
        })
        resp = BasicMMS.delete_basic_module(request)
        resp = json.loads(resp.getvalue())
        self.assertEquals(resp['errcode'], 72201)

    def test_id_less_error(self):
        """
        should get the error code:
            72202
        :return:
        """
        name = 'basic007'
        request = Request('POST', {
            'name': name
        })
        resp = BasicMMS.add_basic_module(request)
        resp = json.loads(resp.getvalue())
        self.assertEquals(resp['errcode'], 72202)

    def test_db_integrity_error(self):
        """"
        should get code:
            72204
        """
        name = random.choice(DummyData.name)
        description = random.choice(DummyData.description)
        request = Request('POST', {
            'name': name,
            'description':description
        })
        resp = BasicMMS.add_basic_module(request)
        resp = json.loads(resp.getvalue())
        self.assertEquals(resp['errcode'], 72204)

    def test_db_nexist_error(self):
        """
        should get code:
            72205
        :return:
        """
        id = len(DummyData.name) + 1
        request = Request('POST', {
            'id': id
        })
        resp = BasicMMS.delete_basic_module(request)
        resp = json.loads(resp.getvalue())
        self.assertEquals(resp['errcode'], 72205)

    @skipIf('sqlite3' in settings.DATABASES['default']['ENGINE'].split('.'), 'SQLite3 do not support field length check.')
    def test_db_field_error(self):
        """
        should get code:
            72203
        :return:
        """
        name = 'a' * 200
        description = random.choice(DummyData.description)
        request = Request('POST', {
            'name': name,
            'description':description
        })
        resp = BasicMMS.add_basic_module(request)
        resp = json.loads(resp.getvalue())
        self.assertEquals(resp['errcode'], 72205)
