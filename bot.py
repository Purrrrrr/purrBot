import random
from common import *

def move(state):
    loc = get_player_location(state)
    possible_moves = get_legal_moves(state, loc)
    #pprint(state)
    my_move = run_logic(state)
    print("Currently at %s, possible moves are %s, going to do %s" %
            (loc, possible_moves, my_move))
    return my_move

def run_logic(state):
    loc = get_player_location(state)
    money = get_in(state, "playerState", "money")
    health = get_in(state, "playerState", "health")
    weapons = get_in(state, "playerState", "usableItems")
    items = get_in(state, "gameState", "items")
    enemies = [p for p in get_in(state, "gameState", "players") if player_pos(p) != loc]
    buyables = [item for item in items if item["price"] <= money]
    
    """
    if len(weapons):
        print "Fire!"
        return "USE"
    """
    
    if len(buyables):
        item = max(buyables, key=to_item_value(state))
        return try_to_buy(state, item)

    if health <= 50:
        print "Exit!"
        return try_to_exit(state)
        
    if len(enemies):
        nearest = sorted(enemies, key=lambda enemy: distance(state, loc, get_pos_in(p, "position")))
        return go_to(state, player_pos(nearest))

    return go_to(state, get_player_location(state))

def player_pos(player):
    return get_pos_in(player, "position")

def to_item_value(state):
    def val(item):
        return item_value(state, item)
    return val

def item_value(state, item):
    loc = get_player_location(state)
    dest = get_pos_in(item, "position")
    dist = distance(state, loc, dest)
    return (get_in(item, "discountPercent") + 1) / max(1, dist)

def try_to_buy(state, item):
    loc = get_player_location(state)
    dest = get_pos_in(item, "position")

    if loc == dest:
        return 'PICK'
    else:
        return go_to(state, dest)


def try_to_exit(state):
    exit_loc = get_exit_location(state)
    return go_to(state,exit_loc)

def get_exit_location(state):
    return get_pos_in(state, "gameState",  "map", "exit")

def go_to(state, dest):
    loc = get_player_location(state)

    path = get_path_to(state, loc, dest)
    try:
        path = get_path_to(state, loc, dest)
        if len(path):
            return path[0]
        else:
            print "??"
            return move_random(state)
    except:
        print "!!?!"
        return move_random(state)

def move_random(state):
    loc = get_player_location(state)
    possible_moves = get_legal_moves(state, loc)
    return random.choice(possible_moves)

def move2(state):
    loc = get_player_location(state)
    possible_moves = get_legal_moves(state, loc)
    if 'PICK' in possible_moves: my_move = 'PICK'
    else: my_move = random.choice(possible_moves)

    return my_move

