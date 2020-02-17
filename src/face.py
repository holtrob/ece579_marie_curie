import servo
import yaml
import time

SERVO_DESC_FNAME = "marie_servo_descriptions.yaml"
FACIAL_EXPRESSIONS_FNAME = "expressions_gestures.yaml"

class Face:
    def __init__(self, controller):
        """
        __init__ Constructor for the Marie Curie face
        instance.  This expects a Maestro controller
        object and handles abstraction between the face
        as a whole and the servos it controls.
        
        Arguments:
            controller {maestro.Controller} -- This is an
                instance of a controller which allows for
                calls to set target positions to servos.
                instances of Servo also require this controller
        """
        # Parse the YAML file to get the actual servo descriptions
        with open(SERVO_DESC_FNAME, 'r') as f:
            self.servo_descriptions = yaml.load(f, Loader=yaml.FullLoader)
        with open(FACIAL_EXPRESSIONS_FNAME, 'r') as f:
            exp_gestures = yaml.load(f, Loader=yaml.FullLoader)
            self.expressions = exp_gestures['expressions']
            self.gestures = exp_gestures['gestures']
        self.servos = {}
        for name in self.servo_descriptions.keys():
            self.servos[name] = servo.Servo(name, controller)
    
    def __del__(self):
        """
        __del__ This function acts as a deconstructor for the instance
        of Face to ensure that the yaml files get written back incase
        they were modified during runtime (i.e. via the GUI)
        """
        with open(SERVO_DESC_FNAME, 'w') as f:
            yaml.dump(self.servo_descriptions, f)
        with open(FACIAL_EXPRESSIONS_FNAME, 'w') as f:
            exp_gestures = {
                'expressions': self.expressions,
                'gestures': self.gestures
            }
            yaml.dump(exp_gestures, f)
    
    def __str__(self):
        all_servo_names = ", ".join(self.servos.keys())
        expressions = ", ".join(self.expressions.keys())
        return f"Face has servos: {all_servo_names}.\nFace has expressions: {expressions}"

    def __repr__(self):
        all_servo_names = ", ".join(self.servos.keys())
        expressions = ", ".join(self.expressions.keys())
        return f"Face has servos: {all_servo_names}.\nFace has expressions: {expressions}"
    
    def get_expression_names(self):
        """
        get_expression_names Simple convenience function
            for providing a list of names for expressions.
            Currently used by the GUI to populate a ComboBox,
            however also useful when using the interpreter
        
        Returns:
            list of strings -- list of expression strings
        """
        return list(self.expressions.keys())

    def perform_gesture(self, ges_name):
        # Fix this for threading
        pose_list = self.gestures[ges_name]
        pose_list.sort(key=lambda x: x['time'])
        last_time = 0.0
        for pose in pose_list:
            dt = pose['time'] - last_time
            time.sleep(dt)
            self.perform_expression(pose['exp'])



    def perform_expression(self, exp_name, default_positions=True):
        """
        perform_expression Allows abstract interface to request that an expression
            be shown on the Face.  Involves setting all of the servos to their intended
            position as defined by self.expressions.  If default_positions is true,
            then all servos not defined in an expression are set to their default value
            according to self.servo_descriptions
        
        Arguments:
            exp_name {string} -- name of the expression which needs to be shown.
                Names are stored in self.expressions.
        
        Keyword Arguments:
            default_positions {bool} -- Indicates whether servos not defined are to be
                set to their default postition. (default: {True})
        """
        staged_movements = {}

        # if default positions are desired for unspecified servos, then stage all resets
        if default_positions:
            for name in self.servos.keys():
                staged_movements[name] = self.servo_descriptions[name]['default_position']
        
        #Update staged movements with those explicitly set in the expression
        for s_name, pos in self.expressions[exp_name].items():
            staged_movements[s_name] = pos

        # Execute all movements
        for s_name, pos in staged_movements.items():
            self.servos[s_name].set_sem_pos(pos)

if __name__ == "__main__":
    import maestro
    face = Face(maestro.Controller())
    face.perform_expression('meh')
    print(face)
    