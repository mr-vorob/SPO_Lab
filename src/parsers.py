from functools import reduce
from syntax_p import *

def key(kw):
    return Const(kw, "Const")

def parse(tokens):
    ast = parser()(tokens, 0)
    return ast

def parser():
    return Phrase(list())

def stmt():
    return appoint() | while_my()

name_p = Token_tag("id")

def appoint():
    def process(parsed):
        ((name, _), exp) = parsed
        return Statement(name, exp)

    return name_p + key('=') + aexp() ^ process

def while_my():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return While(condition, body)

    return key('while') + bexp() + key('do') + Funct(list) + key('end') ^ process

def list():
    separator = key(';') ^ (lambda x: lambda l, r: Component(l, r))
    return Match(stmt(), separator)

def bexp():
    return priority(term(), 'and', logic_p)

def term():
    return relop() | group()

def relop():
    relops = ['<', '>']
    return aexp() + operator(relops) + aexp() ^ relop_p

def group():
    return key('(') + Funct(bexp) + key(')') ^ group_p

def aexp():
    return priority(aexp_term(), [['*', '/'], ['+', '-']], binop)

def aexp_term():
    return aexp_val() | aexp_group()

def aexp_group():
    return key('(') + Funct(aexp) + key(')') ^ group_p

num = Token_tag("int") ^ (lambda i: int(i))

def aexp_val():
    return (num ^ (lambda i: Int(i))) | (name_p ^ (lambda v: Var(v)))

def priority(parser_v, priority_l, combine):
    def parser_op(precedence_l):
        return operator(precedence_l) ^ combine
    parser = parser_v * parser_op(priority_l[0])
    for precedence_level in priority_l[1:]:
        parser = parser * parser_op(precedence_level)
    return parser

def binop(op):
    return lambda l, r: Bin(op, l, r)

def relop_p(parsed):
    ((left, op), right) = parsed
    return Relop(op, left, right)

def logic_p(op):
    if op == 'and':
        return lambda l, r: And(l, r)

def group_p(parsed):
    ((_, p), _) = parsed
    return p

def operator(ops):
    op_parsers = [key(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser
