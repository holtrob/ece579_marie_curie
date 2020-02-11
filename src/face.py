import marie_servo_config
import facial_expressions
import servo

class Face:
    def __init__(self, controller):
        self.servos = {}
        for name in marie_servo_config.servo_descriptions.keys():
            self.servos[name] = servo.Servo(name, controller)
    
    def __str__(self):
        all_servo_names = ", ".join(self.servos.keys())
        print(f"Face has servos: {all_servo_names}")

    def __repr__(self):
        all_servo_names = ", ".join(self.servos.keys())
        print(f"Face has servos: {all_servo_names}")
    
    def perform_expression(self, exp_name, default_positions=True):
        staged_movements = {}

        # if default positions are desired for unspecified servos, then stage all resets
        if default_positions:
            for name in self.servos.keys():
                staged_movements[name] = marie_servo_config.servo_descriptions[name]['default_pos']
        
        #Update staged movements with those explicitly set in the expression
        for s_name, pos in facial_expressions.marie_expressions[exp_name].items():
            staged_movements[s_name] = pos

        # Execute all movements
        for s_name, pos in staged_movements.items():
            self.servos[s_name].set_sem_pos(pos)

if __name__ == "__main__":
    import maestro
    face = Face(maestro.Controller())
    face.perform_expression('meh')
    print(face)
    