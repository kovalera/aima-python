"""
Implementation of the 15 squares games by using all the different search algorithms
learned in Chapter 3
"""
import time
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

    def h2(self, state):
        """
        Inversed tiles heuristic
        """
        puzzle = state.state
        count = 0
        for i in puzzle:
            for j in puzzle[(puzzle.index(i)+1):]:
                if j > 0:
                    if j < i:
                        count = count + 1
        return count

    def h3(self,state):
        """
        Manhattan distance
        """
        s = 0
        r = list(state.state)
        g = list(self.goal)
        for i in r:
            s = s + abs(r.index(i)%self.n - g.index(i)%self.n)
            s = s + abs(r.index(i)/self.n - g.index(i)/self.n)
        return s

    def h4(self,state):
        """
        Manhattan + inversed distance heuristic
        so far the fastest heuristic but not the most efficient solution found
        """
        s = 0
        r = list(state.state)
        g = list(self.goal)
        for i in r:
            s = s + abs(r.index(i)%self.n - g.index(i)%self.n)
            s = s + abs(r.index(i)/self.n - g.index(i)/self.n)
        puzzle = state.state
        count = 0
        for i in puzzle:
            for j in puzzle[(puzzle.index(i)+1):]:
                if j > 0:
                    if j < i:
                        count = count + 1
        return s + count
    def h(self,state):
        """
        Nilsson's Sequence Score - my understanding of it -
        speed is roughly the same as the manhattan distance
        """
        s = 0
        t = 0
        r = list(state.state)
        g = list(self.goal)
        for i in r:
            s = s + abs(r.index(i)%self.n - g.index(i)%self.n)
            s = s + abs(r.index(i)/self.n - g.index(i)/self.n)
        for k in r:
            if (r.index(k) != 15):
                if (r[r.index(k)+1] != k + 1 ):
                    t = t + 2
        return (s + 3*t)

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
    Puzzle_8 = [8,1,3,\
                4,0,2,\
                7,6,5]
    """
    Puzzle_8 = [1,2,3,\
                4,5,6,\
                0,7,8]
    # Depth 29 - right now solved in 143 seconds
    # With mixed heuristic solved in 9 seconds depth 35

    Puzzle_15 = [1,0,10,6,\
                 5,7,3,4,\
                 9,15,2,11,\
                 13,14,8,12]
    """
    Puzzle_15 = [5,1,10,6,\
                 9,7,3,4,\
                 15,2,0,11,\
                 13,14,8,12]

    Puzzle_15 = [2,7,11,5,\
                 13,0,9,4,\
                 14,1,8,6,\
                 10,3,12,15]
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

    if check_solvable(Puzzle_15,4):
        t = search.astar_search(game_15(Puzzle_15,4))
    else:
        print "Puzzle is unsolvable, please change"

    """
    if check_solvable(Puzzle_15,4):
        p = search.InstrumentedProblem(game_15(Puzzle_15,4))

        #t = search.astar_search(p)
        time1 = time.time()
        t = search.astar_search(p)
        #t = search.recursive_best_first_search(p)
        time2 = time.time()
        print p
        #search.compare_searchers(problems = [game_15(Puzzle_8,3)],header=['Searcher', 'Puzzle 8'])
        print t.solution()
        print t.depth
        print "time taken is:"
        print time2 - time1
    else:
        print "Sorry the puzzle is not feasible"
    """
    count = 0
    # Count all the inversions in the puzzle
    puzzle = [15,14,13,12,\
              11,10,9,8,\
              7,6,5,4,\
              3,2,1,0]
    goal = [1,2,3,4,\
            5,6,7,8,\
            9,10,11,12,\
            13,14,15,0]
    for i in puzzle:
            for j in puzzle[(puzzle.index(i)+1):]:
                if j > 0:
                    if j < i:
                        count = count + 1

    s = 0
    r = puzzle
    g = goal
    for i in r:
        s = s + abs(r.index(i)%4 - g.index(i)%4)
        s = s + abs(r.index(i)/4 - g.index(i)/4)
    print s

    print count
    """