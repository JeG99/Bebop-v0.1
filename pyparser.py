import ply.yacc as yacc
import sys
import json

from pylexer import tokens, lexer

func_dir = {}
curr_scope = 'global'
declaration = False
curr_var = ''

def p_routine0(p):
    '''
    routine0 : ROUTINE ID SEMICOLON global_scope routine1 main0
    ''' 
    p[0] = 1
    vars = json.dumps(func_dir, indent=4)
    print(vars)

def p_routine1(p):
    '''
    routine1 : class0 routine1 
             | function0 routine1
             | declaration0 routine1
             | assignment0 routine1
             | empty
    '''

def p_global_scope(p):
    '''
    global_scope :
    '''
    func_dir[curr_scope] = {}

def p_class0(p):
    '''
    class0 : CLASS id_def class1 LBRACKET class2 constructor class3 RBRACKET SEMICOLON
    '''

def p_id_def(p):
    '''
    id_def : ID
    '''
    global curr_scope
    curr_scope = p[1]
    func_dir[curr_scope] = {}

def p_class1(p):
    '''
    class1 : COLON ID
           | empty
    '''
    if(p[1] == ':'):
        func_dir[curr_scope].update(func_dir[p[2]])
        
        

def p_class2(p):
    '''
    class2 : attributes
           | empty
    '''

def p_class3(p):
    '''
    class3 : methods 
           | empty  
    '''

def p_function0(p):
    '''
    function0 : DEF ID LPAREN params0 RPAREN ARROW function1 LSQRBRACKET LSQRBRACKET function2 RSQRBRACKET RSQRBRACKET function_block0
    '''

def p_function1(p):
    '''
    function1 : type
              | VOID
    '''

def p_function2(p):
    '''
    function2 : simple_declaration function2    
              | simple_assignment function2
              | empty
    '''

def p_declaration0(p):
    '''
    declaration0 : ID COLON declaration1 SEMICOLON
    '''
    global curr_scope, declaration, curr_var
    declaration = True
    curr_var = p[1]
    func_dir[curr_scope][p[1]] = {"type" : p[3]}

def p_declaration1(p):
    '''
    declaration1 : type
                 | complex_type
                 | type LSQRBRACKET exp0 RSQRBRACKET declaration2
    '''

def p_declaration2(p):
    '''
    declaration2 : LSQRBRACKET exp0 RSQRBRACKET
                 | empty
    '''

def p_assignment0(p):
    '''
    assignment0 : ID EQUALS expression0 SEMICOLON
                | ID LSQRBRACKET exp0 RSQRBRACKET EQUALS expression0 SEMICOLON
                | ID LSQRBRACKET exp0 RSQRBRACKET LSQRBRACKET exp0 RSQRBRACKET EQUALS expression0 SEMICOLON
    '''
    global curr_scope
    if(p[2] != "["):
        func_dir[curr_scope][p[1]]["value"] = p[3]    
    

def p_constructor(p):
    '''
    constructor : CONSTRUCT ID LPAREN params0 RPAREN function_block0
    '''

#def p_extension0(p): # quitamos polimorfismo temporalmente
#    '''
#    extension0 : ID
#    '''

def p_attributes(p):
    '''
    attributes : data_access simple_declaration attributes
               | simple_assignment attributes
               | empty
    '''

def p_methods(p):
    '''
    methods : data_access function0 methods
            | empty
    '''

def p_params0(p):
    '''
    params0 : type ID params1
            | empty
    '''

def p_params1(p):
    '''
    params1 : COMMA params0
            | empty
    '''

def p_function_block0(p):
    '''
    function_block0 : LBRACKET function_block1 RBRACKET
    '''

def p_function_block(p):
    '''
    function_block1 : function_statement function_block1
                    | empty
    '''

def p_type(p):
    '''
    type : INT
         | FLOAT
         | STRING
         | BOOL
    '''
    global declaration, curr_var
    if declaration:
        func_dir[curr_scope][curr_var]['type'] = p[1]
    declaration = False

def p_simple_declaration(p):
    '''
    simple_declaration : ID COLON type SEMICOLON
    '''
    global curr_scope, declaration, curr_var
    declaration = True
    curr_var = p[1]
    func_dir[curr_scope][p[1]] = {"type" : p[3]}

def p_simple_assignment(p):
    '''
    simple_assignment : ID EQUALS expression0 SEMICOLON
    '''
    global curr_scope
    func_dir[curr_scope][p[1]]["value"] = p[3]

def p_complex_type(p):
    '''
    complex_type : ID
    '''

def p_logic_or0(p):
    '''
    logic_or0 : logic_and0 logic_or1
    '''
def p_logic_or1(p):
    '''
    logic_or1 : OR logic_or0
              | empty
    '''

def p_logic_and0(p):
    '''
    logic_and0 : logic_operand logic_and1
    '''

