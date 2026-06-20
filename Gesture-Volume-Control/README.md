# Gesture Volume Control

## Overview

This project allows users to control their computer's volume using hand gestures detected through a webcam. By tracking the distance between the thumb and index finger, the system adjusts the system volume in real time without requiring physical interaction.

The project combines computer vision and hand tracking techniques to create a simple touchless human-computer interaction system.

## Features

* Real-time hand tracking
* Gesture-based volume control
* Webcam integration
* Volume adjustment using finger distance
* Visual feedback on screen
* Lightweight and easy to run

## Tech Stack

* Python
* OpenCV
* MediaPipe
* pycaw
* NumPy

## How It Works

1. The webcam captures live video frames.
2. MediaPipe detects hand landmarks.
3. The positions of the thumb and index finger are identified.
4. The distance between the fingers is calculated.
5. The distance is mapped to the system volume range.
6. Volume is adjusted in real time using pycaw.

## Project Structure

```text
Gesture-Volume-Control/
│
├── HandTrackingModule.py
├── main.py
├── requirements.txt
├── image/
└── README.md
```

## Installation

```bash
git clone <repository-url>
cd Gesture-Volume-Control

pip install -r requirements.txt
```

## Run the Project

```bash
python main.py
```

Ensure that your webcam is connected and accessible before running the application.

## Example Use Cases

* Touchless volume control
* Computer vision demonstrations
* Human-computer interaction projects
* Gesture recognition learning

## Learning Outcomes

Through this project, I learned:

* Real-time computer vision processing
* Hand landmark detection using MediaPipe
* Gesture recognition techniques
* OpenCV video processing
* Audio control using Python
* Human-computer interaction concepts

## Future Improvements

* Additional gesture controls
* Brightness control support
* Media playback controls
* Cross-platform compatibility
* Custom gesture mapping

## License

This project is based on open-source code released under the MIT License.
Original copyright belongs to the respective author.
I have used this project for learning, documentation, and portfolio-building purposes.
