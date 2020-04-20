import websockets
import asyncio
import numpy as np
import cv2
import base64

# Capture video from file
# cap = cv2.VideoCapture('D:/09d980032ed1.480.mp4')
cap = cv2.VideoCapture('src//assets//1.mp4')


async def echo(websocket, path):
    async for message in websocket:
        print(message)
        ret, frame = cap.read()

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

        if ret == True:
            cv2.imshow('frame', frame)
            retval, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            await websocket.send(jpg_as_text)
            print('send')

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()# your code goes here
