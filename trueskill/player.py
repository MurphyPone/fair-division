import numpy as np

class Player():
    """eventually players can have different skill sets, but for now, they're just numbers"""
    
    def __init__(self, stats=None, name=None):
        """stats is a dictionary of attributes and scores"""

        if stats is None:
            self.stats = {'skill': np.random.uniform()}
        else:
            self.stats = stats 

        self.name = name

    def get_skill(self):
        return np.mean([v for v in self.stats.values()])

    def __getitem__(self, key):
        """mean of the player's stat block"""
        return self.stats[key]

    def __lt__(self, other):
        """o better be another Player"""
        assert(isinstance(other, Player))

        return self.get_skill() < other.get_skill()

    def __add__(self, other):
        assert(isinstance(other, Player))
        return self.get_skill() + other.get_skill()

    def __repr__(self):
        fmt_skill = "{:.3f}".format(self.get_skill())
        if self.name:
            return f"{self.name}: {self.stats} -> {fmt_skill}"
        else:
            return f"{self.stats} -> {fmt_skill}"


if __name__ == "__main__":
    # run some tests

    p1 = Player({"int": 5, "dex": 3}, name="p1")
    p2 = Player({"int": 6, "dex": 6}, name="p2")

    assert(p1.get_skill() == 4)
    assert(p1 < p2)
    print(p1)

