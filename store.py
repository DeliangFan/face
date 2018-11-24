import sys
import os

import cv2
import hashlib
import face_recognition
import json


LOCAL_STORE_PATH = "/.face.json"


class Store(object):
    def __init__(self):
        current_path = os.path.abspath(__file__)
        current_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
        self.store_file_path = current_dir + LOCAL_STORE_PATH

        if os.path.exists(self.store_file_path):
            with open(self.store_file_path) as f:
                self.data = json.load(f)
        else:
            self.data = {
                "faces": []
            }
    
    def get_face_by_hash(self, image_hash):
        for face in self.data["faces"]:
            if face["hash"] == image_hash:
                return face
        return None

    def list_faces(self):
        return self.data

    def create_face(self, face):
        self.data["faces"].append(face)
        with open(self.store_file_path, 'w') as f:
            json.dump(self.data, f)

    def delete_face(self):
        pass


if "__main__" == __name__:
    if len(sys.argv) < 3:
        print("Enter face file and name")
        os.Exits()

    data_entry = DataEntry()
    data_entry.load_image(sys.argv[1], sys.argv[2])
