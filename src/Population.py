"""
ECE 579 Intelligent Robotics II
Team 3 - Marie Curie Robot
R. Holt
D. Yakovlev
Population.py
"""
from Candidate import Candidate
from ga_utils import num_children_gen, clip_chromosome_limits
import random
import numpy as np

class Population:
    def __init__(self, popsize):
        self.popsize = popsize
        self.candidates = []
        self.new_candidates = []
        for _ in range(popsize):
            self.new_candidates.append(Candidate.create_random())
        return
    
    def breed_new(self, num_to_breed, num_per_parents=2):
        """
        breed_new breeds num_to_breed candidates from the candidate
        pool using built in methods to define the mating pool and
        actually perform the mating.  num_per_parents represents how
        many of the total num_to_breed candidates should come from each
        pair of parents.  All new candidates are added to self.new_candidates.
        
        :param num_to_breed: total number of new candidates to breed
        :type num_to_breed: int
        :param num_per_parents: number of candidates to have each group
        of parents produce, defaults to 2
        :type num_per_parents: int, optional
        """
        print(f"Breeding {num_to_breed} candidates with {num_per_parents} per parents")
        q, r = divmod(num_to_breed, num_per_parents)
        num_pairs = q + int(r > 0)
        print(f"Need {num_pairs} pairs of parents")
        
        all_parents = self._get_mating_pool(num_pairs)
        parent_pairs = self._pair_off_parents(all_parents)

        for parent1, parent2, num in num_children_gen(parent_pairs, num_to_breed, num_per_parents):
            self.new_candidates += self._mate(parent1, parent2, num)
        print(self.new_candidates)
    
    def merge_and_drop_candidates(self, num_merged_dropped=None):
        """
        merge_and_drop_candidates concatenates the self.new_candidates with
        the previous self.candidates.  It then drops the worst num_merged_dropped
        candidates from the pool.
        
        :param num_merged_dropped: quantity of Candidates to remove from the pool
        :type num_merged_dropped: int
        """
        print(f"Merging {len(self.new_candidates)} into the previous population of {len(self.candidates)}")
        self.candidates += self.new_candidates
        self.new_candidates = []
        print(f"Now dropping {num_merged_dropped} candidates")
        self._drop_worst(num_merged_dropped)
    
    def get_best_candidate(self):
        """
        get_best_candidate simply returns the most fit candidate
        as deteremined based on the scores of all candidates in self.candidates.
        
        :return: most fit candidate
        :rtype: Candidate
        """
        self.candidates = self._sort_population()
        return self.candidates[0]
    
    def _pair_off_parents(self, parents):
        """
        _pair_off_parents Creates a list of lists where each
        sublist is a pair of two parents.  CUrrently this pairs
        the most fit parents together.
        
        :param parents: flat list of candidates which are the parents
        :type parents: list of Candidates
        :return: list of list of paired candidates
        :rtype: list of list of Candidates
        """
        # TODO: improve this to pair off parents in other statistical ways
        # zip together into a list pairs of parents sequentially
        return list(zip(parents[::2], parents[1::2]))

    def _get_mating_pool(self, num_pairs):
        """
        _get_mating_pool identifies the parents which should make up the
        entire mating pool based on the number of pairs of parents.
        Currently it only takes the most fit 2 * num_pairs candidates.
        
        :param num_pairs: Quantity of pairs of parents
        :type num_pairs: integer
        :return: candidates which represent the mating pool
        :rtype: list of Candidates
        """
        # TODO: Improve this to select candidates with some probability
        # such that sometimes lesser fit candidates are matched in
        # order to introduce variety into gene pool
        self._sort_population()
        # This only returns the top scoring candidates
        return self.candidates[:2 * num_pairs]

    def _sort_population(self, high_score_is_better=False):
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
            
        return sorted(self.candidates, key=lambda x: x.score, reverse=high_score_is_better)

    def _mate(self, candidate1, candidate2, num_new=2, mut_std=50):
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
        :param mut_std: Standard deviation of the individual gene mutations in quarter microseconds
        :type mut_std: int
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

            # Crossover the parent's chromosomes
            new_cand = Candidate(parents[0].chromosome[:slice_loc] + parents[1].chromosome[slice_loc:])

            # Apply variation to each gene in the chromosome.
            # The mutation is based on a multivariate normal distribution with means centered
            # on the inherited genes via crossover.  The variance controls how severe the mutation is
            # a standard deviation (mut_std) indicates that ~68% of the time, the new gene will be within
            # 50 quarter microseconds of the inherited gene.
            new_cand.chromosome = list(np.random.normal(loc=new_cand.chromosome, scale=mut_std).astype('int'))
            
            # Saturate the genes at their allowed limits to ensure that the hardware is not damaged.
            new_cand.chromosome = clip_chromosome_limits(new_cand.chromosome)

            new_candidates.append(new_cand)
        return new_candidates
    
    def _drop_worst(self, num_to_drop=None):
        """
        drop_worst Removes the worst num_to_drop candidates from self.candidates
        using the self._sort_population function.

        :param num_to_drop: Quantity of candidates to remove from the population
        :type num_to_drop: int
        """
        if not num_to_drop:
            return
        else:
            self.candidates = self._sort_population()[:-num_to_drop]
        return

if __name__ == "__main__":
    pop = Population(100)
    for cand in pop.new_candidates:
        cand.set_score(random.random())
        print(cand)
    pop.merge_and_drop_candidates()

    print("Finding best...")
    best = pop.get_best_candidate()
    print(best)

    print("Testing mating...")
    pop._mate(pop.candidates[0], pop.candidates[1])
