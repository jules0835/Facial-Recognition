# Import libraries and modules needed
from datetime import datetime
from deepface import DeepFace
import threading
import requests
import json
import time
import cv2
import os


cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

# Set the camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0
face_match = False
face_name = ""
reference_faces_folder = 'faces'
reference_faces = [os.path.join(reference_faces_folder, f) for f in os.listdir(
    reference_faces_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]


def send_notification(name):
    webhook_url = "https://discord.com/api/webhooks/XXXXXXXXXXXXXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    message = {
        "content": "Face match found! : " + name + " Heure : " + time.strftime("%H:%M:%S"),
        "username": "Secutity Bot",
        "avatar_url": "https://sciencepost.fr/wp-content/uploads/2018/10/iStock-851960058.jpg"
    }
    payload = json.dumps(message)
    headers = {"Content-Type": "application/json"}
    requests.post(webhook_url, data=payload, headers=headers)
    print("Sending notification...")


def log_reco(name):
    log_record = open("log.txt", "r")
    current_logs = log_record.readlines()
    log_record.close()
    log_record = open("log.txt", "w")
    now = datetime.now()
    date_time_stamp = get_timestamp()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    log_record.write(name + "/cam1/" + formatted_date_time +
                     "/" + date_time_stamp + "\n")
    log_record.writelines(current_logs)
    log_record.close()
    print("Logging reco...")


def get_timestamp():
    now = datetime.now()
    date_reference = datetime(2020, 1, 1)
    date_time_stamp = (now - date_reference).total_seconds()
    date_time_stamp = str(date_time_stamp).split(".")[0]
    return date_time_stamp


def check_last_reco(name):
    log_record = open("log.txt", "r")
    current_logs = log_record.readlines()
    log_record.close()
    print("name : " + name)
    for line in current_logs:
        if name in line:
            date = line.split("/")[3].strip()
            print("date : " + date)
            time_difference = int(get_timestamp()) - int(date)
            if time_difference < 15:
                return False
    return True


def action_if_reco(ref_image):
    global face_name
    matching_image_name = os.path.basename(ref_image)
    matching_image_name = os.path.splitext(matching_image_name)[0]
    face_name = matching_image_name
    if check_last_reco(matching_image_name):
        send_notification(matching_image_name)
        log_reco(matching_image_name)
        print("Face recognized")
    else:
        print("Face already recognized less than 15 seconds ago")


def check_face(frame):
    global face_match
    try:
        for reference_img_path in reference_faces:
            reference_img = cv2.imread(reference_img_path)
            result = DeepFace.verify(frame, reference_img)
            if result["verified"]:
                face_match = True
                action_if_reco(reference_img_path)

                break
            else:
                face_match = False
                face_name = ""
    except ValueError:
        face_match = False
        face_name = ""


while True:
    ret, frame = cap.read()

    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face,
                                 args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1

        if face_match:
            cv2.putText(frame, 'Face Match: ' + face_name, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        else:
            cv2.putText(frame, 'No Match', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        cv2.imshow('video', frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cv2.destroyAllWindows()
