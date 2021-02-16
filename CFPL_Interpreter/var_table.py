class ValuesTable:  # for storing values and datatype of variables
    val = dict()

    @staticmethod
    def add_var(name, value):
        for key in ValuesTable.val:
            if key == name:
                ValuesTable.val[key] = value
                return

        ValuesTable.val[name] = value

    @staticmethod
    def find_var(name):
        for key in ValuesTable.val:
            if key == name:
                return ValuesTable.val[key]

        raise Exception("Variable not defined")


