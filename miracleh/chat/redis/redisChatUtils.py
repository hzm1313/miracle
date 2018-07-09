import redis
import chat.conf.coomonConf as conf

pool = redis.ConnectionPool(host=conf.redis_host, port=conf.redis_port)

def setHashKey(name, key, value):
    r = redis.Redis(connection_pool=pool)
    r.hset(name=name, key=key, value=value)

def expireTime(key, time):
    r = redis.Redis(connection_pool=pool)
    r.expire(name=key, time=time)

def getHashKeyAll(name):
    r = redis.Redis(connection_pool=pool)
    return r.hgetall(name=name)

def getHashKeyValue(name, key):
    r = redis.Redis(connection_pool=pool)
    return r.hget(name=name, key=key)

def getStringKey(name):
    r = redis.Redis(connection_pool=pool)
    return r.get(name=name)

def setStringKey(name, value):
    r = redis.Redis(connection_pool=pool)
    r.setnx(name=name, value=value)

if __name__ == "__main__":
    setHashKey(1, 2, 3)
    print(getHashKeyAll(name=1))
    print(getHashKeyValue(name=1, key=2))
    setStringKey(name=1,value=2)
    print(getStringKey(name=1))

#第一层级询问
#第二层级询问
#第三层级询问
#redis list hash string set zset
# hash{} next -> pre