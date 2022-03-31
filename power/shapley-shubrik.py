from typing import List
from collections import defaultdict
from itertools import permutations

class Coalition():
    def __init__(self, majority: int, weights: List[int]):
        """majority: amount required for coalition to pass
           weights: amount of votes for each voter P 
        """
        self.majority = majority 
        self.weights = {f"P{i+1}": w for i, w in enumerate(weights)}

    def get_perms(self):
        return list(permutations(self.weights))

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
                # once a majority has been reach
                if total >= self.majority:
                    res[w] += 1
                    break 
        
        n_perms = len(perms)
        res = {k: round(float(v)/n_perms, 4) for k, v in res.items()}
        return res

    def sum_perm(self, perm):
        """given a tuple of the form ('P1', 'P2', 'P3') return the sum of the association weights"""

        return sum(self.weights[p] for p in perm)


    def count_critical(self):
        """Banzhaf"""
        # start by listing all coalitions, then eliminating non winning coalitions
        perms = self.get_perms()
        winning_perms = [ perm for perm in perms if self.sum_perm(perm) > self.majority ]
        critical_counts = { k: 0 for k in self.weights }
        
        # for each passing coalition
        for wp in winning_perms:
            total = 0

            # iterate over each voter 
            for p in wp:
                # if their cast vote meets/beats the majority, break
                if total >= self.majority:
                    print()
                    break 

                total += self.weights[p]
                critical_counts[p] += 1
                print(p, total)
                
        return critical_counts


    def __repr__(self):
        dict_str = ""
        for k, v in self.weights.items():
            dict_str += f"({k}, {v}), "
        dict_str = dict_str[:-2]

        res = f"[{self.majority}: {dict_str}".replace("[", "").replace("]", "")
        return f"[{res}]"

C1 = Coalition(6, [4, 3, 2])
print(C1)
# print(C1.get_perms())
print(C1.count_pivotal())

C2 = Coalition(36, [20, 17, 15])
print(C2)
# print(C2.get_perms())
print(C2.count_pivotal())

C3 = Coalition(8, [6, 4, 3, 2])
print(C3)
# print(C3.get_perms())
print(C3.count_pivotal())

print()

C4 = Coalition(8, [6, 3, 2])
print(C4)
print(C4.count_critical())