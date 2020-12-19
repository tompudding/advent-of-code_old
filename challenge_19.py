data = []
rules_text = {}
rules = {}
import itertools

with open('challenge_19') as file:
    parsing_rules = True
    for line in file:
        line = line.strip()

        if parsing_rules:
            try:
                n, rule = line.split(':')
                rules_text[int(n)] = rule.strip()
                continue
            except ValueError:
                parsing_rules = False

        if not line:
            continue
        data.append(line)

class Text:
    def __init__(self, text):
        self.text = text

    def match(self, target):
        if target.startswith(self.text):
            yield target[len(self.text):]

    def __repr__(self):
        return f'Text({self.text})'

class Rule:
    # A rule consists of a list of parts, any of which can match entirely for it to be considered a match
    def __init__(self, text):
        self.rules = []
        self.is_text = False

        if '"' in text:
            self.rules.append([Text(text.strip('"'))])
            self.is_text = True
            return

        if '|' in text:
            for part in text.split('|'):
                self.rules.append([Rule(part.strip())])

            return

        rule_list = []
        for n in [int(v) for v in text.split()]:

            if n not in rules:
                rules[n] = Rule(rules_text[n])

            rule_list.append(rules[n])

        # any adjacent rules that are just strings can be appended

        collapsed = []
        for pos in range(len(rule_list) - 1):
            if rule_list[pos].is_text and rule_list[pos+1].is_text:
                rule_list[pos+1] = Rule('"' + rule_list[pos].rules[0][0].text + rule_list[pos+1].rules[0][0].text + '"')
            else:
                collapsed.append(rule_list[pos])

        collapsed.append(rule_list[-1])

        self.rules.append(collapsed)

    def match(self, target):

        for rule_list in self.rules:
            current = target
            match = False

            stack = (target,)
            for rule in rule_list:
                new_stack = []
                for item in stack:
                    new_stack = itertools.chain(new_stack, (rest for rest in rule.match(item)))
                stack = new_stack

            for item in stack:
                yield item

    def __repr__(self):
        out = []
        for rule_list in self.rules:
            out.append(' + '.join([str(rule) for rule in rule_list]))
        return '{' + '\n'.join(out) + '}'

def match_rule_zero():
    for n, rule in rules_text.items():
        if n not in rules:
            rules[n] = Rule(rule)

    count = 0
    for line in data:
        for rest in rules[0].match(line):
            if not rest:
                #print('***',line)
                count += 1
                break

    return count

def expand(n, text):
    out = []
    current = text
    for i in range(5):
        current = current.replace(n, text)
        out.append(current.replace(n, '').strip())

    return ' | '.join(out)

print(f'Part 1 Total {match_rule_zero()}')

rules = {}

rules_text[11] = '42 31 | ' + expand('11', '42 11 31')
rules_text[8] = '42 | ' + expand('8', '42 8')

print(f'Part 2 Total {match_rule_zero()}')
