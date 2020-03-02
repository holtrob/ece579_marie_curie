import Population
import ga_utils
import cv2
import os
from datetime import datetime
import matplotlib.pyplot as plt

NUM_GENS = 100
POPSIZE = 100
NUM_BRED_PER_GEN = 50

# TODO: make the next two lines inputs via argument parser
ref_img_path = "reference_images/happy.jpg"
expression_name = 'test'
# Get some information about the current datetime in order
# to create a new folder for this run
dt_str = datetime.now().strftime(format="%Y_%b_%d_%H_%M_%S")
rel_run_name = f"ga_{expression_name}_{dt_str}"
abs_run_name = os.path.join(os.getcwd(), rel_run_name)
os.mkdir(abs_run_name)
print(f"Calculating landmarks on reference image")
ref_landmarks = ga_utils.get_ref_img_landmarks(ref_img_path)
print(f"Initializing population")

best_scores = []

pop = Population.Population(POPSIZE)
for i, candidate in enumerate(pop.new_candidates):
    score, scored_image = ga_utils.get_score(candidate.chromosome, ref_landmarks)
    cv2.imwrite(os.path.join(abs_run_name, f"gen{0:04}candidate{i:04}.jpg"), scored_image)
    candidate.set_score(score, scored_image)
    print(f"Candidate {i}: {score}")
pop.merge_and_drop_candidates()

best_scores.append(pop.get_best_candidate().score)

print(f"Beginning evolution")
for gen_num in range(1, NUM_GENS + 1):
    print(f"Now evolving generation {gen_num}")
    pop.breed_new(NUM_BRED_PER_GEN)
    print(f"Now scoring {len(pop.new_candidates)} new candidates")
    for i, candidate in enumerate(pop.new_candidates):
        score, scored_image = ga_utils.get_score(candidate.chromosome, ref_landmarks)
        cv2.imwrite(os.path.join(abs_run_name, f"gen{gen_num:04}candidate{i:04}.jpg"), scored_image)
        candidate.set_score(score, scored_image)
    pop.merge_and_drop_candidates(NUM_BRED_PER_GEN)
    this_gen_best_img = pop.get_best_candidate().get_image()
    best_scores.append(pop.get_best_candidate().score)
    cv2.imwrite(os.path.join(abs_run_name, f"best_img_gen{gen_num:04}.jpg"), this_gen_best_img)

print("Done!  Getting best candidate")
winning_candidate = pop.get_best_candidate()
print(winning_candidate)
cv2.imwrite(os.path.join(abs_run_name, "best_run_img.jpg"), winning_candidate.get_image())
print("Displaying best candidate on robot")
ga_utils.actuate_chromosome(winning_candidate.chromosome)

# Scores over generations
print(f"Scores over gen's: {best_scores}")

plt.plot(best_scores)
plt.show()

ga_utils.CAP.release()
ga_utils.CONTROLLER.close()
print("Adding expression to expressions list")
#ga_utils.add_exp(expression_name, winning_candidate.chromosome)
