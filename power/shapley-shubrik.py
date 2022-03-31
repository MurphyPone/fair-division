from typing import List
from itertools import permutations, combinations
import matplotlib.pyplot as plt


class Coalition():
    def __init__(self, majority: int, weights: List[int]):
        """majority: amount required for coalition to pass
           weights: amount of votes for each voter P 
        """
        self.majority = majority 
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

    def sum_perm(self, perm):
        """given a tuple of the form ('P1', 'P2', 'P3') return the sum of the association weights"""

        return sum(self.weights[p] for p in perm)
    

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
        for k, v in res.items():
            if n_perms > 0:
                res[k] = round(float(v)/n_perms, 4)
            else: 
                res[k] = 0
        # res = {k: round(float(v)/n_perms, 4) for k, v in res.items()}
        return res

    def count_critical(self):
        """Banzhaf"""
        # start by listing all coalitions, then eliminating non winning coalitions
        combos = self.get_combos()
        winning_combos = [ combo for combo in combos if self.sum_perm(combo) >= self.majority ]
        critical_counts = { k: 0 for k in self.weights }
        
        # for each passing coalition
        for wp in winning_combos:
            total = self.sum_perm(wp)

            # iterate over each voter 
            for p in wp:
                # if their cast vote meets/beats the majority, break
                if total - self.weights[p] < self.majority:
                    critical_counts[p] += 1
                # print(p, total)
        
        n_critical = sum([critical_counts[k] for k in critical_counts])
        # critical_counts = {k: round(float(v)/n_critical, 4) for k, v in critical_counts.items()}
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

C1 = Coalition(6, [4, 3, 2])
print(C1)

C2 = Coalition(36, [20, 17, 15])
print(C2)

C3 = Coalition(8, [6, 4, 3, 2])
print(C3)

C4 = Coalition(8, [6, 3, 2])
print(C4)

# make an EC map by weight
# TODO: modify the constructor to accept labels
C5 = Coalition(270, [55, 38, 16])
print(C5)


fig, (ax1, ax2) = plt.subplots(1, 2)
labels, weights = C5.count_critical().keys(), C5.count_critical().values()
ax1.pie(weights, labels=labels, autopct='%1.1f%%')
ax1.set_title("Shapley-Shubrik")

labels, weights = C5.count_pivotal().keys(), C5.count_pivotal().values()
ax2.pie(weights, labels=labels, autopct='%1.1f%%')
ax2.set_title("Banzhaf")

plt.show()