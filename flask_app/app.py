# -*- coding: UTF-8 -*-

__author__ = 'MeoWoodie'

from flask import Flask, request, got_request_exception
from behavior_collector import refine_senz_prob_list
import json
import os

from logger import logger
import rollbar
import rollbar.contrib.flask

app = Flask(__name__)

logger.info('[rawsenz.refinedsenzes] start')


@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init('ec8dca105f8948ed92490a57cf846923',
                 'petchat-flask',
                 root=os.path.dirname(os.path.realpath(__file__)),
                 allow_logging_basic_config=False)

    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


@app.route('/behavior_collector/', methods=['POST'])
def behaviorCollectorAPI():
    result = {'code': 1, 'message': ''}

    # params JSON validate
    try:
        incoming_data = json.loads(request.data)
    except ValueError, err_msg:
        logger.error('[ValueError] err_msg: %s, params=%s' % (err_msg, request.data))
        result['message'] = 'Unvalid params: NOT a JSON Object'
        return json.dumps(result)

    # params key checking
    try:
        scale_type  = incoming_data['scale_type']
        senz_list   = incoming_data['senz_list']
        start_scale_value = incoming_data['start_scale_value']
        end_scale_value = incoming_data['end_scale_value']
    except KeyError, err_msg:
        logger.error('[KeyError] err_msg: %s, params=%s' % (err_msg, incoming_data))
        result['message'] = "Params Contents Error: Can't find keys " \
                            "['scale_type', 'senz_list', 'start_scale_value', 'end_scale_value']"
        return json.dumps(result)

    try:
        result['result'] = refine_senz_prob_list(scale_type, start_scale_value, end_scale_value, senz_list)
        result['code'] = 0
        result['message'] = 'success'
        return json.dumps(result)
    except Exception, e:
        logger.error('[Exception] generate result error: %s' % (str(e)))
        result['code'] = 1
        result['message'] = '500 Internal Error'
        return json.dumps(result)


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=9010)
