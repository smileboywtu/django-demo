# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from BasicMMS.models import BasicModule


class VerList(models.Model):
    """存储版本信息"""
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=200)


class VerModule(models.Model):
    """用于存储所有版本的模块信息"""
    name = models.CharField(max_length=32, unique=True)
    moduleID = models.ForeignKey(BasicModule, db_column='moduleID', on_delete=models.CASCADE)
    verID = models.ForeignKey(VerList, db_column='verID', on_delete=models.CASCADE)
    config = models.TextField()