"""
Implementation of an Agent navigation the world of geometrical shapes - problem number 3.
"""
import time
from utils import *
import random, copy
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
    if line[1] == None:
        return False
    return True

def crossing(A,B):
    try:
        int(A[1])&int(B[1])
        if(A[0]==B[0]):
            return ()
        x = (B[1]-A[1])/(A[0]-B[0])
        y = A[0]*x + A[1]
        if x > A[2][0] & x < A[2][1] & x > B[2][0] & x < B[2][1]:
            return (x,y)
        else:
            return ()
    except (TypeError, ValueError):
        return ()

def crossing_world(A,World):
    """
    Returns the first crossing of a line in the with any of the shapes in the world
    """
    for shape in World.shapes:
        for line in shape.lines():
            print crossing(A,line)

class td_world():
    """
    A geometrical graph world made of straight line shapes.

    """
    def __init__(self, shapes=None):
        self.shapes = shapes

    def add_shape(self,shape):
        self.shapes.append(shape)

    def world_lines(self):
        l = []
        for s in self.shapes:
            l.extend(s.lines())
        l.sort(key=lambda tup: tup[2][0])
        return l

class nav_world(Problem):
    def __init__(self,world,initial,goal):
        self.world = world
        self.initial = tuple(initial)
        self.goal = tuple(goal)

    def actions(self,state):
        print 1


if __name__ == "__main__":
    A = shape(((1.0,3.0),(2.0,6.0),(3.0,3.0)))
    a = A.lines()
    print a
    B = shape(((2,7),(3,5),(4,7),(3,8)))
    b = B.lines()
    print b
    C = shape(((4,2),(6,2),(6,5),(4,5)))
    c = C.lines()
    print c
    d = td_world((A,B,C))
    print d.world_lines()
    LA = line((0.0,0.0),(2.0,2.0))
    LB = line((0.0,4.0),(3.0,0.0))
    print crossing_world(LA,d)