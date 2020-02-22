"""
ECE 579 Intelligent Robotics II
Team 3 - Marie Curie Robot
R. Holt
D. Yakovlev
Population.py
"""
from Candidate import Candidate
import random

class Population:
    def __init__(self, popsize, landmarks):
        self.popsize = popsize
        self.candidates = []
        self.new_candidates = []
        self.ref_landmarks = landmarks
        for _ in range(popsize):
            self.new_candidates.append(Candidate.create_random())
        return
    
    def breed_new(self, num_to_breed, num_per_parents=2):
        num_parents = int(num_to_breed / num_per_parents)
        # TODO: get the mating pool
        # TODO: pair off the parents in pairs
        parent_pairs = [(None, None)]
        for parent1, parent2 in parent_pairs:
            self.new_candidates += self._mate(parent1, parent2, num_per_parents)
    
    def merge_and_drop_candidates(self, num_merged_dropped):
        self.candidates += self.new_candidates
        self._drop_worst(num_merged_dropped)
    
    def get_best_candidate(self):
        self._sort_population()
        return self.candidates[0]

    def _get_mating_pool(self, num_pairs):
        # TODO: implement method to pair off most fit candidates
        # maybe do this with some probability such that sometimes lesser
        # candidates are matched in order to introduce variety
        # into gene pool
        pass

    def _sort_population(self, high_better=False):
        """
        _sort_population Function to sort member candidates from the population.
        Puts the "best" candidates in low indices of returned list.

        :param high_better: indicates whether high candidate scores are better, defaults to False
        :type high_better: bool, optional
        :raises Exception: when not all Candidates have scores to sort by
        :return: list of candidates
        :rtype: list of instances of Candidate
        """     
        # If not all candidates have a score, then raise an error
        if not all([True if candidate.score else False for candidate in self.candidates]):
            raise Exception("Cannot sort population, not all candidates are scored")
            
        return sorted(self.candidates, key=lambda x: x.score, reverse=high_better)

    def _mate(self, candidate1, candidate2, num_new=2):
        """
        _mate Combine parents into a number of new child candidates.
        Contiguous sections of the individual parent chromosomes are selected for
        each child.  The parent for lower/upper indices of the child chromosome
        is randomized for each child.

        :param candidate1: First parent candidate
        :type candidate1: instance of Candidate
        :param candidate2: Second parent candidate
        :type candidate2: instance of Candidate
        :param num_new: number of children to generate from these parents, defaults to 2
        :type num_new: int, optional
        :return: Child Candidates
        :rtype: list of Candidates
        """
        chrom_len = len(candidate1.chromosome)
        parents = [candidate1, candidate2]
        new_candidates = []
        for _ in range(num_new):
            # Randomize the order of the parents
            random.shuffle(parents)

            # Determine how much to take from the parents
            # This can be improved by biasing the location in
            # favor of taking more genes from the more fit parent.
            slice_loc = random.randint(1, chrom_len - 1)

            # select from parents chromosomes
            new_cand = parents[0][:slice_loc] + parents[1][slice_loc:]

            # TODO: introduce mutation from what was spliced
            # together
            new_candidates.append(new_cand)
        return new_candidates
    
    def _drop_worst(self, num_to_drop):
        """
        drop_worst Removes the worst num_to_drop candidates from self.candidates
        using the self._sort_population function.

        :param num_to_drop: Quantity of candidates to remove from the population
        :type num_to_drop: int
        """
        self.candidates = self._sort_population()[:-num_to_drop]
        return
