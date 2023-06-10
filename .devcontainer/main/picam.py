import io
import picamera
from flask import Flask, Response

app = Flask(__name__)

# Create a route for streaming video
@app.route('/')
def stream_video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to generate image frames
def generate_frames():
    with picamera.PiCamera() as camera:
        # Set camera resolution as desired
        camera.resolution = (640, 480)

        # Allow the camera to warm up
        camera.start_preview()
        time.sleep(2)

        # Capture and stream video indefinitely
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, format='jpeg'):
            # Reset the stream for next frame
            stream.seek(0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')

            # Reset the stream for next frame
            stream.seek(0)
            stream.truncate()

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8123)
