import os
import sys

contains = {}
contained_by = {}

with open('challenge_7','r') as file:
    for line in file:
        colour, rest = line.strip().strip('.').split('bags contain',maxsplit=1)
        colour = colour.strip()

        this_contains = {}
        #print(rest)
        if rest.strip() == 'no other bags':
            contains[colour] = {}
            continue
        for bag in rest.strip().split(','):
            bag = bag.strip()
            if not bag:
                continue

            if bag.endswith(' bags'):
                bag = bag[:-5:]
            elif bag.endswith(' bag'):
                bag = bag[:-4:]

            space = bag.index(' ')
            num = int(bag[:space])
            inner_colour = bag[space+1:]



            this_contains[inner_colour] = num
            try:
                contained_by[inner_colour].add(colour)
            except KeyError:
                contained_by[inner_colour] = set([colour])

        contains[colour] = this_contains

def get_all_contains(colour):
    chain = []

    try:
        yield (colour,)
        for bag in contained_by[colour]:
            for extra_chain in get_all_contains(bag):
                yield (colour,) + extra_chain
    except KeyError:
        pass


# outer_bags = set()
# for chain in get_all_contains('shiny gold'):
#     if len(chain) == 1:
#         continue
#     outer_bags.add(chain[-1])

# print(len(outer_bags))

def get_num_contains(colour):
    total = 1
    for bag, number in contains[colour].items():
        print(bag, number, total)
        total += get_num_contains(bag)*number

    return total

print(contains['shiny gold'])
#Exclude the original bag
print(get_num_contains('shiny gold') - 1)
