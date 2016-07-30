# -*- coding: utf-8 -*-

# Home View
# Created: 2016-7-21
# Copyright: (c) 2016<smileboywtu@gmail.com>

from django.shortcuts import render_to_response


def index(request):
    """
    Home page render

    :param request: http request
    :return: html
    """
    return render_to_response('index.html')