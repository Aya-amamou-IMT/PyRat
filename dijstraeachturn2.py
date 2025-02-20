"""dijkstra amélioré qui s'arrête quand il rencontre UN fromage et le renvoie comme cible"""
###################################################################### IMPORTS ######################################################################


# Import PyRat
from pyrat import *


# External imports
from collections import deque

# import heapq
import heapq


###################################################################### PREVIOUSLY DEVELOPPED FUNCTIONS ######################################################################
import os
import sys

import tutorial
###########################################################################################
############################################################### CONSTANTS & VARIABLES


# [TODO] It is good practice to keep all your constants and global variables in an easily identifiable section




##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################



def traversal ( source:             int,
                graph:              Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                create_structure:   Callable[[], Any],
                push_to_structure:  Callable[[Any, Tuple[int, int, int]], None],
                pop_from_structure: Callable[[Any], Tuple[int, int, int]],
                cibles:List
              ) ->                  Tuple[Dict[int, int], Dict[int, Union[None, int]]]:

    """
        Traversal function that explores a graph from a given vertex.
        This function is generic and can be used for most graph traversal.
        To adapt it to a specific traversal, you need to provide the adapted functions to create, push and pop elements from the structure.
        In:
            * source:             Vertex from which to start the traversal.
            * graph:              Graph on which to perform the traversal.
            * create_structure:   Function that creates an empty structure to use in the traversal.
            * push_to_structure:  Function that adds an element of type B to the structure of type A.
            * pop_from_structure: Function that returns and removes an element of type B from the structure of type A.
        Out:
            * distances_to_explored_vertices: Dictionary where keys are explored vertices and associated values are the lengths of the paths to reach them.
            * routing_table:                  Routing table to allow reconstructing the paths obtained by the traversal.
    """

    # Initialize a data structure with start vertex
    queuing_structure = create_structure()
    push_to_structure(queuing_structure, (0, source, None))

    # Explore the graph
    distances_to_explored_vertices = {}
    routing_table = {}
    while len(queuing_structure) > 0:

        # Get an unexplored element from the structure
        (distance_to_current_vertex, current_vertex, parent) = pop_from_structure(queuing_structure)
        if current_vertex not in distances_to_explored_vertices:

            # It is now explored
            distances_to_explored_vertices[current_vertex] = distance_to_current_vertex
            routing_table[current_vertex] = parent

            # Add its neighbors to the structure for later exploration
            for neighbor in tutorial.get_neighbors(current_vertex, graph):
                distance_to_neighbor = distance_to_current_vertex + tutorial.get_weight(current_vertex, neighbor, graph)
                push_to_structure(queuing_structure, (distance_to_neighbor, neighbor, current_vertex))
            #return when one cheese is found
            if current_vertex in cibles:
                return distances_to_explored_vertices,routing_table,current_vertex

    # Once all vertices have been explored, it is over
    return distances_to_explored_vertices, routing_table




def dijkstra( source: int,
               graph:  Union[numpy.ndarray, Dict[int, Dict[int, int]]],
               cible
             ) ->      Tuple[Dict[int, int], Dict[int, Union[None, int]]]:
    """
        Dijkstra's algorithm is a particular traversal where vertices are explored in an order that is proportional to the distance to the source vertex.
        In:
            * source: Vertex from which to start the traversal.
            * graph:  Graph on which to perform the traversal.
        Out:
            * distances_to_explored_vertices: Dictionary where keys are explored vertices and associated values are the lengths of the paths to reach them.
            * routing_table:                  Routing table to allow reconstructing the paths obtained by the traversal.
    """

    # Function to create an empty priority queue
    def create_structure ():
        return []
    # Function to add an element to the priority queue
    def push_to_structure (structure, element):
        heapq.heappush(structure, element)
    # Function to extract an element from the priority queue
    def pop_from_structure (structure):
        if len(structure)!=0:
            return heapq.heappop(structure)

    # Perform the traversal
    distances_to_explored_vertices, routing_table ,cheese= traversal(source, graph, create_structure, push_to_structure, pop_from_structure,cible)
    return distances_to_explored_vertices, routing_table,cheese



def find_route ( routing_table: Dict[int, Union[None, int]],
                 source:        int,
                 target:        int
               ) ->             List[int]:
    """
        Function to return a sequence of locations using a provided routing table.
        In:
            * routing_table: Routing table as obtained by the traversal.
            * source:        Vertex from which we start the route (should be the one matching the routing table).
            * target:        Target to reach using the routing table.
        Out:
            * route: Sequence of locations to reach the target from the source, as perfomed in the traversal.
    """
    route=deque()
    route.appendleft(target)
    while target!=source:
        target=routing_table[target] #On suit les clé-valeurs du dictionnaire jusqu'à remonter à la source
        route.appendleft(target)
    return route

