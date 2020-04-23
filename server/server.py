import websockets
import asyncio
import numpy as np
import cv2
import base64

# Capture video from file
cap = cv2.VideoCapture('src//assets//video_test.mp4')


async def echo(websocket, path):
    async for message in websocket:
        print(message)
        ret, frame = cap.read()

        if ret == True:
            retval, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            await websocket.send(jpg_as_text)

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()# your code goes here
