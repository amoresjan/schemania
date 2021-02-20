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
        (re.compile(r'^\B["][\w\s]+["]\B'), "bool"),  # bool
        # SPECIAL CHARACTERS
        (re.compile(r"^[+*/%-]"), "operators"),  # operators
        (re.compile(r"^[()]"), "parenthesis"),  # parenthesis
        (re.compile(r"^="), "assignment"),  # assignment
        (re.compile(r"^,"), "comma"),  # comma
    ]

    tokens = []

    while len(text):
        text = text.lstrip()

        matched = False

        for token, token_type in token_regex:
            is_same = token.match(text)
            if is_same:
                matched = True
                tok = (is_same.group(0), token_type)
                tokens.append(tok)
                text = token.sub('', text)
                text = text.lstrip()
                break

        if not matched:
            raise Exception("Invalid token")

    if ('STOP', 'STOP') not in tokens:
        tok = ("EOF", "EOF")
        tokens.append(tok)
    # else:
    #     tok = ("END", "END")
    #     tokens.append(tok)

    return tokens
