import random
import itertools
from collections import Counter

N = 15        # initial population size
epochs = 10   # game limit

# TODO move this to a class
MODEST  = 1.0/3  # 1/3 
FAIR    = 1.0/2  # 1/2 
GREEDY  = 2.0/3  # 2/3

AGENTS = [MODEST, FAIR, GREEDY]

population = [random.choice(AGENTS) for i in range(N)]
counter = Counter(population)
print(f"Initial distribution: {counter}, len(population): {len(population)}")

def get_pairs(P):
    """Given a population P of even length, returns a random combination of pairs of individuals"""
    # TODO pair generation could be moved to a util

    # don't want to randomize in place with shuffle
    randomized = sorted(P, key = lambda k: random.random())
    pairs = zip(randomized[::2], randomized[1::2])
    return list(pairs)


# TODO move this to a class to be abstracted
def succeeds(agent_1, agent_2):
    """given two agents, determines whether or not their matching satisfies both preferences"""
    return agent_1 + agent_2 == 1.0


# for every time step
# TODO doesn't make sense for there to be odd numbered populations at any step 
def train(epochs=epochs):
    """runs the generic training algorithm for a set of agent"""
    # TODO plot the data, and plot a bar graph of highest population over time

    for t in range(epochs):

        # generate all possible combination
        pairs = get_pairs(population)

        # pairings happen "simultaneously"
        for pair in pairs:
            agent_1, agent_2 = pair
            
            # if they succeed, reproduce
            if succeeds(agent_1, agent_2):
                population.append(agent_1)
                population.append(agent_2)
        
        if t % 10 == 0:
            print(f"t: {t}\tN: {len(population)}")

    print(f"t: {epochs} (final)\tN: {len(population)}")
    print(f"len(pairs): {len(pairs)}")
    counter = Counter(population)
    print(f"Final distribution: {counter}")


train()





