from kaggle_environments.envs.halite.helpers import *

ship_states = {}

def agent(obs, config):

    size = config.size
    board = Board(obs, config)
    me = board.current_player

    # if len(me.shipyards) == 0:


    for ship in me.ships:
        if ship.next_action == None:
            if len(me.shipyards) == 0:
                ship.next_action = ShipAction.CONVERT
            if len(me.shipyards) > 0 and len(me.ships) < 1:
                me.shipyards[0].next_action = ShipyardAction.SPAWN
                

            ship.next_action = ShipAction.NORTH
    
    if board.step == 1:
        print(obs)

    return me.next_actions