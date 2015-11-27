"""
Implementation of an Agent navigation the world of geometrical shapes - problem number 3.
"""
import time
from utils import *
import random, copy
import matplotlib
from agents import *
from search import *
class shape():
    """
    A geometrical shape existing in the world, each shape is a tuple of coordinates that are connected
    The constructor call is something like:
        g = shape((1,2),(3,5),(2,7)))
    This creates a triangle with all three nodes connected to each other
    """
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def nodes_num(self):
        """
        Returns the total number of the nodes in the shape
        """
        return self.coordinates.__len__()

    def lines(self):
        """
        Returns all the lines of the shape, in the form of y = ax + b, the return is a tuple (a,b,(x1,x2))
        returns empty if only a point.
        """
        lines = []
        if self.nodes_num() < 2:
            return lines
        elif self.nodes_num() == 2:
            lines.extend(line(self.coordinates[0],self.coordinates[1]))
        else:
            for crd in range(self.nodes_num()):
                if crd == 0:
                    lines.append((line(self.coordinates[crd],self.coordinates[crd+1])))
                    lines.append((line(self.coordinates[crd],self.coordinates[-1])))
                elif crd < self.nodes_num() - 1:
                    lines.append((line(self.coordinates[crd],self.coordinates[crd+1])))
        lines.sort(key=lambda tup: tup[2][0])
        return lines


def line(A,B):
    """
    Returns the values of the straight line from A to B, if x values are the same then
    it is a vertical line and the values that are returned are (X,Null,(Y1,Y2))
    """
    if A[0] != B[0]:
        a = (A[1]-B[1])/(A[0]-B[0])
    else:
        if A[1] < B[1]:
            return tuple((A[0],None,(A[1],B[1])))
        else:
            return tuple((A[0],None,(B[1],A[1])))
    b = A[1]-a*A[0]
    if A[0] < B[0]:
        return tuple((a,b,(A[0],B[0])))
    else:
        return tuple((a,b,(B[0],A[0])))

def line_type(line):
    """
    False if vertical, True otherwise
    """
    try:
        int(line[1])
        return True
    except (TypeError, ValueError):
        return False

def crossing(A,B):
    if line_type(A)&line_type(B):
        int(A[1])&int(B[1])
        if(A[0]==B[0]):
            return ()
        x = (B[1]-A[1])/(A[0]-B[0])
        y = A[0]*x + A[1]
        if (x > A[2][0]) & (x < A[2][1]) & (x > B[2][0]) & (x < B[2][1]):
            return (x,y)
        else:
            return ()
    else:
        if line_type(A):
            x = B[0]
            y = A[0]*x + A[1]
            if (x > A[2][0]) & (x < A[2][1]) & (y > B[2][0]) & (y < B[2][1]):
                return (x,y)
            else:
                return ()
        elif line_type(B):
            x = A[0]
            y = B[0]*x+B[1]
            if (y > A[2][0]) & (y < A[2][1]) & (x > B[2][0]) & (x < B[2][1]):
                return (x,y)
            else:
                return ()
        else:
            return()



def crossing_world(A,World):
    """
    Returns the first crossing of a line in the with any of the shapes in the world
    """
    smallest = ()
    for shape in World.shapes:
        for line in shape.lines():
            cross = crossing(A,line)
            if cross != ():
                if smallest == ():
                    smallest = cross
                else:
                    if(line[2][0]<A[0]):
                        if cross[0] < smallest[0]:
                            smallest = cross
                    else:
                        return (smallest)
    return smallest


