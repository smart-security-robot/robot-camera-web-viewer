"""
    -----------------------------------------------------------
    ECE441 - Illinois Institute of Technology
    Author: Alae Moudni
    Email: amoudni@hawk.iit.edu
    Date: October 2023
    
    Description:
    This code is a part of the ECE441 project. Unauthorized copying,
    distribution, or any form of plagiarism without explicit permission is
    strictly prohibited. All rights reserved.
    -----------------------------------------------------------
"""

##################################################

from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # Use default camera

@app.route('/')
def index():
    return render_template('index.html')

def generate():
    while True:
        success, frame = camera.read()
        if not success:
            print("Failed to read frame")
            break
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            print("Failed to encode frame")
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
