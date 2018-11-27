import time
import face_recognition
import cv2

from store import Store


FAST_PROCESS = True
FAST_FRAG = 2
INTERVAL = 5
TOLERANCE = 0.45


def get_time_stamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    stamp = ("".join(time_stamp.split()[0].split("-"))+"".join(time_stamp.split()[1].split(":"))).replace('.', '')
    return stamp


class Video(object):
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.load_face()

    def load_face(self):
        store = Store()
        self.faces = store.list_faces()

        self.known_face_encodings = []
        self.known_face_names = []

        for face in self.faces["faces"]:
            self.known_face_encodings.append(face["face_encoding"])
            self.known_face_names.append(face["name"])

    def start(self):
        count = 0
        face_locations, face_encoding, face_names = [], [], []
        
        while True:
            count = count + 1
            ret, frame = self.video_capture.read()

            if FAST_PROCESS: 
                ratio = 1.0 / FAST_FRAG
                recog_frame = cv2.resize(frame, (0, 0), fx=ratio, fy=ratio)
            else:
                recog_frame = frame
            rgb_recog_frame = recog_frame[:, :, ::-1]

            if count >= INTERVAL:
                count = 0
                # Note(laofan), I find that the cnn is better than hogs while costs lots of computation.
                face_locations = face_recognition.face_locations(
                    rgb_recog_frame,
                    number_of_times_to_upsample=1,
                    model="hog")

                if len(face_locations) > 0:
                    face_encodings = face_recognition.face_encodings(rgb_recog_frame, face_locations)
                    for face_encoding in face_encodings:
                        face_names = []
                        name = "Unknown"
                        matches = self.best_match(self.known_face_encodings, face_encoding, TOLERANCE)
                        if True in matches:
                            first_match_index = matches.index(True)
                            name = self.known_face_names[first_match_index]

                        face_names.append(name)
                else:
                    count = INTERVAL

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                if FAST_PROCESS:
                    top *= FAST_FRAG
                    right *= FAST_FRAG
                    bottom *= FAST_FRAG
                    left *= FAST_FRAG

                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

    def calculate_distances(self):
        pass

    def sample(self):
        pass

    def is_not_obvious(self):
        pass

    def best_match(self, known_face_encodings, face_encoding_to_check, tolerance):
        ret = [False] * len(known_face_encodings)
        face_distance = list(face_recognition.api.face_distance(known_face_encodings, face_encoding_to_check))
        if min(face_distance) <= tolerance:
            ret[face_distance.index(min(face_distance))] = True
        return ret
