#-*- encoding: UTF-8 -*-
"""
Write in the redis 1000000 key-value
"""
#---------------------------------import---------------------------------------
import json
from random import randint
import redis
#------------------------------------------------------------------------------


def write_redis():

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    user_dict = {}
    for i in xrange(1000000):
        user_id = randint(1, 10000)
        action = randint(1, 7)
        question_id = randint(1, 10000)
        if user_id in user_dict:
            unix_time = user_dict[user_id] + randint(1, 31556926 * 4)
        else:
            unix_time = randint(1, 31556926 * 4) + 1411000000
        user_dict[user_id] = unix_time
        # write in the redis
        r.set(str(user_id) + ':' + str(question_id), action)
        r.zadd(str(user_id) + ':timeline', str(unix_time), str(question_id))


def main():

    write_redis()

if __name__ == '__main__':
    main()
###############################################################################
