import os
import sys

class SeatType:
    FLOOR = '.'
    EMPTY = 'L'
    FULL = '#'


class Layout:
    def __init__(self, filename):
        self.seats = []
        self.seats_in_row = []
        self.width = 0
        self.height = 0

        if filename is None:
            return

        with open(filename, 'r') as file:
            for line in file:
                current_seats = set()
                current_row = []

                line = line.strip()
                if self.width and len(line) != self.width:
                    raise Exception('Bad line length')

                self.width = len(line)

                for i,c in enumerate(line):
                    if c == '.':
                        current_row.append(SeatType.FLOOR)
                    else:
                        current_seats.add(i)
                        current_row.append(c)

                self.seats.append(current_row)
                self.seats_in_row.append(current_seats)

        self.height = len(self.seats)

    def update_rule(self, col, row):
        neighbours_occupied = 0

        current = self.seats[row][col]
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if x == y == 0:
                    continue
                new_col = col + x
                new_row = row + y
                if new_col < 0 or new_row < 0:
                    continue
                try:
                    neighbour = self.seats[new_row][new_col]
                except IndexError:
                    continue
                neighbours_occupied += 1 if neighbour == SeatType.FULL else 0

        if current == SeatType.FULL:
            if neighbours_occupied >= 4:
                return SeatType.EMPTY
            else:
                return SeatType.FULL

        elif current == SeatType.EMPTY:
            if neighbours_occupied == 0:
                return SeatType.FULL
            else:
                return current

        print(col, row, current)
        raise Exception()

    def step(self):
        #We're going to create a new Layout which is this one stepped

        out = self.__class__(None)

        for row_num, row in enumerate(self.seats):
            #Make a row that's all floor
            new_row = ['.' for i in range(len(row))]

            for seat_pos in self.seats_in_row[row_num]:
                new_row[seat_pos] = self.update_rule(seat_pos, row_num)

            out.seats.append(new_row)
            out.seats_in_row.append(self.seats_in_row[row_num])

        out.width = self.width
        out.height = self.height

        return out

    def num_occupied(self):
        count = 0

        for row in self.seats:
            count += row.count(SeatType.FULL)

        return count

    def __repr__(self):
        out = [f'Layout dimensions {self.width} x {self.height}']

        for row in self.seats:
            out.append(''.join((item for item in row)))

        return '\n'.join(out)

    def __eq__(self, other):

        for i in range(len(self.seats)):
            if self.seats[i] != other.seats[i]:
                return False

        return True

class LayoutPart2(Layout):
    def update_rule(self, col, row):
        neighbours_occupied = 0
        current = self.seats[row][col]
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if x == y == 0:
                    continue

                for step in range(1,self.width):
                    new_col = col + x*step
                    new_row = row + y*step
                    if new_col < 0 or new_row < 0:
                        continue
                    try:
                        neighbour = self.seats[new_row][new_col]
                    except IndexError:
                        continue
                    if neighbour == SeatType.FLOOR:
                        continue
                    neighbours_occupied += 1 if neighbour == SeatType.FULL else 0
                    break

        if current == SeatType.FULL:
            if neighbours_occupied >= 5:
                return SeatType.EMPTY
            else:
                return SeatType.FULL

        elif current == SeatType.EMPTY:
            if neighbours_occupied == 0:
                return SeatType.FULL
            else:
                return current

        print(col, row, current)
        raise Exception()


def get_answers(layout):
    steps = 0

    while True:
        next_layout = layout.step()
        steps += 1
        #print(next_layout)
        if next_layout == layout:
            break
        layout = next_layout

    return layout.num_occupied(), steps



#layout = Layout('challenge_11')
#num_occupied, steps = get_answers(layout)
#print(f'part one results: {num_occupied=} after {steps=}')

layout = LayoutPart2('challenge_11')
num_occupied, steps = get_answers(layout)
print(f'part one results: {num_occupied=} after {steps=}')
