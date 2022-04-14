from typing import List
from itertools import permutations, combinations
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Measure():
    def __init__(self, majority: int, weights: List[int], labels = None):
        """majority: amount required for coalition to pass
           weights: amount of votes for each voter P 
        """
        self.majority = majority 
        if labels:
            self.weights = {f"{l}": w for l, w in zip(labels, weights)}
        else: 
            self.weights = {f"P{i+1}": w for i, w in enumerate(weights)}

    def get_perms(self):
        """gets all (comprehensive) permutations of weights"""
        return list(permutations(self.weights))

    def get_combos(self):
        """gets all (partial) combinations of weights"""
        def flatten(lls):
            flattened = []
            for e in lls:
                if type(e) is list:
                    for item in e:
                        flattened.append(item)
                else:
                    flattened.append(e)
            return flattened

        combos = []
        for r in range(len(self.weights) + 1):
            combos.append(list(combinations(self.weights, r)))
        return flatten(list(combos))

    def sum_seq(self, seq):
        """given a tuple of the form ('P1', 'P2', 'P3') return the sum of the associated weights"""

        return sum(self.weights[p] for p in seq)
    

    def count_pivotal(self):
        """Shapley-Shubrik"""
        res = {k: 0 for k in self.weights }

        # for each permutation
        perms = self.get_perms()
        for perm in perms:
            total = 0
            # start summing the weights of the sequenced coalition
            for w in perm:
                total += self.weights[w]
                # once a majority has been reached
                if total >= self.majority:
                    res[w] += 1
                    break # stop counting the "dummy" voters
        
        n_perms = len(perms)
        for k, v in res.items():
            if n_perms > 0:
                res[k] = round(float(v)/n_perms, 4)
            else: 
                res[k] = 0

        return res

    def count_critical(self):
        """Banzhaf"""
        # start by listing all coalitions, then eliminating non winning coalitions
        combos = self.get_combos()
        winning_combos = [ combo for combo in combos if self.sum_seq(combo) >= self.majority ]
        critical_counts = { k: 0 for k in self.weights }
        
        # for each passing measure
        for wp in winning_combos:
            total = self.sum_seq(wp)

            # iterate over each voter 
            for p in wp:
                # if their cast vote is necessary for the measure to pass, they are considered critical
                if total - self.weights[p] < self.majority:
                    critical_counts[p] += 1
        
        n_critical = sum([critical_counts[k] for k in critical_counts])
        for k, v in critical_counts.items():
            if n_critical > 0:
                critical_counts[k] = round(float(v)/n_critical, 4)
            else: 
                critical_counts[k] = 0

        return critical_counts

    def __repr__(self):
        dict_str = ""
        for k, v in self.weights.items():
            dict_str += f"({k}, {v}), "
        dict_str = dict_str[:-2]

        res = f"[{self.majority}: {dict_str}".replace("[", "").replace("]", "")
        res = f"[{res}]"
        res += f"\nShapley-Shubrik:\t{self.count_pivotal()}"
        res += f"\nBanzhaf:\t\t{self.count_critical()}\n"
        return res

## Tests

C1 = Measure(6, [4, 3, 2], ["P1", "P2", "P3"])
print(C1)

# print(crits, labels)
# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])
# ax.bar(crits, labels)
# plt.show()

weights = [35, 20, 15, 10, 10, 10]
agents = ["Jack", "Peter", "Chuck", "P3", "P4", "P5"]
i_am_not_a_control_freak_i_swear = Measure(51, weights, agents)
print(i_am_not_a_control_freak_i_swear)

fig, ax = plt.subplots()
crits = list(C1.count_pivotal().keys()) 
labels = list(C1.count_pivotal().values())
ax.bar(crits,labels)
ax.set_title("Shapley-Shubrik")
ax.set_yticks(np.arange(0, 1, .1))

# plt.show()

C2 = Measure(20, [7, 12, 3])
# print(C2)

C3 = Measure(8, [6, 4, 3, 2])
# print(C3)

C4 = Measure(8, [6, 3, 2])
# print(C4)
