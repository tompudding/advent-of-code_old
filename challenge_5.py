import os
import sys
import string

translation = ''.maketrans('FBLR','0101')
max_id = 0
seats = set(range(1<<10))
taken = set()
with open('challenge_5','r') as file:
    for line in file:
        id = int(line.strip().translate(translation),2)
        row = id >> 3
        col = id & 0x7

        if id > max_id:
            max_id = id
        taken.add(id)

for seat in seats - taken:
    row = seat >> 3
    col = seat & 0x7
    print(seat, row, col)
