import os
import sys

numbers = {}

with open('challenge_1','r') as file:
    data = [int(n.strip()) for n in file.readlines()]

#data.sort()
numbers = set(data)

data.sort()

def get_sum(total):
    for n in data:
        if total-n in numbers:
            return n, total-n

a,b = get_sum(2020)
print(a*b)

for n in data:
    result = get_sum(2020 - n)
    if result is None:
        continue
    a, b = result
    print(n, a, b, n*a*b)
