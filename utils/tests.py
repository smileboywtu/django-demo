# -*- coding: utf-8 -*-

# test the utils module
# Created: 2016-7-25
# Copyright: (c) 2016<smileboywtu@gmail.com>


from pprint import pprint
from django.test import TestCase

from utils.http_response import split_page


class UtilsTestCase(TestCase):

    def test_split_array(self):
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEquals(split_page(array, 2, 1), [1, 2])
        self.assertEquals(split_page(array, 3, 2), [4, 5, 6])

