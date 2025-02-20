#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
   greedy qui va au fromage le plus dense à chaque turn
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
import dijstra2 as dj



#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def density (graph , mazeheight, mazewidth : int ,cheese : list [int] , pos_cheese:int ):#cette fonction associe une densité a un fromage particulier
    nbr_c=mazewidth #take the maze width
    nbr_l=mazeheight#take the maze height
    #find the position of the cheese
    l=pos_cheese // nbr_c
    c=pos_cheese % nbr_c
    #initiate number of cheese in proximity
    nbr_cheese=0
    for i in cheese :
        # We count the number of cheese in the square of 7x7 with on the mid a cheese
        if (i // nbr_c in range(max([l-3,0]),min([l+4,nbr_l]) )) and (i % nbr_c in range(max([c-3,0]),min([c+4,nbr_c])) ) :
            nbr_cheese+=1
    dens=nbr_cheese/len(cheese) #calcul of density
    return dens






def give_density ( graphique: Union[numpy.ndarray, Dict  [int, Dict[int, int]]],mazeheight,
                  mazewidth : int ,
                 current_vertex: int,
                 cheese : List
                 ) :
    """
 Fonction qui associe un score à chaque frommage .
 Dans:
 * graphe : graphe contenant les sommets.
 * current_vertex : emplacement actuel du joueur dans le labyrinthe.

 Dehors:
 * densities : densité  attribués aux frommages(cheese ).
 * routing_table : Table de routage obtenue à partir du sommet actuel.
    """
    densities=[] #initiate the list of density

    for i in range(len(cheese)):
        d=density(graphique,mazeheight,mazewidth,cheese,cheese[i])
        densities.append(d)
    #give a list with the density of all the cheeses.
    return densities





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
    memory.route=dj.locations_to_actions(greedy_1(maze,maze_width,player_locations[name],cheese),maze_width)

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

#################################################################################################################
###################################################### GO ! #####################################################
#################################################################################################################
if __name__ == "__main__":
    # Map the functions to the character
    players = [{"name": "greedy 1", "preprocessing_function": preprocessing, "turn_function": turn}]
    # Customize the game elements
    config = {"maze_width": 15,
              "maze_height": 11,
              "mud_percentage": 40.0,
              "nb_cheese": 21,
              "trace_length": 1000,
              "preprocessing_time":0,
              "turn_time":0.1}
    # Start the game
    game = PyRat(players, **config)
    stats = game.start()
    # Show statistics
    print(stats)
#################################################################################################################
#################################################################################################################

#####################################################################################################################################################
#####################################################################################################################################################
