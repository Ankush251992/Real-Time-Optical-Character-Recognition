# RealTime_OCR_Tessaract.py

import cv2
import pytesseract
from pytesseract import Output
import imutils
import numpy as np

# Function to add branding to a frame
def add_branding(frame, text="Code Depot", position=(50, 50), font_scale=1, font_thickness=2, text_color=(255, 255, 255), bg_color=(0, 0, 0)):
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

# Initialize the video stream from the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Resize the frame for faster processing
    frame = imutils.resize(frame, width=600)

    # Convert the frame to grayscale for OCR
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use Tesseract to do OCR on the grayscale frame
    text = pytesseract.image_to_string(gray, config='--psm 6')
    data = pytesseract.image_to_data(gray, output_type=Output.DICT)

    # Draw bounding boxes around detected text and update text properties
    n_boxes = len(data['level'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 60:  # Confidence threshold
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = data['text'][i].strip()
            if text:  # Only draw text if there's something to draw
                font_scale = 0.6  # Adjust font scale if necessary
                frame = cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 6)
                frame = cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)

    # Add branding to the frame
    frame = add_branding(frame)

    # Display the resulting frame with OCR text
    cv2.imshow('Real-Time OCR - Code Depot', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture when everything is done
cap.release()
cv2.destroyAllWindows()