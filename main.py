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
    tasks = [{"bar1" : 3, "bar2" : 1, "keuken" : 0, "gardarobe" : 2, "bekers" : 1, "deur" : 2, "kassa" : 1},
             {"bar1" : 3, "bar2" : 1, "keuken" : 1, "gardarobe" : 2, "bekers" : 1, "deur" : 1, "kassa" : 1},
             {"bar1" : 3, "bar2" : 1, "keuken" : 1, "gardarobe" : 2, "bekers" : 1, "deur" : 1, "kassa" : 1},
             {"bar1" : 3, "bar2" : 0, "keuken" : 0, "gardarobe" : 2, "bekers" : 3, "deur" : 1, "kassa" : 1}]

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
    if unlucky_person is not None:
        #print(unlucky_person.name + " got an edge to " + uncompleted_task)
        graph.add_edge(unlucky_person.name, uncompleted_task, 1, 0)

def find_uncomplete_task(graph, tasks):
    uncompleted_tasks = [task for task in tasks if graph.get_outgoing_edges(task)[0].capacity != graph.get_outgoing_edges(task)[0].flow]
    task = random.choice(uncompleted_tasks)
    return task

def find_unlucky_person(graph, people, task, preference_faults):
    # Find people who have less unlucky shifts
    candidates = [person for person in people if person.unlucky_count <= preference_faults // len(people)]
    candidates_for_task = [person for person in candidates if task not in person.assigned_tasks]

    # First try people who havent dont the task and where lucky untill now
    unlucky_person = pick_random_person(graph, candidates_for_task, task)

    # Otherwise try people who where lucky untill now
    if unlucky_person is None:
        unlucky_person = pick_random_person(graph, candidates, task)

    # Finally try people all people
    if unlucky_person is None:
            unlucky_person = pick_random_person(graph, people, task)
    
    return unlucky_person

def pick_random_person(graph, people, task):
    attempted_people = []
    # Attempt find a person who doesnt have the edge already from candidates
    for i in range(len(people)):
        # Pick random person from the list
        unlucky_person = random.choice([person for person in people if person not in attempted_people])
        attempted_people.append(unlucky_person)

        # Check if edge already exists
        assigned_tasks = [edge.sink_vertex.label for edge in graph.get_outgoing_edges(unlucky_person.name)]
        if task not in assigned_tasks:
            return unlucky_person
        
    return None

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