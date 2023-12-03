class Node():

    def __init__(self, parentNode=None, position=None):
        self.parentNode = parentNode
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def aStarAlgorithm(levelList, start, end):
    

    startNode = Node(None, start)
    startNode.g = startNode.h = startNode.f = 0
    endNode = Node(None, end)
    endNode.g = endNode.h = endNode.f = 0

    
    openList = []
    closedList = []

    openList.append(startNode)

    
    while len(openList) > 0:

        currentNode = openList[0]
        currentIndex = 0
        for index, item in enumerate(openList):
            if item.f < currentNode.f:
                currentNode = item
                currentIndex = index

        openList.pop(currentIndex)
        closedList.append(currentNode)

        if currentNode == endNode:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parentNode
            return path[::-1] 

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: 

            nodePosition = (currentNode.position[0] + new_position[0], currentNode.position[1] + new_position[1])

            
            if nodePosition[0] > (len(levelList) - 1) or nodePosition[0] < 0 or nodePosition[1] > (len(levelList[len(levelList)-1]) -1) or nodePosition[1] < 0:
                continue

            if levelList[nodePosition[0]][nodePosition[1]] != 20 and levelList[nodePosition[0]][nodePosition[1]] != 14:
                continue

            new_node = Node(currentNode, nodePosition)

            children.append(new_node)

        for child in children:

            for closed_child in closedList:
                if child == closed_child:
                    continue

            child.g = currentNode.g + 1
            child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)
            child.f = child.g + child.h

            for open_node in openList:
                if child == open_node and child.g > open_node.g:
                    continue

            openList.append(child)


def main():

    levelList = [[20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 2, 20, 10, 20, 20, 20, 20, 20, 20, 20, 2, 20, 20, 20, 2, 20, 20, 2, 20, 20, 2, 20, 20, 2, 20, 2, 2, 20, 20, 20, 20, 20, 20, 20, 20], 
            [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 2, 20, 2, 2, 20, 20, 20, 20, 20, 20, 2, 20, 20, 20, 2, 20, 20, 2, 20, 20, 2, 2, 20, 2, 20, 2, 2, 20, 20, 20, 20, 20, 20, 20, 20], 
            [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 2, 10, 20, 20, 2, 20, 20, 20, 20, 20, 2, 20, 2, 20, 2, 20, 20, 2, 20, 20, 2, 20, 2, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], 
            [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 2, 2, 20, 20, 20, 2, 2, 20, 20, 20, 20, 2, 2, 2, 20, 20, 20, 2, 20, 20, 2, 20, 20, 2, 20, 2, 2, 20, 20, 20, 20, 20, 20, 20, 20], 
            [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 2, 20, 10, 20, 20, 20, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], 
            [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 2, 20, 2, 20, 20, 20, 20, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], 
            [20, 20, 20, 20, 20, 20, 20, 20, 14, 14, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 2, 2, 20, 20, 2, 10, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], 
            [20, 20, 20, 20, 20, 20, 20, 20, 2, 2, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20, 2, 2, 20, 20, 20, 2, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20], 
            [20, 20, 20, 20, 20, 20, 20, 2, 2, 2, 2, 2, 20, 20, 20, 20, 20, 20, 20, 2, 2, 20, 20, 2, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20, 2, 2, 2, 2, 2, 2, 2, 2, 20, 20, 20, 20, 20, 20, 20, 20, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20], 
            [20, 20, 20, 20, 20, 20, 2, 2, 2, 2, 2, 2, 2, 20, 20, 20, 20, 8, 2, 2, 20, 20, 2, 20, 20, 20, 20, 2, 20, 20, 20, 20, 20, 2, 20, 2, 20, 20, 20, 20, 20, 2, 20, 20, 20, 20, 20, 20, 20, 20, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20], 
            [20, 20, 20, 20, 20, 2, 2, 2, 2, 2, 2, 2, 2, 2, 20, 20, 20, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 2, 2, 2, 2, 2, 20, 2, 20, 20, 20, 20, 20, 2, 20, 20, 20, 20, 20, 20, 20, 20, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20], 
            [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 20, 20, 20, 20, 20, 2, 20, 20, 20, 20, 20, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 20, 20, 20, 20, 20, 20, 20, 20, 20]]

    start = (5, 10)
    end = (3, 6)

    path = aStarAlgorithm(levelList, start, end)
    print(path)


if __name__ == '__main__':
    main()