"""
Population Class
"""
import Candidate

class Population:
    def __init__(self, popsize, landmarks):
        self.popsize = popsize
        self.candidates = []
        self.ref_landmarks = landmarks
        # TODO: initialize list of candidates using Candidate.create_random()
    
    def breed_new(self, num_to_breed, num_per_parents=2):
        num_parents = int(num_to_breed / num_per_parents)
        # TODO: sort population then get the mating pool
    
    def get_best_candidate(self):
        self._sort_population()
        return self.candidates[0]

    def _get_mating_pool(self, num_pairs):
        # TODO: implement method to pair off most fit candidates
        # maybe do this with some probability such that sometimes lesser
        # candidates are matched in order to introduce variety
        # into gene pool
        pass

    def _sort_population(self):
        # TODO: sort self.candidates so that most fit candidates
        # are in low indices
        pass

    def _mate(self, candidate1, candidate2, num_new=2):
        new_candidates = []
        for _ in range(num_new):
            # TODO: slice chromosome randomly for each new
            # candidate and combine.
            # TODO: introduce mutation from what was spliced
            # together
            new_candidates.append(None)
        return new_candidates
    
    def drop_lowest(self, num_to_drop):
        # TODO: sort population again then kill off the weakest
        pass