import maestro
import yaml
import dlib
from imutils import face_utils
import time
import cv2

try:
    CONTROLLER = maestro.Controller()
except:
    print("Controller couldnt be initialized, expect problems")

try:
    CAP = cv2.VideoCapture(0)
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

    # Capture frame
    ret, frame = CAP.read()
    
    # Our operations on the frame come here
    # Make the frame grayscale
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect bounding box for faces
    dets = DETECTOR(img, 1)
    
    # Assume only one face is going to be found
    shape = PREDICTOR(img, d[0])


    score = None
    return score, img

def _get_normed_landmarks(img):
    # TODO: Take image and derive landmark locations
    return

def get_ref_img_landmarks(img):
    return _get_normed_landmarks(img)
