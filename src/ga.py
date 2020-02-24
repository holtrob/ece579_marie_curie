import Population
import ga_utils
import os
from datetime import datetime

NUM_GENS = 10
POPSIZE = 100

if __name__ == "__main__":
    # TODO: make the next two lines inputs via argument parser
    ref_img_path = "whatever.jpg"
    expression_name = 'testing'

    # Get some information about the current datetime in order
    # to create a new folder for this run
    dt_str = datetime.now().strftime(format="%Y_%b_%d_%H_%M")
    rel_run_name = f"ga_{expression_name}_{dt_str}"
    abs_run_name = os.path.join(os.getcwd(), rel_run_name)
    os.mkdir(abs_run_name)

    ref_landmarks = ga_utils.get_ref_img_landmarks()

    pop = Population.Population(POPSIZE, ref_landmarks)

    for i in range(1, NUM_GENS + 1):
        print(f"Now evolving generation {i}")
        abs_this_gen_path = os.mkdir(os.path.join(abs_run_name, f"gen_{i}"))
        pop.breed_new(50)
        for i, candidate in enumerate(pop.new_candidates):
            score, scored_image = ga_utils.get_score(candidate.chromosome, ref_landmarks)
            cv2.imwrite(os.path.join(abs_this_gen_path, f"candidate{i}.jpg"), scored_image)
            candidate.set_score(score)
        pop.merge_and_drop_candidates(50)

    winning_candidate = pop.get_best_candidate()
    print(winning_candidate)

    ga_utils.actuate_chromosome(winning_candidate.chromosome)

    ga_utils.CAP.release()

    # TODO: Do stuff to save the winner's chromosome as an actual expression
    # This might require modifying it or adding in servo settings that were
    # not part of the chromosome (i.e. pupil positions which) cannot
    # be reflected in fitness function