import sys
from functools import partial
from math import lcm

class Module:
    def __init__(self, line, sink=False):
        if sink:
            self.name = line
            self.function = None
            self.destinations = []
            self.is_on = False
            self.inputs = []
            self.memory = []
            self.sink = True
            return

        split_line = line.split(' -> ')
        self.name = split_line[0][1:] if split_line[0] != "broadcaster" else "broadcaster"
        self.function = split_line[0][0] if self.name != "broadcaster" else "broadcaster"
        self.destinations = split_line[1].split(', ')
        self.is_on = False
        self.inputs = []
        self.memory = []
        self.sink = False
    
    def pulse(self, module_map, sender, value):
        if self.sink: return []
        if self.name == "broadcaster":
            return self.partial_send(module_map, value)
        elif self.function == "%": # low pulse 0, high pulse 255
            if value != 0: return []
            self.is_on = not self.is_on
            return self.partial_send(module_map, 255 if self.is_on else 0)
        elif self.function == "&":
            self.memory[self.inputs.index(sender)] = value
            signal = 0 if all([x == 255 for x in self.memory]) else 255
            return self.partial_send(module_map, signal)
        else:
            raise Exception("Unknown module type: " + self.name, self.function)

    def partial_send(self, module_map, value):
        partial_pulses = []
        for module in self.destinations:
            partial_pulses.append(partial(module_map[module].pulse, module_map, sender=self.name, value=value))
        return partial_pulses
    
    def __repr__(self):
        return f"{self.name}{self.function}{self.is_on}{self.memory}"

def connect_inputs(module_map):
    new_modules = []
    for module in module_map.values():
        for destination in module.destinations:
            if destination not in module_map:
                new_modules.append(Module(destination, sink=True))
                continue
            module_map[destination].inputs.append(module.name)
            module_map[destination].memory.append(0)
    for module in new_modules:
        module_map[module.name] = module
    return module_map

def push_button(module_map, dependencies=["fv", "kk", "vt", "xr"], part_2=False):
    to_pulse = [partial(module_map["broadcaster"].pulse, module_map, sender="button", value=0)]
    high_count = 0
    low_count = 0
    triggered_dependencies = [0 for _ in dependencies]
    while to_pulse:
        pulse = to_pulse.pop()
        if pulse.keywords["sender"] in dependencies and pulse.keywords["value"] == 255:
            triggered_dependencies[dependencies.index(pulse.keywords["sender"])] += 1
        partial_pulses = pulse()
        high_count += 1 if pulse.keywords["value"] == 255 else 0
        low_count += 1 if pulse.keywords["value"] == 0 else 0
        to_pulse.extend(partial_pulses)
    return (high_count, low_count) if not part_2 else triggered_dependencies

def prepare_input(lines):
    modules = [Module(line) for line in lines]
    module_map = {module.name: module for module in modules}
    connect_inputs(module_map)
    return module_map

def part_1(lines):
    module_map = prepare_input(lines)
    high_count, low_count = 0, 0
    for i in range(1000):
        high, low = push_button(module_map)
        high_count += high
        low_count += low
    return high_count * low_count

def hash_states(module_map):
    return hash("".join([str(module) for module in module_map.values()]))

def print_memory(module_map, module_name):
    print(module_name, module_map[module_name].memory)

def part_2(lines):
    module_map = prepare_input(lines)
    i = 0
    triggered_index = [None for _ in range(4)]
    while not all(triggered_index):
        i += 1
        triggered = push_button(module_map, part_2=True)
        for j, trigger in enumerate(triggered):
            if trigger and triggered_index[j] is None:
                triggered_index[j] = i + trigger - 1
                print(triggered_index, lcm(*[x for x in triggered_index if x is not None]))
    return lcm(*[x for x in triggered_index if x is not None])

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in sys.stdin if line.rstrip('\n')]
    print(part_1(lines))
    print(part_2(lines))
