import sys
sys.path.append('../')
from search import Node, StackFrontier, QueueFrontier

def main():
    """
    Positions:
    0: boat
    1: fox
    2: chicken
    3: grain
    """
    start = (0, 0, 0, 0)
    target = (1, 1, 1, 1)
    
    path = get_path(start, target)
    
    if path:
        for state, action in path:
            print(f"State: {state}, Action: {action}")
    else:
        print("No valid solution found.")

def get_neighbors(state):
    """
    Generate valid moves from a given state.
    """
    boat, fox, chicken, grain = state
    next_states = []
    
    # Possible moves: alone or with one item
    moves = [(1,), (1, 1), (1, 2), (1, 3)]  # Boat alone, Boat+Fox, Boat+Chicken, Boat+Grain
    
    for move in moves:
        new_state = list(state)
        valid = True
        
        # Flip boat's position
        new_state[0] = 1 - boat
        
        # Move additional entity if included in the move
        if len(move) > 1:
            entity = move[1]
            if new_state[entity] == boat:  # Only move if on same side as the boat
                new_state[entity] = 1 - boat
            else:
                continue  # Invalid move if entity isn't on boat's side
        
        new_state = tuple(new_state)
        
        # Check for invalid states
        if (new_state[1] == new_state[2] != new_state[0]) or (new_state[2] == new_state[3] != new_state[0]):
            valid = False  # Fox eats Chicken or Chicken eats Grain
        
        if valid:
            next_states.append((new_state, move))
    
    return next_states

def get_path(start, target):
    """
    Use BFS to find the shortest path to the solution.
    """
    frontier = QueueFrontier()
    frontier.add(Node(state=start, parent=None, action=None))
    visited = set()
    
    while not frontier.empty():
        node = frontier.remove()
        
        if node.state == target:
            # Reconstruct path
            path = []
            while node.parent is not None:
                path.append((node.state, node.action))
                node = node.parent
            return path[::-1]  # Reverse to get the correct order
        
        visited.add(node.state)
        
        for neighbor, action in get_neighbors(node.state):
            if neighbor not in visited:
                frontier.add(Node(state=neighbor, parent=node, action=action))
    
    return None  # No solution found

if __name__ == "__main__":
    main()
