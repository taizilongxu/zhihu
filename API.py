#-*- encoding: UTF-8 -*-
#---------------------------------import---------------------------------------
import json
import time
from random import randint
import redis
#------------------------------------------------------------------------------


def user_timeline(user_id, page=0, length=-1):
    try:
        r = redis.StrictRedis()
        id_score = r.zrevrange(user_id, page * length, (page + 1) * length - 1, withscores=True)
        if not id_score:
            return json.dumps({'r': '0'})
        posts = [{
            'action': r.get(user_id + ':' + i[0] + ':action'),
            'question_id': i[0],
            'unix_time': int(i[1])
            } for i in id_score]
        return json.dumps(posts)
    except:
        return json.dumps({'r': '0'})


def hide_question(user_id, question_id):
    try:
        r = redis.StrictRedis()
        # the question in the hide zset
        if r.zscore(user_id + ':hide', question_id):
            return json.dumps({'r': '0'})
        unix_time = r.zscore(user_id, question_id)
        r.zrem(user_id, question_id)  # del the question
        r.zadd(user_id + ':hide', unix_time, question_id)  # add the question
        return json.dumps({'r': '1'})
    except:
        return json.dumps({'r': '0'})


def display_question(user_id, question_id):
    try:
        r = redis.StrictRedis()
        # the question in the zset
        if r.zscore(user_id, question_id):
            return json.dumps({'r': '0'})
        unix_time = r.zscore(user_id + ':hide', question_id)
        r.zrem(user_id + ':hide', question_id)  # del the question
        r.zadd(user_id, unix_time, question_id)  # add the question
        return json.dumps({'r': '1'})
    except:
        return json.dumps({'r': '0'})

print user_timeline('1', 0, 5)
# print hide_question('1', '7341')
###############################################################################
