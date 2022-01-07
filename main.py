import face_recognition
import cv2
import numpy as np
from glob import glob
import os

names = glob("known_faces/*/")
all_files = list()
all_dirs = list()

# Iterate for each dict object in os.walk()

images=[]
#print(names)
name_list= [
    "Dan",
    "Rechard",
    "Tilde"
]
faces=[]
encodings=[]
# Load a sample picture and learn how to recognize it.
print("Image loading and endcoding started..")
for name in names:

    for root, dirs, files in os.walk(name):
        # Add the files list to the the all_files list
        all_files.extend(files)
        temp_images=[]
        temp_encodings=[]
        for file in files:
            #print(name+file)
            image=face_recognition.load_image_file(str(name+file))
            temp_images.append(image)
            try:

                encod=face_recognition.face_encodings(image)[0]
            except:
                print("No face found ",name+file)
            temp_encodings.append(encod)
        faces.append(temp_images)
        encodings.append(temp_encodings)
        # Add the dirs list to the all_dirs list
        all_dirs.extend(dirs)

print("encoding successfully done for "+str(len(encodings))+" people")


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    scores=[]

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
        count = []
        for encoding in encodings:

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(encoding, face_encoding)

                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    #print(matches)
                    count.append(matches.count(True))

                else:
                    # no matching images
                    count.append(0)

        #         # Or instead, use the known face with the smallest distance to the new face
        #         face_distances = face_recognition.face_distance(encoding, face_encoding)
        #         scores.append(np.sum(face_distances))
        # result=np.array(scores)
        try:

            if np.max(np.array(count))>0:
                #print(result)
                best_match_index = count.index(np.max(np.array(count)))
                name=name_list[best_match_index]

            else:
                name="unknown"
        except:
            print("No person")
        face_names.append(name)

    process_this_frame = not process_this_frame


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