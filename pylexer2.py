####   Library Importing
import ply.lex as lex

####   Token Array Definition
tokens = [
    'ID',
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
    'DOT',
    'CONST_INT',
    'CONST_FLOAT',
    'CONST_STRING',
    'CONST_BOOL'
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
    'private' : 'PRIVATE',
    'public' : 'PUBLIC',
    'def' : 'DEF',
    'return' : 'RETURN',
    'new': 'NEW',
    'while' : 'WHILE',
    'if' : 'IF',
    'else' : 'ELSE',
    'void' : 'VOID'
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
t_OR = r'\|\|'
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
t_POWER = r'\*\*'
t_SQRT = r'\|/'
t_DOT = r'\.'
t_CONST_BOOL = r'true|false'
t_CONST_STRING = r'\"(\"\"|[^\"$])*\"'

t_ignore = ' \t'

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_CONST_FLOAT(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t

def t_CONST_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()