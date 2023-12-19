import sys
from functools import cache
from itertools import product
import copy

class Workflow:
    def __init__(self, line):
        self.line = line
        self.name = line.split("{")[0]
        self.rules = self.parse_rules(line)
    def __repr__(self):
        return f"Workflow({self.name}, {self.rules})"
    
    def parse_rules(self, line):
        rule_line = line[len(self.name)+1:-1]
        rule_strings = rule_line.split(",")
        rules = [Rule(rule_string) for rule_string in rule_strings]
        return rules

    def apply(self, part):
        for rule in self.rules:
            destination = rule.apply(part)
            if destination:
                return destination
    
    def apply_range(self, part_range):
        results = []
        current_part = part_range
        for rule in self.rules:
            destinations = rule.apply_range(current_part)
            destination = [d for d in destinations.keys() if d != "negative"][0]
            results.append((destination, destinations[destination]))
            if "negative" in destinations:
                current_part = destinations["negative"]
            else:
                break
        return results

class Rule:
    def __init__(self, rule_string):
        operators = ["<", ">"]
        operator_lambdas = { "<": lambda x, y: x < y, ">": lambda x, y: x > y }
        self.operator, self.operator_foo, self.variable, self.value, self.destination = None, None, None, None, None
        if any(operator in rule_string for operator in operators):
            self.operator = next(operator for operator in operators if operator in rule_string)
            self.operator_foo = operator_lambdas[self.operator]
            self.variable = rule_string.split(self.operator)[0]
            self.value = int(rule_string.split(self.operator)[1].split(":")[0])
            self.destination = rule_string.split(":")[1]
        else:
            self.destination = rule_string

    def __repr__(self):
        return f"Rule({self.operator}, {self.variable}, {self.value}, {self.destination})"
    
    def apply(self, part):
        if self.operator:
            if self.operator_foo(getattr(part, self.variable), self.value):
                return self.destination
            else:
                return None
        else:
            return self.destination
        
    def apply_range(self, part_range):
        if self.operator:
            result = part_range.split(self.variable, self.value, self.operator)
            destinations = { self.destination: result["positive"], "negative": result["negative"] }
            return destinations
        else:
            return { self.destination: part_range }

class Part:
    def __init__(self, line):
        line = line[1:-1].split(",")
        numbers = [int(prop.split("=")[1]) for prop in line]
        self.x, self.m, self.a, self.s = numbers
    
    def __repr__(self):
        return f"Part({self.x}, {self.m}, {self.a}, {self.s})"
    
    def evaluate(self, workflow_dict):
        current = "in"
        while current not in ["A", "R"]:
            current = workflow_dict[current].apply(self)
        return current
    
    def score(self):
        return self.x + self.m + self.a + self.s
    
class PartRange:
    def __init__(self, min, max):
        self.x = set(range(min, max+1))
        self.m = set(range(min, max+1))
        self.a = set(range(min, max+1))
        self.s = set(range(min, max+1))
    
    def __repr__(self):
        return f"PartRange({min(self.x)}, {max(self.x)}, {min(self.m)}, {max(self.m)}, {min(self.a)}, {max(self.a)}, {min(self.s)}, {max(self.s)})"
    
    def score(self):
        return (max(self.x) - min(self.x) + 1) * (max(self.m) - min(self.m) + 1) * (max(self.a) - min(self.a) + 1) * (max(self.s) - min(self.s) + 1)

    def overlaps(self, other):
        return all([self[variable].intersection(other[variable]) for variable in ["x", "m", "a", "s"]])

    def split(self, variable, value, operator):
        result = {"positive": None, "negative": None}
        if operator == "<":
            positive_set = set(range(1, value))
            negative_set = set(range(value, 4001))
        elif operator == ">":
            positive_set = set(range(value+1, 4001))
            negative_set = set(range(1, value+1))

        if self[variable].intersection(positive_set):
            new_range = copy.deepcopy(self)
            new_range[variable] = new_range[variable].intersection(positive_set)
            result["positive"] = new_range
        if self[variable].intersection(negative_set):
            new_range = copy.deepcopy(self)
            new_range[variable] = new_range[variable].intersection(negative_set)
            result["negative"] = new_range

        return result

    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)

def parse(lines):
    workflow_dict = parse_workflows(lines)
    parts = parse_parts(lines)
    return workflow_dict, parts

def parse_workflows(lines):
    workflows = []
    for line in lines:
        if line and line[0] != "{":
            workflows.append(Workflow(line))
    workflow_dict = { workflow.name: workflow for workflow in workflows }
    return workflow_dict

def parse_parts(lines):
    parts = []
    for line in lines:
        if line and line[0] == "{":
            parts.append(Part(line))
    return parts

def part_1(lines):
    workflow_dict, parts = parse(lines)
    accepted = [part for part in parts if part.evaluate(workflow_dict) == "A"]
    return sum(part.score() for part in accepted)

def random_part(min = 1, max = 4000):
    from random import randint
    return Part(f"{{x={randint(min, max)},m={randint(min, max)},a={randint(min, max)},s={randint(min, max)}}}")

def part_2(lines):
    workflow_dict, parts = parse(lines)
    part_range = PartRange(1, 4000)
    current = [("in", part_range)]
    solved = []
    while current:
        next = []
        for workflow, part_range in current:
            next.extend(workflow_dict[workflow].apply_range(part_range))
        solved.extend([(workflow, part_range) for workflow, part_range in next if workflow in ["A", "R"]])
        current = [(workflow, part_range) for workflow, part_range in next if workflow not in ["A", "R"]]

    return sum([x.score() for w, x in solved if w == "A"])

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
