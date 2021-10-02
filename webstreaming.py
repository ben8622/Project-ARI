#Import necessary libraries
from flask import Flask, render_template, Response, request
import cv2
from aruco_detection import aruco_detect
#Initialize the Flask app
app = Flask(__name__)
ar = aruco_detect.aruco_detect()
camera = cv2.VideoCapture(0)

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame = ar.get_tags(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/background_process_test', methods=['POST'])
def background_process_test():
    val = request.json['data']
    print("Value passed = ", val)

@app.route('/test', methods=['GET','POST'])
def test():
    print(ar.ar_counts)
    return ar.ar_counts

if __name__ == "__main__":
    app.run(debug=True)