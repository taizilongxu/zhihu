#-*- encoding: UTF-8 -*-
"""
Write in the redis 1000000 key-value
"""
#---------------------------------import---------------------------------------
import json
from random import randint
import redis
import getopt
import sys
import os
#------------------------------------------------------------------------------


def write_redis(host='localhost', port=6379, db=0):

    r = redis.StrictRedis(host, port, db)
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
    opts, args = getopt.getopt(sys.argv[1:], 'h:p:d:')
    if len(opts) == 0:
        try:
            write_redis()
            print 'OK'
        except:
            print 'Redis error'
    elif len(opts) == 3:
        options = {}
        for op, value in opts:
            if op == '-h':
                options['host'] = value
            if op == '-p':
                options['port'] = value
            if op == '-d':
                options['db'] = value
        path = os.getcwd()
        with open(path + '/.redis.conf', 'w') as F:
            F.write(json.dumps(options))
        try:
            write_redis(options['host'], options['port'], options['db'])
            print 'OK'
        except:
            print 'Redis error'
    else:
        print 'Args error!'


if __name__ == '__main__':
    main()
###############################################################################
