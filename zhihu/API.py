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


def fun_question(user_id, question_id, tag):
    tmp1 = user_id + ':hide'
    tmp2 = user_id + ':timeline'
    if tag != 1:
        tmp1, tmp2 = tmp2, tmp1
    try:
        # the question in  zset
        if r.zscore(tmp1, question_id):
            return ERROR
        unix_time = r.zscore(tmp2, question_id)
        pipe.zrem(tmp2, question_id)  # del the question
        pipe.zadd(tmp1, unix_time, question_id)  # add the question
        pipe.execute()
        return json.dumps({'r': '1'})
    except:
        return ERROR


def hide_question(user_id, question_id):
    return fun_question(user_id, question_id, 1)


def display_question(user_id, question_id):
    return fun_question(user_id, question_id, 0)


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


if __name__ == '__main__':
    main()
###############################################################################
