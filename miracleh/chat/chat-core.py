import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

def handleMessage(message):
    #优先进行Key，value模式的回答
    print()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(echo, 'localhost', 8765))
    asyncio.get_event_loop().run_forever()