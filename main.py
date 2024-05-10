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
    tasks = [{"bar1" : 3, "bar2" : 1, "keuken" : 0, "gardarobe" : 3, "bekers" : 2, "deur" : 1},
             {"bar1" : 3, "bar2" : 1, "keuken" : 1, "gardarobe" : 2, "bekers" : 2, "deur" : 1},
             {"bar1" : 3, "bar2" : 1, "keuken" : 1, "gardarobe" : 2, "bekers" : 2, "deur" : 1},
             {"bar1" : 3, "bar2" : 1, "keuken" : 0, "gardarobe" : 3, "bekers" : 2, "deur" : 1}]

    amount_of_shifts = 4
    preference_faults = 0

    for i in range(amount_of_shifts):
        print("--------- SHIFT " + str(i) + "---------")
        graph = create_graph(people, tasks[i])
        GraphAlgorithms.ford_fulkerson(graph)
        if not graph.is_max_flow():
            fix_maximum_flow(graph, people, tasks[i], preference_faults)
        preference_faults += assign_tasks(graph, people)

    print("--------- ASSIGNMENTS ---------")
    for person in people:
        person.print_assignment()

def fix_maximum_flow(graph, people, tasks, preference_faults):
    while not graph.is_max_flow():
        add_random_edge(graph, people, tasks, preference_faults)
        GraphAlgorithms.ford_fulkerson(graph)

def add_random_edge(graph, people, tasks, preference_faults):
    # Find uncomplete task
    uncompleted_task = find_uncomplete_task(graph, tasks)

    # Pick person to assign task too
    unlucky_person = find_unlucky_person(graph, people, uncompleted_task, preference_faults)

    # Add edge
    graph.add_edge(unlucky_person.name, uncompleted_task, 1, 0)

def find_uncomplete_task(graph, tasks):
    for task in tasks:
        edge = graph.get_outgoing_edges(task)[0] # Only has 1 outgoing edge

        # Check if the task has enough people assigned
        if edge.capacity != edge.flow:
            return task
    
    return None

def find_unlucky_person(graph, people, task, preference_faults):
    unlucky_candidates = [person for person in people if person.unlucky_count <= preference_faults // len(people)]
    if not unlucky_candidates:
        return None

    unlucky_person = random.choice(unlucky_candidates)
    possible_tasks = graph.get_outgoing_edges(unlucky_person)
    while task in possible_tasks:
        unlucky_person = random.choice(unlucky_candidates)
        possible_tasks = graph.get_outgoing_edges(unlucky_person)

    return unlucky_person

def assign_tasks(max_flow_graph, people):
    preference_faults = 0
    for person in people:
        assigned_edges = [edge for edge in max_flow_graph.get_reachable_edges(person.name) if edge.flow != 0]
        if not assigned_edges:
            continue

        task = assigned_edges[0].sink_vertex.label
        preference_faults += person.assign_task(task)
        max_flow_graph.delete_edge(assigned_edges[0].source_vertex.label, assigned_edges[0].sink_vertex.label)
    return preference_faults

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