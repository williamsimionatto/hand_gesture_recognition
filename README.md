# Hand Gesture Recognition

Hand Gesture Recognition is a project aimed at developing a system capable of accurately detecting and recognizing hand gestures in real-time. Hand gestures serve as a powerful form of non-verbal communication and can be utilized to control a wide range of applications and devices. This project leverages computer vision techniques and machine learning algorithms to analyze video input from a webcam and identify specific hand gestures.

## Features
###  V1.3.2 (Coming soon 2023-06-09) ⏰
* Integrate the image widget with the hand gesture recognition system

###  V1.3.1 (Coming soon 2023-06-09) ⏰
* Create a Widget to show a image

###  V1.3.0 (Coming soon 2023-06-09) ⏰
* Add hand gesture recognition to control the zoom of the image widget (Zoom in, Zoom Out)
* Add new Tkinter mode, key `z` and tkinter_mode `1`

###  V1.2.1  (Available 2023-06-02) ✅
* Integrate the slider widget with the hand gesture recognition system

### V1.2.0  (Available 2023-06-02) ✅
* Add hand gesture recognition to control the slider widget (Clamping)
* Add new mode to enable Tkinter, key `t` and mode `2`
* Add new Tkinter mode, key `c` and tkinter_mode `0`

### 1.1.0  (Available 2023-06-02) ✅
* Configure Tkinter
* Create a Widget to show a slider

### 1.0.1 (Available 2023-05-27) ✅
*  Detect if all hands are closed to exit application

### 1.0.0 (Available 2023-05-27) ✅
* Real-time hand tracking.
* Detection and display of finger landmark points.
* Drawing lines representing the movement of the index finger when it is raised.
* Clearing the drawn lines when the hand is opened.
* Text messages indicating the hand state (open hand, closed hand, raised index finger).

## Prerequisites
- Python 3.9.6
- OpenCV
- MediaPipe
- WebCam

## Installation

Install the required libraries by executing the following command in your terminal:

```bash
pip3 install -r requirements.txt
```

## Usage

1. Run the Python script hand_tracking.py in your development environment or execute the following command in the terminal:
  ```bash
  python3 hand_tracking.py
  ```
2. A window will open showing the live camera feed with the overlay of hand landmark points and lines tracking the movement of the index finger when it is raised.

3. To exit the program, close either hand.

## Demonstration


## Limitations
The current implementation of the hand gesture recognition system has the following limitations:
* The Python version is limited to `3.9.6`, as the MediaPipe library is not compatible with Python `3.10+`.


## Contributors

<div align="center">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/NatanOPelizzoni">
          <img src="https://github.com/NatanOPelizzoni.png" width="100px">
          <br>
          <sub>
            <b>Natan</b>
          </sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/williamsimionatto">
          <img src="https://github.com/williamsimionatto.png" width="100px">
          <br>
          <sub>
            <b>William</b>
          </sub>
        </a>
      </td>
    </tr>
  </table>
<div>

#

> Work developed during the Digital Image Processing course at the University of Passo Fundo - 2023/1.
