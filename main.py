import random
import sys
import time
from person import Person
from graph import Graph
from vertex import Vertex
from edge import Edge
from graph_algorthms import GraphAlgorithms

# Loads preferences from file and formats it to the Person class.
def parse_data(file_name):
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
    person_pick_list = people.copy()
    while person_pick_list:
        person = random.choice(person_pick_list)
        person_vertex = Vertex(person.name)
        vertices.append(person_vertex)

        # connect all people to the source
        edges.append(Edge(source, person_vertex, 1, 0))

        # add edges between person and preferences
        task_pick_list = [vertex for vertex in vertices if vertex.label in person.preferences]
        while task_pick_list:
            task = random.choice(task_pick_list)
            edges.append(Edge(person_vertex, task, 1, 0))
            task_pick_list.remove(task)

        person_pick_list.remove(person)

    return Graph(vertices, edges)

def assign_tasks(max_flow_graph, people):
    for person in people:
        assigned_edges = [edge for edge in max_flow_graph.get_reachable_edges(person.name) if edge.flow != 0]
        for edge in assigned_edges:
            task = edge.sink_vertex.get_label()
            person.assign_task(task)
            max_flow_graph.remove_edge(edge)
    return 

def fix_maximum_flow(graph, people, tasks, preference_faults):
    non_negative_edges = [edge for edge in graph.get_reachable_edges("source") if edge.flow != 0]

    while len(non_negative_edges) != len(people):
        add_random_edge(graph, people, tasks, preference_faults)
        GraphAlgorithms.ford_fulkerson(graph)
        non_negative_edges = [edge for edge in graph.get_reachable_edges("source") if edge.flow != 0]
        preference_faults += 1
    
    return preference_faults

def add_random_edge(graph, people, tasks, preference_faults):
    
    # Find uncomplete task
    uncompleted_task = find_uncomplete_task(graph, tasks)

    # Pick person to assign task too
    unlucky_person = random.choice(people)
    while unlucky_person.unlucky_count > (preference_faults // len(people)):
        unlucky_person = random.choice(people)

    # Add edge and bookkeeping
    graph.add_edge(unlucky_person.name, uncompleted_task, 1, 0)
    print(unlucky_person.name + " got fucked with " + uncompleted_task)
    print(unlucky_person.unlucky_count)
        
    return

def find_uncomplete_task(graph, tasks):
    for task in tasks:
        edge = graph.get_outgoing_edges(task)[0] # Only has 1 outgoing edge

        # Check if the task has enough people assigned
        if edge.capacity != edge.flow:
            return task
    
    return None

# REQUIREMENT: Amount of people should equal amount of tasks
def create_schedule():
    input_file_name = "input.txt"

    # TODO Add person data for every shift
    data = parse_data(input_file_name)
    tasks = [{"bar1" : 1, "bar2" : 0, "keuken" : 1, "gardarobe" : 0, "bekers" : 0, "deur" : 0},
             {"bar1" : 1, "bar2" : 0, "keuken" : 0, "gardarobe" : 1, "bekers" : 0, "deur" : 0},
             {"bar1" : 1, "bar2" : 0, "keuken" : 0, "gardarobe" : 0, "bekers" : 1, "deur" : 0},
             {"bar1" : 1, "bar2" : 0, "keuken" : 0, "gardarobe" : 1, "bekers" : 0, "deur" : 0}]

    amount_of_shifts = 4
    preference_faults = 0

    for i in range(amount_of_shifts):
        print("--------- SHIFT " + str(i) + "---------")
        graph = create_graph(data, tasks[i])
        GraphAlgorithms.ford_fulkerson(graph)
        preference_faults = fix_maximum_flow(graph, data, tasks[i], preference_faults)
        assign_tasks(graph, data)

    for person in data:
        person.print_assignment()

def main():
    create_schedule()
    
if __name__ == "__main__":
    main()

#    def dijkstras_algorithm(graph):
#     unvisted_vertices = graph.get_vertex_labels()
#     start_vertex = graph.get_vertex("source").get_label()

#     shortest_path = {}
#     previous_nodes = {}

#     max_value = sys.maxsize
#     for vertex in unvisted_vertices:
#         shortest_path[vertex] = max_value

#     shortest_path[start_vertex] = 0

#     # The algorithm executes until we visit all nodes
#     while unvisted_vertices:

#         current_vertex = unvisted_vertices[0]
#         for vertex in unvisted_vertices:
#             if shortest_path[vertex] < shortest_path[current_vertex]:
#                 current_vertex = vertex

#         # The code block below retrieves the current node's neighbors and updates their distances
#         outgoing_edges = graph.get_reachable_edges(current_vertex)

#         for edge in outgoing_edges:
#             neighbour = edge.sink_vertex.get_label()
#             tentative_value = shortest_path[current_vertex] + 1
#             #print("tentative value to " + neighbour + " is " + str(tentative_value))
#             if tentative_value < shortest_path[neighbour]:
#                 shortest_path[neighbour] = tentative_value
#                 previous_nodes[neighbour] = current_vertex

#         # After visiting its neighbors, we mark the node as "visited"
#         unvisted_vertices.remove(current_vertex)

#     return previous_nodes, shortest_path

# def get_augmenting_path(graph, previous_vertices):
#     path = []
#     next_vertex = "sink"
#     while next_vertex != "source":
#         source = graph.get_vertex(previous_vertices[next_vertex])
#         sink = graph.get_vertex(next_vertex)
#         edge = graph.get_edge(source, sink)
#         path.append(edge)
#         next_vertex = previous_vertices[next_vertex]
#     return path

# def ford_fulkerson(graph):
#     while True:
#         residual_network = graph.get_residual_network()
        
#         previous_vertices, shortest_path = dijkstras_algorithm(residual_network)
#         if "sink" not in previous_vertices:
#             #print(" --------- FINAL GRAPH --------- ")
#             #graph.print()
#             break
#         augmenting_path = get_augmenting_path(residual_network, previous_vertices)
#         graph.increase_flow(augmenting_path)