import json

import redis
import chat.conf.CoomonConf as conf
from chat.coomon.CommonUtils import convert

pool = redis.ConnectionPool(host=conf.redis_host, port=conf.redis_port, encoding='GBK')

def setHashKey(name, key, value):
    r = redis.Redis(connection_pool=pool)
    r.hset(name=conf.redis_chat_pre + name, key=key, value=value)

def expireTime(key, time):
    r = redis.Redis(connection_pool=pool)
    r.expire(name=conf.redis_chat_pre + key, time=time)


def getHashKeyAll(name):
    r = redis.Redis(connection_pool=pool)
    return r.hgetall(name=conf.redis_chat_pre + name)


def getHashKeyValue(name, key):
    r = redis.Redis(connection_pool=pool)
    return r.hget(name=conf.redis_chat_pre + name, key=key)


def getStringKey(name):
    r = redis.Redis(connection_pool=pool)
    return r.get(name=conf.redis_chat_pre + name)


def setStringKey(name, value):
    r = redis.Redis(connection_pool=pool)
    r.setnx(name=conf.redis_chat_pre + name, value=value)


def getHashKeySize(name):
    r = redis.Redis(connection_pool=pool)
    return r.hlen(name=conf.redis_chat_pre + name)

if __name__ == "__main__":
    # 第一层
    keyMain = 'main'
    chatCommonObj = {}
    chatCommonObj['content'] = 'EasyGo微信配置问题'
    chatCommonObj['key'] = keyMain + ':wxType'
    chatCommonObj['isHaveNext'] = 'true'
    setHashKey(keyMain, 1, json.dumps(chatCommonObj))
    chatCommonObj = {}
    chatCommonObj['content'] = 'EasyGo微信支付问题---暂未完善'
    chatCommonObj['key'] = ''
    chatCommonObj['isHaveNext'] = 'false'
    setHashKey(keyMain, 2, json.dumps(chatCommonObj))
    # 第二层
    key = keyMain + ':wxType'
    chatCommonObj['content'] = 'EasyGo微信'
    chatCommonObj['key'] = key + ':wxType'
    chatCommonObj['isHaveNext'] = 'true'
    setHashKey(key, 1, json.dumps(chatCommonObj))
    # 第二层终结
    key = keyMain + ':wxPayType'
    chatCommonObj['content'] = '微信公众号配置流程1，。。。。。。/r/t 微信公众号配置流程2，。。。。。/r/t 微信公众号配置流程3，。。。。。/r/t'
    chatCommonObj['key'] = ''
    chatCommonObj['isHaveNext'] = 'false'
    setHashKey(key, 1, json.dumps(chatCommonObj))
    key = keyMain + ':wxPayType'
    chatCommonObj['content'] = '微信自定义菜单配置1，。。。。。。/r/t 微信自定义菜单配置2，。。。。。/r/t 微信自定义菜单配置3，。。。。。/r/t'
    chatCommonObj['key'] = ''
    chatCommonObj['isHaveNext'] = 'false'
    setHashKey(key, 2, json.dumps(chatCommonObj))

    result = getHashKeyAll(name=key)
    resultStr = str(convert(result))
    print(resultStr)
    print(getHashKeySize(name=key))
