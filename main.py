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
        edges.append(Edge(vertex, sink, 1, 0))

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

def main():
    input_file_name = "input.txt"
    tasks = ["bar1", "bar2", "keuken", "gardarobe", "bekers", "deur"]

    data = load_data(input_file_name)
    graph = create_graph(data, tasks)

    for person in data:
        person.print()

if __name__ == "__main__":
    main()