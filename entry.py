import sys
import os

import cv2
import hashlib
import face_recognition
import json

from store import Store


LOCAL_STORE_PATH = "./face.json"


class Entry(object):
    def __init__(self):
        self.store = Store()

    def load_image(self, file_path, name):
        if not os.path.exists(file_path):
            print("Image file not existed")
            return -1

        image_hash = self.compute_hash(file_path)
        if self.store.get_face_by_hash(image_hash):
            print("Face already recorded.")
            return -2

        try:
            image = face_recognition.load_image_file(file_path)
            face_encoding = face_recognition.face_encodings(image)[0]
        except Exception:
            print("Failed to recognition face")
            return -3

        face = {
            "name": name,
            "hash": image_hash,
            "face_encoding": list(face_encoding)
        }

        self.store.create_face(face)

    def compute_hash(self, file_path):
        with open(file_path, "r") as f:
            data = f.read()
            image_md5 = hashlib.md5(data)
            return image_md5.hexdigest()


if "__main__" == __name__:
    if len(sys.argv) < 3:
        print("Enter face file and name")
        os.Exits()

    entry = Entry()
    entry.load_image(sys.argv[1], sys.argv[2])
