# -*- coding: UTF-8 -*-

"""Unit test for app.py"""

__author__ = 'jiaying.lu'

from unittest import TestCase
from flask_app.app import app
import json

class TestBehaviorCollectorAPI(TestCase):

    def setUp(self):
        # super(TestBehaviorCollectorAPI, self).setUp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        # super(TestBehaviorCollectorAPI, self).tearDown()
        app.config['TESTING'] = False

    def test_empty_params(self):
        rv = self.app.post('/behavior_collector/', data='')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(1, result['code'])

    def test_unvalid_params(self):
        rv = self.app.post('/behavior_collector/', data='OhMyParams')
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(1, result['code'])