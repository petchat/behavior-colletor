# -*- coding: UTF-8 -*-

"""Unit test for app.py"""

__author__ = "jiaying.lu"

from unittest import TestCase
from flask_app.app import app
import json

class TestBehaviorCollectorAPI(TestCase):

    def setUp(self):
        # super(TestBehaviorCollectorAPI, self).setUp()
        app.config["TESTING"] = True
        self.app = app.test_client()

    def tearDown(self):
        # super(TestBehaviorCollectorAPI, self).tearDown()
        app.config["TESTING"] = False

    def test_empty_params(self):
        rv = self.app.post("/behavior_collector/", data="")
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(1, result["code"])

    def test_unvalid_params(self):
        rv = self.app.post("/behavior_collector/", data="OhMyParams")
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(1, result["code"])

    def test_valid_params(self):
        scale_type = "perHourScale"
        senz_prob_list = [
            {
                "motionProb": {"A": 0.7, "B": 0.3},
                "timestamp": 21921921213,
                "perHourScale": 23,
                "senzId": 11
            },
            {
                "motionProb": {"A": 0.3, "C": 0.7},
                "timestamp": 11223333,
                "perHourScale": 23,
                "senzId": 12
            },
            {
                "motionProb": {"B": 0.7, "C": 0.3},
                "timestamp": 333222,
                "perHourScale": 0,
                "senzId": 21
            },
            {
                "motionProb": {"A": 0.7, "C": 0.3},
                "timestamp": 992222,
                "perHourScale": 2,
                "senzId": 41
            },
        ]
        data = {
            "scaleType": scale_type,
            "startScaleValue": 22,
            "endScaleValue": 2,
            "senzList": senz_prob_list,
        }
        rv = self.app.post("/behavior_collector/", data=json.dumps(data))
        self.assertEqual(200, rv.status_code)
        result = json.loads(rv.data)
        self.assertEqual(0, result["code"])
