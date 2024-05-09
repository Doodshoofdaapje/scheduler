import random
import sys
import time
from person import Person
from graph import FlowGraph
from vertex import Vertex
from edge import Edge
from graph_algorthms import GraphAlgorithms

# REQUIREMENT: Amount of people should equal amount of tasks
def create_schedule():
    input_file_name = "input.txt"

    # TODO Add person data for every shift
    people = parse_data(input_file_name)
    tasks = [{"bar1" : 1, "bar2" : 0, "keuken" : 1, "gardarobe" : 0, "bekers" : 0, "deur" : 0},
             {"bar1" : 1, "bar2" : 0, "keuken" : 0, "gardarobe" : 1, "bekers" : 0, "deur" : 0},
             {"bar1" : 1, "bar2" : 0, "keuken" : 0, "gardarobe" : 0, "bekers" : 1, "deur" : 0},
             {"bar1" : 1, "bar2" : 0, "keuken" : 0, "gardarobe" : 1, "bekers" : 0, "deur" : 0}]

    amount_of_shifts = 2
    preference_faults = 0

    for i in range(amount_of_shifts):
        print("--------- SHIFT " + str(i) + "---------")
        graph = create_graph(people, tasks[i])
        GraphAlgorithms.ford_fulkerson(graph)
        assign_tasks(graph, people)

    for person in people:
        person.print_assignment()

def assign_tasks(max_flow_graph, people):
    for person in people:
        assigned_edges = [edge for edge in max_flow_graph.get_reachable_edges(person.name) if edge.flow != 0]
        if not assigned_edges:
            continue

        task = assigned_edges[0].sink_vertex.label
        person.assign_task(task)
        max_flow_graph.delete_edge(assigned_edges[0].source_vertex.label, assigned_edges[0].sink_vertex.label)

def create_graph(people, tasks):
    """
    Creates graph
    """
    graph = FlowGraph()
    graph.add_vertex("source")
    graph.add_vertex("sink")

    # Shuffling to get rid of order bias
    task_list = list(tasks.items())
    random.shuffle(task_list)
    for task, capacity in task_list:
        graph.add_vertex(task)
        graph.add_edge(task, "sink", capacity, 0)

    # Shuffling to get rid of order bias
    random.shuffle(people)
    for person in people:
        graph.add_vertex(person.name)
        graph.add_edge("source", person.name, 1, 0)

        # Shuffling to get rid of order bias
        random.shuffle(person.preferences)
        for preference in person.preferences:
            graph.add_edge(person.name, preference, 1, 0)

    return graph

def parse_data(file_name):
    """
    Parses data file and stores people and there preferences
    """
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

def main():
    create_schedule()
    
if __name__ == "__main__":
    main()