class td_world():
    """
    A geometrical graph world made of straight line shapes.

    """
    def __init__(self, shapes=None):
        self.shapes = shapes

    def add_shape(self,shape):
        self.shapes.append(shape)

    def point_lines(self,P):
        """
        Returns all the lines that are extending from a given point
        """
        l = []
        for s in self.shapes:
            for line in s.lines():
                if line_type(line):
                    P1 = (line[2][0],line[0]*line[2][0]+line[1])
                    P2 = (line[2][1],line[0]*line[2][1]+line[1])
                    if (P1 == P) | (P2==P):
                        l.append(line)
                else:
                    P1 = (line[0],line[2][0])
                    P2 = (line[0],line[2][1])
                    if (P1 == P) | (P2==P):
                        l.append(line)

        return l

    def world_lines(self):
        l = []
        for s in self.shapes:
            l.extend(s.lines())
        l.sort(key=lambda tup: tup[2][0])
        return l

    def world_points(self):
        p = []
        for s in self.shapes:
            p.extend(s.coordinates)
        return p


class nav_world(Problem):
    def __init__(self,world,initial,goal):
        self.world = world
        self.initial = tuple(initial)
        self.goal = tuple(goal)
    def h(self,state):
        h = ((state.state[0]-self.goal[0])**2+(state.state[1]-self.goal[1])**2)**0.5
        return h
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. the
        function used here, is the distance travelled
        """
        return ((state1[0]-state2[0])**2+(state1[1]-state2[1])**2)**0.5

    def actions(self,state):
        acts = []
        if state is not None:
            if crossing_world(line(state,self.goal),self.world):
                lpn = self.world.point_lines(state)
                if lpn == []:
                    for p in self.world.world_points():
                        if not crossing_world(line(state,p),self.world):
                            acts.append(p)
                else:
                    for p in self.world.world_points():
                        # All the world points that are not crossed
                        if not crossing_world(line(state,p),self.world):
                            if (line_type(lpn[0])) & (line_type(lpn[1])):
                                la = lpn[0][0]
                                lb = lpn[1][0]
                                if (line(state,p)[0]>= max(la,lb)) | (line(state,p)[0]<= min(la,lb)):
                                    acts.append(p)


                    #Add points on the shape that are connected to the point
                    for ln in lpn:
                        if line_type(ln):
                            if state[0] == ln[2][0]:
                                acts.append((ln[2][0],ln[0]*ln[2][0]+ln[1]))
                            else:
                                acts.append((ln[2][0],ln[0]*ln[2][0]+ln[1]))
                        else:
                            if state[1] == ln[2][0]:
                                acts.append((ln[0],ln[2][1]))
                            else:
                                acts.append((ln[0],ln[2][0]))

            else:
                acts.append(self.goal)
        else:
            state = self.initial
        return acts

    def result(self,state,action):
        return action


if __name__ == "__main__":
    A = shape(((1.0,3.0),(2.0,6.0),(3.0,3.0)))
    a = A.lines()
    print a
    B = shape(((2.0,7.0),(3.0,5.0),(4.0,7.0),(3.0,8.0)))
    b = B.lines()
    print b
    C = shape(((4.0,2.0),(6.0,2.0),(6.0,5.0),(4.0,5.0)))
    c = C.lines()
    D = shape(((7.0,1.0),(8.0,1.0),(8.0,3.0),(7.0,3.0)))
    E = shape((((5.0,8.0),(7.0,4.0),(8.0,5.0),(7.0,6.0),(7.0,7.0),(6.0,8.0))))
    print c
    d = td_world((A,B,C,E))
    print d.world_lines()
    LA = line((0.0,0.0),(10.0,10.0))
    LB = line((0.0,4.0),(3.0,0.0))
    print crossing_world(LA,d)
    print d.point_lines((2.0,7.0))
    print d.world_points()
    print "-"*100
    p = InstrumentedProblem(nav_world(d,(0,0),(10,10)))

    #t = astar_search(p)
    time1 = time.time()
    #t =uniform_cost_search(p)
    #t = recursive_best_first_search(p)
    t = depth_limited_search(p,3)
    time2 = time.time()
    print p
    print t.solution()
    #a = Agent(nav_world(d,(0,0),(10,10)))