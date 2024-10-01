class Node:
    def __init__(self, state: tuple[int], parent=None, cost=None) -> None:
        self.state = state
        self.parent: Node = parent
        self.cost = cost


class StackFrontier(list):
    def __init__(self) -> None:
        self.frontier = []

    def add(self, node: Node):
        self.frontier.append(node)

    def remove(self) -> Node:
        if self.isempty():
            raise Exception("can't remove - frontier is empty!")

        return self.frontier.pop()

    def isempty(self) -> bool:
        return len(self.frontier) == 0


class QueueFrontier(StackFrontier):
    def remove(self) -> Node:
        if self.isempty():
            raise Exception("can't remove - frontier is empty!")

        first = self.frontier[0]
        self.frontier = self.frontier[1:]
        return first


class Maze:
    def __init__(self, maze: str) -> None:
        # Check maze has start and goal
        if maze.count("S") != 1:
            raise Exception("maze must have exactly one start point")
        if maze.count("G") != 1:
            raise Exception("maze must have exactly one goal")

        # Remove empty new lines
        mazelines = maze.splitlines()
        mazelines = mazelines[1 : len(mazelines)]

        # Get height / width
        self.height = len(mazelines)
        self.width = len(mazelines[0])

        # Keep track of walls
        self.walls: list[list[bool]] = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if mazelines[i][j] == "S":
                    self.start = (i, j)
                    row.append(False)
                elif mazelines[i][j] == "G":
                    self.goal = (i, j)
                    row.append(False)
                elif mazelines[i][j] == " ":
                    row.append(False)
                else:
                    row.append(True)
            self.walls.append(row)

        self.solution = None
        self.pathcost = None
        self.visited = set()

    def print(self):
        prettymaze = []

        for i, row in enumerate(self.walls):
            mapped = []
            for j, col in enumerate(row):
                if col:
                    mapped.append("█")
                else:
                    if (i, j) == self.start:
                        mapped.append("S")
                    elif (i, j) == self.goal:
                        mapped.append("G")
                    else:
                        mapped.append(" ")
            prettymaze.append(mapped)

        if self.solution is not None:
            for x, y in self.solution:
                if prettymaze[x][y] != "S" and prettymaze[x][y] != "G":
                    prettymaze[x][y] = "*"

        for prettyrow in prettymaze:
            print("".join(prettyrow))

        if self.pathcost is not None:
            print("Cost:", self.pathcost)

        print("Total explored:", len(self.visited))

    def getneighbours(self, cell: Node):
        x, y = cell.state[0], cell.state[1]

        neighbours = []

        # up
        if x - 1 >= 0 and self.walls[x - 1][y] == False:
            neighbours.append((x - 1, y))
        # down
        if x + 1 < len(self.walls) and self.walls[x + 1][y] == False:
            neighbours.append((x + 1, y))
        # left
        if y - 1 >= 0 and self.walls[x][y - 1] == False:
            neighbours.append((x, y - 1))
        # right
        if y + 1 < len(self.walls[0]) and self.walls[x][y + 1] == False:
            neighbours.append((x, y + 1))

        return neighbours

    def solve(self) -> Node | None:
        frontier = StackFrontier()

        startnode = Node(state=self.start, cost=0)
        goalnode = None
        frontier.add(startnode)

        while frontier.isempty() == False:
            # Remove a node from the frontier
            current = frontier.remove()
            self.visited.add(current.state)

            # If the node is the goal, set solution found
            if current.state == self.goal:
                goalnode = current
                break

            neighbours = self.getneighbours(current)
            for n in neighbours:
                if n not in self.visited:
                    frontier.add(Node(state=n, parent=current, cost=current.cost + 1))

        if goalnode is None:
            return

        self.pathcost = goalnode.cost
        self.solution = []
        while current:
            self.solution.append(current.state)
            current = current.parent
        self.solution.reverse()


maze1 = """
 # # ###  #G
 # #   # ## 
   # #   ## 
# ## # # ## 
#    # #    
### ## #####
S   ##      
"""

m = Maze(maze1)
m.solve()
m.print()

maze2 = """
###                 #########
#   ###################   # #
# ####                # # # #
# ################### # # # #
#                     # # # #
##################### # # # #
#   ##                # # # #
# # ## ### ## ######### # # #
# #    #   ##G#         # # #
# # ## ################ # # #
### ##             #### # # #
### ############## ## # # # #
###             ##    # # # #
###### ######## ####### # # #
###### ####             #   #
S      ######################
"""

m = Maze(maze2)
m.solve()
m.print()

maze3 = """
##    #
## ## #
#G #  #
# ## ##
     ##
S######
"""

m = Maze(maze3)
m.solve()
m.print()
