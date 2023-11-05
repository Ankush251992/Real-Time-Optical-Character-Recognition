# Script 1: process_video.py

import cv2
import pytesseract
from pytesseract import Output
import os
import numpy as np

# Define paths
input_video_path = '../video/OCR_Video.MOV'
output_video_path = '../output/annotated_video.mp4'

# Make sure the output directory exists
os.makedirs(os.path.dirname(output_video_path), exist_ok=True)

# Initialize video capture
cap = cv2.VideoCapture(input_video_path)
if not cap.isOpened():
    print(f"Error: Cannot open video file {input_video_path}")
    exit(1)

# Get the frame rate of the input video to set for the output video
input_frame_rate = cap.get(cv2.CAP_PROP_FPS)

# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None  # Will be defined later with the correct dimensions


# Function to add branding to a frame
def add_branding(frame, text="Code Depot", position=(50, 50), font_scale=2, font_thickness=3,
                 text_color=(255, 255, 255), bg_color=(0, 0, 0)):
    overlay = frame.copy()
    alpha = 0.6  # Transparency factor.

    # Get the width and height of the text box
    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
    x, y = position

    # Draw a rectangle and put the text on it
    cv2.rectangle(overlay, (x, y + 10), (x + text_width, y - text_height - 10), bg_color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, font_thickness)

    return frame


while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Perform OCR on the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_data(gray, output_type=Output.DICT)

    # Draw bounding boxes around text and update text properties
    n_boxes = len(data['level'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 70:
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = data['text'][i].strip()
            if text:  # Only draw text if there's something to draw
                # Put text with border for better visibility
                font_scale = 0.6
                frame = cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 6)
                frame = cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)

    # Add branding to the frame
    frame = add_branding(frame)

    # Initialize VideoWriter with the original frame dimensions
    if out is None:
        out = cv2.VideoWriter(output_video_path, fourcc, input_frame_rate, (frame.shape[1], frame.shape[0]))

    # Write the frame with OCR to the output video
    out.write(frame)

# Release everything when the job is finished
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()