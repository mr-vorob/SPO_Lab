import re
def leksem(type):
    position = 0
    tokens = []
    my_tokens = [(r'[ \n\t]+', None),(r'#[^\n]*', None),
        (r'\:=', "Const"),(r'\(', "Const"),(r'\)', "Const"),(r';', "Const"),(r'\+', "Const"),
        (r'-', "Const"),(r'\*', "Const"), (r'/', "Const"),(r'<=', "Const"),(r'<', "Const"),
        (r'>=', "Const"),(r'>', "Const"), (r'!=', "Const"),(r'=', "Const"),(r'and', "Const"),
        (r'or', "Const"),(r'not', "Const"),(r'if', "Const"),(r'then', "Const"),(r'else', "Const"),
        (r'while', "Const"),(r'do', "Const"),(r'end', "Const"),
        (r'[0-9]+', "int"),(r'[A-Za-z][A-Za-z0-9_]*', 'id'),]
    while position < len(type):
        match = None
        for token_expr in my_tokens:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(type, position)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        position = match.end(0)
    return tokens

