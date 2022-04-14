from player import Player
import numpy as np

class Team():
    def __init__(self, players, name=""):
        """let the Game class do the driving in terms of guaranteeing small teams"""
        self.roster = sorted(players)
        self.name = name

    def get_cum_skill(self):
        """get the cumulative skill of the team"""
        return sum([p.get_skill() for p in self.roster])

    
    def get_skill(self):
        """get the average skill of the team"""
        return np.mean([p.get_skill() for p in self.roster])

    def get_std_dev(self):
        """get the standard deviation skill of the team"""
        return np.std([p.get_skill() for p in self.roster])


    def __lt__(self, other):
        """o better be another Player"""
        assert(isinstance(other, Team))

        return self.get_skill() < other.get_skill()
    
    def __repr__(self):

        fmt_sum = "{:.3f}".format(self.get_cum_skill())
        fmt_mean = "{:.3f}".format(self.get_skill())
        fmt_stddev = "{:.3f}".format(self.get_std_dev())

        fmt_roster = "\n"
        for p in self.roster:
            fmt_roster += f"\t{p}\n"

        
        return f"{self.name}: {fmt_roster} total = {fmt_sum}, μ = {fmt_mean}, σ = {fmt_stddev}"

if __name__ == "__main__":
    # run some tests

    p1 = Player({"int": 5, "dex": 3}, name="p1")
    p2 = Player({"int": 6, "dex": 6}, name="p2")

    p3 = Player({"int": 1, "dex": 1}, name="p3")
    p4 = Player({"int": 6, "dex": 10}, name="p4")

    t1 = Team([p1, p2], "Team 1")
    t2 = Team([p3, p4], "Team 2")
    print(t1)
    print(t2)
    assert(t2 < t1)

