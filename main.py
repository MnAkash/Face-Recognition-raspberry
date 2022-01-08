# importing library
import face_recognition
import cv2
import numpy as np

import pyttsx3
import time
from glob import glob
import os
from datetime import datetime

engine = pyttsx3.init()  # object creation
import datetime as dt
import random

# this is for getting the directories of each person images
names = glob("known_faces/*/")
all_files = list()
all_dirs = list()


images = []
# print(names)

# please input the name of all person here alphabetically
name_list = [
    "Dan",
    "Rechard",
    "Tilde"
]

# face stores all the face it got from image directory and encodings store all the encodings of faces
faces = []
encodings = []


# this check if corrent time is within the time span or not
def validity(start, end):
    return start < datetime.now().time() < end


# this function speak with whatever the text it has
def speaking(text):
    """ RATE"""
    rate = engine.getProperty('rate')  # getting details of current speaking rate
    print(rate)  # printing current voice rate
    engine.setProperty('rate', 100)  # setting up new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')  # getting to know current volume level (min=0 and max=1)
    print(volume)  # printing current volume level
    engine.setProperty('volume', 1.0)  # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')  # getting details of current voice
    # engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female

    engine.say(text)
    engine.runAndWait()
    engine.stop()


# person_names has all the name of person of txt directory
person_names = glob("records/*/")
all_files = list()
all_dirs = list()



#input all the person name in this list
name_list = [
    "Dan",
    "Rechard",
    "Tilde"
]

#input all the weman name in this list
women_name = [
    "Tilde"
]

#input all the man name in this list
man_name = [
    "Dan",
    "Rechard"
]
record = []             #record stores all the txt file locations
name_sequence = []
for name in person_names:
    temp = str(glob(str(name) + "*.txt")).split(".")
    n = temp[0].split("\\")
    name_sequence.append(n[-1])
    record.append(glob(str(name) + "*.txt")[0])
print(record)

print("Image loading and endcoding started..")
# this block of code load all the images and also generate the encodings of them
for name in names:

    for root, dirs, files in os.walk(name):
        # Add the files list to the the all_files list
        all_files.extend(files)
        temp_images = []
        temp_encodings = []
        for file in files:
            # print(name+file)
            image = face_recognition.load_image_file(str(name + file))
            temp_images.append(image)
            try:

                encod = face_recognition.face_encodings(image)[0]
            except:
                print("No face found ", name + file)
            temp_encodings.append(encod)
        faces.append(temp_images)
        encodings.append(temp_encodings)
        # Add the dirs list to the all_dirs list
        all_dirs.extend(dirs)

print("encoding successfully done for " + str(len(encodings)) + " people")

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
prev_detected_names = ""            #this variable keep track wheather same person or group of persons repeat on sequential frame or not

