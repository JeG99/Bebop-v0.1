import sys
import ply.lex as lex
import ply.yacc as yacc

#List of tokens
tokens = [
    'ID',
    'COLON',
    'DOT',
    'SEMICOLON',
    'BRACEOPEN',
    'BRACECLOSE',
    'EQUALSIGN',
    'PARENTHESISOPEN',
    'GREATERTHAN',
    'LESSTHAN',
    'NOTEQUAL',
    'MULTIPLICATION',
    'DIVISION',
    'ADDITION',
    'SUBTRACTION',
    'PARENTHESISCLOSE',
    'CTEI',
    'CTEF',
    'CTESTRING'
]

reserved = {
    'program':'PROGRAM',
    'if':'IFSTMT',
    'else':'ELSESTMT',
    'print':'PRINT',
    'var':'VAR',
    'int':'INT',
    'float':'FLOAT',
}

tokens += list(reserved.values())

t_DOT = r'\.'
t_ADDITION = r'\+'
t_SUBTRACTION = r'\-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'\/'
t_COLON = r'\:'
t_SEMICOLON = r'\;'
t_BRACEOPEN = r'\{'
t_BRACECLOSE = r'\}'
t_PARENTHESISOPEN = r'\('
t_PARENTHESISCLOSE = r'\)'
t_EQUALSIGN = r'\='
t_GREATERTHAN = r'\>'
t_LESSTHAN = r'\<'
t_NOTEQUAL = r'<>'
t_ignore = r' '

def t_CTEI(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTEF(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTESTRING(t):
    r'\"(\"\"|[^\"$])*\"'
    t.value = str(t.value)
    return t
    
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_error(t):
    print("Error Encontrado")
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()

#Gramática Programa

def p_programa(p):
    '''programa : PROGRAM ID SEMICOLON vars bloque
                | PROGRAM ID SEMICOLON bloque'''
    p[0] = "COMPILED"


#Gramática Vars
def p_vars(p):
    '''
    vars : VAR varss
    '''
def p_varss(p):
    '''varss : ID COLON tipo SEMICOLON
                | ID COLON tipo SEMICOLON varss
                | ID DOT varss'''

#Gramática Tipo
def p_tipo(p):
    '''tipo : INT
            | FLOAT'''
    p[0] = p[1]

#Gramática Estatuto
def p_estatuto(p):
    '''estatuto : asignacion
        | condicion
        | escritura'''

#Gramática Asignación
def p_asignacion(p):
    'asignacion : ID EQUALSIGN expresion SEMICOLON'

#Gramática Condición
def p_condicion(p):
    '''condicion : IFSTMT PARENTHESISOPEN expresion PARENTHESISCLOSE bloque SEMICOLON
                | IFSTMT PARENTHESISOPEN expresion PARENTHESISCLOSE bloque ELSESTMT bloque SEMICOLON'''

#Gramática Bloque
def p_bloque(p):
    'bloque : BRACEOPEN bloquee BRACECLOSE'
def p_bloquee(p):
    '''
    bloquee : estatuto
    | estatuto bloquee
    | vacio
    '''

#Gramática Escritura
def p_escritura(p):
    'escritura : PRINT PARENTHESISOPEN escrituraa PARENTHESISCLOSE SEMICOLON'
def p_escrituraa(p):
    '''escrituraa : expresion
                | expresion DOT escrituraa
                | CTESTRING
                | CTESTRING DOT escritura'''


#Gramática Expresión:
def p_expresion(p):
    '''expresion : exp GREATERTHAN exp
                | exp LESSTHAN exp
                | exp NOTEQUAL exp
                | exp'''

#Gramática EXP
def p_exp(p):
    'exp : termino expp'
def p_expp(p):
    '''expp : ADDITION exp
            | SUBTRACTION exp 
            | vacio'''

#Gramática Término
def p_termino(p):
    'termino : factor terminoo'
def p_terminoo(p):
    '''terminoo : MULTIPLICATION termino
                | DIVISION termino
                | vacio'''

#Gramática Factor 
def p_factor(p):
    '''factor : PARENTHESISOPEN expresion PARENTHESISCLOSE
                | ADDITION varcte
                | SUBTRACTION varcte
                | varcte'''

#Gramática varcte
def p_varcte(p):
    '''varcte : ID
    | CTEI
    | CTEF'''

def p_vacio(p):
    '''
    vacio :
    '''
    p[0] = None

def p_error(p):
    print(p)
    print("HAY UN ERROR")


parser = yacc.yacc()


if __name__ == '__main__':
    try:
        archivo = open('test_file.txt','r')
        info = archivo.read()
        archivo.close()
        if(yacc.parse(info, tracking=True) == 'COMPILED'):
            print("success")
        else:
            print("Error de Sintaxis")
    except EOFError:
        print(EOFError)