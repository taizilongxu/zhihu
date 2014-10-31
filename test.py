#-*- encoding: UTF-8 -*-
#---------------------------------import------------------------------------
#---------------------------------------------------------------------------
#!/usr/bin/python2
import redis
import time
def without_pipeline():
    r=redis.Redis()
    for i in range(10000):
        r.ping()
    return
def with_pipeline():
    r=redis.Redis()
    pipeline=r.pipeline()
    for i in range(10000):
        pipeline.ping()
    pipeline.execute()
    return
def bench(desc):
    start=time.clock()
    desc()
    stop=time.clock()
    diff=stop-start
    print "%s has token %s" % (desc.func_name,str(diff))
if __name__=='__main__':
    bench(without_pipeline)
    bench(with_pipeline)
############################################################################
