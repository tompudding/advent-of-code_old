import re
import math

translation = ''.maketrans('#. ','100')

def parse_row(line):
    return int(line.translate(translation), 2)

def flip_horizontal(lines):
    return lines[0:1] + [line[::-1] for line in lines[1:]]

def flip_vertical(lines):
    return lines[0:1] + lines[1:][::-1]

def bit_reverse(n, width):
    format = '{num:0%db}' % width
    return int(format.format(num=n)[::-1],2)

class Tile:
    def __init__(self, lines, flipped_horiz=False, flipped_vertical=False):
        self.id = int(re.match('Tile (\d+):',lines[0]).groups()[0])

        self.width = len(lines[1])
        self.height = len(lines)-1
        self.flipped_horiz=flipped_horiz
        self.flipped_vertical=flipped_vertical

        self.rows = [parse_row(line) for line in lines[1:]]

        self.set_edges()

    def set_edges(self):
        self.top = self.rows[0]
        self.bottom = bit_reverse(self.rows[-1], self.width)
        self.left = sum((((self.rows[i] & (1 << (self.width-1))) >> (self.width - 1- i)) for i in range(self.width)))
        self.right = sum((((self.rows[i] & 1) << (self.width -1 -i)) for i in range(self.width)))
        #self.right = sum((((self.rows[i] & 1) << (i)) for i in range(self.width)))

        self.edges = [self.top, self.right, self.bottom, self.left]

    def rotate(self, n):
        # The top row will be all the MSBs of the rows
        new_rows = []

        new_row = 0
        for bit in range(self.width-1, -1, -1):
            new_row = 0
            for row in self.rows[::-1]:
                new_row <<= 1
                new_row |= ((row >> bit) & 1)
            new_rows.append(new_row)

        self.rows = new_rows
        self.set_edges()

    def __repr__(self):
        out = [f'Tile {self.id}:']
        for row in self.rows:
            format = '{row:0%db}' % self.width
            out.append(format.format(row=row))
        out.append('')
        for name in ('top','right','bottom','left'):
            value = getattr(self, name)
            out.append(f'{name:6s} : {value:010b}')
        out.append('')
        out.append(f'{self.flipped_horiz=} {self.flipped_vertical=}')
        print('')
        return '\n'.join(out)


class Grid(Tile):
    monster_pattern = ['                  # ',
                       '#    ##    ##    ###',
                       ' #  #  #  #  #  #   ']
    def __init__(self, tiles):

        self.rows = []

        tile_height = tiles[0][0].height
        tile_width = tiles[0][0].width
        n_mask = (1 << (tile_width - 2))-1

        self.width = (tile_width-2) * len(tiles)
        self.height = (tile_height-2) * len(tiles[0])
        print(f'Grid width = {self.width} height = {self.height}')

        for y in range(len(tiles[0])):
            for line_y in range(1, tile_height - 1):
                num = 0
                for col in tiles:
                    num <<= (tile_width - 2)
                    num |= (col[y].rows[line_y] >> 1) & n_mask

                self.rows.append(num)

        self.monster_bits = [parse_row(row) for row in self.monster_pattern]
        self.total_bits = sum(f'{row:b}'.count('1') for row in self.rows)
        self.total_monster_bits = sum(f'{row:b}'.count('1') for row in self.monster_bits)

    def flip_vertical(self):
        self.rows = self.rows[::-1]

    def count_monsters(self):
        count = 0
        roughness = 0

        #Can sea monster overlap? If not roughness is easy to calculate. Let's do that

        for row_num in range(self.height - len(self.monster_bits)):
            for x in range(self.width - len(self.monster_pattern[0])):
                for i,monster_row in enumerate(self.monster_bits):
                    if monster_row != ((self.rows[row_num + i] >> x) & monster_row):
                        break
                else:
                    count += 1

        return count, self.total_bits - count*self.total_monster_bits


    def get_roughness(self):
        #Find a configuration where there are some monsters. There's a bit of redundancy here
        for horiz in (0,1):
            for rotate in range(4):
                n, roughness = self.count_monsters()

                if n:
                    print(f'Got {n} matches')
                    return roughness
                self.rotate(1)
            self.flip_vertical()

    def __repr__(self):
        out = []

        for row in self.rows:
            format = '{row:0%db}' % self.width
            out.append(format.format(row=row))
        return '\n'.join(out)



with open('challenge_20','r') as file:
    data = file.read().split('\n\n')

data = [text.split('\n') for text in data]
tiles_by_id = {}
tiles = [Tile(text) for text in data]

num_tiles = len(tiles)
grid_width = grid_height = int(math.sqrt(num_tiles))
if grid_width * grid_height != num_tiles:
    raise Exception(f'Bad number of tiles {num_tiles}')

for text in data:
    tiles.append(Tile(flip_horizontal(text), flipped_horiz=True))
    tiles.append(Tile(flip_vertical(text), flipped_vertical=True))

edges = {}

def is_unknown(edge):
    return len({tile.id for tile in edges[edge]}) == 1

def num_unknown(tile):
    return len([edge for edge in tile.edges if is_unknown(edge)])

for tile in tiles:
    try:
        tiles_by_id[tile.id].append(tile)
    except KeyError:
        tiles_by_id[tile.id] = [tile]
    for edge in tile.edges:
        try:
            edges[edge].append(tile)
        except KeyError:
            edges[edge] = [tile]

product = 1
corners = {}
for tile in tiles:
    if num_unknown(tile) == 2:
        # We can start with any corner, it shouldn't matter
        corners[tile.id] = tile


#We now need a set of corners with consistent unknown edges
corners = corners.values()
for corner in corners:
    product *= corner.id

print(f'Part 1: {product}')

#Now we actually need to care about the rest of the tiles, so let's lay them out
tile_config = {}
tiles_used = {}
grid = [[None for x in range(grid_width)] for y in range(grid_height)]

#we need to rotate the corner piece until it's got its unknown edges as top and left
while not (is_unknown(corner.top) and is_unknown(corner.left)):
    corner.rotate(1)

print(f'Chosen corner top left {corner.id}')

for y in range(grid_height):
    for x in range(grid_width):
        if x == y == 0:
            grid[x][y] = corner
            continue

        above = grid[x][y-1] if y > 0 else None
        to_left = grid[x-1][y] if x > 0 else None
        to_right = grid[x+1][y] if x < grid_width-1 else None
        below = grid[x][y+1] if y < grid_height-1 else None

        if x == 0:
            #At the start of the row we need to match above us, and unknown to the left
            candidates = [tile for tile in edges[bit_reverse(above.bottom, above.width)] if tile.id != above.id]
            tile = candidates[0]
            while tile.top != bit_reverse(above.bottom, above.width):
                tile.rotate(1)
        else:
            candidates = [tile for tile in edges[bit_reverse(to_left.right, to_left.height)] if tile.id != to_left.id]
            tile = candidates[0]
            while tile.left != bit_reverse(to_left.right, to_left.height):
                tile.rotate(1)

        grid[x][y] = tile

grid = Grid(grid)

roughness = grid.get_roughness()

print(f'Part 2 : {roughness}')
