import sys, time
import signal
import cv2
import numpy as np
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import frame_pb2 as pr_frame
import requests

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter("front_camera.mp4", fourcc, 30.0, (640, 360))

if not video_writer.isOpened():
    print("Error: Could not open video writer.")
    sys.exit(3)

def signal_handler(_sig, _frame):
    print('Quit.')
    if video_writer:
        video_writer.release()
        video_file = open("front_camera.mp4", "rb")
        files = {'video': video_file}
        url = "https://59b3-217-92-84-125.ngrok-free.app/api/upload_video"
        response = requests.post(url, files=files)
        video_file.close()

        if response.status_code == 200:
            print("Video uploaded successfully.")
        else:
            print(f"Failed to upload video. Status code: {response.status_code}")
    ecal_core.finalize()
    sys.exit(0)

def callback(_topic_name, msg, _time):
    frame = np.frombuffer(msg.pixel_data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
    print(f"Received frame shape: {frame.shape}")
    video_writer.write(frame)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    ecal_core.initialize(sys.argv, "Subscriber")

    subscriber = ProtoSubscriber("front_camera", pr_frame.Image)

    subscriber.set_callback(callback)

    while ecal_core.ok():
        time.sleep(0.5)
    ecal_core.finalize()
