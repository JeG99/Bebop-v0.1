# TYPE CODEs
# int       : 0
# float     : 1
# bool      : 2
# string    : 3

# OPERATOR CODES
# sum       : 0
# sub       : 1
# mul       : 2
# div       : 3
# exp       : 4
# sqrt      : 5
# =         : 6
# <         : 7
# >         : 8
# ==        : 9
# <>        : 10

# ERR       : -1

# RESULTING_TYPE = sem_cube[OPERATOR][OP1][OP2]
# EX:
# RESULTING_TYPE = sem_cube[DIV][INT][FLOAT]
# RESULTING_TYPE = sem_cube[3][0][1] = 1 = FLOAT

from enum import Enum

class types(Enum):
    INT = 0
    FLOAT = 1
    BOOL = 2
    STRING = 3

class operators(Enum):
    SUM = 0
    SUB = 1
    MUL = 2
    DIV = 3
    EXP = 4
    SQRT = 5
    EQUAL = 6
    LT = 7
    GT = 8
    EQUIVALENT = 9
    NEQUIVALENT = 10

sem_cube = {
    'sum': {
        ('int', 'int'): 'int',
        ('int', 'float'): 'float',
        ('int', 'bool'): 'ERR',
        ('int', 'string'): 'ERR',

        ('float', 'int'): 'float',
        ('float', 'float'): 'float',
        ('float', 'bool'): 'ERR',
        ('float', 'string'): 'ERR',

        ('bool', 'int'): 'ERR',
        ('bool', 'float'): 'ERR',
        ('bool', 'bool'): 'ERR',
        ('bool', 'string'): 'ERR',

        ('string', 'int'): 'ERR',
        ('string', 'float'): 'ERR',
        ('string', 'bool'): 'ERR',
        ('string', 'string'): 'ERR'
    },
    'sub': {
        ('int', 'int'): 'int',
        ('int', 'float'): 'float',
        ('int', 'bool'): 'ERR',
        ('int', 'string'): 'ERR',

        ('float', 'int'): 'int',
        ('float', 'float'): 'float',
        ('float', 'bool'): 'ERR',
        ('float', 'string'): 'ERR',

        ('bool', 'int'): 'ERR',
        ('bool', 'float'): 'ERR',
        ('bool', 'bool'): 'ERR',
        ('bool', 'string'): 'ERR',

        ('string', 'int'): 'ERR',
        ('string', 'float'): 'ERR',
        ('string', 'bool'): 'ERR',
        ('string', 'string'): 'ERR'
    },
    'mul': {
        ('int', 'int'): 'int',
        ('int', 'float'): 'float',
        ('int', 'bool'): 'ERR',
        ('int', 'string'): 'ERR',

        ('float', 'int'): 'int',
        ('float', 'float'): 'float',
        ('float', 'bool'): 'ERR',
        ('float', 'string'): 'ERR',

        ('bool', 'int'): 'ERR',
        ('bool', 'float'): 'ERR',
        ('bool', 'bool'): 'ERR',
        ('bool', 'string'): 'ERR',

        ('string', 'int'): 'ERR',
        ('string', 'float'): 'ERR',
        ('string', 'bool'): 'ERR',
        ('string', 'string'): 'ERR'
    },
    'div': {
        ('int', 'int'): 'int',
        ('int', 'float'): 'float',
        ('int', 'bool'): 'ERR',
        ('int', 'string'): 'ERR',

        ('float', 'int'): 'int',
        ('float', 'float'): 'float',
        ('float', 'bool'): 'ERR',
        ('float', 'string'): 'ERR',

        ('bool', 'int'): 'ERR',
        ('bool', 'float'): 'ERR',
        ('bool', 'bool'): 'ERR',
        ('bool', 'string'): 'ERR',

        ('string', 'int'): 'ERR',
        ('string', 'float'): 'ERR',
        ('string', 'bool'): 'ERR',
        ('string', 'string'): 'ERR'
    },
    'exp': {
        ('int', 'int'): 'int',
        ('int', 'float'): 'float',
        ('int', 'bool'): 'ERR',
        ('int', 'string'): 'ERR',

        ('float', 'int'): 'int',
        ('float', 'float'): 'float',
        ('float', 'bool'): 'ERR',
        ('float', 'string'): 'ERR',

        ('bool', 'int'): 'ERR',
        ('bool', 'float'): 'ERR',
        ('bool', 'bool'): 'ERR',
        ('bool', 'string'): 'ERR',

        ('string', 'int'): 'ERR',
        ('string', 'float'): 'ERR',
        ('string', 'bool'): 'ERR',
        ('string', 'string'): 'ERR'
    },
    'sqrt': {
        ('int', 'int'): 'int',
        ('int', 'float'): 'float',
        ('int', 'bool'): 'ERR',
        ('int', 'string'): 'ERR',

        ('float', 'int'): 'int',
        ('float', 'float'): 'float',
        ('float', 'bool'): 'ERR',
        ('float', 'string'): 'ERR',

        ('bool', 'int'): 'ERR',
        ('bool', 'float'): 'ERR',
        ('bool', 'bool'): 'ERR',
        ('bool', 'string'): 'ERR',

        ('string', 'int'): 'ERR',
        ('string', 'float'): 'ERR',
        ('string', 'bool'): 'ERR',
        ('string', 'string'): 'ERR'
    },
    '=': {
        ('int', 'int'): 'int',
        ('int', 'float'): 'ERR',
        ('int', 'bool'): 'ERR',
        ('int', 'string'): 'ERR',

        ('float', 'int'): 'ERR',
        ('float', 'float'): 'float',
        ('float', 'bool'): 'ERR',
        ('float', 'string'): 'ERR',

        ('bool', 'int'): 'ERR',
        ('bool', 'float'): 'ERR',
        ('bool', 'bool'): 'bool',
        ('bool', 'string'): 'ERR',

        ('string', 'int'): 'ERR',
        ('string', 'float'): 'ERR',
        ('string', 'bool'): 'ERR',
        ('string', 'string'): 'string'
    },
    '<': {
        ('int', 'int'): 'bool',
        ('int', 'float'): 'bool',
        ('int', 'bool'): 'ERR',
        ('int', 'string'): 'ERR',

        ('float', 'int'): 'bool',
        ('float', 'float'): 'bool',
        ('float', 'bool'): 'ERR',
        ('float', 'string'): 'ERR',

        ('bool', 'int'): 'ERR',
        ('bool', 'float'): 'ERR',
        ('bool', 'bool'): 'ERR',
        ('bool', 'string'): 'ERR',

        ('string', 'int'): 'ERR',
        ('string', 'float'): 'ERR',
        ('string', 'bool'): 'ERR',
        ('string', 'string'): 'ERR'
    },
    '>': {
        ('int', 'int'): 'bool',
        ('int', 'float'): 'bool',
        ('int', 'bool'): 'ERR',
        ('int', 'string'): 'ERR',

        ('float', 'int'): 'bool',
        ('float', 'float'): 'bool',
        ('float', 'bool'): 'ERR',
        ('float', 'string'): 'ERR',

        ('bool', 'int'): 'ERR',
        ('bool', 'float'): 'ERR',
        ('bool', 'bool'): 'ERR',
        ('bool', 'string'): 'ERR',

        ('string', 'int'): 'ERR',
        ('string', 'float'): 'ERR',
        ('string', 'bool'): 'ERR',
        ('string', 'string'): 'ERR'
    },
    '==': {
        ('int', 'int'): 'bool',
        ('int', 'float'): 'bool',
        ('int', 'bool'): 'ERR',
        ('int', 'string'): 'ERR',

        ('float', 'int'): 'bool',
        ('float', 'float'): 'bool',
        ('float', 'bool'): 'ERR',
        ('float', 'string'): 'ERR',

        ('bool', 'int'): 'ERR',
        ('bool', 'float'): 'ERR',
        ('bool', 'bool'): 'ERR',
        ('bool', 'string'): 'ERR',

        ('string', 'int'): 'ERR',
        ('string', 'float'): 'ERR',
        ('string', 'bool'): 'ERR',
        ('string', 'string'): 'ERR'
    },
    '<>': {
        ('int', 'int'): 'bool',
        ('int', 'float'): 'bool',
        ('int', 'bool'): 'ERR',
        ('int', 'string'): 'ERR',

        ('float', 'int'): 'bool',
        ('float', 'float'): 'bool',
        ('float', 'bool'): 'ERR',
        ('float', 'string'): 'ERR',

        ('bool', 'int'): 'ERR',
        ('bool', 'float'): 'ERR',
        ('bool', 'bool'): 'ERR',
        ('bool', 'string'): 'ERR',

        ('string', 'int'): 'ERR',
        ('string', 'float'): 'ERR',
        ('string', 'bool'): 'ERR',
        ('string', 'string'): 'ERR'
    }
}

sem_cube = (
    ((0, 1, -1, -1), (1, 1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((0, 1, -1, -1), (1, 1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((0, 1, -1, -1), (1, 1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((0, 1, -1, -1), (1, 1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((0, 1, -1, -1), (1, 1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((0, 1, -1, -1), (1, 1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((0, -1, -1, -1), (-1, 1, -1, -1), (-1, -1, 2, -1), (-1, -1, -1, 3)),
    ((2, 2, -1, -1), (2, 2, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((2, 2, -1, -1), (2, 2, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((2, 2, -1, -1), (2, 2, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((2, 2, -1, -1), (2, 2, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1))
)

def typeMatch(operator, op1_type, op2_type):
    try:
        return types(sem_cube[operators[operator.upper()].value][types[op1_type.upper()].value][types[op2_type.upper()].value]).name
    except ValueError:
        raise ValueError('Error de semantica: %s y %s no son compatibles' % (op1_type, op2_type))