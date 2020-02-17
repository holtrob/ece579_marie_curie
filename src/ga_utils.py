import maestro
import yaml
import dlib
import cv2

CONTROLLER = maestro.Controller()

# TODO: bring in the servo descriptions via yaml and reference
# when generating random candidates to ensure their servo positions
# are never out of range

def actuate_chromosome(chromosome):
    # TODO: use maestro controller object to actuate this face
    return

def get_score(chromosome, landmarks):
    # TODO: Implement algorithm for taking picture and
    # finding landmarks.  Then compare to reference photo
    # Right now this is a terrible pattern because it needs
    # to know the reference photo and it doesnt make
    # sense for the Candidates to have to know it.
    score = None
    return score

def _get_normed_landmarks(img):
    # TODO: Take image and derive landmark locations 
    return

def get_ref_img_landmarks(img):
    return _get_normed_landmarks(img)