class Var:
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            return 0

class Component:
    def __init__(self, first, second):
        self.first = first
        self.second = second


    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)

class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, env):
        condition_val = self.condition.eval(env)
        while condition_val:
            self.body.eval(env)
            condition_val = self.condition.eval(env)

class Int:
    def __init__(self, i):
        self.i = i

    def eval(self, env):
        return self.i

class Bin:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        l_val = self.left.eval(env)
        r_val = self.right.eval(env)
        if self.op == '+':
            val = l_val + r_val
        elif self.op == '-':
            val = l_val - r_val
        elif self.op == '*':
            val = l_val * r_val
        elif self.op == '/':
            val = l_val / r_val
        return val

class Relop:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, env):
        l_val = self.left.eval(env)
        r_val = self.right.eval(env)
        if self.op == '<':
            val = l_val < r_val
        elif self.op == '>':
            val = l_val > r_val
        return val

class And:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        l_val = self.left.eval(env)
        r_val = self.right.eval(env)
        return l_val and r_val
class Result:
    def __init__(self, val, pos):
        self.val = val
        self.pos = pos

class Parser:
    def __add__(self, other):
        return Coupling(self, other)

    def __mul__(self, other):
        return Match(self, other)

    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, function):
        return Process(self, function)

class Token_tag(Parser):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None

class Const(Parser):
    def __init__(self, val, tag):
        self.val = val
        self.tag = tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][0] == self.val and tokens[pos][1] is self.tag:
            return Result(tokens[pos][0], pos + 1)
        else:
            return None

class Coupling(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        l_result = self.left(tokens, pos)
        if l_result:
            r_result = self.right(tokens, l_result.pos)
            if r_result:
                val = (l_result.val, r_result.val)
                return Result(val, r_result.pos)
        return None

class Match(Parser):
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)

        def process_next(parsed):
            (sepfunc, right) = parsed
            return sepfunc(result.val, right)
        parser_n = self.separator + self.parser ^ process_next

        result_n = result
        while result_n:
            result_n = parser_n(tokens, result.pos)
            if result_n:
                result = result_n
        return result            

class Alternate(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, pos):
        l_result = self.left(tokens, pos)
        if l_result:
            return l_result
        else:
            r_result = self.right(tokens, pos)
            return r_result

class Parser_f(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        results = []
        result = self.parser(tokens, pos)
        while result:
            results.append(result.val)
            pos = result.pos
            result = self.parser(tokens, pos)
        return Result(results, pos)

class Process(Parser):
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            result.val = self.function(result.val)
            return result

class Funct(Parser):
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser(tokens, pos)

class Phrase(Parser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result and result.pos == len(tokens):
            return result
        else:
            return None

class Statement:
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp

    def eval(self, env):
        val = self.aexp.eval(env)
        env[self.name] = val