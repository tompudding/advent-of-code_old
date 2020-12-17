import numpy

class Range:
    def __init__(self, a, b):
        self.min = a
        self.max = b

    def items(self, extra=0):
        for n in range(self.min-extra, self.max+extra):
            yield n

    def expand(self, extra):
        self.min -= extra
        self.max += extra

class Extents:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def expand(self, extra):
        for item in self.x, self.y, self.z:
            item.expand(extra)

class Extents4D:
    def __init__(self,x,y,z,w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def expand(self, extra):
        for item in self.x, self.y, self.z, self.w:
            item.expand(extra)

class Grid:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            data = file.readlines()

        self.grid = numpy.zeros([70,70,70])
        width = 0

        for y,line in enumerate(data):
            line = line.strip()
            width = len(line)
            for x, char in enumerate(line):
                self.grid[x][y][0] = 0 if '.' == char else '1'

        self.extents = Extents(x=Range(0, width),
                               y=Range(0, len(data)),
                               z=Range(0, 1))

    def active(self, x, y, z):
        on = self.grid[x][y][z]
        total = -on

        for a in (-1,0,1):
            for b in (-1, 0, 1):
                for c in (-1, 0, 1):
                    total += self.grid[x+a][y+b][z+c]

        if on:
            if 2 <= total <= 3:
                return 1
            return 0

        else:
            if total == 3:
                return 1
            return 0

    def step(self):

        new_grid = numpy.array(self.grid, copy=True)

        for x in self.extents.x.items(extra=1):
            for y in self.extents.y.items(extra=1):
                for z in self.extents.z.items(extra=1):
                    new_grid[x][y][z] = self.active(x, y, z)

        self.grid = new_grid
        self.extents.expand(1)

    def __repr__(self):
        lines = []
        for z in self.extents.z.items():
            lines.append(f'z={z}')

            for y in self.extents.y.items():
                line = ['#' if self.grid[x][y][z] else '.' for x in self.extents.x.items()]
                lines.append(''.join(line))

            lines.append('')

        return '\n'.join(lines)

    def count(self):
        total = 0
        for x in self.extents.x.items():
            for y in self.extents.y.items():
                for z in self.extents.z.items():
                    total += self.grid[x][y][z]

        return total


class Grid4D:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            data = file.readlines()

        self.grid = numpy.zeros([70,70,70,70])
        width = 0

        for y,line in enumerate(data):
            line = line.strip()
            width = len(line)
            for x, char in enumerate(line):
                self.grid[x][y][0][0] = 0 if '.' == char else '1'

        self.extents = Extents4D(x=Range(0, width),
                                 y=Range(0, len(data)),
                                 z=Range(0, 1),
                                 w=Range(0, 1),
        )

    def active(self, x, y, z, w):
        on = self.grid[x][y][z][w]
        total = -on

        for a in (-1,0,1):
            for b in (-1, 0, 1):
                for c in (-1, 0, 1):
                    for d in (-1, 0, 1):
                        total += self.grid[x+a][y+b][z+c][w+d]

        if on:
            if 2 <= total <= 3:
                return 1
            return 0

        else:
            if total == 3:
                return 1
            return 0

    def step(self):

        new_grid = numpy.array(self.grid, copy=True)

        for x in self.extents.x.items(extra=1):
            for y in self.extents.y.items(extra=1):
                for z in self.extents.z.items(extra=1):
                    for w in self.extents.w.items(extra=1):
                        new_grid[x][y][z][w] = self.active(x, y, z, w)

        self.grid = new_grid
        self.extents.expand(1)

    def __repr__(self):
        lines = []
        for z in self.extents.z.items():
            lines.append(f'z={z}')

            for y in self.extents.y.items():
                line = ['#' if self.grid[x][y][z] else '.' for x in self.extents.x.items()]
                lines.append(''.join(line))

            lines.append('')

        return '\n'.join(lines)

    def count(self):
        total = 0
        for x in self.extents.x.items():
            for y in self.extents.y.items():
                for z in self.extents.z.items():
                    for w in self.extents.w.items():
                        total += self.grid[x][y][z][w]

        return total

grid = Grid('challenge_17')

for i in range(6):
    grid.step()
    count = grid.count()
    print(f'{i} {count}')
print(f'Part 1 : {count}')

grid = Grid4D('challenge_17')

for i in range(6):
    grid.step()
    count = grid.count()
    print(f'{i} {count}')

print(f'Part 2 : {count}')
