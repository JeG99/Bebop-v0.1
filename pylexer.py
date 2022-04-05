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
    'CONS_INT',
    'CONS_FLOAT',
    'AND',
    'OR',
    'NOT',
    'RSQBRACKET',
    'LSQBRACKET'
]

reserved = {
    'routine': 'ROUTINE',
    'if':'IF',
    'else': 'ELSE',
    'print': 'PRINT',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'public' : 'PUBLIC',
    'private' : 'PRIVATE',
    'return' : 'RETURN',
    'void' : 'VOID',
    'construct' : 'CONSTRUCT',
    'def' : 'DEF',
    'while' : 'WHILE',
    'stack' : 'STACK',
    'new' : 'NEW',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'main' : 'MAIN'
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
t_AND = r'&&'
t_OR = r'||'
t_NOT = r'!'
t_RSQBRACKET = r'['
t_LSQBRACKET = r']'

t_ignore = ' \t'

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_FLOAT_CTE(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t

def t_CONS_INT(t):
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