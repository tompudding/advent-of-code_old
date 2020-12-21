allergens = {}
all_ingredients = set()
all_allergens = set()

full_ingredients_list = []

with open('challenge_21','r') as file:
    for line in file:
        current_ingredients, current_allergens = line.split('(contains ')
        current_ingredients = current_ingredients.strip().split()
        current_allergens = [v.strip() for v in current_allergens.strip(')\n').split(',')]

        full_ingredients_list.extend(current_ingredients)
        current_ingredients = set(current_ingredients)

        all_ingredients.update(current_ingredients)
        all_allergens.update(current_allergens)

        for allergen in current_allergens:
            try:
                allergens[allergen].append(current_ingredients)
            except KeyError:
                allergens[allergen] = [current_ingredients]

risky_ingredients = set()
possibilities = {}

for allergen in all_allergens:
    # take the intersection of all
    total = {a for a in all_ingredients}

    for ing in allergens[allergen]:
        total &= ing

    possibilities[allergen] = total

    risky_ingredients.update(total)

# For part one we want the ingredients that can't contain anything
safe_ingredients = all_ingredients - risky_ingredients
print(safe_ingredients)
safe_count = sum( (full_ingredients_list.count(ingredient) for ingredient in safe_ingredients) )
print(f'Part 1 : {safe_count}')

print(possibilities)

# This is a lot like a previous part, where we can remove a subset of n with only n possibilities between them
# from all others. For a first pass let's try using n = 1 as it's easier
contains = {}

while True:
    match = None
    for allergen, ingredients in possibilities.items():
        if len(ingredients) == 1:
            match = allergen, list(ingredients)[0]
            break

    if not match:
        print('No more things')
        if possibilities:
            print('But there are things left!')
            print(possibilities)
            raise Exception('badness')
        break

    allergen, ingredient = match
    contains[ingredient] = allergen
    del possibilities[allergen]
    for potential_ingredients in possibilities.values():
        try:
            potential_ingredients.remove(ingredient)
        except KeyError:
            pass

contained_by = {a:i for i,a in contains.items()}

canonical_allergens = sorted(contained_by.keys())

canonical_ingredients = ','.join((contained_by[allergen] for allergen in canonical_allergens))
print(canonical_ingredients)
