# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from BasicMMS.models import BasicModule


class EnvList(models.Model):
    """存储环境信息"""
    name = models.CharField(max_length=32, unique=True, blank=False)
    description = models.CharField(max_length=200)


class EnvModule(models.Model):
    """用于存储所有环境的模块信息"""
    name = models.CharField(max_length=32, unique=True, blank=False)
    moduleID = models.ForeignKey(BasicModule, db_column='moduleID', on_delete=models.CASCADE)
    envID = models.ForeignKey(EnvList, db_column='envID', on_delete=models.CASCADE)
    config = models.TextField()
