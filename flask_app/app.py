# -*- coding: UTF-8 -*-

__author__ = 'MeoWoodie'

from flask import Flask, request, got_request_exception
from behavior_collector import refine_senz_prob_list
import json
import os

from config import *
import logging
from logentries import LogentriesHandler
import bugsnag
from bugsnag.flask import handle_exceptions

# Configure Logentries
logger = logging.getLogger('logentries')
logger.setLevel(logging.INFO)
logentries_handler = LogentriesHandler(LOGENTRIES_TOKEN)
logger.addHandler(logentries_handler)

# Configure Bugsnag
bugsnag.configure(
    api_key=BUGSNAG_TOKEN,
    project_root=os.path.dirname(os.path.realpath(__file__)),
)

app = Flask(__name__)

# Attach Bugsnag to Flask's exception handler
handle_exceptions(app)


@app.before_first_request
def init_before_first_request():
    import datetime

    init_tag = "[Initiation of Service Process]\n"

    log_init_time = "Initiation START at: \t%s\n" % datetime.datetime.now()
    log_app_env = "Environment Variable: \t%s\n" % APP_ENV
    log_bugsnag_token = "Bugsnag Service TOKEN: \t%s\n" % BUGSNAG_TOKEN
    log_logentries_token = "Logentries Service TOKEN: \t%s\n" % LOGENTRIES_TOKEN
    logger.info(init_tag + log_init_time)
    logger.info(init_tag + log_app_env)
    logger.info(init_tag + log_bugsnag_token)
    logger.info(init_tag + log_logentries_token)

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
        scale_type  = incoming_data['scaleType']
        senz_list   = incoming_data['senzList']
        start_scale_value = incoming_data['startScaleValue']
        end_scale_value = incoming_data['endScaleValue']
    except KeyError, err_msg:
        logger.error('[KeyError] err_msg: %s, params=%s' % (err_msg, incoming_data))
        result['message'] = "Params Contents Error: Can't find keys " \
                            "['scaleType', 'senzList', 'startScaleValue', 'endScaleValue']"
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
