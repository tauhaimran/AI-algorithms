# tauha imran 22i1239 cs-g AI A2 q1
import time
import random
from collections import defaultdict

##########################################################################################
def local_beam_search(graph, k, max_iterations, num_colors, pre_assigned_colors=None):

    # Get all unique nodes from the graph's adjacency list
    all_nodes = set()
    for node, neighbors in graph.items():
        all_nodes.add(node)
        all_nodes.update([neighbor[0] for neighbor in neighbors])  # Extract neighbors from tuples
    num_vertices = len(all_nodes)  # Number of vertices based on unique nodes

    print('all unique vertices found....')

    # Generate random initial states
    states = []
    for _ in range(k):
        state = [-1] * num_vertices
        for node in range(num_vertices):
            if pre_assigned_colors and node in pre_assigned_colors:
                state[node] = pre_assigned_colors[node]  # Use pre-assigned color
            else:
                state[node] = random.randint(0, num_colors - 1)  # Random valid color
        states.append(state)

    print('intial random states generated....')

    # Helper function to calculate the heuristic = no. of colou conflicts
    def heuristic(state, graph):
      conflicts = 0

      # Iterate over all vertices in the graph
      for node, neighbors in graph.items():
          if node < len(state):  # Check if the node is in the state
              for neighbor, _ in neighbors:  # Unpack the neighbor tuple
                  if neighbor < len(state):  # Check if the neighbor is in the state
                      if state[node] == state[neighbor]:  # Conflict: both vertices have the same colour
                          conflicts += 1

      return conflicts

    print('starting the local beam search...')
    # Perform Local Beam Search
    for _ in range(max_iterations):
        # Generate successors
        successors = []
        for state in states:
            for node in range(num_vertices):
                current_color = state[node]
                for new_color in range(num_colors):
                    if new_color != current_color:
                        new_state = state[:]
                        new_state[node] = new_color
                        successors.append(new_state)

        # Sort successors by heuristic value
        # Use a lambda function to provide the graph argument to heuristic
        successors.sort(key=lambda state: heuristic(state, graph))
        print('successors generated....')

        # Keep top k states
        states = successors[:k]

        print('top k states generated....')
        # Check for a solution with no conflicts
        if heuristic(states[0], graph) == 0: # Pass graph to heuristic here as well
            print('solution found....')
            return states[0] ,heuristic(states[0], graph)

    print('no solution found....')
    # Return the best state found
    return states[0] , heuristic(states[0], graph)

##########################################################################################
def load_graph_from_file(file_path):
    graph = {}  # Initialize the graph as an empty dictionary

    with open(file_path, 'r') as file:
        # Skip the header line
        next(file)

        # Process the remaining lines
        for line in file:
            # Split the line into Source, Destination, and Heuristic
            source, dest, heuristic = line.strip().split()

            # Convert to proper types: Source and Destination are integers, Heuristic is a float
            source = int(source)
            dest = int(dest)
            heuristic = float(heuristic)

            # Add the destination and heuristic to the source node's list
            if source not in graph:
                graph[source] = []
            graph[source].append((dest, heuristic))

    return graph
##########################################################################################
# Example Usage
if __name__ == "__main__":
    # Save the example data in a file named "graph_data.txt"
    file_path = "hypercube_dataset.txt"  # Replace with your file's actual path

    # Load the graph from the file
    graph_stats = load_graph_from_file(file_path)

    # Print the graph for verification
    #for i in range(0,5):
    #for node, neighbors in graph.items():
    #    node = i
    #    neighbors = graph_stats[node]
    #    print(f"Node {node} has neighbors: {neighbors}")


    # Pre-assigned colors
    pre_assigned_colors = {0: 0}  # Vertex 0 is pre-colored with color 0

    #assigning graph till a finite number of states
    graph = {}
    size = len(graph_stats)
    size = int(size/20)
    for i in range(0,size):
        graph.update({i:graph_stats[i]})

    # Parameters for Local Beam Search
    k = 50  # Beam width
    max_iterations = 7 # Maximum number of iterations
    num_colors = 7  # Maximum colors allowed

    # Measure the start time
    start_time = time.time()

    # Call the function you want to measure

    print("total nodes in graph : ",size)
    print('calling beam search function now....')
    # Run Local Beam Search
    best_coloring, heuristic_value = local_beam_search(graph, k, max_iterations, num_colors, pre_assigned_colors)

    # Measure the end time
    end_time = time.time()

    # Calculate the time taken
    time_taken = end_time - start_time

    print(f"\n\n -------------------------------------- \n Time taken to execute the function: {time_taken} seconds \n -------------------------------------- \n ")

    # Output the result
    print("Heuristic Value:", heuristic_value)
    print("Best Coloring Found:\n", best_coloring)
