import torch
import cv2
import json
import os

# Load YOLOv8 model from PyTorch Hub with trust_repo parameter
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)

# Define paths
video_path = 'my_file.mp4'
result_dir = 'result'
os.makedirs(result_dir, exist_ok=True)

# Initialize video capture
cap = cv2.VideoCapture(video_path)

# Initialize result data
results_data = []

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection
    results = model(frame)

    # Save detection results
    for result in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = result
        results_data.append({
            'frame': frame_count,
            'class': int(cls),
            'confidence': float(conf),
            'bbox': [int(x1), int(y1), int(x2), int(y2)]
        })

        # Draw bounding box on the frame
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f'{int(cls)} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Save the frame with detections
    result_frame_path = os.path.join(result_dir, f'frame_{frame_count}.jpg')
    cv2.imwrite(result_frame_path, frame)

    frame_count += 1

# Release video capture
cap.release()

# Save results to JSON file
result_json_path = os.path.join(result_dir, 'results.json')
with open(result_json_path, 'w') as f:
    json.dump(results_data, f, indent=4)

print(f'Results saved in {result_dir}')