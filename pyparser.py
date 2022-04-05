import ply.yacc as yacc
import sys

from pylexer import tokens, lexer

def p_program(p):
    '''
    program : ROUTINE ID SEMICOLON class VAR vars function block
            | ROUTINE ID SEMICOLON VAR vars function block
            | ROUTINE ID SEMICOLON class VAR vars block
            | ROUTINE ID SEMICOLON VAR vars block
            | ROUTINE ID SEMICOLON block
    '''
    p[0] = 1

def p_vars(p):
    '''
    vars : vars0 vars 
         | vars0
    '''

def p_vars0(p):
    '''
    vars0 : ID vars1
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
                | ID EQUALS object_assignation SEMICOLON
    '''

def p_object_assignation(p):
    '''
    object_assignation : NEW ID LPAREN RPAEN 
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
    exp1 : PLUS exp0
         | MINUS exp0
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
    term0 : factor term1
    term1 : DIVIDE term0
          | TIMES term0
          | empty
    '''

def p_factor(p):
    '''
    factor : LPAREN expression RPAREN
           | PLUS var_cte
           | MINUS var_cte
           | var_cte
           | PLUS function_call
             | MINUS function_call
            | function_call
    '''

def p_var_cte(p):
    '''
    var_cte : CONS_INT
            | CONS_FLOAT
            | ID
    '''

def p_import(p):
    '''
    import : MINUS GTHAN library 
    '''
#  -> import file

#def p_function(p):
'''
function : type ID LPAREN param RPAREN MINUS GTHAN type LBRACKET vars block RBRACKET function
        | type ID LPAREN param RPAREN MINUS GTHAN type LBRACKET vars block RBRACKET
        | VOID ID LPAREN param RPAREN MINUS GTHAN type LBRACKET vars block RBRACKET function
        | VOID ID LPAREN param RPAREN MINUS GTHAN type LBRACKET vars block RBRACKET 
'''


def function_call(p):
    '''
    function_call : ID LPAREN function_call_param RPAREN 
    '''

def function_call_param(p):
    '''
    function_call_param : ID param
            | COMMA ID param
            | empty
    '''

def p_param(p):
    '''
    param : type ID param
            | COMMA type ID param
            | empty
    '''


def p_class(p):
    '''
    class : CLASS ID LBRACKET attribute constructor method RBRACKET SEMICOLON
            | CLASS ID COLON extension LBRACKET attribute constructor method RBRACKET SEMICOLON
    '''

def p_constructor(p):
    '''
    constructor: CONSTRUCT LPAREN param RPAREN LBRACKET block RBRACKET  
    '''

def p_data_access(p):
    '''
    data_access : PRIVATE
                | PUBLIC
    '''

def p_extension(p): 
    '''
    extension : data_access ID COMMA
                | data_access ID
    '''

def p_attribute(p):
    '''
    attribute : data_access type ID semicolon attribute
            | data_access type ID semicolon
    '''

def p_method(p):
    '''
    method : data_access function method
            | empty
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
            lexer.input(source)
            
            for lexem in lexer:
                print(lexem)

            if parser.parse(source) == 1:
                print("Código válido.")
            
        except EOFError:
            print(EOFError)
    else:
        print('Se necesita un archivo como argumento.')