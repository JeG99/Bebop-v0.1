import ply.lex as lex

tokens = [
    'PLUS',
    'MINUS',
    'DIVIDE',
    'TIMES',
    'EQUALS',
    'GTHAN',
    'LTHAN',
    'DIFFERENT',
    'ID',
    'COMMA',
    'STRING',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'SEMICOLON',
    'COLON',
    'INT_CTE',
    'FLOAT_CTE'
]

reserved = {
    'program': 'PROGRAM',
    'if':'IF',
    'else': 'ELSE',
    'print': 'PRINT',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT'
}

tokens += list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_COLON = r':'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_GTHAN = r'>'
t_LTHAN = r'<'
t_EQUALS = r'='
t_DIFFERENT = r'<>'
t_STRING = r'\"(\"\"|[^\"$])*\"'

t_ignore = ' \t'

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_FLOAT_CTE(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t

def t_INT_CTE(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    #print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()