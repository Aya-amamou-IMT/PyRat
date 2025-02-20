######################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
   greedy qui calcul la densite à chaque turn et se dirige vers le fromage le plus dense s'il n'y a pas d'autres fromages dans un rayon de 5 cases. De plus, s'il n'y a pas de fromage plus dense qu'un autre alors il va juste au fromage le plus proche
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# Import PyRat
from pyrat import *

# External imports
import numpy

# Previously developed functions
import os
import sys
import dijstraeachturn2 as dj
import greedy_avec_density as grd



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


    # list of density
    density_values = grd.give_density(maze,maze_height, maze_width, player_locations[name], cheese)
    max_density = max(density_values) #find max density and its index
    index = density_values.index(max_density)
    #routing_table
    distances_to_explored_vertices, routing_table,cible=dj.dijkstra( player_locations[name],
               maze,
               [cheese[index]]
             )
    #find_route
    memory.route=dj.locations_to_actions(dj.find_route(routing_table,player_locations[name] ,cible ),maze_width)
    memory.cheese=cible




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



    #perform dijkstra and give the nearest target
    distances_to_explored_vertices,  routing_table,cible=dj.dijkstra(player_locations[name] ,maze,cheese)
    # if the nearest target is too far ( in more than 5 cases)
    if  distances_to_explored_vertices[cible]>5 :
            #calcul the density of all cheeses
            density_values = grd.give_density(maze,maze_height, maze_width, player_locations[name], cheese)
            #select the max density
            max_density = max(density_values)
            # if the max density is significative with more than one cheese in the delimited square we go to the cheese with max density
            if max_density>1/(len(cheese)):

                 index = density_values.index(max_density)

                 distances_to_explored_vertices, routing_table,cible=dj.dijkstra( player_locations[name],
               maze,
               [cheese[index]]
             )

                 memory.route=dj.locations_to_actions(dj.find_route(routing_table,player_locations[name] ,cible ),maze_width)
                 memory.cheese=cible
            #if all the cheese have the same density we just go to the nearest
            else:
                memory.route=dj.locations_to_actions(dj.find_route(routing_table,player_locations[name] ,cible ),maze_width)
                memory.cheese=cible
    #if the nearest target is not far we go to it
    else:
            memory.route=dj.locations_to_actions(dj.find_route(routing_table,player_locations[name] ,cible ),maze_width)
            memory.cheese=cible


    action= memory.route.pop()

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
    print(player_scores)
    # [TODO] Write your postprocessing code here
    pass

#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################

if __name__ == "__main__":
    # Map the functions to the character
    players = [{"name": "greedydensite", "preprocessing_function": preprocessing, "turn_function": turn}]
    # Customize the game elements
    config = {"maze_width": 31,
"maze_height": 29,
"cell_percentage": 80.0,
"wall_percentage": 10.0,
"mud_percentage": 10.0,
"mud_range": [4, 9],
"nb_cheese": 41,#41
"trace_length":1000,
"preprocessing_time": 0 ,
"synchronous":True,
"turn_time": 0}
    # Start the game
    game = PyRat(players, **config)
    stats = game.start()
    # Show statistics
    print(stats)
#################################################################################################################
#################################################################################################################

#####################################################################################################################################################
#####################################################################################################################################################