import maestro
import yaml
import dlib
from imutils import face_utils
import time
import cv2
import numpy as np

try:
    CONTROLLER = maestro.Controller()
except:
    print("Controller couldnt be initialized, expect problems")

try:
    CAP = cv2.VideoCapture(0)
    CAP.set(cv2.CAP_PROP_BUFFERSIZE, 1)
except:
    print("Video device couldnt be initialized, expect problems)")

DETECTOR = dlib.get_frontal_face_detector()
PREDICTOR = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def get_servo_limits(yaml_filename="marie_servo_descriptions.yaml"):
    # Open up the yaml file and bring in the servo descriptions
    with open(yaml_filename, 'r') as f:
        servo_descs = yaml.load(f, Loader=yaml.FullLoader)
    # Sort the servo descriptions by channel number
    servo_desc_list = list(servo_descs.values())
    servo_desc_list.sort(key=lambda x: x['channel'])

    limits = []
    # Iterate through the descriptions and build a min/max limit tuple
    for servo_desc in servo_desc_list:
        limits.append((servo_desc['min_pos'], servo_desc['max_pos']))
    return tuple(limits)

LIMITS = get_servo_limits()

def actuate_chromosome(chromosome):
    servo_pos = chromosome
    CONTROLLER.setMultipleTargets(0, servo_pos)
    return

def get_score(chromosome, ref_norm_landmarks):
    # TODO: Implement algorithm for taking picture and
    # finding landmarks.  Then compare to reference photo landmarks
    
    # Actuate the face and wait for it to be actuated
    actuate_chromosome(chromosome)
    time.sleep(1)

    # Throw away a capture because the minimum buffersize is 1
    _, _ = CAP.read()
    # Take the actual image
    ret, frame = CAP.read()
    
    # Our operations on the frame come here
    # Make the frame grayscale
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    adjusted_landmarks = _get_normed_landmarks(img)

    diff_landmarks = ref_norm_landmarks - adjusted_landmarks
    score = np.linalg.norm(diff_landmarks @ diff_landmarks.T, ord='fro')

    return score, img

def _get_normed_landmarks(img):
    # TODO: derive landmark locations
    # Detect bounding box for faces
    dets = DETECTOR(img, 1)

    # Assume only one face is going to be found
    shape = PREDICTOR(img, dets[0])
    raw_landmarks = face_utils.shape_to_np(shape, dtype='float')

    bbox_l, bbox_r, bbox_t, bbox_b = shape.rect.left(), shape.rect.right(), shape.rect.top(), shape.rect.bottom()

    center = [shape.rect.center().x, shape.rect.center().y]
    x_factor = float(bbox_r - center[0])
    y_factor = float(bbox_b - center[1])

    adjusted_landmarks = raw_landmarks - center
    adjusted_landmarks[:,0] = adjusted_landmarks[:, 0] / x_factor
    adjusted_landmarks[:,1] = adjusted_landmarks[:, 1] / y_factor
    return adjusted_landmarks

def get_ref_img_landmarks():
    # Throw away a capture because the minimum buffersize is 1
    _, _ = CAP.read()
    # Take the actual image
    ret, frame = CAP.read()
    
    # Our operations on the frame come here
    # Make the frame grayscale
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return _get_normed_landmarks(img)
