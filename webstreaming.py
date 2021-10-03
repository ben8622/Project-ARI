#Import necessary libraries
from flask import Flask, render_template, Response, request
import cv2
from aruco_detection import aruco_detect
#Initialize the Flask app
app = Flask(__name__)
ar = aruco_detect.aruco_detect()
camera = cv2.VideoCapture(0)
ar.scanning = False

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            if(ar.scanning):
                ## do oscars type of ar.scanning
                g_check = ar.gate_check(frame)
                if g_check:
                    ar.count_tags(frame)
                    frame = ar.draw_tags(frame)
            else:
                frame = ar.draw_tags_count(frame)

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
    return ar.ar_counts

@app.route('/change_preview', methods=['GET','POST'])
def change_preview():
    ar.scanning = not ar.scanning
    ar.ar_count = {'0': 0, '1': 0, '2': 0, '10': 0, '20':0,'30': 0}
    return "test"
    ## TODO: Add actual flag switch

if __name__ == "__main__":
    app.run(debug=True)