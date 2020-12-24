def east(pos):
    return (pos[0] + 1, pos[1])


def west(pos):
    return (pos[0] - 1, pos[1])


def south_east(pos):
    return (pos[0] + 1 if (pos[1] & 1) else pos[0], pos[1] + 1)


def south_west(pos):
    return (pos[0] if (pos[1] & 1) else pos[0] - 1, pos[1] + 1)


def north_west(pos):
    return (pos[0] if (pos[1] & 1) else pos[0] - 1, pos[1] - 1)


def north_east(pos):
    return (pos[0] + 1 if (pos[1] & 1) else pos[0], pos[1] - 1)


directions = {"se": south_east, "sw": south_west, "nw": north_west, "ne": north_east, "w": west, "e": east}


def flip(tiles, path):
    pos = (0, 0)
    while path:
        try:
            handler = directions[path[:2]]
            path = path[2:]
        except KeyError:
            handler = directions[path[:1]]
            path = path[1:]
        pos = handler(pos)
    print(f"Flipping tile at position {pos}")

    if pos in tiles:
        tiles.pop(pos)
    else:
        tiles[pos] = 1


def step(tiles):
    # We just need to analyse every set tile, and the neighbour of every set tile
    neighbours = set()
    new_tiles = {}

    for set_tile in tiles:
        tile_neighbours = {dir(set_tile) for dir in directions.values()}
        count = sum([neighbour in tiles for neighbour in tile_neighbours])
        if 1 <= count <= 2:
            # this will remain set
            new_tiles[set_tile] = 1
        neighbours |= tile_neighbours

    # Neighbours is now the set of tiles that border a set tile and thus may get turned on
    for unset_tile in neighbours:
        if unset_tile in tiles:
            # This one was actually set
            continue
        tile_neighbours = {dir(unset_tile) for dir in directions.values()}
        count = sum([neighbour in tiles for neighbour in tile_neighbours])
        if count == 2:
            new_tiles[unset_tile] = 1

    return new_tiles


with open("challenge_24", "r") as file:
    paths = [line.strip() for line in file.readlines()]

tiles = {}

for path in paths:
    flip(tiles, path)

total_black = sum(tiles.values())
print(f"Part 1 : {total_black}")

for day in range(100):
    tiles = step(tiles)

    print(f"Day {day+1}: {sum(tiles.values())}")
