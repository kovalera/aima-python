"""
Implementation of the 15 squares games by using all the different search algorithms
learned in Chapter 3
"""
from utils import *
import random, copy
import agents, search

class game_15(search.Problem):
    def __init__(self, initial,n):
        self.initial = tuple(initial)
        self.n = n
        temp = range(1,n*n)
        temp.extend([0])
        #temp = [0]
        #temp.extend(range(1,n*n))
        self.goal= tuple(temp)

    def left(self,state):
        move = list(state)
        ind = move.index(0)
        move[ind] = move[ind+1]
        move[ind+1] = 0
        return tuple(move)

    def right(self, state):
        move = list(state)
        ind = move.index(0)
        move[ind] = move[ind-1]
        move[ind-1] = 0
        return tuple(move)

    def up(self, state):
        move = list(state)
        ind = move.index(0)
        move[ind] = move[ind+self.n]
        move[ind+self.n] = 0
        return tuple(move)

    def down(self, state):
        move = list(state)
        ind = move.index(0)
        move[ind] = move[ind-self.n]
        move[ind-self.n] = 0
        return tuple(move)

    def h(self,state):
        """
        Manhattan distance heuristic
        """
        s = 0
        r = list(state.state)
        g = list(self.goal)
        for i in r:
            s = s + abs(r.index(i)%self.n - g.index(i)%self.n)
            s = s + abs(r.index(i)/self.n - g.index(i)/self.n)
        return s

    def h1(self,state):
        """
        Displaced tiles heuristic
        """
        s = 0
        r = list(state.state)
        g = list(self.goal)
        for i in r:
            if r.index(i)==g.index(i):
                s = s + 1
        return self.n ** 2 - s

    def actions(self,state):
        acts = []
        if state is not None:
            if state.index(0) % self.n == 0:
                acts.extend([self.left(state)])
            elif state.index(0) % self.n == self.n - 1:
                acts.extend([self.right(state)])
            else:
                acts.extend([self.left(state)])
                acts.extend([self.right(state)])

            if state.index(0) < self.n:
                acts.extend([self.up(state)])
            elif state.index(0) >= self.n * (self.n - 1):
                acts.extend([self.down(state)])
            else:
                acts.extend([self.up(state)])
                acts.extend([self.down(state)])
        else:
            state = self.initial
        return acts

    def result(self,state,action):
        #state = list(action)
        #print state
        return action

def check_solvable(puzzle,n):
    count = 0
    # Count all the inversions in the puzzle
    for i in puzzle:
            for j in puzzle[(puzzle.index(i)+1):]:
                if j > 0:
                    if j < i:
                        count = count + 1

    if (n%2 == 1):
        if count % 2 == 0:
            return True
        return False
    else:
        if (n**2 - puzzle.index(0)/n)%2 == 0:
            if count % 2 == 0:
                return False
            return True
        else:
            if count % 2 == 0:
                return True
            return False

if __name__ == "__main__":
    """
    This is the test unit of the different searches, the following states were tested and work:
    3,6,0,1,5,2,4,7,8 - depth 12
    8,1,3,4,0,2,7,6,5 - depth 14
    1,10,3,6,\
    9,5,2,4,\
    0,7,15,8,\
    13,14,12,11 - depth 20 works with A* search
    """
    # The following 4 algorithms used are uninformed search algorithms
    #Works - long time, long solution - depth 12
    #a = search.uniform_cost_search(game_15([8,1,3,4,0,2,7,6,5],3))
    #Works - much longer time than UCS - depending on the limit, if limit 15 then depth 15 if 13 then 13 if 50 then 49
    #a = search.depth_limited_search(game_15([1,6,5,4,0,8,2,3,7],3),18)
    #Works - depth 13
    #a = search.iterative_deepening_search(game_15([3,1,5,0,6,8,4,2,7],3))
    #Works - fastest time depth also 13
    #a = search.breadth_first_search(game_15([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0],4))
    #a = search.astar_search(game_15([1,10,3,6,\
    #                                 5,7,2,4,\
    #                                 9,15,8,11,\
    #                                 13,14,0,12],4))
    #a = search.recursive_best_first_search(game_15([1,10,3,6,\
    #                                 5,7,2,4,\
    #                                 9,15,8,11,\
    #                                 13,14,0,12],4))
    """
    a = search.astar_search(game_15([9,5,2,4,\
                                     7,0,3,8,\
                                     10,6,13,11,\
                                     12,14,15,1],4))
    print a.solution()
    print a.depth
    """
    t = check_solvable([3,1,5,0,6,8,4,2,7],3)
    print t
    