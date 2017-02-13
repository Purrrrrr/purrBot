import pprint
pp = pprint.PrettyPrinter(indent=2)

pprint = pp.pprint

def get_pos_in(state, *args):
    return position_to_location(get_in(state, *args))

def get_in(state, *args):
    if not args: return state
    return get_in(state[args[0]], *args[1:])

def get_player_location(state):
    pos = get_in(state, 'playerState', 'position')
    return position_to_location(pos)

def position_to_location(pos): return (pos['x'], pos['y'])

def get_tile_at(state, location):
    x, y = location
    map = get_in(state, 'gameState', 'map', 'tiles')
    return map[y][x]

def delta(loc, delta):
    return (loc[0] + delta[0], loc[1] + delta[1])

def get_moved_location(location, action):
    return delta(location, directions[action])

def reverse(delta):
    return (-delta[0], -delta[1])

def get_moved_location(location, action):
    return delta(location, directions[action])

def get_legal_actions(state, location):
    item_locs = (position_to_location(item['position'])
            for item in get_in(state, 'gameState', 'items'))
    return ['PICK'] if location in item_locs else []

def get_legal_moves(state, location):
    return get_legal_directions(state, location) + \
            get_legal_actions(state, location)

directions = {'UP': (0, -1),
              'DOWN': (0, 1),
              'LEFT': (-1, 0),
              'RIGHT': (1, 0)}

def get_legal_directions(state, location):
    return [direction[0]
            for direction in directions.viewitems()
            if get_tile_at(state, delta(location, direction[1])) != 'x']


def distance(state, loc_from, loc_to):
    return len(get_path_to(state, loc_from, loc_to))

def get_path_to(state, loc_from, loc_to):
    visited = set([loc_from])
    queue = [loc_from]
    fromLoc = {loc_from: None}

    while loc_to not in visited and len(queue) > 0:
        cur = queue.pop(0)
        candidates = [(action, get_moved_location(cur, action)) for action in get_legal_directions(state, cur)]
        for (action, l) in candidates:
            if l in queue or l in visited:
                continue
            fromLoc[l] = action
            queue.append(l)
            visited.add(l)

    list = []
    pos = loc_to
    while True:
        action = fromLoc[pos]
        if not action:
            break
        pos = delta(pos, reverse(directions[action]))
        list.insert(0, action)

    return list
