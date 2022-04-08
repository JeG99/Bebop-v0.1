####   Library Importing
from ply.lex import lex

####   Token Array Definition
tokens = [

    'SEMICOLON',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'LSQRBRACKET',
    'RSQRBRACKET',
    'ARROW',
    'COLON',
    'EQUALS',
    'READ',
    'WRITE',
    'OR',
    'AND',
    'NOT',
    'LTHAN',
    'GTHAN',
    'DIFFERENT',
    'EQUIVALENT',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'POWER',
    'SQRT',
    'DOT'


]

####   Reserved Dictionary Definition

reserved = {
    'routine' : 'ROUTINE',
    'class' : 'CLASS',
    'int': 'INT',
    'float': 'FLOAT',
    'string' : 'STRING',
    'bool' : 'BOOL',
    'construct' : 'CONSTRUCT',
    'function' : 'FUNCTION',
    'private' : 'PRIVATE',
    'public' : 'PUBLIC',
    'def' : 'DEF',
    'return' : 'RETURN',
    'new': 'NEW',
    'while' : 'WHILE',
    'if' : 'IF',
    'else' : 'ELSE',
    'true' : 'TRUE',
    'false' : 'FALSE'

}

tokens += list(reserved.values())

t_SEMICOLON = r';'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQRBRACKET = r'\['
t_RSQRBRACKET = r'\]'
t_ARROW = r'->'
t_COLON = r':'
t_EQUALS = r'='
t_WRITE = r'<<<'
t_READ = r'>>>'
t_OR = r'||'
t_AND = r'&&'
t_NOT = r'\!'
t_LTHAN = r'\<'
t_GTHAN = r'\>'
t_DIFFERENT = r'<>'
t_EQUIVALENT = r'=='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_POWER = r'**'
t_SQRT = r'|/'
t_DOT = r'\.'

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
    t.lexer.skip(1)