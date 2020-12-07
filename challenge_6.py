import os
import sys

group = []
groups = []
with open('challenge_6','r') as file:
    for line in file:
        q = line.strip()
        if not q:
            groups.append(group)
            group = []
        else:
            group.append(set(q))

groups.append(group)

total = 0

for group in groups:
    all_questions = set('abcdefghijklmnopqrstuvwxyz')

    for person in group:
        all_questions &= person

    total += len(all_questions)

print(total)
