from flask import Flask, request, Response, send_file
from pynput.keyboard import Controller
from camera import Camera

import time
import threading
import json

app = Flask(__name__) # 初始化網頁物件
keyboard = Controller()
cmds = []

def keystroke(data):
    t = 0.2 * len(data['key'])
        
    keyboard.press(data['key'][0])
    time.sleep(t)
    keyboard.release(data['key'][0])

@app.route('/') # 當收到預設路徑(http://xxx.xxx/)時處理請求
def root():
    return send_file('index.html') # 返回html給client

@app.route('/cmd', methods = ['POST'])
def cmd():
    data = request.get_json() # 抓取json資料
    cmds.append(data['key'])

    thread = threading.Thread(target=keystroke, args=(data,))
    thread.start()

    return 'OK' # 返回200 OK

@app.route('/cmd_list')
def cmd_list():
    return json.dumps(cmds)

def gen(camera):
    while True:
        time.sleep(0.033)
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host = '0.0.0.0') #將網頁架設在5000 port
