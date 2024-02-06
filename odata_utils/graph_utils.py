# graph_utils.py
import heapq

def dijkstra(graph, start, end):
    # Create a priority queue to store vertices and their distances
    if start not in graph:
        graph[start] = set()
    if end not in graph:
        graph[end] = set()
    priority_queue = [(0, start)]
    # Dictionary to store distances from the start to each vertex
    distances = {vertex: float("infinity") for vertex in graph}
    distances[start] = 0
    # Dictionary to store predecessors for reconstructing the path
    predecessors = {vertex: None for vertex in graph}

    while priority_queue:
        # Get the vertex with the smallest distance
        try:
            current_distance, current_vertex = heapq.heappop(priority_queue)
        except IndexError:
            # If the queue is empty, break out of the loop
            break

        # Check if the current distance is greater than the known distance
        if current_distance > distances[current_vertex]:
            continue

        # If the end vertex is reached, reconstruct the path and return
        if current_vertex == end:
            path = []
            while current_vertex is not None:
                path.insert(0, current_vertex)
                current_vertex = predecessors[current_vertex]
            # If end vertex is not reachable from the start
            if end not in distances:
                return float("infinity"), []

            # Return the shortest distance and path
            # If end vertex is not reachable from the start
            if distances[end] == float("infinity"):
                return float("infinity"), []

            return distances[end], path

        # Iterate over neighbors of the current vertex
        for neighbor in graph.get(current_vertex, set()):
            distance = current_distance + 1  # Assuming each edge has a weight of 1

            # If a shorter path is found, update the distance and predecessor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    # If end vertex is not reachable from the start
    
    return float("infinity"), []


def add_value_to_dict_set(dictionary, key, value=""):
    # Check if the key already exists in the dictionary
    if key in dictionary:
        # If the key exists, add the value to the existing set
        dictionary[key].add(value)
    else:
        # If the key does not exist, create a new set with the provided value
        dictionary[key] = {value}