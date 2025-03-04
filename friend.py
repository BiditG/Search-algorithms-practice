import pandas as pd

# Load CSV and build an undirected graph
df = pd.read_csv("data[1].csv")
connections = {}

for user, friend in zip(df["user"], df["friend"]):
    connections.setdefault(user, []).append(friend)
    connections.setdefault(friend, []).append(user)  

class StackFrontier:
    def __init__(self):
        self.stack = []

    def add(self, node):
        self.stack.append(node)

    def remove(self):
        if self.empty():
            raise Exception("No path found")
        return self.stack.pop()  

    def empty(self):
        return len(self.stack) == 0

    def contains_state(self, state):
        return any(node.state == state for node in self.stack)

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

def get_neighbors(person):
    """Return a list of neighbors (friends) for a given person."""
    return connections.get(person, [])

def find_connection(person1, person2):
    """Find a connection path using DFS (StackFrontier)."""
    if person1 not in connections or person2 not in connections:
        return None

    start_node = Node(state=person1)
    frontier = StackFrontier()
    frontier.add(start_node)

    explored = set()

    while not frontier.empty():
        node = frontier.remove()

        if node.state == person2:
            # Build path by backtracking
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            return path[::-1]  

        explored.add(node.state)

        for neighbor in get_neighbors(node.state):
            if neighbor not in explored and not frontier.contains_state(neighbor):
                child_node = Node(state=neighbor, parent=node)
                frontier.add(child_node)


# Example usage
person1, person2 = "user_2", "user_10"
path = find_connection(person1, person2)

print(f"DFS Path: {' -> '.join(path)}" if path else "No connection found.")
