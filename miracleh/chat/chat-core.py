import asyncio
import websockets
import chat.redis.RedisChatUtils as redisChatUtils

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

def handleMessage(message):
    #优先进行Key，value模式的回答
    message  = redisChatUtils.getHashKeyAll(name=message)
    if message != '':
        print(message)
    else:
        #开始特殊的回答
        return 'Pursuit Excellence'

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(echo, 'localhost', 8765))
    asyncio.get_event_loop().run_forever()