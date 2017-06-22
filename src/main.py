import sys
from parsers import *
from lexer import *
if __name__ == '__main__':
    filename = 'lang.txt'
    text = open(filename).read()
    tokens = leksem(text)
    print(tokens)
    parse_result = parse(tokens)
    if not parse_result:
        sys.stderr.write('Ошибка парсера\n')
        sys.exit(1)
    ast = parse_result.val
    env = {}
    ast.eval(env)
    print('Результат:')
    for name in env:
        print('%s: %s' % (name, env[name]))
