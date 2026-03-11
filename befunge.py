#!/usr/bin/env python3
"""Befunge-93 interpreter — 2D stack-based esoteric language."""
import sys, random

class Befunge:
    def __init__(self, code):
        lines = code.split('\n')
        self.grid = [[' ']*80 for _ in range(25)]
        for y, line in enumerate(lines[:25]):
            for x, c in enumerate(line[:80]):
                self.grid[y][x] = c
        self.stack = []; self.x = self.y = 0; self.dx = 1; self.dy = 0
        self.string_mode = False; self.output = []
    def push(self, v): self.stack.append(v)
    def pop(self): return self.stack.pop() if self.stack else 0
    def step(self):
        c = self.grid[self.y][self.x]
        if self.string_mode:
            if c == '"': self.string_mode = False
            else: self.push(ord(c))
        elif c == '"': self.string_mode = True
        elif c.isdigit(): self.push(int(c))
        elif c == '+': self.push(self.pop() + self.pop())
        elif c == '-': b, a = self.pop(), self.pop(); self.push(a - b)
        elif c == '*': self.push(self.pop() * self.pop())
        elif c == '/': b, a = self.pop(), self.pop(); self.push(a // b if b else 0)
        elif c == '%': b, a = self.pop(), self.pop(); self.push(a % b if b else 0)
        elif c == '!': self.push(0 if self.pop() else 1)
        elif c == '`': b, a = self.pop(), self.pop(); self.push(1 if a > b else 0)
        elif c == '>': self.dx, self.dy = 1, 0
        elif c == '<': self.dx, self.dy = -1, 0
        elif c == '^': self.dx, self.dy = 0, -1
        elif c == 'v': self.dx, self.dy = 0, 1
        elif c == '?': self.dx, self.dy = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        elif c == '_': self.dx, self.dy = (-1,0) if self.pop() else (1,0)
        elif c == '|': self.dx, self.dy = (0,-1) if self.pop() else (0,1)
        elif c == ':': v = self.pop(); self.push(v); self.push(v)
        elif c == '\\': a, b = self.pop(), self.pop(); self.push(a); self.push(b)
        elif c == '$': self.pop()
        elif c == '.': self.output.append(str(self.pop()))
        elif c == ',': self.output.append(chr(self.pop()))
        elif c == '#': self.x = (self.x+self.dx) % 80; self.y = (self.y+self.dy) % 25
        elif c == 'p': y, x, v = self.pop(), self.pop(), self.pop(); self.grid[y][x] = chr(v)
        elif c == 'g': y, x = self.pop(), self.pop(); self.push(ord(self.grid[y][x]))
        elif c == '@': return False
        self.x = (self.x + self.dx) % 80; self.y = (self.y + self.dy) % 25
        return True
    def run(self, max_steps=100000):
        for _ in range(max_steps):
            if not self.step(): break
        return "".join(self.output)

if __name__ == "__main__":
    programs = {
        "hello": '>25*"!dlroW ,olleH":v\n                v:,_@\n                >  ^',
        "factorial": '&>:1-:v v *_$.@ \n ^    _$>\\:^',
        "fibonacci": '01>:.:0g1+:9`#@_01g+01p:01g02p.01>:.:0g1+:9`#@_01g+01p:01g02p.'
    }
    name = sys.argv[1] if len(sys.argv) > 1 else "hello"
    if name in programs:
        code = programs[name]
    elif len(sys.argv) > 1 and sys.argv[1].endswith('.bf'):
        code = open(sys.argv[1]).read()
    else:
        code = programs["hello"]
    bf = Befunge(code)
    result = bf.run()
    print(f"Output: {result}")
    if bf.stack: print(f"Stack: {bf.stack}")
