from kaggle_environments.envs.halite.helpers import *
from random import choice

# Returns best direction to move from one position (fromPos) to another (toPos)
# Example: If I'm at pos 0 and want to get to pos 55, which direction should I choose?
def getDirTo(fromPos, toPos, size):
    fromX, fromY = divmod(fromPos[0],size), divmod(fromPos[1],size)
    toX, toY = divmod(toPos[0],size), divmod(toPos[1],size)
    if fromY < toY: return ShipAction.NORTH
    if fromY > toY: return ShipAction.SOUTH
    if fromX < toX: return ShipAction.EAST
    if fromX > toX: return ShipAction.WEST

# Directions a ship can move
directions = [ShipAction.NORTH, ShipAction.EAST, ShipAction.SOUTH, ShipAction.WEST]

# Will keep track of whether a ship is collecting halite or carrying cargo to a shipyard
ship_states = {}


def agent(obs,config):
    
    size = config.size
    board = Board(obs, config)
    me = board.current_player
    
    
    board_halite = obs['halite']
    list_halite = []
    for i in range(size):
        temp_list = []
        for j in range(size):
            temp_list.append(board_halite[i+(j*21)])
        list_halite.append(temp_list)
    
    #TODO: add avoiding collision with my own ships and deterministic collisions with foreign

    if size%2 == 1:
        corner_size = int((size-1)/2)
    else:
        corner_size = int(size/2)
    
    max_halite_value = 0
    max_halite_pos = [corner_size/2, corner_size/2]
    for i in range(corner_size):
        for j in range(corner_size):
            if list_halite[i][j] > max_halite_value:
                max_halite_value = list_halite[i][j]
                max_halite_pos = [i,j]


    if board.step == 10:
        print(obs)
        print(list_halite)
        print("max halite value:{}, max halite pos:{}".format(max_halite_value, max_halite_pos))
        

    # If there are no ships, use first shipyard to spawn a ship.
    if len(me.ships) == 0 and len(me.shipyards) > 0:
        me.shipyards[0].next_action = ShipyardAction.SPAWN
    
    # if board.step == 100:
    #     print("check for position of shipyard")
    #     print(me.shipyards[0].position)
    #     print("new shippe to be spawned")
    #     if me.shipyards[0].position != me.ships[0].position:
    #         me.shipyards[0].next_action = ShipyardAction.SPAWN

    # If there are no shipyards, convert first ship into shipyard.
    if len(me.shipyards) == 0 and len(me.ships) > 0:
        # ship.next_action = directions[]
        me.ships[0].next_action = ShipAction.CONVERT
    
    for ship in me.ships:

        if ship.next_action == None:
            
            ### Part 1: Set the ship's state 
            if ship.halite < 100: # If cargo is too low, collect halite
                ship_states[ship.id] = "COLLECT"
            if ship.halite > 600: # If cargo gets very big, deposit halite
                ship_states[ship.id] = "DEPOSIT"


            ### Part 2: Use the ship's state to select an action
            if ship_states[ship.id] == "COLLECT":
                # If halite at current location running low, 
                # move to the adjacent square containing the most halite
                if ship.cell.halite < 100:
                    neighbors = [ship.cell.north.halite, ship.cell.east.halite, 
                                 ship.cell.south.halite, ship.cell.west.halite]
                    if max(neighbors) < 100:
                        direction = getDirTo(ship.position, max_halite_pos, size)
                        if direction: ship.next_action = direction
                    else:
                        best = max(range(len(neighbors)), key=neighbors.__getitem__)
                        ship.next_action = directions[best]
            if ship_states[ship.id] == "DEPOSIT":
                # Move towards shipyard to deposit cargo
                direction = getDirTo(ship.position, me.shipyards[0].position, size)
                if direction: ship.next_action = direction
        
        if board.step == 10:
            print("ship current position{}".format(ship.cell.position))
    return me.next_actions
