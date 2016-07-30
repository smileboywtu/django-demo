# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class BasicModule(models.Model):
    """用于存储基础的模块信息"""
    name = models.CharField(max_length=32, unique=True)              # 模块名字
    description = models.CharField(max_length=200)                   # 模块描述