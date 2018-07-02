import redis
import sys
sys.path.append("F:\workspace\worksapce-core\smart-console\src\chat")

import src.conf.coomonConf as conf

pool = redis.Redis(host=conf.redis_host,port=conf.redis_port)
def redisConnect():
    global pool
    pool = redis.Redis(host=conf.redis_host, port=conf.redis_port)


def setHashKey():
    redis.left


