import os
import sys

required_fields = {'byr','iyr','eyr','hgt','hcl','ecl','pid','cid'}


def check_range(digits, start, end):
    def check_range_value(value):
        if len(value) != digits:
            return False
        value = int(value)
        if value < start or value > end:
            return False
        return True
    return check_range_value

def check_height(value):
    type = value[-2:]
    if type == 'cm':
        start, end = 150, 193
    elif type == 'in':
        start, end = 59, 76
    else:
        return False

    value = int(value[:-2])
    return start <= value <= end

def check_hair_colour(value):
    if value[0] != '#' or len(value) != 7:
        return False

    if any(v not in '0123456789abcdef' for v in value[1:]):
        return False

    return True

def check_eye_colour(value):
    return value in {'amb','blu','brn','gry','grn','hzl','oth'}

def check_passport_id(value):
    if len(value) != 9 or not value.isdigit():
        return False
    return True

validations = {'byr' : check_range(4, 1920, 2002),
               'iyr' : check_range(4, 2010, 2020),
               'eyr' : check_range(4, 2020, 2030),
               'hgt' : check_height,
               'hcl' : check_hair_colour,
               'ecl' : check_eye_colour,
               'pid' : check_passport_id}

def handle_data(fields):
    missing = required_fields - fields.keys()
    if missing and missing != {'cid'}:
        return 0

    for name, value in fields.items():
        if name in validations and not validations[name](value):
            return 0
    return 1

fields = {}
count = 0
with open('challenge_4','r') as file:
    for line in file:
        line = line.strip()
        if not line:
            count += handle_data(fields)
            fields = {}
            continue
        for item in line.split():
            name,value = item.split(':')
            fields[name] = value

count += handle_data(fields)

print(count)
