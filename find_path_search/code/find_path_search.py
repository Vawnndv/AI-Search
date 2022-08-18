# 20127662 - Nguyễn Đình Văn
# 20127061 - Lưu Minh Phát
# 20127166 - Nguyễn Huy Hoàn
import numpy as np
from turtle import Screen, Turtle

TILE_SIZE = 20
CURSOR_SIZE = 20

class Pen(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('square')
        self.shapesize(TILE_SIZE / CURSOR_SIZE)
        self.pencolor('black')
        self.penup()
        self.speed('fastest')

class Draw():
    def __init__(self, level):
        self.maze_height, self.maze_width = len(level), len(level[0])
        self.level = level
        self.pen = Pen()

    def axis(self):
        for x in range(self.maze_height):
            screen_x = (x - self.maze_height / 2) * (TILE_SIZE)
            screen_y = (-1.5 - self.maze_width / 2) * (TILE_SIZE)
            self.pen.goto(screen_x, screen_y)
            self.pen.write(x,align='center')
        for y in range(self.maze_width):
            screen_x = (-1 - self.maze_height / 2) * TILE_SIZE
            screen_y = (y - 0.3 - self.maze_width / 2) * TILE_SIZE
            self.pen.goto(screen_x, screen_y)
            self.pen.write(y,align='center')

    def drawSquare(self, x, y):
        # calculate the screen x, y coordinates
        screen_x = (x - self.maze_height / 2) * TILE_SIZE
        screen_y = (y - self.maze_width / 2) * TILE_SIZE

        self.pen.goto(screen_x, screen_y)
        self.pen.stamp()

    def drawCharacter (self, pos, value):
        screen_x = (pos[0] - self.maze_height / 2) * TILE_SIZE
        screen_y = (pos[1] - 0.3 - self.maze_width / 2) * TILE_SIZE
        self.pen.goto(screen_x, screen_y)
        self.pen.write(value, align='center')

    def setup_maze(self):
        ''' Conversion from the list to the map in turtle. '''
        self.axis()
        for x in range(self.maze_height):
            for y in range(self.maze_width):
                # get the character at each x,y coordinate
                character = self.level[x][y]

                if character == 0:
                    self.pen.fillcolor('white')
                if character == -1:
                    self.pen.fillcolor('gray')
                
                self.drawSquare(x,y)

    def polygons(self, listPoints, index):
        for i in range(index):
            self.aPolygon(listPoints[i])

    def aPolygon(self, listpoint):
        numbersPoint = len(listpoint)
        list = listpoint
        list.append(listpoint[0])

        for i in range(0, numbersPoint):
            if (list[i] and list[i+ 1]) in listpoint:
                self.pen.fillcolor('red')
                self.drawSquare(list[i][0], list[i][1])
                self.drawSquare(list[i+1][0], list[i+1][1])
                self.level[list[i][0]][list[i][1]] = -1
                self.level[list[i + 1][0]][list[i + 1][1]] = -1

            if list[i][1] <= list[i + 1][1]:
                self.edgeOfPolygon(list[i], list[i+1])
            else:
                self.edgeOfPolygon(list[i+1], list[i])

    def edgeOfPolygon (self, left, right):

        self.pen.fillcolor('yellow')
        if right[0] == left[0]:                     #hang ngang
            for i in range(left[1] + 1, right[1]):
                self.level[right[0]][i] = -1
                self.drawSquare(right[0], i)
            return

        if right[1] == left[1]:                     #hang doc
            s = right[0]
            e = left[0]
            if right[0] > left[0]:
                s = left[0]
                e = right[0]
            for i in range(s + 1, e):
                self.level[i][right[1]] = -1
                self.drawSquare(i, right[1])
            return

        chenhlech = right[0] - left[0]
        
        if chenhlech >= 0:  #cheo len
            chenhlech = chenhlech - 1
            x = left[0]
            for i in range(left[1], right[1] + 1):
                if chenhlech >= 0:
                    x += 1
                chenhlech = chenhlech - 1
                if self.level[x][i] == -1:
                    continue
                self.level[x][i] = -1
                self.drawSquare(x, i)
            if not(x == right[0] and i == right[1]):
                self.edgeOfPolygon([x, i], right)
        
        else:   #cheo duoi
            chenhlech = chenhlech * -1
            x = left[0]
            for i in range(left[1], right[1] + 1):
                if chenhlech >= 0:
                    x -= 1
                chenhlech -= 1
                if self.level[x][i] == -1:
                    continue
                self.level[x][i] = -1
                self.drawSquare(x, i)
            if not(x == right[0] and i == right[1]): 
                self.edgeOfPolygon([x, i], right)

class Graph(Draw): 
    # Constructor
    def __init__(self, start, goal, maze):
        Draw.__init__(self, maze)
        self.start = start
        self.goal = goal
        self.costExpandNode = 0
        self.costPath = 0
        self.depth = 0
        self.setup_maze()

    def calcG (self, Pos1, Pos2, value):
        return abs(Pos1[0] - Pos2[0]) + abs(Pos1[1] - Pos2[1]) + 2 + value

    def calcH (self, Pos):
        return abs(self.goal[0] - Pos[0]) + abs(self.goal[1] - Pos[1])

    def posOfQueue(self, list, value):
        temp = []
        
        for i in range (0, len(list)):
            temp.append(list[i][1])
        for i in range(len(temp)):
            if temp[i] > value:
                return i - 1
        return 0  

    def drawStartGoal(self):
        self.pen.fillcolor('pink')
        self.drawSquare(self.start[0], self.start[1])
        self.drawCharacter(start, 'S')
        self.drawSquare(self.goal[0], self.goal[1])
        self.drawCharacter(goal, 'G')

    def printCost (self):
        
        E = "Cost of expanded node: " + str(self.costExpandNode)
        P = "Cost of final path: " + str(self.costPath)
        self.drawCharacter([self.maze_height / 2, self.maze_width + 3], E)
        self.drawCharacter([self.maze_height / 2, self.maze_width + 2], P)
        if self.depth != 0:
            D = "Depth: " + str(self.depth)
            self.drawCharacter([self.maze_height / 2, self.maze_width + 1], D)
        self.drawCharacter([self.maze_height / 2, self.maze_width + 9], "")
        self.pen.color('white')

    def BFS(self):
        visited = []
        
        # Queue for traversing the
        # graph in the BFS
        queue = [[self.start]]
        # Loop to traverse the graph
        # with the help of the queue
        while queue:
            path = queue.pop(0)
            node = path[-1]
        
            # Condition to check if the
            # current node is not visited
            if node not in visited:
                self.costExpandNode += 1
                self.pen.fillcolor('blue')
                self.drawSquare(node[0], node[1])
                neighbours = []
                if self.level[node[0] + 1][node[1]] != -1:      # Up
                    neighbours.append([node[0] + 1, node[1]])
                if self.level[node[0]][node[1] + 1] != -1:      # Right    
                    neighbours.append([node[0], node[1] + 1])   
                if self.level[node[0] - 1][node[1]] != -1:      # Down
                    neighbours.append([node[0] - 1, node[1]])
                if self.level[node[0]][node[1] - 1] != -1:      # Left
                    neighbours.append([node[0], node[1] - 1])
                if len(neighbours) == 0:                        # don't have neighbours
                    return
                # Condition to check if the
                # current node is goal
                if node == self.goal:
                    self.pen.fillcolor('green')
                    for i in path:
                        self.drawSquare(i[0], i[1])
                    self.drawStartGoal()
                    self.costPath = len(path)
                    return

                # Loop to iterate over the
                # neighbours of the node
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                visited.append(node)
        return

    def UCS(self):
        visited = []
        
        # Queue for traversing the
        # graph in the BFS
        queue = [[[self.start, 0]]]
        # Loop to traverse the graph
        # with the help of the queue
        while queue:
            path = queue.pop(0)
            node = path[-1][0]
            
            neighbours = []
            # Condition to check if the
            # current node is not visited
            if node not in visited:
                self.pen.fillcolor('blue')
                self.costExpandNode += 1
                self.drawSquare(node[0], node[1])
                if self.level[node[0] + 1][node[1]] != -1:      # Up
                    neighbours.insert(self.posOfQueue(neighbours, self.calcG(node, [node[0] + 1, node[1]], path[-1][1])), 
                        ([[node[0] + 1, node[1]], self.calcG(node, [node[0] + 1, node[1]], path[-1][1])]))                    
  
                if self.level[node[0]][node[1] + 1] != -1:      # Right    
                    neighbours.insert(self.posOfQueue(neighbours, self.calcG(node, [node[0], node[1] + 1], path[-1][1])), 
                        ([[node[0], node[1] + 1], self.calcG(node, [node[0], node[1] + 1], path[-1][1])]))   

                if self.level[node[0] - 1][node[1]] != -1:      # Down
                    neighbours.insert(self.posOfQueue(neighbours, self.calcG(node, [node[0] - 1, node[1]], path[-1][1])), 
                        ([[node[0] - 1, node[1]], self.calcG(node, [node[0] - 1, node[1]], path[-1][1])]))

                if self.level[node[0]][node[1] - 1] != -1:      # Left
                    neighbours.insert(self.posOfQueue(neighbours, self.calcG(node, [node[0], node[1] - 1], path[-1][1])), 
                        ([[node[0], node[1] - 1], self.calcG(node, [node[0], node[1] - 1], path[-1][1])]))

                # Condition to check if the
                # current node is goal
                if node == self.goal:
                    self.pen.fillcolor('green')
                    for i in path:
                        self.drawSquare(i[0][0], i[0][1])
                    self.drawStartGoal()
                    self.costPath = len(path)
                    return

                if len(neighbours) == 0:                        # don't have neighbours
                    return
                # Loop to iterate over the
                # neighbours of the node
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                visited.append(node)
        return    

    def GBFS(self):
        visited = []
        
        # Queue for traversing the
        # graph in the BFS
        queue = [[[self.start, self.calcH(self.start)]]]
        # Loop to traverse the graph
        # with the help of the queue
        while queue:
            path = queue.pop(0)
            node = path[-1][0]

            neighbours = []
            # Condition to check if the
            # current node is not visited
            if node not in visited:
                self.pen.fillcolor('blue')
                self.costExpandNode += 1
                self.drawSquare(node[0], node[1])
                if self.level[node[0] + 1][node[1]] != -1:      # Up
                    neighbours.insert(self.posOfQueue(neighbours, self.calcH([node[0] + 1, node[1]])), 
                        ([[node[0] + 1, node[1]], self.calcH([node[0] + 1, node[1]])]))                    
  
                if self.level[node[0]][node[1] + 1] != -1:      # Right    
                    neighbours.insert(self.posOfQueue(neighbours, self.calcH([node[0], node[1] + 1])), 
                        ([[node[0], node[1] + 1], self.calcH([node[0], node[1] + 1])]))   

                if self.level[node[0] - 1][node[1]] != -1:      # Down
                    neighbours.insert(self.posOfQueue(neighbours, self.calcH([node[0] - 1, node[1]])), 
                        ([[node[0] - 1, node[1]], self.calcH([node[0] - 1, node[1]])]))

                if self.level[node[0]][node[1] - 1] != -1:      # Left
                    neighbours.insert(self.posOfQueue(neighbours, self.calcH([node[0], node[1] - 1])), 
                        ([[node[0], node[1] - 1], self.calcH([node[0], node[1] - 1])]))

                # Condition to check if the
                # current node is goal
                if node == self.goal:
                    self.pen.fillcolor('green')
                    for i in path:
                        self.drawSquare(i[0][0], i[0][1])
                    self.drawStartGoal()
                    self.costPath = len(path)
                    return

                if len(neighbours) == 0: 
                    return
                # Loop to iterate over the
                # neighbours of the node
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                visited.append(node)
        return
    
    def AStar(self):
        visited = []
        
        # Queue for traversing the
        # graph in the BFS
        queue = [[[self.start, self.calcH(self.start)]]]
        # Loop to traverse the graph
        # with the help of the queue
        while queue:
            path = queue.pop(0)
            node = path[-1][0]
            # Condition to check if the
            # current node is goal
            if node == self.goal:
                self.pen.fillcolor('green')
                for i in path:
                    self.drawSquare(i[0][0], i[0][1])
                self.drawStartGoal()
                self.costPath = len(path)
                return
            #node = node[0]
            neighbours = []
            # Condition to check if the
            # current node is not visited
            if node not in visited:
                self.pen.fillcolor('blue')
                self.costExpandNode += 1
                self.drawSquare(node[0], node[1])
                if self.level[node[0] + 1][node[1]] != -1:      # Up
                    neighbours.insert(self.posOfQueue(neighbours, self.calcG(node, [node[0] + 1, node[1]], path[-1][1]) + self.calcH([node[0] + 1, node[1]])), 
                        ([[node[0] + 1, node[1]], self.calcG(node, [node[0] + 1, node[1]], path[-1][1]) + self.calcH([node[0] + 1, node[1]])]))                    
  
                if self.level[node[0]][node[1] + 1] != -1:      # Right    
                    neighbours.insert(self.posOfQueue(neighbours, self.calcG(node, [node[0], node[1] + 1], path[-1][1]) + self.calcH([node[0], node[1] + 1])), 
                        ([[node[0], node[1] + 1], self.calcG(node, [node[0], node[1] + 1], path[-1][1]) + self.calcH([node[0], node[1] + 1])]))   

                if self.level[node[0] - 1][node[1]] != -1:      # Down
                    neighbours.insert(self.posOfQueue(neighbours, self.calcG(node, [node[0] - 1, node[1]], path[-1][1]) + self.calcH([node[0] - 1, node[1]])), 
                        ([[node[0] - 1, node[1]], self.calcG(node, [node[0] - 1, node[1]], path[-1][1]) + self.calcH([node[0] - 1, node[1]])]))

                if self.level[node[0]][node[1] - 1] != -1:      # Left
                    neighbours.insert(self.posOfQueue(neighbours, self.calcG(node, [node[0], node[1] - 1], path[-1][1]) + self.calcH([node[0], node[1] - 1])), 
                        ([[node[0], node[1] - 1], self.calcG(node, [node[0], node[1] - 1], path[-1][1]) + self.calcH([node[0], node[1] - 1])]))

                if len(neighbours) == 0:
                    return
                # Loop to iterate over the
                # neighbours of the node
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                visited.append(node)
        return 

    def DLS(self, start, goal, maxDepth, matrix):

        if matrix[start[0], start[1]] == -1 or matrix[goal[0], goal[1]] == -1:
            return False

        matrix[start[0], start[1]] = -1

        self.pen.fillcolor('blue')
        self.drawSquare(start[0], start[1])
        self.costExpandNode += 1

        if start == goal: 
            self.costPath += 1
            return True
 
        # If reached the maximum depth, stop recursing.
        if maxDepth <= 0 :
            return False
 
        # Recur for all the vertices adjacent to this vertex
        for i in [[0, -1], [1, 0], [0, 1], [-1, 0]]:    # Left -> Up -> Right -> Down
            if (matrix[start[0] + i[0], start[1] + i[1]] != -1):
                if(self.DLS([start[0] + i[0], start[1] + i[1]], goal, maxDepth-1, matrix)):
                    self.pen.fillcolor('green')
                    self.drawSquare(start[0] + i[0], start[1] + i[1])
                    self.costPath += 1
                    return True
        return False
 
    # It uses recursive DLS()
    def IDS(self):
        maxDepth = 100
        # Repeatedly depth-limit search till the
        # maximum depth
        for i in range(maxDepth):
            matrix = self.level.copy()
            self.costExpandNode = 0
            if (self.DLS(self.start, self.goal, i, matrix)):
                self.drawStartGoal()
                self.depth = i
                return True
        return False

def visualize (start, goal, maze, listPoints, index, type):
    screen = Screen()
    screen.setup(700, 700)
    screen.title("FINDING PATH")

    G = Graph(start, goal, maze)
    G.polygons(listPoints, index)
    if type == '1':
        G.BFS()
    elif type == '2':
        G.UCS()
    elif type == '3':
        G.IDS()
    elif type == '4':
        G.GBFS()
    elif type == '5':
        G.AStar()

    G.printCost()
    screen.mainloop()

if __name__ == "__main__":

    with open('input.txt') as f:
        w, h = [int(x) for x in next(f).split()] # read first line
        a, b, c, d = [int(x) for x in next(f).split()]
        index = int(f.readline())
        listPoints = []
        for line in f: # read rest of lines
            temp = []
            k = line.split()
            for i in range(len(k) // 2):
                x = k[i * 2]
                y = k[i * 2 + 1]
                temp.append([int(x), int(y)])
            listPoints.append(temp)

    maze = []
    maze = np.zeros((w + 1, h + 1))
    maze[0] = -1
    maze [-1] = -1
    maze [:, 0] = -1
    maze [:, -1] = -1

    start = [a, b]
    goal = [c, d]

    # EACH SEARCH IS ONLY SELECTED ONCE WHEN RUN
    print("1. Breath first seach")
    print("2. Uniform cost search")
    print("3. Iterative deepening search")
    print("4. Greedy  best first search")
    print("5. Graph search A*")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        visualize(start, goal, maze, listPoints, index, choice)
    elif choice == '2':
        visualize(start, goal, maze, listPoints, index, choice)
    elif choice == '3':
        visualize(start, goal, maze, listPoints, index, choice)
    elif choice == '4':
        visualize(start, goal, maze, listPoints, index, choice)
    elif choice == '5':
        visualize(start, goal, maze, listPoints, index, choice)
    else:
        print("Thank for using program!!")