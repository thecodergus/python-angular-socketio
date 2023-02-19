import logging
import asyncio
import uvicorn
from uvicorn.loops.asyncio import asyncio_setup
import socketio
from fastapi import FastAPI

# Set some basic logging
logging.basicConfig(
    level=2,
    format="%(asctime)-15s %(levelname)-8s %(message)s"
)

# Create a basic app
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*'
)
app = FastAPI()
app.mount("/", socketio.ASGIApp(sio, sio))


@sio.on('connect')
async def connect(sid, environ):
    logging.info(f"connect {sid}")

@sio.on('message')
async def message(sid, data):
    logging.info(f"message {data}")
    
@sio.on("contador")
async def contador(sid, data):
    logging.info(f"Contador: {data}")

@sio.on('disconnect')
async def disconnect(sid):
    logging.info(f'disconnect {sid}')


# Set up the event loop
async def start_background_task():
    i = 1
    while True:
        logging.info(f"Background tasks that ticks every 1s.")
        await sio.emit("contador", i)
        i += 1                
        await sio.sleep(1.0)

async def start_uvicorn():
    config = uvicorn.config.Config(app, host='localhost', port=3000)
    server = uvicorn.server.Server(config)
    await server.serve()

async def main(loop):
    await asyncio.wait([
        asyncio.create_task(start_uvicorn()),
        asyncio.create_task(start_background_task()),
    ], return_when=asyncio.FIRST_COMPLETED)


if __name__ == '__main__':
    asyncio_setup()
    loop = asyncio.get_event_loop()
    asyncio.run(main(loop))