def locations_to_actions ( locations:  List[int],
                           maze_width: int
                         ) ->          List[str]:
    """
        Function to transform a list of locations into a list of actions to reach vertex i+1 from vertex i.
        In:
            * locations:  List of locations to visit in order.
            * maze_width: Width of the maze in number of cells.
        Out:
            * actions: Sequence of actions to visit the list of locations.
    """

    # We iteratively transforms pairs of locations in the corresponding action
    actions = deque()
    for i in range(len(locations) - 1):
        action = tutorial.locations_to_action(locations[i], locations[i + 1], maze_width)
        actions.appendleft(action)
    return actions

#####################################################################################################################################################
##################################################### EXECUTED ONCE AT THE BEGINNING OF THE GAME ####################################################
#####################################################################################################################################################

def preprocessing ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                    maze_width:       int,
                    maze_height:      int,
                    name:             str,
                    teams:            Dict[str, List[str]],
                    player_locations: Dict[str, int],
                    cheese:           List[int],
                    possible_actions: List[str],
                    memory:           threading.local
                  ) ->                None:

    """
        This function is called once at the beginning of the game.
        It is typically given more time than the turn function, to perform complex computations.
        Store the results of these computations in the provided memory to reuse them later during turns.
        To do so, you can crete entries in the memory dictionary as memory.my_key = my_value.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * None.
    """
    # [TODO] Write your preprocessing code here
    memory.route=locations_to_actions(find_route(dijkstra(player_locations[name],maze,cheese)[1],player_locations[name] ,cheese[0] ),maze_width) #avec dijkstra on détermine les actions à faire

#####################################################################################################################################################
######################################################### EXECUTED AT EACH TURN OF THE GAME #########################################################
#####################################################################################################################################################

def turn ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
           maze_width:       int,
           maze_height:      int,
           name:             str,
           teams:            Dict[str, List[str]],
           player_locations: Dict[str, int],
           player_scores:    Dict[str, float],
           player_muds:      Dict[str, Dict[str, Union[None, int]]],
           cheese:           List[int],
           possible_actions: List[str],
           memory:           threading.local
         ) ->                str:

    """
        This function is called at every turn of the game and should return an action within the set of possible actions.
        You can access the memory you stored during the preprocessing function by doing memory.my_key.
        You can also update the existing memory with new information, or create new entries as memory.my_key = my_value.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * player_scores:    Scores for all players in the game.
            * player_muds:      Indicates which player is currently crossing mud.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * action: One of the possible actions, as given in possible_actions.
    """

    # [TODO] Write your turn code here and do not forget to return a possible action
    action= memory.route.pop() #on sort l'action à faire
    return action

#####################################################################################################################################################
######################################################## EXECUTED ONCE AT THE END OF THE GAME #######################################################
#####################################################################################################################################################

def postprocessing ( maze:             Union[numpy.ndarray, Dict[int, Dict[int, int]]],
                     maze_width:       int,
                     maze_height:      int,
                     name:             str,
                     teams:            Dict[str, List[str]],
                     player_locations: Dict[str, int],
                     player_scores:    Dict[str, float],
                     player_muds:      Dict[str, Dict[str, Union[None, int]]],
                     cheese:           List[int],
                     possible_actions: List[str],
                     memory:           threading.local,
                     stats:            Dict[str, Any],
                   ) ->                None:

    """
        This function is called once at the end of the game.
        It is not timed, and can be used to make some cleanup, analyses of the completed game, model training, etc.
        In:
            * maze:             Map of the maze, as data type described by PyRat's "maze_representation" option.
            * maze_width:       Width of the maze in number of cells.
            * maze_height:      Height of the maze in number of cells.
            * name:             Name of the player controlled by this function.
            * teams:            Recap of the teams of players.
            * player_locations: Locations for all players in the game.
            * player_scores:    Scores for all players in the game.
            * player_muds:      Indicates which player is currently crossing mud.
            * cheese:           List of available pieces of cheese in the maze.
            * possible_actions: List of possible actions.
            * memory:           Local memory to share information between preprocessing, turn and postprocessing.
        Out:
            * None.
    """

    # [TODO] Write your postprocessing code here
    pass

#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################




if __name__ == "__main__":

    # Map the function to the character
    players = [{"name": "dijkstra", "skin": "default", "preprocessing_function": preprocessing, "turn_function": turn}]

    # Customize the game elements
    config = {"maze_width": 31,
"maze_height": 29,
"cell_percentage": 80.0,
"wall_percentage": 60.0,
"mud_percentage": 20.0,
"mud_range": [4, 9],
"nb_cheese": 1,#41
"preprocessing_time": 0,
"turn_time": 0}

    # Start the game
    game = PyRat(players, **config)

    stats = game.start()

    # Show statistics
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################