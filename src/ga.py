import Population
import ga_utils
import os
from datetime import datetime

NUM_GENS = 10
POPSIZE = 100
NUM_BRED_PER_GEN = 50

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

    print(f"Calculating landmarks on reference image")
    ref_landmarks = ga_utils.get_ref_img_landmarks()
    
    print(f"Initializing population")
    abs_init_path = os.mkdir(os.path.join(abs_run_name, f"init_pop"))
    pop = Population.Population(POPSIZE)
    for i, candidate in enumerate(pop.new_candidates):
        score, scored_image = ga_utils.get_score(candidate.chromosome, ref_landmarks)
        cv2.imwrite(os.path.join(abs_init_path, f"candidate{i}.jpg"), scored_image)
        candidate.set_score(score, scored_image)
    pop.merge_and_drop_candidates()

    print(f"Beginning evolution")
    for gen_num in range(1, NUM_GENS + 1):
        print(f"Now evolving generation {gen_num}")
        abs_this_gen_path = os.mkdir(os.path.join(abs_run_name, f"gen_{gen_num}"))
        pop.breed_new(NUM_BRED_PER_GEN)
        for i, candidate in enumerate(pop.new_candidates):
            score, scored_image = ga_utils.get_score(candidate.chromosome, ref_landmarks)
            cv2.imwrite(os.path.join(abs_this_gen_path, f"candidate{i}.jpg"), scored_image)
            candidate.set_score(score, scored_image)
        pop.merge_and_drop_candidates(NUM_BRED_PER_GEN)
        this_gen_best_img = pop.get_best_candidate().get_image()
        cv2.imwrite(os.path.join(abs_this_gen_path, "best_img_gen{gen_num}.jpg"), this_gen_best_img)

    print("Done!  Getting best candidate")
    winning_candidate = pop.get_best_candidate()
    print(winning_candidate)
    cv2.imwrite(os.path.join(abs_run_name, "best_run_img.jpg"))

    print("Displaying best candidate on robot")
    ga_utils.actuate_chromosome(winning_candidate.chromosome)

    ga_utils.CAP.release()
    ga_utils.CONTROLLER.close()

    print("Adding expression to expressions list")
    ga_utils.add_exp(expression_name, winning_candidate.chromosome)