while True:
    scores = []

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        count = [0, 0, 0]
        for face_encoding in face_encodings:
            c = 0

            for encoding in encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(encoding, face_encoding)

                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    print(matches)
                    print(c)
                    # first_match_index = matches.index(True)
                    # print(encodings.index(encoding))
                    count[c] = matches.count(True)
                else:
                    # no matching images
                    name = "unkown"
                c += 1
            try:
                # find highest matching name from the image
                if np.max(np.array(count)) > 0:
                    print(count)
                    best_match_index = count.index(np.max(np.array(count)))
                    name = name_list[best_match_index]
                    face_names.append(name)
                    count = [0, 0, 0]

                else:
                    # if not matching then detected person name will be as "unknown"
                    name = "unknown"
                    face_names.append(name)
            except:
                print("No person")

        print(face_names)
        detected_names = face_names

        if detected_names == prev_detected_names:
            # if same result repeat on two sequential frame
            print("Already Said")
        else:

            if len(detected_names) > 0:

                if "unknown" not in detected_names:

                    if len(detected_names) == 1:
                        nam = detected_names[0]

                        if nam != "unknown":

                            if validity(dt.time(5, 30), dt.time(10, 0)):
                                file_index = name_sequence.index(nam)   # find the txt file for detected person
                                print(str(record[file_index]))
                                file_name = str(record[file_index])
                                status = ""
                                with open(file_name, 'r') as f:
                                    status = f.readline()
                                    print(status)
                                    f.close()
                                if str(status) == "0":          # check if we look him or her first time or not
                                    speaking("Good morning {}".format(nam))
                                with open(file_name, 'w') as f:
                                    lines = f.write("1")
                                    f.close()

                            if validity(dt.time(10, 1), dt.time(16, 30)):   #checking the validity
                                file_index = name_sequence.index(nam)
                                print(str(record[file_index]))
                                file_name = str(record[file_index])
                                text = ["hello", "hey"]
                                text_ind = random.randint(0, 1)
                                selected_text = text[text_ind]
                                speaking(selected_text + "{}".format(nam))
                            if validity(dt.time(16, 31), dt.time(18, 30)):
                                file_index = name_sequence.index(nam)
                                print(str(record[file_index]))
                                file_name = str(record[file_index])
                                text = ["hello", "hey"]
                                text_ind = random.randint(0, 1)
                                selected_text = text[text_ind]
                                speaking(selected_text + "{}".format(nam))
                                status = ""
                                with open(file_name, 'r') as f:
                                    status = f.readline()
                                    print(status)
                                    f.close()
                                if str(status) == "1":
                                    speaking("Have a nice evening {}".format(nam))
                                # with open(file_name, 'w') as f:
                                #     lines = f.write("1")
                                #     f.close()
                        if nam == "unknown":
                            if validity(dt.time(5, 30), dt.time(10, 0)):
                                speaking("Good Morning")

                            if validity(dt.time(10, 1), dt.time(16, 30)):
                                speaking("Hello")

                            if validity(dt.time(16, 31), dt.time(18, 30)):
                                speaking("Have a pleasant evening")
                    if len(detected_names) > 1:
                        women_count = 0
                        man_count = 0
                        for name in detected_names:
                            if name in women_name:
                                women_count += 1
                            if name in man_name:
                                man_count += 1
                        if women_count > 0 and man_count == 0:
                            if validity(dt.time(5, 30), dt.time(10, 0)):
                                speaking("Good Morning Ladies")

                            if validity(dt.time(10, 1), dt.time(16, 30)):
                                speaking("Hello Ladies")

                            if validity(dt.time(16, 31), dt.time(18, 30)):
                                speaking("Good evening Ladies")
                        if man_count > 0 and women_count == 0:
                            if validity(dt.time(5, 30), dt.time(10, 0)):
                                speaking("Morning Guys")

                            if validity(dt.time(10, 1), dt.time(16, 30)):
                                speaking("Hey Guys")

                            if validity(dt.time(16, 31), dt.time(18, 30)):
                                speaking("Evening Guys")
                        if man_count != 0 and women_count != 0:
                            if validity(dt.time(5, 30), dt.time(10, 0)):
                                speaking("Good morning")

                            if validity(dt.time(10, 1), dt.time(16, 30)):
                                speaking("Hey All")

                            if validity(dt.time(16, 31), dt.time(18, 30)):
                                speaking("Good Evening")
                else:
                    if len(detected_names) == 1:
                        nam = detected_names[0]
                        if validity(dt.time(5, 30), dt.time(10, 0)):
                            speaking("Good morning and welcome")

                        if validity(dt.time(10, 1), dt.time(16, 30)):
                            speaking("Hello and welcome")

                        if validity(dt.time(16, 31), dt.time(18, 30)):
                            speaking("Good evening and welcome")
                    else:
                        if len(detected_names) != detected_names.count("unknown"):

                            if validity(dt.time(5, 30), dt.time(10, 0)):
                                speaking("Good morning")

                            if validity(dt.time(10, 1), dt.time(16, 30)):
                                speaking("Hey All")

                            if validity(dt.time(16, 31), dt.time(18, 30)):
                                speaking("Good Evening")
                        else:
                            if validity(dt.time(5, 30), dt.time(10, 0)):
                                speaking("Good morning and welcome")

                            if validity(dt.time(10, 1), dt.time(16, 30)):
                                speaking("Hello and welcome")

                            if validity(dt.time(16, 31), dt.time(18, 30)):
                                speaking("Good evening and welcome")

    process_this_frame = not process_this_frame
    prev_detected_names = detected_names

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
