# /!\ Only works on Mac OS /!\

# Import libraries and modules needed
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from deepface import DeepFace
import threading
import time
import cv2
import os
import json


# Ask if the user wants to edit the settings before starting the program
while True:
    askStart = input(
        "Do you want to edit the settings before starting the program? (y/n) ")
    if askStart == "y":
        os.system("python settings.py")
        break
    elif askStart == "n":
        break
    else:
        print("Please enter y or n")

# Start the camera
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

# Set the camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 940)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 780)

# Initialize variables
counter = 0
face_match = False
face_name = ""
main_faces_folder = 'faces'
x = 0
y = 0
w = 0
h = 0


# Get the reference faces from the faces folder
def get_reference_faces(folder):
    reference_faces = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(('.jpg', '.png', '.jpeg')):
                folder_name = os.path.basename(root)
                reference_faces.append((folder_name, os.path.join(root, file)))
    return reference_faces


reference_faces = get_reference_faces(main_faces_folder)

# Get the settings from the settings.json file


def get_settings(data_name):
    with open('assets/settings.json') as json_file:
        data = json.load(json_file)
        return data[data_name]


# Send a notification on Discord when a face is recognized using a webhook
def send_notification(name):
    webhook_url = get_settings("webhook_url")

    webhook = DiscordWebhook(url=webhook_url, username=get_settings("webhook_name"),
                             avatar_url=get_settings("webhook_avatar"))

    embed = DiscordEmbed(title="Face match found!",
                         description=f"**Name:** {name}\n**Time:** {time.strftime('%H:%M:%S')}\n**Last log:** {get_last_log(name)}",
                         color=0x00ff00)  # Vous pouvez changer la couleur en fonction de vos préférences

    webhook.add_embed(embed)
    webhook.execute()
    print("Sending notification...")


# Log the face reconized in the log.txt file
def log_reco(name):
    log_record = open("assets/log.txt", "r")
    current_logs = log_record.readlines()
    log_record.close()
    log_record = open("assets/log.txt", "w")
    now = datetime.now()
    date_time_stamp = get_timestamp()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    log_record.write(name + "/cam1/" + formatted_date_time +
                     "/" + date_time_stamp + "\n")
    log_record.writelines(current_logs)
    log_record.close()
    print("Logging reco...")


# Get the timestamp of the current time
def get_timestamp():
    now = datetime.now()
    date_reference = datetime(2020, 1, 1)
    date_time_stamp = (now - date_reference).total_seconds()
    date_time_stamp = str(date_time_stamp).split(".")[0]
    return date_time_stamp


# Check if the face has been recognized less than -- seconds ago (the detection interval is set in the settings.json file)
def check_last_reco(name):
    log_record = open("assets/log.txt", "r")
    current_logs = log_record.readlines()
    log_record.close()
    print("Checking last reco2")
    print("name : " + name)
    for line in current_logs:
        if name in line:
            date = line.split("/")[3].strip()
            print("date : " + date)
            time_difference = int(get_timestamp()) - int(date)
            if time_difference < int(get_settings("detection_interval")):
                return False
    return True


# Action if the face is recognized
def action_if_reco(folder_name):
    print("Face recognized")
    global face_name
    matching_image_name = os.path.splitext(folder_name)[0]
    face_name = matching_image_name
    if check_last_reco(matching_image_name):
        send_notification(matching_image_name)
        log_reco(matching_image_name)
        print("Face recognized")
    else:
        print("Face already recognized less than 15 seconds ago")


# Get the last log of the face recognized
def get_last_log(name):
    log_record = open("assets/log.txt", "r")
    current_logs = log_record.readlines()
    log_record.close()
    for line in current_logs:
        if name in line:
            date = line.split("/")[2].strip()
            return date
    return True


# Check if the face is recognized
def check_face(frame):
    global face_match
    global face_name
    global x
    global y
    global w
    global h
    try:
        for folder_name, reference_img_path in reference_faces:
            reference_img = cv2.imread(reference_img_path)
            result = DeepFace.verify(frame, reference_img)
            print(result)

            if result["verified"]:
                x, y, w, h = result['facial_areas']['img1']['x'], result['facial_areas']['img1'][
                    'y'], result['facial_areas']['img1']['w'], result['facial_areas']['img1']['h']
                face_match = True
                action_if_reco(folder_name)

                break
            else:
                face_match = False
                face_name = ""
    except ValueError:
        face_match = False
        face_name = ""


# Main loop
while True:
    # Read the camera frame
    ret, frame = cap.read()

    if ret:
        # Check if the face is recognized every 30 frames
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face,
                                 args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1

        cv2.putText(frame, 'Press S for settings', (50, 630),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        if face_match:
            now = datetime.now()
            start_point = (x, y)
            end_point = (x + w, y + h)
            color = (255, 0, 0)
            thickness = 2
            hour = now.strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, 'Face Match: ' + face_name, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
            cv2.putText(frame, 'Infos : ' + hour, (50, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
            cv2.putText(frame, 'Last log: ' + get_last_log(face_name), (50, 130),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
            frame = cv2.rectangle(frame, start_point,
                                  end_point, color, thickness)
            cv2.putText(frame, 'Name: ' + face_name, (x, y + h + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

        else:
            cv2.putText(frame, 'No Match', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        # Display the resulting frame
    cv2.imshow('video', frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        os.system("python settings.py")

    if key == ord('q'):
        break

cv2.destroyAllWindows()
