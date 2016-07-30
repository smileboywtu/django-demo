# -*- coding: utf-8 -*-

# 环境管理路径
# Created: 2016-7-22
# Copyright: (c) 2016<smileboywtu@gmail.com>


from django.conf.urls import url

from . import views


# 所有基础模块管理的url配置
urlpatterns = [
    url(r'^EnvList/$', views.get_environs),
    url(r'^EnvDetail/$', views.get_env),
    url(r'^newEnv/$', views.add_env),
    url(r'^updateEnv/$', views.update_env),
    url(r'^deleteEnv/$', views.delete_env),
    url(r'^newModule/$', views.add_env_module),
    url(r'^updateModule/$', views.update_env_module),
    url(r'^deleteModule/$', views.delete_env_module)
]