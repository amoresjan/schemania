import re


def tokenizer(text):
    data_types = ['INT', 'CHAR', 'BOOL', 'FLOAT']

    token_regex = [
        (re.compile(r"^\b(?:%s)\b" % "|".join(data_types)), "data_types"),
        (re.compile(r"^VAR"), "VAR"),
        (re.compile(r"^AS"), "AS"),
        (re.compile(r"^START"), "START"),
        (re.compile(r"^STOP"), "STOP"),
        (re.compile(r"^INPUT:"), "INPUT"),
        (re.compile(r"^OUTPUT:"), "OUTPUT"),
        (re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*"), "identifier"),  # variables
        (re.compile(r"^([1-9]\d*|0)\.([1-9]\d*|0)"), "float"),  # float
        (re.compile(r"^([1-9]\d*|0)"), "integer"),  # integer
        (re.compile(r"^\B'\w'\B"), "char"),  # char
        (re.compile(r'^\B["][TRUE|FALSE]+["]\B'), "bool"),  # bool
        (re.compile(r'^\B["].*["]\B'), "string"),  # string
        # SPECIAL CHARACTERS
        (re.compile(r"^[+*/%-]"), "operators"),  # operators
        (re.compile(r"^\("), "lparen"),  # left parenthesis
        (re.compile(r"^\)"), "rparen"),  # right parenthesis
        (re.compile(r"^="), "assignment"),  # assignment
        (re.compile(r"^,"), "comma"),  # comma
        (re.compile(r"^&"), "ampersand"),  # ampersand
    ]

    tokens = []

    while len(text):
        text = text.lstrip()

        matched = False

        for token, token_type in token_regex:
            if is_same := token.match(text):
                matched = True
                tok = (is_same.group(0), token_type)
                tokens.append(tok)
                text = token.sub('', text)
                text = text.lstrip()
                break

        if not matched:
            raise Exception("%s is invalid" % text.split("\n")[0])

    if ('STOP', 'STOP') not in tokens:
        tok = ("EOF", "EOF")
        tokens.append(tok)
    # else:
    #     tok = ("END", "END")
    #     tokens.append(tok)

    return tokens
