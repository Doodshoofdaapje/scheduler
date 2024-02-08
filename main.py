import sys
import time
from person import Person
from graph import Graph
from vertex import Vertex
from edge import Edge

# Loads preferences from file and formats it to the Person class.
def load_data(file_name):
    people = []
    file = open(file_name)

    for line in file:
        # Strips '\n' from each line
        line = line[:-1] 
        name = line.split("|")[0]
        preferences = line.split("|")[1].split(", ")
        
        person = Person(name, preferences)
        people.append(person)

    return people

def create_graph(people, tasks):
    # Initial graph
    source = Vertex("source")
    sink = Vertex("sink")
    vertices = [source, sink]
    edges = []

    # create all task vertices
    for task in tasks:
        vertex = Vertex(task)
        vertices.append(vertex)

        # connect all tasks to the sink
        edges.append(Edge(vertex, sink, tasks[task], 0))

    # create all person vertices 
    for person in people:
        person_vertex = Vertex(person.name)
        vertices.append(person_vertex)

        # connect all people to the source
        edges.append(Edge(source, person_vertex, 1, 0))

        # add edges between person and preferences
        for vertex in vertices:
            if vertex.label in person.preferences:
                edges.append(Edge(person_vertex, vertex, 1, 0))

    return Graph(vertices, edges)

def dijkstras_algorithm(graph):
    unvisted_vertices = graph.get_vertex_labels()
    start_vertex = graph.get_vertex("source").get_label()

    shortest_path = {}
    previous_nodes = {}

    max_value = sys.maxsize
    for vertex in unvisted_vertices:
        shortest_path[vertex] = max_value

    shortest_path[start_vertex] = 0

    # The algorithm executes until we visit all nodes
    while unvisted_vertices:

        current_vertex = unvisted_vertices[0]
        for vertex in unvisted_vertices:
            if shortest_path[vertex] < shortest_path[current_vertex]:
                current_vertex = vertex

        # The code block below retrieves the current node's neighbors and updates their distances
        outgoing_edges = graph.get_edges_by_vertex(current_vertex)

        for edge in outgoing_edges:
            neighbour = edge.sink_vertex.get_label()
            tentative_value = shortest_path[current_vertex] + 1
            #print("tentative value to " + neighbour + " is " + str(tentative_value))
            if tentative_value < shortest_path[neighbour]:
                shortest_path[neighbour] = tentative_value
                previous_nodes[neighbour] = current_vertex

        # After visiting its neighbors, we mark the node as "visited"
        unvisted_vertices.remove(current_vertex)

    return previous_nodes, shortest_path

def get_augmenting_path(graph, previous_vertices):
    path = []
    next_vertex = "sink"
    while next_vertex != "source":
        source = graph.get_vertex(previous_vertices[next_vertex])
        sink = graph.get_vertex(next_vertex)
        path.append(graph.get_edge(source, sink))
        next_vertex = previous_vertices[next_vertex]
    return path

def ford_fulkerson(graph):
    while True:
        residual_network = graph.get_residual_network()
        
        previous_vertices, shortest_path = dijkstras_algorithm(residual_network)
        if "sink" not in previous_vertices:
            #print(" --------- FINAL GRAPH --------- ")
            #graph.print()
            break
        augmenting_path = get_augmenting_path(graph, previous_vertices)
        graph.increase_flow(augmenting_path)

def assign_tasks(max_flow_graph, people):
    for person in people:
        assigned_edges = [edge for edge in max_flow_graph.get_edges_by_vertex(person.name) if edge.flow != 0]
        for edge in assigned_edges:
            task = edge.sink_vertex.get_label()
            person.assign_task(task)
            max_flow_graph.remove_edge(edge)
    return 

def create_schedule():
    input_file_name = "input.txt"
    data = load_data(input_file_name)
    tasks = {"bar1" : 3, "bar2" : 2, "keuken" : 2, "gardarobe" : 3, "bekers" : 3, "deur" : 2}

    amount_of_shifts = 4
    for i in range(amount_of_shifts):
        graph = create_graph(data, tasks)
        ford_fulkerson(graph)

        non_negative_edges = [edge for edge in graph.get_edges_by_vertex("source") if edge.flow != 0]
        while len(non_negative_edges) != len(data):
            #add random edge
            ford_fulkerson(graph)

        assign_tasks(graph, data)

    for person in data:
        person.print_assignment()

def main():
    create_schedule()
    
    
if __name__ == "__main__":
    main()