with open('challenge_16','r') as file:
    data = [line.strip() for line in file]

class RangeRule:
    def __init__(self, name, desc, num):
        self.ranges = []
        self.num = num
        self.name = name
        for rng in desc.split(' or '):
            start, end = (int(n) for n in rng.split('-'))
            self.ranges.append( (start, end) )

    def check(self, value):
        for rule in self.ranges:
            if value >= rule[0] and value <= rule[1]:
                return True
        return False


rules = {}

for pos in range(len(data)):
    line = data[pos]
    if not line:
        break
    name, rest = line.split(': ')
    ranges = RangeRule(name, rest, pos)
    rules[name] = ranges

for pos in range(pos+2, len(data)):
    line = data[pos]
    if not line:
        break
    #ignore my ticket for now
    my_ticket = [int(v) for v in line.split(',')]

valid_tickets = []

error_rate = 0
for pos in range(pos+2, len(data)):
    line = data[pos]
    if not line:
        break
    values = [int(v) for v in line.split(',')]
    reject_ticket = False
    for value in values:
        valid = False
        for name, rule in rules.items():
            if rule.check(value):
                valid = True
        if not valid:
            reject_ticket = True
            print(f'{value} fails all checks')
            error_rate += value
    if not reject_ticket:
        valid_tickets.append(values)

print(f'Part 1 error rate : {error_rate}')

for name, rule in rules.items():
    rule.possible = set(range(len(valid_tickets[0])))


# walk the tickets at each position. If any of them fail a rule, then that rule cannot be at that position
for pos in range(len(valid_tickets[0])):
    for name, rule in rules.items():
        for i,ticket in enumerate(valid_tickets):
            if rule.name == 'wagon':
                print(f'Check ticket {i} position {pos} ({ticket[pos]}) for rule {name}')
            if not rule.check(ticket[pos]):
                if rule.name == 'wagon':
                    print(f'Bad so remove {pos} from {rule.name}')
                rule.possible.remove(pos)
                break

# Now we can do a back-substitution stage. If any n rules have exactly possibilities between them, we can remove
# them from all other rules. Let's just do it with n=1 first in case that's sufficient
changed = True
while changed:
    changed = False
    for rule in rules.values():
        if len(rule.possible) != 1:
            continue
        for other in rules.values():
            if other is rule:
                continue
            if len(other.possible & rule.possible) == 0:
                continue
            changed = True
            other.possible -= rule.possible

mapping = {}

for name, rule in rules.items():
    if len(rule.possible) != 1:
        raise Exception('You need to implement more complicated logic!')

    rule.num = rule.possible.pop()

product = 1
for name, rule in rules.items():
    if rule.name.startswith('departure'):
        print(f'Multiply by {rule.name} {my_ticket[rule.num]}')
        product *= my_ticket[rule.num]

print(f'Part 2: {product}')
