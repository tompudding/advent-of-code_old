N = 20201227

def get_loop_size(rem):
    p = 1
    for loop_size in range(10000000):
        p *= 7
        p %= N
        if p == rem:
            return loop_size+1

card_key = 1327981
door_key = 2822615

door_loop_size = get_loop_size(door_key)

key = 1
for i in range(door_loop_size):
    key *= card_key
    key %= N

print(key)
