OCR Project

Introduction
------------
This OCR (Optical Character Recognition) project utilizes pytesseract, a Python wrapper for Google's Tesseract-OCR Engine, along with opencv-python for image processing to extract text from images, videos, and real-time webcam feeds.

Features
--------
- Real-time OCR from webcam feed.
- Text extraction from static images with annotation.
- Video processing for text recognition with annotated output.

Installation
------------
To set up and run this project, you'll need Python installed on your machine as well as the following dependencies:
- numpy
- opencv-python
- pytesseract
- imutils

You can install all the necessary libraries using the following command:
pip install -r requirements.txt

Usage
-----
Real-time OCR from Webcam:
Run the RealTime_OCR_Tessaract.py script to begin text recognition from your webcam. Press 'q' to exit the webcam feed.
Command: python RealTime_OCR_Tessaract.py

OCR from Static Images:
Use the process_image.py script to perform OCR on a static image. Update the 'input_image_path' in the script with the path to your image.
Command: python process_image.py

OCR from Video Files:
Run the process_video.py script to extract text from a video file. Update the 'input_video_path' with the path to your video.
Command: python process_video.py

Real-World Applications
-----------------------
- Document Digitization: Transform physical documents into digital formats for easy editing and searching.
- License Plate Recognition: Useful in traffic surveillance for real-time license plate capture.
- Assistive Technology: Aid for the visually impaired by reading aloud text from images or a live environment.
- Automated Data Entry: Extracting and digitizing information from forms into databases.
- Subtitle Generation: Create subtitles for videos by recognizing and transcribing spoken text.

License
-------
This project is released under the MIT License.

Contributions
-------------
Contributions to this project are welcome. Feel free to fork, modify, and make pull requests.

Contact
-------
For any inquiries or contributions, please contact me at ankush.saxena.dev@gmail.com.