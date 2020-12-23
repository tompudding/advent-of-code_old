with open('challenge_23','r') as file:
    ring = [int(n) for n in file.read().strip()]

full_ring_len = len(ring)
initial_ring = ring[::]
move_num = 1

def print_ring(ring, cup_index):
    out = ['cups:']

    for i, n in enumerate(ring):
        if i == cup_index:
            out.append(f'({n})')
        else:
            out.append(f'{n}')

    print(' '.join(out))

def print_ring_large(ring, cup_index):
    out = ['cups:']

    for i, n in enumerate(ring):
        if i == cup_index:
            out.append(f'({n})')
        else:
            out.append(f'{n}')
    out.append('...')

    print(' '.join(out))

def get_canonical(ring):
    start = ring.index(1)

    ring = ring[start+1:] + ring[:start]
    return ''.join((f'{n}' for n in ring))

def get_canonical_linked(ring):
    last = ring[1]
    out = [last]
    for n in range(len(ring)-3):
        out.append(ring[last])
        last = ring[last]

    return ''.join((f'{n}' for n in out))


def move(ring, cup_index):
    global move_num
    #print(f'-- move {move_num} --')
    #print_ring(ring, cup_index)
    move_num += 1
    start = ring[cup_index]

    taken = []

    taken = (ring + ring)[cup_index+1:cup_index+3+1]

    if cup_index >= len(ring) - 3:
        ring = ring[(cup_index + 3+1) % len(ring): cup_index+1]
    else:
        ring = ring[:cup_index+1] + ring[cup_index+1+3:]

    #print('pick up:', ', '.join((f'{n}' for n in taken)))
    destination = start - 1
    dest_pos = None
    while dest_pos is None:
        try:
            if destination <= 0:
                destination += full_ring_len
            dest_pos = ring.index(destination)
        except ValueError:
            #print(f'{destination} not in ring')
            destination -= 1

    #print(f'destination: {destination}\n')

    ring[(dest_pos+1):(dest_pos+1)] = taken

    return ring, (ring.index(start) + 1) % len(ring)

def move_linked_list(ring, cup, max_index=1000000):
    #The three things after cup index get moved
    pickup = ring[cup]
    destination = cup - 1
    if destination == 0:
        destination = max_index

    new_next = pickup
    picked = set()

    for i in range(3):
        picked.add(new_next)
        last_picked = new_next
        new_next = ring[new_next]

    while destination in picked:
        destination -= 1
        if destination == 0:
            destination = max_index

    #print(f'{last_picked=} {destination=} {cup=} {pickup=} {new_next=}')
    #print(f'Set {last_picked} => {ring[destination]}')
    ring[last_picked] = ring[destination]
    #print(f'Set {destination} => {pickup}')
    ring[destination] = pickup
    #print(f'Set {cup} => {new_next}')
    ring[cup] = new_next

    return ring, new_next

cup_index = 0
for n in range(100):
    ring, cup_index = move(ring, cup_index)

print('-- final --')
print_ring(ring, cup_index)

answer = get_canonical(ring)

print(f'Part 1 {answer}')

#For part 2 we'll use a linked list, ignoring the first one
ring_nexts = [n+1 for n in range(1000001)]

#ring_nexts = list(range(10))
ring = initial_ring
for i in range(len(ring)-1):
    ring_nexts[ring[i]] = ring[i+1]
ring_nexts[ring[-1]] = 10
ring_nexts[-1] = ring[0]

cup = ring[0]
for n in range(10000000):
    ring_nexts, cup = move_linked_list(ring_nexts, cup)

a = ring_nexts[1]
b = ring_nexts[a]
print(a,b,a*b)


#print(get_canonical_linked(ring_nexts))
