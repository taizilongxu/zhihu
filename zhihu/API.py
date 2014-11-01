#-*- encoding: UTF-8 -*-
#---------------------------------import---------------------------------------
import json
import time
from random import randint
import redis
import os
#------------------------------------------------------------------------------


class ZhihuApi(object):
    def __init__(self):
        self.r = self.login_redis()
        self.pipe = self.r.pipeline()
        self.ERROR = json.dumps({'r': '0'})

    def login_redis(self):
        """Get the args of the redis"""
        options = {}
        path = os.getcwd() + '/.redis.conf'
        if os.path.exists(path):
            with open(path, 'r') as F:
                options = json.loads(F.read())
            pool = redis.ConnectionPool(host=options['host'], port=int(options['port']), db=int(options['db']))
        else:
            pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        r = redis.StrictRedis(connection_pool=pool)
        return r

    def user_timeline(self, user_id, page=0, length=1):
        """Get the timeline of user"""
        try:
            id_score = self.r.zrevrange(user_id + ':timeline', page * length, (page + 1) * length - 1, withscores=True)
            if not id_score:
                return self.ERROR
            if length < 3:
                posts = [{
                    'action': self.r.get(user_id + ':' + i[0]),
                    'question_id': i[0],
                    'unix_time': str(int(i[1]))
                    } for i in id_score]
            else:
                for i in id_score:
                    self.pipe.get(user_id + ':' + i[0])
                actions = self.pipe.execute()
                posts = [{
                    'action': actions[index],
                    'question_id': i[0],
                    'unix_time': str(int(i[1]))
                    } for index, i in enumerate(id_score)]
            return json.dumps(posts)
        except:
            return self.ERROR

    def fun_question(self, user_id, question_id, tag):
        tmp1 = user_id + ':hide'
        tmp2 = user_id + ':timeline'
        if tag != 1:
            tmp1, tmp2 = tmp2, tmp1
        try:
            # the question in  zset
            if self.r.zscore(tmp1, question_id):
                return self.ERROR
            unix_time = self.r.zscore(tmp2, question_id)
            self.pipe.zrem(tmp2, question_id)  # del the question
            self.pipe.zadd(tmp1, unix_time, question_id)  # add the question
            self.pipe.execute()
            return json.dumps({'r': '1'})
        except:
            return self.ERROR

    def hide_question(self, user_id, question_id):
        """Hide the question"""
        return self.fun_question(user_id, question_id, 1)

    def display_question(self, user_id, question_id):
        """Display the question"""
        return self.fun_question(user_id, question_id, 0)
###############################################################################
