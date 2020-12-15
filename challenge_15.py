
def solve_slow(n):
    with open('challenge_15_example','r') as file:
        numbers = [int(v) for v in file.read().strip().split(',')][::-1]

    while len(numbers) != n:
        try:
            index = numbers.index(numbers[0], 1)
            new_number = index
        except ValueError:
            new_number = 0

        numbers.insert(0, new_number)

    return numbers[0]

def solve(n):
    with open('challenge_15','r') as file:
        numbers = [int(v) for v in file.read().strip().split(',')]

    numbers_dict = {}

    for i in range(len(numbers)):
        last_num = numbers[i]
        numbers_dict[last_num] = i

    new_num = numbers[-1]

    updates = []

    for pos in range(len(numbers), n):
        if new_num in numbers_dict:
            next_new_num = pos - 1 - numbers_dict[new_num]
        else:
            next_new_num = 0

        updates.append(next_new_num)
        if len(updates) > 1:
            numbers_dict[updates.pop(0)] = pos - 1

        new_num = next_new_num

    return new_num

print(solve(2020))
print(solve(30000000))
