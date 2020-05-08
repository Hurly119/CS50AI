import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

## name = { "name": [1(id),2(id)]}

##people = { 1(id) : {"name":"personname", "birth":"birthdate", "movies": [1,2,3,4]}}

##movies = { 1(movieID): {"title":"titlename", "year":1998, "stars":{[1,2,3,4]}}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    # directory = "small"
    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")



def targetInNeighbors(neighbors,target):
    for neighbor in neighbors:
        if neighbor[1] == target:
            return True
    return False

def selectStart(source, target, exploredNodes, Frontier):
    neighbors = neighbors_for_person(source)
    startNode = None
    print(neighbors)
    for neighbor in neighbors:
        if targetInNeighbors(neighbors,target):
            if neighbor[1] == target:
                startNode = Node(state=neighbor,parent=None,action=None)
                return startNode
        elif neighbor not in exploredNodes and not Frontier.contains_state(neighbor) and neighbor[1] != source:
            startNode = Node(state=neighbor,parent=None,action=None)

    return startNode


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    Frontier = QueueFrontier()

    exploredNodes = set()
    # exploredStartNodes = set()

    start = selectStart(source,target,exploredNodes,Frontier)
    if start == None:
        raise Exception("No solution")

    # exploredStartNodes.add(start.state)
    exploredNodes.add(start.state)

    while True:

        if Frontier.empty():
            newStart = selectStart(source,target,exploredNodes,Frontier)
            if newStart == None:
                raise Exception("No Solution")
            else:
                Frontier.add(newStart)
                # exploredStartNodes.add(newStart.state)
                exploredNodes.add(newStart.state)
        else:

            node = Frontier.remove()

            if node.state[1] == target:
                cells = []

                ##Add the current node and its parents
                cells.append(node.state)
                while(node.parent is not None):
                    cells.append(node.parent.state)
                    node = node.parent
                cells.reverse()
                return cells

            neighborsOfNodes = neighbors_for_person(node.state[1])

            for neighbor in neighborsOfNodes:
                if targetInNeighbors(neighborsOfNodes,target):
                    if neighbor[1] == target:
                        child = Node(state=neighbor,parent=node,action=None)
                        Frontier.add(child)
                        exploredNodes.add(child.state)
                elif neighbor not in exploredNodes and not Frontier.contains_state(neighbor):
                    child = Node(state=neighbor,parent=node,action=None)
                    Frontier.add(child)
                    exploredNodes.add(child.state)






    # TODO
    # raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
