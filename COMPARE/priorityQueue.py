import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        #returns smallest cost element, and just the element and not the cost, since this was
        #only a heuristic
        return heapq.heappop(self.elements)[1]
