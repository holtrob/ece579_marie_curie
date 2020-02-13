import servo
import yaml

class Face:
    def __init__(self, controller):
        # Parse the YAML file to get the actual servo descriptions
        servo_desc_fname = "marie_servo_descriptions.yaml"
        with open(servo_desc_fname, 'r') as f:
            self.servo_descriptions = yaml.load(f, Loader=yaml.FullLoader)
        facial_expressions_fname = "expressions_gestures.yaml"
        with open(facial_expressions_fname, 'r') as f:
            exp_gestures = yaml.load(f, Loader=yaml.FullLoader)
            self.expressions = exp_gestures['expressions']

        self.servos = {}
        for name in self.servo_descriptions.keys():
            self.servos[name] = servo.Servo(name, controller)
    
    def __str__(self):
        all_servo_names = ", ".join(self.servos.keys())
        expressions = ", ".join(self.expressions.keys())
        return f"Face has servos: {all_servo_names}.\nFace has expressions: {expressions}"

    def __repr__(self):
        all_servo_names = ", ".join(self.servos.keys())
        expressions = ", ".join(self.expressions.keys())
        return f"Face has servos: {all_servo_names}.\nFace has expressions: {expressions}"
    
    def get_expression_names(self):
        return list(self.expressions.keys())

    def perform_expression(self, exp_name, default_positions=True):
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
    