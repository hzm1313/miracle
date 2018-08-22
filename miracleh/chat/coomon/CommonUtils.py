from chat.conf.CoomonConf import charest, redis_encode_charest


def convert(data):
    if isinstance(data, bytes):  return data.decode(redis_encode_charest)
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data