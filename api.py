__author__ = 'MeoWoodie'

from flask import Flask, request, url_for, Response, send_file
from behavior_collector import BehaviorCollector
import json


app = Flask(__name__)

@app.route('/behavior_collector/', methods=['POST'])
def behaviorCollectorAPI():
    result = 'Your request is illegal'
    if request.method == 'POST':
        incoming_data = json.loads(request.data)
        scale_type  = incoming_data['scale_type']
        senz_list   = incoming_data['senz_list']
        scale_value = incoming_data['scale_value']
        print 'Received scale type is', scale_type, ', and scale value is', scale_value
        print 'The senz list is\n', senz_list
        senz_tuple  = BehaviorCollector(senz_list)
        senz_tuple[scale_type] = int(scale_value)
        result = json.dumps({ 'result': senz_tuple })
    return result

if __name__ == '__main__':
    app.debug = True
    app.run(port=9010)