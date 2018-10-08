from walker_base import WalkerBase
import numpy as np
from priorityQueue import PriorityQueue
import maze_constants


OPENLIST_COLOR = 'green'
FOUND_COLOR = 'red'
CLOSEDLIST_COLOR = 'light blue'
TEMPORARILYDISCARDED_COLOR = 'grey'
##Notes
#  2 lists: an open list containing the cells to explore and a closed list containing the processed cells.
# start: starting point in open list and nothing in the processed list

class Astar(WalkerBase):

    def __init__(self, maze):
        #super already sets the start as the current cell
        super(Astar, self).__init__(maze, maze.start())
        self.strategy = "Euclidean" #make it possible to choose an option which heuristic can be used
        #current position not necessary, stored in walker
        #open list containing all cells to explore
        self.open = PriorityQueue()
        self.closed = dict()# node:parent
        self.g = 10 #total costs the agent took so far
        self.last = None
        self.closed[self._cell] = None

    def heuristic(self,cell):
        '''

        :param currentPoint:
        :return: the distance (aka the costs) from the current point to reach the goal based on the current
                 heuristic
        '''
        return np.sqrt(np.square(maze_constants.XCELLS - cell._xLoc)+np.square(maze_constants.YCELLS - cell._yLoc))

    #Function tracking back to the last decision point, recursive?
    def backToDecisionPoint(self,cell):
        #paint the current cell which will be temporarily discarded
        self.paint(self._cell,TEMPORARILYDISCARDED_COLOR)
        self.last = self._cell
        self._cell = cell


    def step(self):
        if self._cell is self._maze.start():
            paths = self._cell.get_paths(last=self.last) #self._cell.parent where we came from
            for i in paths:
                costs = self.heuristic(self._cell) + self.g
                self.open.put([i,self._cell,0,self.g],costs)
                self.paint(i,OPENLIST_COLOR)
                self.last = self._cell

        if self._cell is self._maze.finish():
            road = []
            tmp = self._cell
            i = 0
            while not (tmp._yLoc == 0 and tmp._xLoc == 0):
                road.append(tmp)
                tmp = self.closed[tmp]
                i+=1
            road = road[::-1]

            for i in road:
                self.paint(i, FOUND_COLOR)

            self._isDone = True
            return

        #what are the possible steps from here?
        paths = self._cell.get_paths(last=self.last)

        #as long as there are cells in the open list,
        #  get the one with the lowest costs
        next = self.open.get()
        while next[0] in self.closed.keys():
            next = self.open.get()

        #continue the walk from where we are right now
        if next[1] == self._cell:
            self.paint(next[0],CLOSEDLIST_COLOR)
            self.closed[next[0]] = self._cell
            self._cell = next[0]
            self.g += 10

        #is the next cell an adjacent cell of the current cell?
        elif not next[0] in paths:
            #discard the current position
            self.paint(self._cell,TEMPORARILYDISCARDED_COLOR)
            self._cell = next[0]
            self.last = next[1]
            self.g = next[2]
            self.closed[self._cell] = self.last
            self.paint(self.last,CLOSEDLIST_COLOR)
            self.paint(self._cell,CLOSEDLIST_COLOR)

        #Append the open list for the current position
        newPaths = self._cell.get_paths(last=self.last)
        if len(newPaths) > 0:
            for i in newPaths:
                if not i in self.closed:
                    self.paint(i,OPENLIST_COLOR)
                    f = self.heuristic(i) + self.g
                    self.open.put([i,self._cell,self.g],f)
        if len(newPaths) == 0 and self.open.empty():
            print("This is not suppossed to happen, please start new")













