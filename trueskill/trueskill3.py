from player import Player
from team import Team
from itertools import permutations
import numpy as np

        
class Game():
    def __init__(self, players=None):
        """players is a list of n < 10, n is even floats"""
        if players is None or len(players) % 2 != 0:
            print("I reject your players and subsitute my own (even and fewer than 11)")
            self.players = []
            for i in range(10):
                self.players.append(Player())
        else:
            self.players = players

        self.teams = self.get_teams()

    def get_teams(self, optimize_std=False):
        """returns two teams with closest mean naively based on closest sum"""
        """TODO: optimize for min stddev too"""
        team_a, team_b = [], []

        if optimize_std:
            half = len(self.players)//2
            team_a = Team(self.players[:half], "Team A")
            team_b = Team(self.players[half:], "Team B")
            diff = abs(team_a.get_std_dev() - team_b.get_std_dev())

            for perm in list(permutations(self.players)):
                temp_team_a = Team(perm[:half], "Team A")
                temp_team_b = Team(perm[half:], "Team B")

                temp_diff = abs(temp_team_a.get_std_dev() - temp_team_b.get_std_dev())
                if temp_diff < diff:
                    diff = temp_diff
                    team_a = Team(perm[:half], "Team A")
                    team_b = Team(perm[half:], "Team B")
            
            return team_a, team_b 

        else:
            for i, p in enumerate(self.players):
                if i % 4 == 0 or i % 4 == 3:
                    team_a.append(p)
                else:
                    team_b.append(p)

        return Team(team_a, "Team A"), Team(team_b, "Team B")

    def __repr__(self):
        res = ""
        for t in self.teams:
            res += f"{t}\n" 
        
        return res

if __name__ == "__main__":
    p1 = Player({"int": 5, "dex": 3}, name="p1")
    p2 = Player({"int": 6, "dex": 6}, name="p2")

    p3 = Player({"int": 1, "dex": 1}, name="p3")
    p4 = Player({"int": 6, "dex": 10}, name="p4")
    
    print("input players")
    players = [p1, p2, p3, p4]
    for p in players:
        print(p)
    print()

    g = Game([p1, p2, p3, p4])
    print(g)

    print("optimizing for stddev")
    t1, t2 = g.get_teams(True)
    print(t1)
    print(t2)