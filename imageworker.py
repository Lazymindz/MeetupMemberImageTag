import face_recognition
from PIL import Image, ImageDraw
import logging
import os, os.path
import time
import re
import numpy as np

# This is an example of running face recognition on a single image
# and drawing a box around each person that was identified.
# Code skeleton from https://github.com/ageitgey/face_recognition/blob/master/examples/recognize_faces_in_pictures.py

# Load a sample picture and learn how to recognize it.
def createandloadencodings():
    loaded_face_encodings = {}
    if len(os.listdir('WorkingFolder/MeetupImages')) > 0:
        for fil in os.listdir('WorkingFolder/MeetupImages'):
            name = fil.replace('.jpeg','')
            name_image = face_recognition.load_image_file(os.path.join('WorkingFolder/MeetupImages',fil))
            name_face_encoding = face_recognition.face_encodings(name_image)
            if len(name_face_encoding) > 0:
                loaded_face_encodings[name] = name_face_encoding[0]
    np.save('./.metadata/meetup_faces.npy', loaded_face_encodings)
    return loaded_face_encodings

def loadencodings(retrain=False):
    if (not os.path.exists('./.metadata/meetup_faces.npy')) or (retrain==True):
        createandloadencodings()
    else:
        return np.load('./.metadata/meetup_faces.npy')

def tagmembers(meetup_image, loaded_face_encodings, tolerance=0.6):

    known_face_names, known_face_encodings = list(loaded_face_encodings[()].keys()), list(loaded_face_encodings[()].values())

    # Load an image with an unknown face
    unknown_image = face_recognition.load_image_file(meetup_image)
    
    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    pil_image = Image.fromarray(unknown_image)
    
    # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=tolerance)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(255, 0, 0), outline=(255, 0, 0))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Display the resulting image
    #pil_image.show()

    # Save a copy of the new image to disk
    timestring = time.strftime("%Y%m%d-%H")
    pil_image.save(f"./WorkingFolder/OutputImages/Output-{timestring}.PNG", "PNG")