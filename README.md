# Facial-Recognition
Simple facial recognition security system implemented in Python.

## Unstable version.
## Project under development, currently available only on Mac.

# Facial Recognition Security System

This is a simple facial recognition security system implemented in Python using the [DeepFace](https://github.com/serengil/deepface) library. The system captures video from a camera, performs facial recognition against a set of reference faces, and takes action when a match is found (send message on Discord, log the match in a file...).

## Prerequisites

Make sure you have the following libraries installed before running the code:

- [OpenCV](https://pypi.org/project/opencv-python/): `pip install opencv-python`
- [DeepFace](https://pypi.org/project/deepface/): `pip install deepface`
- [Requests](https://pypi.org/project/requests/): `pip install requests`

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/votre-utilisateur/votre-repo.git
    cd votre-repo
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the script:

    ```bash
    python facial_recognition.py
    ```


## Configuration

- The camera resolution is set to 640x480, but you can modify it by changing the values in the following lines:

    ```python
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    ```

- The reference faces are stored in the `faces` folder. You can add or remove faces as needed.

- The notification is sent to a Discord webhook. Update the `webhook_url` variable with your own webhook URL.

## Notifications

Notifications are sent to Discord when a face match is found. You can customize the notification message, username, and avatar URL in the `send_notification` function.

## Logging

Recognition events are logged in the `log.txt` file. Each log entry includes the name of the recognized face, the camera ID, the timestamp, and a unique timestamp value. The `check_last_reco` function ensures that a face is not recognized again within 15 seconds.
