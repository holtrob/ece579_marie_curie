"""
ECE 579 Intelligent Robotics II
Team 3 - Marie Curie Robot
R. Holt
D. Yakovlev
Candidate.py
"""
from ga_utils import LIMITS
from random import randint
# Throughout all of this, servo positions and chromosomes are used interchangably to mean the same thing

class Candidate:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.score = None

    def set_score(self, score):
        self.score = score
    
    def __repr__(self):
        return f"Candidate chromosome: {self.chromosome} / Score: {self.score}"

    def __str__(self):
        return self.__repr__()

    # Classmethod is a special type of method that doesnt receive "self"
    # since it doesnt have a concept of an instance of Candidate.  Instead
    # it receives the class Candidate, and functions as an alternate constructor.
    @classmethod
    def create_random(cls):
        # Calc random servo_positions here
        servo_positions = []
        for limit in LIMITS:
            servo_positions.append(randint(limit[0], limit[1]))
        return cls(servo_positions)

if __name__ == "__main__":
    print(Candidate.create_random())