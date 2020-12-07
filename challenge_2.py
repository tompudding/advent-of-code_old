import sys
import os

count = 0
count_2 = 0
with open('challenge_2','r') as file:
    for line in file:
        bounds, letter, data = line.split()
        a,b = (int(x) for x in bounds.split('-'))

        letter = letter[:1]

        if a <= data.count(letter) <= b:
            count +=1

        match = 1 if data[a-1] == letter else 0
        match += 1 if data[b-1] == letter else 0

        if match == 1:
            count_2 += 1

print(count)
print(count_2)
