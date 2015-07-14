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
from exceptions import BlankConditionException

# Configure Logentries
logger = logging.getLogger('logentries')
if APP_ENV == 'prod':
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s : %(levelname)s, %(message)s'))
    logger.addHandler(ch)
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

@app.route('/', methods=['POST'])
def behaviorCollectorAPI():
    if request.headers.has_key('X-Request-Id'):
        x_request_id = request.headers['X-Request-Id']
    else:
        x_request_id = ''

    logger.info('[behaviorCollector API] enter API')
    result = {'code': 1, 'message': ''}

    # params JSON validate
    try:
        incoming_data = json.loads(request.data)
    except ValueError, err_msg:
        logger.error('<%s>, [ValueError] err_msg: %s, params=%s' % (x_request_id, err_msg, request.data))
        result['message'] = 'Unvalid params: NOT a JSON Object'
        return json.dumps(result)

    # params key checking
    try:
        scale_type  = incoming_data['scaleType']
        senz_list   = incoming_data['senzList']
        start_scale_value = incoming_data['startScaleValue']
        end_scale_value = incoming_data['endScaleValue']
    except KeyError, err_msg:
        logger.error('<%s>, [KeyError] err_msg: %s, params=%s' % (x_request_id, err_msg, incoming_data))
        result['message'] = "Params Contents Error: Can't find keys " \
                            "['scaleType', 'senzList', 'startScaleValue', 'endScaleValue']"
        return json.dumps(result)

    try:
        result['result'] = refine_senz_prob_list(scale_type, start_scale_value, end_scale_value, senz_list)
        result['code'] = 0
        result['message'] = 'success'
        logger.info('%s, [API] success!' % (x_request_id))
    except BlankConditionException, err:
        result['code'] = 1
        result['message'] = str(err)

    return json.dumps(result)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=9010)
