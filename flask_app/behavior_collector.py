# -*- coding: UTF-8 -*-

__author__ = 'MeoWoodie'

__all__ = 'BehaviorCollector'

K_WEIGHT_DEFAULT = 0.5  # default value for _collect_probs() param k_weight

# def CountStrategy(sensor_type_list):
#     # Calculate the new senz's motion type
#     # The new senz's motion type is much more than other type in senzes' motion type in list.
#     _sensor_type = ''
#     sensor_type_count = {}
#     # - calculate the count of every type in list.
#     for sensor_type in sensor_type_list:
#         if sensor_type in sensor_type_count.keys():
#             sensor_type_count[sensor_type] += 1
#         else:
#             sensor_type_count[sensor_type] = 0
#     # - select the largest count.
#     max_count = 0
#     for type in sensor_type_count.keys():
#         if sensor_type_count[type] >= max_count:
#             max_count = sensor_type_count[type]
#             _sensor_type = type
#
#     print 'The largest type is', type, '. the count of it is', max_count
#     return _sensor_type

def FirstStrategy(sensor_type_list):
    return sensor_type_list[0]

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
    motion_prob_list = []
    poi_prob1_list   = []
    poi_prob2_list   = []
    sound_prob_list  = []
    for senz_tuple in input_data:
        timestamp_list.append(senz_tuple['timestamp'])
        motion_prob_list.append(senz_tuple['motionProb'])
        poi_prob1_list.append(senz_tuple['poiProbLv1'])
        poi_prob2_list.append(senz_tuple['poiProbLv2'])
        sound_prob_list.append(senz_tuple['soundProb'])

    # Calculate the new senz's timestamp
    # It is the average of senzes' timestamp in list.
    _timestamp = 0
    for timestamp in timestamp_list:
        _timestamp += timestamp
    _timestamp /= len(timestamp_list)

    # Calculate every sensor's type.
    _motion_prob = FirstStrategy(motion_prob_list)
    _poi_prob1   = FirstStrategy(poi_prob1_list)
    _poi_prob2   = FirstStrategy(poi_prob2_list)
    _sound_prob  = FirstStrategy(sound_prob_list)

    result = {
        'motionProb': _motion_prob,
        'poiProbLv1': _poi_prob1,
        'poiProbLv2': _poi_prob2,
        'soundProb': _sound_prob,
        'timestamp': _timestamp
    }
    print 'The new senz tuple is'
    print result

    return result


def _get_arithmetic_average(prob_list):
    """Calculate arithmetic average of prob_list

    Parameters
    ----------
    prob_list: array_like, shape(1, n)
      elems are dict, with string keys and float values

    Returns
    -------
    prob_result: dict
      with string keys and float values
    """
    prob_result = {}
    prob_length = len(prob_list)

    for elem in prob_list:
        for elem_key in elem:
            if prob_result.has_key(elem_key):
                prob_result[elem_key] += elem[elem_key]
            else:
                prob_result[elem_key] = elem[elem_key]

    for prob_key in prob_result:
        prob_result[prob_key] /= prob_length

    return prob_result


def _collect_probs(cur_prob_list, other_prob_list, k_weight):
    """Collect probs in cur_prob_list, during

    Parameters
    ----------
    cur_prob_list: array_like, shape(1, n)
      elems are dict, with string keys and float values
    other_prob_list: array_like, shape(1, m)
      elems are dict, with string keys and float values
    k_weight: float, limit [0, 1]
      weight for cur_prob_list, represent cur_prob_list's weight in total
      if k_weight out of [0, 1], will use a default value

    Returns
    -------
    prob_result: dict
      with string keys and float values
    """
    if k_weight < 0 or k_weight > 1:
        k_weight = K_WEIGHT_DEFAULT

    cur_prob_result = _get_arithmetic_average(cur_prob_list)
    other_prob_result = _get_arithmetic_average(other_prob_list)

    # process with k_weight
    for key in cur_prob_result:
        cur_prob_result[key] *= (2 * k_weight)
    for key in other_prob_result:
        other_prob_result[key] *= (2 * (1-k_weight))

    prob_list = [cur_prob_result, other_prob_result]

    return _get_arithmetic_average(prob_list)
