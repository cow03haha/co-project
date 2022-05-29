from asyncio import events
from flask import Flask, request, Response, send_file
from flask_socketio import SocketIO
from pynput.keyboard import Controller
from camera import Camera

import eventlet
import time
import threading

eventlet.monkey_patch()
app = Flask(__name__) # 初始化網頁物件
socketio = SocketIO(app)
keyboard = Controller()

def keystroke(data):
    keyboard.press(data['key'])
    time.sleep(0.5)
    keyboard.release(data['key'])

@app.route('/') # 當收到預設路徑(http://xxx.xxx/)時處理請求
def root():
    return send_file('index.html') # 返回html給client

@app.route('/cmd', methods = ['POST'])
def cmd():
    data = request.get_json() # 抓取json資料

    if (data['key']) in ['w', 'a', 's', 'd']: # 判斷是否為 w,a,s,d
        thread = threading.Thread(target=keystroke, args=(data,))
        thread.start()

    socketio.emit('chats', { 'data': data['key'] })

    return 'OK' # 返回200 OK
    

def gen(camera):
    while True:
        time.sleep(0.33)
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0', debug = True) #將網頁架設在5000 port