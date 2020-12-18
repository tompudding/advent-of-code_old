import re

def intify(part):
    return int(part) if part.isdigit() else part

def parse(input):
    # we want to return an array of things that are numbers, parens or operators
    out = [intify(part) for part in re.findall('\d+|\+|\(|\)|\*',input)]
    return out

def multiply(a, b):
    return a * b

def add(a, b):
    return a + b

class Expression:
    def __init__(self, parts):
        # We collapse any parts in brackets
        collapsed = []
        pos = 0

        while pos < len(parts):
            part = parts[pos]
            pos += 1
            if part != '(':
                collapsed.append(part)
                continue
            depth = 1
            for j in range(pos, len(parts)):
                other_part = parts[j]

                if other_part == '(':
                    depth += 1
                elif other_part == ')':
                    depth -= 1

                    if depth == 0:
                        collapsed.append(self.__class__(parts[pos:j]).evaluate())
                        pos = j+1
                        break

        # Now collapsed should just be numbers and operators
        self.operators = []
        self.values = []

        for part in collapsed:
            if part == '*':
                self.operators.append(multiply)
            elif part == '+':
                self.operators.append(add)
            else:
                self.values.append(part)

        self.parts = collapsed

    def evaluate(self):
        current = self.values[0]

        for value, operator in zip(self.values[1:], self.operators):
            current = operator(current, value)

        return current

class AdvancedExpression(Expression):
    def evaluate(self):
        # We start with a pass evaluating the additions
        product_values = []
        current = self.values[0]

        for value, operator in zip(self.values[1:], self.operators):
            if operator == multiply:
                product_values.append(current)
                current = value
            else:
                current = operator(current, value)

        product_values.append(current)

        #then we just multiply everything together
        total = 1
        for value in product_values:
            total *= value
        return total


with open('challenge_18','r') as file:
    data = [line.strip() for line in file]

total = 0
for line in data:
    value = Expression(parse(line)).evaluate()
    total += value
    print(f'{line} = {value}')

print(f'Part 1 Total = {total}')

total = 0
for line in data:
    value = AdvancedExpression(parse(line)).evaluate()
    total += value
    print(f'{line} = {value}')

print(f'Part 2 Total = {total}')
