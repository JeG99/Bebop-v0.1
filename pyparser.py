import ply.yacc as yacc
import sys

from pylexer import tokens

def p_program(p):
    '''
    program : PROGRAM ID SEMICOLON vars0 block
            | PROGRAM ID SEMICOLON block
    '''
    p[0] = 1

def p_vars0(p):
    '''
    vars0 : VAR ID vars1
    vars1 : COMMA ID vars1 
          | vars2   
    vars2 : COLON type SEMICOLON
    '''

def p_type(p):
    '''
    type : INT
         | FLOAT
    '''

def p_block(p):
    '''
    block : LBRACKET statement RBRACKET
    '''

def p_statement(p):
    '''
    statement : asignation statement
              | condition0 statement
              | writing0 statement
              | empty
    '''

def p_asignation(p):
    '''
    asignation : ID EQUALS expression SEMICOLON
    '''

def p_writing0(p):
    '''
    writing0 : PRINT LPAREN writing1 RPAREN SEMICOLON
    writing1 : expression writing2
             | STRING writing2
    writing2 : writing1 
             | empty
    '''


def p_expression(p):
    '''    
    expression : exp0 relop0
    '''

def p_relop(p):
    '''
    relop0 : relop1 exp0
           | empty
    relop1 : LTHAN
           | GTHAN
           | DIFFERENT 
    '''

def p_exp0(p):
    '''
    exp0 : term0 exp1
    exp1 : PLUS term0 exp1
         | MINUS term0 exp1
         | empty
    '''

def p_condition0(p):
    '''
    condition0 : IF LPAREN expression RPAREN block condition1 
    condition1 : ELSE block condition1
               | empty
    '''

def p_term0(p):
    '''    
    term0 : factor0 term1
    term1 : DIVIDE factor0 term1
          | TIMES factor0 term1
          | empty
    '''

def p_factor0(p):
    '''    
    factor0 : LPAREN expression RPAREN 
            | factor1 var_cte
    factor1 : PLUS
            | MINUS
            | empty
    '''

def p_var_cte(p):
    '''
    var_cte : INT_CTE
            | FLOAT_CTE
            | ID
    '''

def p_empty(p):
    '''
    empty :
    '''

def p_error(p):
    print(p.value)
    print("Código inválido.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        parser = yacc.yacc()
        code = sys.argv[1]
        try:
            _file = open(code, 'r')
            source = _file.read()
            _file.close()
            if parser.parse(source) == 1:
                print("Código válido.")
        except EOFError:
            print(EOFError)
    else:
        print('Se necesita un archivo como argumento.')