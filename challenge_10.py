import os
import sys

chargers = [0]
with open('challenge_10','r') as file:
    for line in file:
        jolt = int(line.strip())
        chargers.append(jolt)

chargers.sort()

chargers.append(chargers[-1]+3)

print(chargers)

diffs = [0, 0, 0, 0]
for i in range(len(chargers)-1):
    diff = chargers[i+1] - chargers[i]
    try:
        diffs[diff] += 1
    except KeyError:
        continue

print(diffs)
print(diffs[1]*diffs[3])

#Part 2...

count_cache = {}
def next_part(pos):
    if pos in count_cache:
        return count_cache[pos]

    count = 0
    for next_pos in range(pos+1, len(chargers)):
        if chargers[next_pos] - chargers[pos] <= 3:
            #current_chain = chain + (next_pos,)
            if next_pos == len(chargers)-1:
                #this is the end!
                return count +1
            count += next_part(next_pos)
    count_cache[pos] = count
    print(f'{pos=} {count=}')
    return count


print(next_part(0))