def p_logic_and1(p):
    '''
    logic_and1 : AND logic_and0
               | empty
    '''

def p_logic_operand0(p):
    '''
    logic_operand : NOT expression0
    '''

def p_exp0(p):
    '''
    exp0 : term0 exp1
    '''

def p_exp1(p):
    '''
    exp1 : PLUS exp0
         | MINUS exp0
         | empty
    '''

def p_term0(p):
    '''
    term0 : factor term1
    '''

def p_term1(p):
    '''
    term1 : MULTIPLY term0
          | DIVIDE term0
          | empty
    '''

def p_factor(p):
    '''
    factor : PLUS power0
           | MINUS power0
           | power0 
    '''

def p_power0(p):
    '''
    power0 : LPAREN exp0 RPAREN power2
           | const_var power2
           | function_call power2
           | method_call0 power2
           | attr_access0 power2
           | ID LSQRBRACKET exp0 RSQRBRACKET power1 power2 
    '''

def p_power1(p):
    '''
    power1 : LSQRBRACKET exp0 RSQRBRACKET
           | empty
    '''

def p_power2(p):
    '''
    power2 : POWER power0
           | SQRT power0
           | empty
    '''

def p_const_var(p):
    '''
    const_var : CONST_INT
              | CONST_FLOAT
              | ID
    '''

def p_function_call(p):
    '''
    function_call : ID LPAREN function_call_params0 RPAREN 
    '''

def p_function_call_params0(p):
    '''
    function_call_params0 : expression0 function_call_params1
                          | CONST_STRING function_call_params1
                          | empty function_call_params1
    '''

def p_function_call_params1(p):
    '''
    function_call_params1 : COMMA function_call_params0
                          | empty 
    '''

def p_expression0(p):
    '''
    expression0 : exp0 expression1
                | CONST_BOOL expression1
                | attr_access0 expression1
    ''' 

def p_expression1(p):
    '''
     expression1 : empty
                | expression2
    '''

def p_expression2(p):
    '''
    expression2 : LTHAN expression3 
                | GTHAN expression3
                | DIFFERENT expression3
                | EQUIVALENT expression3
    '''

def p_expression3(p):
    '''
    expression3 : exp0
                | CONST_BOOL
                | attr_access0
    '''

def p_attr_access0(p): # eliminamos anidamiento temporalmente
    '''
    attr_access0 : ID DOT ID
    '''

def p_method_call0(p): # eliminamos anidamiento temporalmente 
    '''
    method_call0 : ID DOT function_call
    '''

def p_data_access(p):
    '''
    data_access : PRIVATE
                | PUBLIC
    '''

def p_function_statement(p):
    '''
    function_statement : simple_assignment
                       | condition0
                       | writing0
                       | reading
                       | return
                       | function_call SEMICOLON
                       | method_call0 SEMICOLON
                       | while
    '''

def p_condition0(p):
    '''
    condition0 : IF LPAREN expression0 RPAREN block0 condition1 SEMICOLON 
    '''

def p_condition1(p):
    '''
    condition1 : ELSE block0
               | empty
    '''

def p_writing0(p):
    '''
    writing0 : WRITE LPAREN writing1 RPAREN SEMICOLON
    '''

def p_writing1(p):
    '''
    writing1 : expression0 writing2
             | CONST_STRING writing2
    '''

def p_writing2(p):
    '''
    writing2 : COMMA writing1
             | empty
    '''

def p_reading(p):
    '''

    reading : READ ID SEMICOLON
    '''

def p_return(p):
    '''
    return : RETURN expression0 SEMICOLON
           | RETURN SEMICOLON
    '''

def p_while(p):
    '''
    while : WHILE LPAREN expression0 RPAREN block0
    '''

def p_block0(p):
    '''
    block0 : LBRACKET block1 RBRACKET
    '''

def p_block1(p):
    '''
    block1 : statement block1
           | empty
    '''

def p_statement(p):
    '''
    statement : assignment0
              | object_assignment
              | condition0
              | writing0
              | reading
              | return
              | function_call SEMICOLON
              | method_call0 SEMICOLON
              | while
    '''

def p_object_assignment(p):
    '''
    object_assignment : ID EQUALS NEW ID LPAREN function_call_params0 RPAREN SEMICOLON  
    '''

def p_main(p):
    '''
    main0 : MAIN main_scope LBRACKET main1 RBRACKET 
    '''

def p_main1(p):
    '''
    main1 : declaration0 main1
          | statement main1 
          | empty
    '''
def p_main_scope(p):
    '''
    main_scope : 
    '''
    global curr_scope
    curr_scope = "main"
    func_dir[curr_scope] = {}

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
            
            #for lexem in lexer:
            #    print(lexem)

            if parser.parse(source) == 1:
                print("Código válido.")
            
        except EOFError:
            print(EOFError)
    else:
        print('Se necesita un archivo como argumento.')