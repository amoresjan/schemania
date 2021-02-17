import re


def tokenizer(string: str):
    data_types = ['INT', 'CHAR', 'BOOL', 'FLOAT']
    # logical_operators = ['AND', 'OR', 'NOT']
    # control_structures = ['IF', 'ELSE', 'WHILE']

    token_regex = [
        (re.compile(r"^\b(?:%s)\b" % "|".join(data_types)), "data_types"),
        (re.compile(r"^VAR"), "VAR"),
        (re.compile(r"^AS"), "AS"),
        (re.compile(r"^START"), "START"),
        (re.compile(r"^STOP"), "STOP"),
        (re.compile(r"^OUTPUT"), "OUTPUT"),
        (re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*"), "identifier"),  # variables
        (re.compile(r"^\d*[.,]?\d"), "numbers"),  # numbers
        # (re.compile(r"^\d*\.\d+"), "float"),  # float
        # (re.compile(r"^([1-9]\d*|0)"), "integer"),  # integer
        # (re.compile(r"^[+*/%-]"), "operators"),  # operators
        # (re.compile(r"^[()]"), "parenthesis"),  # parenthesis
        (re.compile(r"^="), "assignment"),  # assignment
        (re.compile(r"^,"), "comma"),  # comma
        # (re.compile(r"^\B'\w'\B"), "char"),  # char
        # (re.compile(r'^\B["][\w\s]+["]\B'), "bool"),  # bool
    ]

    tokens = []

    while len(string):
        string = string.lstrip()

        matched = False

        for token, token_type in token_regex:
            is_same = token.match(string)
            if is_same:
                matched = True
                tok = (is_same.group(0), token_type)
                tokens.append(tok)
                string = token.sub('', string)
                string = string.lstrip()
                break

        if not matched:
            raise Exception("Invalid token")

    return tokens
