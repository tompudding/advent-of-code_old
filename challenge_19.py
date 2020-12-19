data = []
rules_text = {}
rules = {}

with open('challenge_19_example1') as file:
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
            #print(f'Match text {self.text} for target "{target}"')
            return True, target[len(self.text):]
        else:
            #print(f'No Match text {self.text} for target "{target}"')
            return False, target

    def __repr__(self):
        return f'Text({self.text})'

class Rule:
    # A rule consists of a list of parts, any of which can match entirely for it to be considered a match
    def __init__(self, text, debug=False):
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
            if debug:
                print('XX',n,'|',len(rule_list),'|',rule_list)

            if n not in rules:
                rules[n] = Rule(rules_text[n])

            rule_list.append(rules[n])
            if debug:
                print('YY',n,'|',len(rule_list),'|',rules[n],'|',rule_list[0])


        # any adjacent rules that are just strings can be appended
        if debug:
            print('NNN',rule_list)
        collapsed = []
        for pos in range(len(rule_list) - 1):
            if rule_list[pos].is_text and rule_list[pos+1].is_text:
                rule_list[pos+1] = Rule('"' + rule_list[pos].rules[0][0].text + rule_list[pos+1].rules[0][0].text + '"')
            else:
                collapsed.append(rule_list[pos])

        if debug:
            print('MMM',collapsed)

        collapsed.append(rule_list[-1])

        self.rules.append(collapsed)

    def match(self, target):
        #print('jim',target)
        #print(self)
        #print(len(self.rules))
        for rule_list in self.rules:
            current = target
            match = False
            for rule in rule_list:
                #print('a',rule,current)
                match, current = rule.match(current)

                if not match:
                    break
            if match:
                #print(f'Match {self} for target "{target}"')
                return match, current
        return False, target

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
        match, rest = rules[0].match(line)
        if match and not rest:
            print('***',line)
            count += 1

    return count

def expand(n, text):
    out = []
    current = text
    for i in range(100):
        current = current.replace(n, text)
        out.append(current.replace(n, '').strip())

    return ' | '.join(out)

print(f'Part 1 Total {match_rule_zero()}')

rules = {}

rules_text[11] = '42 31 | ' + expand('11', '42 11 31')
rules_text[8] = '42 | ' + expand('8', '42 8')

print(Rule(rules_text[8]).match('babbbbaabbbbbabbbbbbaabaaabaaa'))

print(f'Part 2 Total {match_rule_zero()}')
