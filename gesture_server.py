import asyncio
import websockets

async def handler(websocket):
    print("Browser Connected")
    async for gesture in websocket:
        print("Gesture:", gesture)

# Start WebSocket server on localhost:8765
async def main():
    print("Waiting for browser...")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
