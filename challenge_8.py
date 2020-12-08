import os
import sys
import string

class Instruction:
    def __init__(self, instruction, operand):
        self.instruction = instruction
        self.operand = operand
        self.count = 0

program = []

with open('challenge_8','r') as file:
    for line in file:
        instruction, operand = line.strip().split(maxsplit=1)
        operand = int(operand)
        program.append(Instruction(instruction, operand))


pc = 0
acc = 0

while pc < len(program):
    ins = program[pc]
    ins.count += 1
    if ins.count > 1:
        print(f'{pc=} {acc=}')
        break
    if ins.instruction == 'nop':
        pc += 1
        continue

    elif ins.instruction == 'acc':
        acc += ins.operand
        pc += 1
        continue

    elif ins.instruction == 'jmp':
        pc += ins.operand
        continue

#part 2

#Start with a pass which puts jump targets in
# targets = {}
# jumps = {}

# for pc in range(0, len(program)):
#     if program[pc].instruction == 'jmp':
#         target = pc + program[pc].operand
#         try:
#             targets[target].append(pc)
#         except KeyError:
#             targets[target] = [pc]
#         jumps[pc] = target

# pc = len(program)-1
# total = 1

# while pc >= 0:
#     #How many ways are there to get to this instruction?
#     if pc not in targets:
#         print(f'{pc=} just 1')
#     else:
#         print(f'{pc=} jumps={len(targets[pc])} {targets[pc]} {total=}')
#         total *= len(targets[pc])


#     pc -= 1


#We're going to execute the program once, and every time we see a nop or a jmp execute it the other way and see if it terminates

def terminates(pc, acc):
    counts = [0 for ins in program]
    while pc < len(program):
        ins = program[pc]
        counts[pc] += 1
        if counts[pc] > 1:
            return False
        if ins.instruction == 'nop':
            pc += 1
            continue

        elif ins.instruction == 'acc':
            acc += ins.operand
            pc += 1
            continue

        elif ins.instruction == 'jmp':
            pc += ins.operand
            continue
    print(f'{acc=}')
    return True

pc = 0
acc = 0

for ins in program:
    ins.count = 0

while pc < len(program):
    ins = program[pc]
    print(pc)
    ins.count += 1
    if ins.count > 1:
        print(f'Error {pc=} {acc=}')
        break
    if ins.instruction in ['nop','jmp']:
        other = 'nop' if ins.instruction == 'jmp' else 'jmp'
        old = ins.instruction
        ins.instruction = other

        if terminates(pc, acc):
            print(f'Terminates at {pc}')
            break

        ins.instruction = old

    if ins.instruction == 'nop':
        pc += 1
        continue

    elif ins.instruction == 'acc':
        acc += ins.operand
        pc += 1
        continue

    elif ins.instruction == 'jmp':
        pc += ins.operand
        continue

#Now we just need to run the program normally
terminates(0, 0)
