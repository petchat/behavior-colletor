__author__ = 'MeoWoodie'

def CountStrategy(sensor_type_list):
    # Calculate the new senz's motion type
    # The new senz's motion type is much more than other type in senzes' motion type in list.
    _sensor_type = ''
    sensor_type_count = {}
    # - calculate the count of every type in list.
    for sensor_type in sensor_type_list:
        if sensor_type in sensor_type_count.keys():
            sensor_type_count[sensor_type] += 1
        else:
            sensor_type_count[sensor_type] = 0
    # - select the largest count.
    max_count = 0
    for type in sensor_type_count.keys():
        if sensor_type_count[type] >= max_count:
            max_count = sensor_type_count[type]
            _sensor_type = type

    print 'The largest type is', type, '. the count of it is', max_count
    return _sensor_type

def BehaviorCollector(input_data):
    '''
    Behavior Collector

    It's used for getting a general senz tuple from a senz list.
    Senz from the list has the same scale value.
    We assumed that they have a general attribute cause of being generated at same time.

    :return: A general senz tuple, with motion type, sound type and poi type.
    '''
    # Extract the information from senz list
    timestamp_list   = []
    motion_type_list = []
    poi_type_list    = []
    sound_type_list  = []
    for senz_tuple in input_data:
        timestamp_list.append(senz_tuple['timestamp'])
        motion_type_list.append(senz_tuple['motionType'])
        sound_type_list.append(senz_tuple['soundType'])
        poi_type_list.append(senz_tuple['poiType'])

    # Calculate the new senz's timestamp
    # It is the average of senzes' timestamp in list.
    _timestamp = 0
    for timestamp in timestamp_list:
        _timestamp += timestamp
    _timestamp /= len(timestamp_list)

    # Calculate every sensor's type.
    _motion_type = CountStrategy(motion_type_list)
    _poi_type    = CountStrategy(poi_type_list)
    _sound_type  = CountStrategy(sound_type_list)

    result = {
        'motionType': _motion_type,
        'poiType': _poi_type,
        'soundType': _sound_type,
        'timestamp': _timestamp
    }
    print 'The new senz tuple is'
    print result

    return result


