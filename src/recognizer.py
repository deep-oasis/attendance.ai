import dlib
import picamera
import numpy as np
from PIL import Image
from os.path import basename
import face_recognition_models as frm
from src.config import log


class Recognizer:
    def __init__(self, employees, resolution=(320, 240), model_type="small", nb_iters=1):
        # nb_iters - the higher is more percise but slower 
        # model_type - "small" / "large" large is more accurate but slower 
        self.camera = picamera.PiCamera()
        self.camera.resolution = resolution
        self.np_output = np.zeros((resolution[1], resolution[0], 3),dtype=np.uint8)
        self.model = frm.face_recognition_model_location()
        self.encoder = dlib.face_recognition_model_v1(self.model)
        self.face_detector = dlib.get_frontal_face_detector()
        self.model_type = model_type
        self.nb_iters = nb_iters
        self.employees = employees

        self.predictor = frm.pose_predictor_five_point_model_location()
        if self.model_type == "large": 
            self.predictor = frm.face_recognition_models.pose_predictor_model_location()

        self.load_faces()


    def load_img(self, path):
        return np.array(Image.open(path).convert('RGB'))


    def raw_face_locations(self, img, nb_upsamples=1):
        return self.face_detector(img, nb_upsamples)


    def trim_css_to_bounds(self, css, image_shape):
        return max(css[0], 0), min(css[1], image_shape[1]), min(css[2], image_shape[0]), max(css[3], 0)


    def rect_to_css(self, rect):
        return rect.top(), rect.right(), rect.bottom(), rect.left()


    def css_to_rect(self, css):
        return dlib.rectangle(css[3], css[0], css[1], css[2])


    def face_locations(self, img, nb_upsamples=1):
        return [self.trim_css_to_bounds(self.rect_to_css(face), img.shape) for face in self.raw_face_locations(img, nb_upsamples)]


    def face_landmarks(self, face_image, known_face_locations):
        face_locations = None
        if not known_face_locations:
            face_locations = self.face_detector(face_image)
        else:
            face_locations = [self.css_to_rect(face_location) for face_location in known_face_locations]
            
        pose_predictor = dlib.shape_predictor(self.predictor)
        return [pose_predictor(face_image, face_location) for face_location in face_locations]


    def faces_encodings_from_img(self, face_image, known_face_locations=None):
        raw_landmarks = self.face_landmarks(face_image, known_face_locations)
        return [np.array(self.encoder.compute_face_descriptor(face_image, raw_landmark_set, self.nb_iters)) for raw_landmark_set in raw_landmarks]


    def load_faces(self):
        for i, emp in enumerate(self.employees):
            log.info("Loading {}'s face image".format(emp.name))
            img = self.load_img(emp.img_path)
            self.employees[i].encoded_face = self.faces_encodings_from_img(img)[0]


    def compare_faces(self, employee, frame_faces, tolerance=0.6):
        if True in list(np.linalg.norm(frame_faces - employee.encoded_face, axis=1) <= tolerance):
            log.info("{} was found!".format(employee.name))
            employee.add_timestamp()

    # def compare_faces(self, face_encoding_to_check, tolerance=0.6):
    #     # Returns face names was found
    #     matches = list(np.linalg.norm(self.face_enc_list - face_encoding_to_check, axis=1) <= tolerance)
    #     face = [i for i, x in enumerate(matches) if x]
    #     if len(face) and len(face) < 1: return self.face_names_list[face[0]]
    #     return None


    def analyze_frame(self, face_loc_list):
        log.info("Found {} faces".format(len(face_loc_list)))
        faces_encodings = self.faces_encodings_from_img(self.np_output, face_loc_list)
        found_list = [self.compare_faces(emp, faces_encodings) for emp in self.employees]
            
        if True in found_list:
            name = "Barack Obama"
            print("I see someone named {}!".format(name))


    def run(self):
        while True:
            # Get a new frame (into self.np_output)
            self.camera.capture(self.np_output, format="rgb")
            face_loc_list = self.face_locations(self.np_output)
            
            if face_loc_list: 
                self.analyze_frame(face_loc_list)
