import Population
import ga_utils

NUM_GENS = 10
POPSIZE = 100

if __name__ == "__main__":
    ref_img_path = "whatever.jpg"
    # TODO: create reference image using cv2
    img = None
    ref_landmarks = ga_utils.get_ref_img_landmarks(img)

    pop = Population.Population(POPSIZE, ref_landmarks)

    for i in range(1, NUM_GENS + 1):
        print(f"Now evolving generation {i}")
        pop.breed_new(50)
        for candidate in pop.candidates:
            score = ga_utils.get_score(candidate.chromosome, ref_landmarks)
            candidate.set_score(score)
        pop.drop_lowest(50)

    winning_candidate = pop.get_best_candidate()

    ga_utils.actuate_chromosome(winning_candidate.chromosome)

    # TODO: Do stuff to save the winner's chromosome as an actual expression
    # This might require modifying it or adding in servo settings that were
    # not part of the chromosome (i.e. pupil positions which) cannot
    # be reflected in fitness function