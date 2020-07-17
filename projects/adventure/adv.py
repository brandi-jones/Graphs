from room import Room
from player import Player
from world import World
from util import Stack, Queue
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "projects/adventure/maps/test_line.txt"
#map_file = "projects/adventure/maps/test_cross.txt"
#map_file = "projects/adventure/maps/test_loop.txt"
#map_file = "projects/adventure/maps/test_loop_fork.txt"
map_file = "projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def bfs(starting_vertex):
    """
    Return a list containing the shortest path from
    starting_vertex to destination_vertex in
    breath-first order.
    """
    path = [starting_vertex]
    q = Queue()
    q.enqueue(path)
    visited = set()
    
    while q.size() > 0:
        current_path = q.dequeue()
        current_node = current_path[-1]

        #if found room with an unknown ? direction
        if '?' in graph[current_node].values():
            return current_path
        
        if current_node not in visited:
            
            visited.add(current_node)
            roomsAccessible = graph[current_node].values()
            for room in roomsAccessible:
                new_path = current_path[:]
                new_path.append(room)

                q.enqueue(new_path)
            

def getOppositeDirection(direction):
    if direction == 's':
        return 'n'
    if direction == 'n':
        return 's'
    if direction == 'e':
        return 'w'
    if direction == 'w':
        return 'e'

#make graph, that will be a dictionary of dictionaries
graph = {}

graph[player.current_room.id] = {} #create a dictionary as the value for the key in the graph of the starting room id
for exitDirection in player.current_room.get_exits(): #for each exit for the current room, fill it with '?' values, as we don't yet know what room that direction leads to
    graph[player.current_room.id][exitDirection] = '?'

allPathsExplored = False #stopping condition for loop
visited = set() #set of visited rooms

while not allPathsExplored:

    #add the current room to the visited set, and reset the next direction to travel to
    visited.add(player.current_room.id)
    nextDirection = ''

    #find the unknown direction for the current room, if there exists one
    for key, value in graph[player.current_room.id].items():
        if value == '?':
            nextDirection = key
            break


    #if next direction is empty, meaning there was no unknown direction in current room
    if nextDirection == '':
        #run a bfs on the graph, with the destination being to find the closest room with a ? 
        backPath = bfs(player.current_room.id)
        
        if backPath == None: #if no backpath to a room with an unknown, then all paths must be explored
            allPathsExplored = True
        else: #if backpath was found, then traverse that path and move your player through it
            for room in backPath:
                for key, value in graph[player.current_room.id].items():
                    #if found room to move back to in the path for the current room we're in, move back in the direction associated with that room
                    if value == room:
                        player.travel(key) 
                        traversal_path.append(key) #append movement to traversal path

    else:
        #log prevRoom id, travel to the nextDirection, and map out information in the graph
        prevRoom = player.current_room.id
        player.travel(nextDirection)
        traversal_path.append(nextDirection) #append movement to traversal path
        graph[prevRoom][nextDirection] = player.current_room.id #fill in info for previous room in graph

        #if this room has never been visited, create dictionary with available directions with values as ?
        if player.current_room.id not in visited:
            graph[player.current_room.id] = {}
            for exitDirection in player.current_room.get_exits():
                graph[player.current_room.id][exitDirection] = '?'

        #backfill the pathway to the previous room you came from to the current room your in
        graph[player.current_room.id][getOppositeDirection(nextDirection)] = prevRoom


# print(graph)
# print(traversal_path)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
