import os
import sys
import string

numbers = []
combinations = {}
pos = 0
preamble_length = 25

with open('challenge_9','r') as file:
    for line in file:
        numbers.append(int(line.strip()))

def part_1():
    for pos in range(preamble_length):
        for other_pos in range(pos+1, preamble_length):
            t = numbers[pos] + numbers[other_pos]
            try:
                combinations[t] += 1
            except KeyError:
                combinations[t] = 1

    for pos in range(preamble_length, len(numbers)):
        if numbers[pos] not in combinations:
            #print(f'Number {numbers[pos]} at line {pos} not a possible combination')
            return numbers[pos]
            break

        #strip the combinations from the one that's falling off
        for i in range(1, preamble_length):
            t = numbers[pos-preamble_length] + numbers[pos-i]
            #print(f'- {i=} {numbers[pos-preamble_length]} {numbers[pos-i]}')
            combinations[t] -= 1
            if combinations[t] == 0:
                del combinations[t]

        #add the combinations from the one that's coming in
        for i in range(1, preamble_length):
            t = numbers[pos] + numbers[pos - i]
            #print(f'+ {i=} {numbers[pos-preamble_length]} {numbers[pos-i]}')
            try:
                combinations[t] += 1
            except KeyError:
                combinations[t] = 1

def part_2(target):
    print(target)

    cumulative = []
    total = 0
    for number in numbers:

        cumulative.append(total)
        total += number
        #print(total)

    #print(cumulative)

    for i in range(len(cumulative)):
        for j in range(i+2, len(cumulative)):
            if cumulative[j] - cumulative[i] == target:
                #print(f'Position {i}, {j}')
                return min(numbers[i:j]) + max(numbers[i:j])

    return 4


target = part_1()

print(part_2(target))
