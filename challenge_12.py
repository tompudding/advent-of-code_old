import sys
import cmath
import math

class Ship:
    def __init__(self):
        self.position = [0,0]
        self.direction = 0

        self.process = {
            'F' : self.go_forward,
            'N' : self.go_north,
            'S' : self.go_south,
            'E' : self.go_east,
            'W' : self.go_west,
            'L' : self.turn_left,
            'R' : self.turn_right,
        }

    def move(self, instruction, amount):
        initial_pos = self.position[:]
        initial_dir = (self.direction * 180) / math.pi
        self.process[instruction](amount)
        final_dir = (self.direction * 180) / math.pi
        print(f'Process {instruction} start_pos=({initial_pos[0]},{initial_pos[1]}) end_pos=({self.position[0]},{self.position[1]}) end_dir={final_dir}')

    def go_forward(self, amount):
        vector = cmath.rect(amount, self.direction)
        self.position[0] += round(vector.real)
        self.position[1] += round(vector.imag)

    def go_north(self, amount):
        self.position[1] += amount

    def go_south(self, amount):
        self.position[1] -= amount

    def go_east(self, amount):
        self.position[0] += amount

    def go_west(self, amount):
        self.position[0] -= amount

    def turn_left(self, amount):
        self.direction += (amount*math.pi) / (180)

    def turn_right(self, amount):
        self.direction -= (amount*math.pi) / (180)

    def get_manhattan(self):
        return sum((abs(x) for x in self.position))

class ShipPart2(Ship):
    def __init__(self):
        super().__init__()
        self.waypoint = [10,1]

    def go_forward(self, amount):
        self.position[0] += (self.waypoint[0] * amount)
        self.position[1] += (self.waypoint[1] * amount)

    def go_north(self, amount):
        self.waypoint[1] += amount

    def go_south(self, amount):
        self.waypoint[1] -= amount

    def go_west(self, amount):
        self.waypoint[0] -= amount

    def go_east(self, amount):
        self.waypoint[0] += amount

    def turn_left(self, amount):
        distance, angle = cmath.polar(self.waypoint[0] + self.waypoint[1]*1j)
        vector = cmath.rect(distance, angle + ((amount * math.pi) / 180))
        self.waypoint = [round(vector.real),round(vector.imag)]

    def turn_right(self, amount):
        return self.turn_left(-amount)

    def move(self, instruction, amount):
        super().move(instruction, amount)

instructions = []

with open('challenge_12','r') as file:
    for line in file:
        ins, amount = line[0], int(line[1:].strip())

        instructions.append((ins, amount))

ship = Ship()

for instruction, amount in instructions:
    ship.move(instruction, amount)

print(f'Part 1 Manhattan distance: {ship.get_manhattan()}')

ship = ShipPart2()

for instruction, amount in instructions:
    ship.move(instruction, amount)

print(f'Part 2 Manhattan distance: {ship.get_manhattan()}')
