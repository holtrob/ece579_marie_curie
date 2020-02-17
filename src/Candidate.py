"""
Candidate Class
"""
# Throughout all of this, servo positions and chromosomes are used interchangably to mean the same thing

class Candidate:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.score = None

    def set_score(self, score):
        self.score = score

    # Classmethod is a special type of method that doesnt receive "self"
    # since it doesnt have a concept of an instance of Candidate.  Instead
    # it receives the class Candidate, and functions as an alternate constructor.
    @classmethod
    def create_random(cls):
        # Calc random servo_positions here
        servo_positions = []
        return cls(servo_positions)

if __name__ == "__main__":
    pass