# -*- coding: utf-8 -*-

# 环境管理路径
# Created: 2016-7-22
# Copyright: (c) 2016<smileboywtu@gmail.com>


from django.conf.urls import url

from . import views


# 所有基础模块管理的url配置
urlpatterns = [
    url(r'^VerList/$', views.get_versions),
    url(r'^VerDetail/$', views.get_ver),
    url(r'^newVer/$', views.add_ver),
    url(r'^updateVer/$', views.update_ver),
    url(r'^deleteVer/$', views.delete_ver),
    url(r'^newModule/$', views.add_ver_module),
    url(r'^updateModule/$', views.update_ver_module),
    url(r'^deleteModule/$', views.delete_ver_module)
]