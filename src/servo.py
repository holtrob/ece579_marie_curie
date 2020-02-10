"""
servo.py

This module features an implementation for a Servo class which abstracts away
the details of the servo positions, and instead loads a servo_description dictionary
which defines what semantic values the servo can take on and gives the position which is actually
to be sent.  This class also interfaces with the Pololu board to perform the actual communication
via the passed Maestro controller instance.
"""

from marie_servo_config import servo_descriptions

class Servo:
    """ Implements a class for interacting and dealing with servos at a semantic level
    :param name: This is the name given to a servo and must match those defined in marie_servo_config.py
    :type str:
    :param maestro_controller: Used for actually issuing the control commands
    :type maestro_controller: maestro.Controller
    :attr last_semantic: Description of semantic position last requested (i.e. up, down)
    """
    def __init__(self, name, maestro_controller):
        self.name = name
        try:
            self.channel = servo_descriptions[name]['channel']
        except:
            print(f'Could not find channel for this controller.  Double check the name and marie_servo_config')
            raise
        self.controller = maestro_controller
        self.last_semantic = 'unknown'

    def __repr__(self):
        print(f"{self.name} servo is on channel {self.channel} in position {self.last_semantic}")

    def __str__(self):
        print(f"{self.name} servo is on channel {self.channel} in position {self.last_semantic}")
    
    def set_sem_pos(self, semantic_pos):
        """ Set a target position based on a name in marie_servo_config.servo_positions
        :param semantic_pos: Named position (i.e. 'open' in case of jaw servo)
        :type semantic_pos: str
        """
        pos = servo_descriptions[self.name]['positions'][semantic_pos]
        self.controller.setTarget(self.channel, pos)
        self.last_semantic = semantic_pos

    def set_num_pos(self, numerical_pos):
        """ Set a target position based on a raw numerical value
        :param numerical_pos: number of microseconds for the PWM pulse
        :type numerical_pos: float
        """
        self.controller.setTarget(self.channel, numerical_pos)
        self.last_semantic = 'unknown'