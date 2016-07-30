# -*- coding: utf-8 -*-

# 基础模块管理路径
# Created: 2016-7-22
# Copyright: (c) 2016<smileboywtu@gmail.com>


from django.conf.urls import url

from . import views


# 所有基础模块管理的url配置
urlpatterns = [
    url(r'^ModuleList/$', views.get_basic_modules),
    url(r'^newModule/$', views.add_basic_module),
    url(r'^updateModule/$', views.update_basic_module),
    url(r'^deleteModule/$', views.delete_basic_module),
]
