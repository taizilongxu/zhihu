#-*- encoding: UTF-8 -*-
#---------------------------------import---------------------------------------
import json
import time
from random import randint
import redis
#------------------------------------------------------------------------------

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)
pipe = r.pipeline()
ERROR = json.dumps({'r': '0'})


def user_timeline(user_id, page=0, length=1):
    try:
        id_score = r.zrevrange(user_id + ':timeline', page * length, (page + 1) * length - 1, withscores=True)
        if not id_score:
            return ERROR
        if length < 3:
            posts = [{
                'action': r.get(user_id + ':' + i[0]),
                'question_id': i[0],
                'unix_time': str(int(i[1]))
                } for i in id_score]
        else:
            for i in id_score:
                pipe.get(user_id + ':' + i[0])
            actions = pipe.execute()
            posts = [{
                'action': actions[index],
                'question_id': i[0],
                'unix_time': str(int(i[1]))
                } for index, i in enumerate(id_score)]
        return json.dumps(posts)
    except:
        return ERROR


def hide_question(user_id, question_id):
    try:
        # the question in hide zset
        if r.zscore(user_id + ':hide', question_id):
            return ERROR
        unix_time = r.zscore(user_id + ':timeline', question_id)
        pipe.zrem(user_id + ':timeline', question_id)  # del the question
        pipe.zadd(user_id + ':hide', unix_time, question_id)  # add the question
        pipe.execute()
        return json.dumps({'r': '1'})
    except:
        return ERROR


def display_question(user_id, question_id):
    try:
        # the question in the zset
        if r.zscore(user_id + ':timeline', question_id):
            return ERROR
        unix_time = r.zscore(user_id + ':hide', question_id)
        pipe.zrem(user_id + ':hide', question_id)  # del the question
        pipe.zadd(user_id + ':timeline', unix_time, question_id)  # add the question
        pipe.execute()
        return json.dumps({'r': '1'})
    except:
        return ERROR


def main():
    for j in xrange(1, 10):
        use_time = 0
        for k in xrange(10):
            start = time.clock()
            for i in xrange(1000):
                user_timeline('1', 0, j)
            end = time.clock()
            use_time += end - start
        print use_time / 10

    # start = time.clock()
    # for i in range(10000):
    #     hide_question('1', '4729')
    #     display_question('1', '4729')
    # end = time.clock()
    # print end - start

if __name__ == '__main__':
    main()
###############################################################################
