import sys
import os

tiles = []

with open('challenge_3','r') as file:
    for line in file:
        tiles.append(line.strip())

def get_count(slope_x, slope_y):
    pos = [0, 0]
    tree_count = 0

    while pos[0] < len(tiles):
        if tiles[pos[0]][pos[1]] == '#':
            tree_count += 1
        pos[0] += slope_y
        pos[1] = (pos[1] + slope_x) % len(tiles[0])
    return tree_count

total = 1
for slope in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
    count = get_count(*slope)
    total *= count

print(total)
