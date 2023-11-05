# Script 2: process_image.py

import cv2
import pytesseract
from pytesseract import Output
import os
import numpy as np

# Define paths
input_image_path = '../Images/OCR_Test02.png'  # Replace with your image path
output_image_path = '../output/annotated_image.jpg'  # Replace with your output path


# Function to add branding to an image
def add_branding(image, text="Code Depot", position=(50, 50), font_scale=1, font_thickness=2,
                 text_color=(255, 255, 255), bg_color=(0, 0, 0)):
    overlay = image.copy()
    alpha = 0.6  # Transparency factor.

    # Get the width and height of the text box
    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
    x, y = position

    # Draw a rectangle and put the text on it
    cv2.rectangle(overlay, (x, y + 10), (x + text_width, y - text_height - 10), bg_color, -1)
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, font_thickness)

    return image


# Make sure the output directory exists
os.makedirs(os.path.dirname(output_image_path), exist_ok=True)

# Read the image
image = cv2.imread(input_image_path)

# Perform OCR
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
data = pytesseract.image_to_data(gray, output_type=Output.DICT)

# Draw bounding boxes around text and update text properties
n_boxes = len(data['level'])
for i in range(n_boxes):
    if int(data['conf'][i]) > 60:  # Confidence threshold
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = data['text'][i].strip()
        if text:  # Only draw text if there's something to draw
            font_scale = 0.6  # Adjust font scale if necessary
            image = cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 6)
            image = cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)

# Add branding to the image
image = add_branding(image)

# Save the annotated image
cv2.imwrite(output_image_path, image)