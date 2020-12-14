import re

def get_mask(source, required_bits, translate):
    bits = [translate[required_bits.index(bit)] if bit in required_bits else '0' for bit in source]
    return int(''.join(bits),2)

def get_addresses(source_mask, set_mask, loop_mask):
    bits = [i for i in range(36) if ((loop_mask >> i) & 1)]

    loop_num = 1 << len(bits)
    values = []

    for value in range(loop_num):
        addr = set_mask
        for i, bit in enumerate(bits):
            addr |= ((value >> i) & 1) << bit

        values.append(addr)

    return values

memory = {}

with open('challenge_15','r') as file:
    lines = file.readlines()

lines = [line.strip() for line in lines]

for line in lines:
    if line.startswith('mask'):
        data_value  = get_mask(line, '01', '01')
        source_mask = get_mask(line, 'X', '1')
        continue

    addr, value = (int(v) for v in re.match('mem\[(\d+)\] = (\d+)', line).groups())
    memory[addr] = (value & source_mask) | data_value
    print(f'Set {addr} to {memory[addr]:b}')

total = sum(memory.values())

print(f'Sum of values in memory: {total}')

#Part 2!
memory = {}

for line in lines:
    if line.startswith('mask'):
        source_mask = get_mask(line, '0', '1')
        set_mask    = get_mask(line, '1', '1')
        loop_mask   = get_mask(line, 'X', '1')

        addresses = get_addresses(source_mask, set_mask, loop_mask)
        continue

    addr, value = (int(v) for v in re.match('mem\[(\d+)\] = (\d+)', line).groups())

    for extra_addr in addresses:
        addr = (addr & source_mask) | extra_addr
        memory[addr] = value
        print(f'Set {addr} to {memory[addr]:b}')

total = sum(memory.values())

print(f'Sum of values in memory: {total}')
