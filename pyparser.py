from cgi import print_environ
import ply.yacc as yacc
import sys
import json

from pylexer import tokens, lexer

func_dir = {}
class_dir = {}
curr_scope = ''
prev_scope = ""
var_id = ""

quadruples = []
quadCounter = 0
operands_stack = []
operators_stack = []
types_stack = []
temp_counter = 0
pSaltos = []
Gi = 0
Gf = 2001
Go = 4001
Li = 5000
Lf = 7001
Lo = 10001
Ti = 11000
Tf = 12001
Tb = 13001
To = 14001
Ts = 15001
Ci = 16000
Cf = 17001

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

sem_cube = {
    'sum': {
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
    ((0, 1, -1, -1), (0, 1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((0, 1, -1, -1), (0, 1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((0, 1, -1, -1), (0, 1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((0, 1, -1, -1), (0, 1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((0, 1, -1, -1), (0, 1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((0, 1, -1, -1), (0, 1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((0, -1, -1, -1), (-1, 1, -1, -1), (-1, -1, 2, -1), (-1, -1, -1, 3)),
    ((2, 2, -1, -1), (2, 2, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((2, 2, -1, -1), (2, 2, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((2, 2, -1, -1), (2, 2, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)),
    ((2, 2, -1, -1), (2, 2, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1))
)


def p_routine0(p):
    '''
    routine0 : goto_main_neur ROUTINE ID SEMICOLON global_scope routine1 main0
    '''
    global quadCounter, quadruples
    p[0] = 1
    quadruples.append(["END", None, None, None])
    quadCounter+=1
    print(json.dumps(func_dir, indent=4))
    #print(operands_stack)
    #print(types_stack)
    #print(operators_stack)
    #print('\nquadruples:')
    #[print(quad) for quad in quadruples]
    #print(pSaltos)

def p_goto_main_neur(p):
    '''
    goto_main_neur :
    '''
    global quadruples, quadCounter
    quadruples.append(["GOTO", "main", None, None])
    quadCounter = quadCounter + 1



def p_routine1(p):
    '''
    routine1 : statement routine1
             | class0 routine1 
             | function0 routine1
             | declaration0 routine1
             | assignment0 routine1
             | empty
    '''
    global func_dir, Gi, Gf, Go, Li, Lf, Lo
    if(p[1] != None and 'def' in p[1][0]):
        if p[1][3] == "int":
            direc = Gi
            Gi += 1
        elif p[1][3] == "float":
            direc = Gf
            Gf += 1
        else:
            direc = Go
            Go += 1
        print(Gi, "a")
        func_dir["global"]["vars_table"][p[1][1]] = {"type": p[1][3], "dirV": direc}
        func_dir[p[1][1]] = {"return_type": None, "vars_table": {}}
        paramsAux = p[1][2]
        func_dir[p[1][1]]["return_type"] = p[1][3]
        while paramsAux != None:
            if paramsAux[0] == "int":
                direc = Li
                Li += 1
            elif paramsAux == "float":
                direc = Lf
                Lf += 1
            else:
                direc = Lo
                Lo += 1
            print(direc)
            func_dir[p[1][1]]["vars_table"][paramsAux[1]] = {
                "type": paramsAux[0], "dirV":direc}
            paramsAux = paramsAux[2]
        Li = 5000
        Lf = 7001
        Lo = 10001


def p_global_scope(p):
    '''
    global_scope :
    '''
    global curr_scope, func_dir
    curr_scope = "global"
    func_dir[curr_scope] = {"return_type": "void", "vars_table": {}}


def p_class0(p):
    '''
    class0 : CLASS class_id_def class1 LBRACKET class2 constructor class3 RBRACKET SEMICOLON revert_global
    '''


def p_revert_global(p):
    '''
    revert_global :
    '''
    global curr_scope
    curr_scope = "global"


def p_revert_scope(p):
    '''
    revert_scope : 
    '''
    global curr_scope, prev_scope
    curr_scope = prev_scope


def p_id_def(p):
    '''
    id_def : ID
    '''
    global curr_scope, func_dir, prev_scope
    prev_scope = curr_scope
    curr_scope = p[1]
    p[0] = p[1]


def p_class_id_def(p):
    '''
    class_id_def : ID
    '''
    global curr_scope, func_dir, prev_scope
    prev_scope = curr_scope
    curr_scope = p[1]
    class_dir[curr_scope] = {"constructor": {},
                             "method_table": {}, "vars_table": {}}
    p[0] = p[1]


def p_class1(p):
    '''
    class1 : COLON ID
           | empty
    '''
    if(p[1] == ':'):
        # pass
        for i in class_dir[p[2]]["vars_table"].keys():
            class_dir[curr_scope]["vars_table"][i] = class_dir[p[2]
                                                               ]["vars_table"][i]
        class_dir[curr_scope]["method_table"] = class_dir[p[2]]["method_table"]


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
    function0 : DEF id_def LPAREN params0 RPAREN ARROW function1 LSQRBRACKET LSQRBRACKET function2 RSQRBRACKET RSQRBRACKET function_block0 revert_scope
    '''
    global quadruples, quadCounter
    p[0] = (p[1], p[2], p[4], p[7])
    quadruples.append(["ENDPROC",None,None,None])
    quadCounter += 1



def p_function1(p):
    '''
    function1 : type
              | VOID
    '''
    p[0] = p[1]


def p_function2(p):
    '''
    function2 : simple_declaration function2    
              | simple_assignment function2
              | empty
    '''


def p_declaration0(p):
    '''
    declaration0 : decl_id_def COLON declaration1 SEMICOLON
    '''
    global Li, Lf, Lo
    if p[3] == "int":
        direc = Li
        Li += 1
    elif p[3] == "float":
        direc = Lf
        Lf += 1
    else:
        direc = Lo
        Lo += 1
    func_dir[curr_scope]["vars_table"][p[1]] = {"type": p[3], "dirV" : direc}


def p_decl_id_def(p):
    '''
    decl_id_def : ID
    '''
    p[0] = p[1]
    global var_id
    var_id = p[1]


def p_declaration1(p):
    '''
    declaration1 : type
                 | complex_type
                 | type LSQRBRACKET exp0 RSQRBRACKET neurMemory declaration2
    '''
    p[0] = p[1]

def p_neurMemory(p):
    '''
    neurMemory :
    '''
    global Li, Lf, Lo, func_dir, curr_scope, var_id, Gi, Gf, Go, operands_stack
    print("Si entra", p[-4])
    if curr_scope != "global":
        if p[-4] == "int":
            direc = Li
            Li += 1
        elif p[-4] == "float":
            direc = Lf
            Lf += 1
        else:
            direc = Lo
            Lo += 1
    else:
        if p[-4] == "int":
            direc = Gi
            Gi += 1
        elif p[-4] == "float":
            direc = Gf
            Gf += 1
        else:
            direc = Go
            Go += 1
    func_dir[curr_scope]["vars_table"][var_id] = {"type": p[-4], "dirv" : direc, "IsArray": True}


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
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter
    if len(p) == 5 and operands_stack:
        value = operands_stack.pop()
        quad = [p[2], value, None, p[1]]
        quadruples.append(quad)
        quadCounter += 1
    elif len(p) == 8 and operands_stack:
        value = operands_stack.pop()



def p_constructor(p):
    '''
    constructor : CONSTRUCT ID LPAREN params0 RPAREN function_block0
    '''
    class_dir[curr_scope]["constructor"][p[2]] = {}
    if(p[4] != None):
        paramsAux = p[4]
        while paramsAux != None:
            class_dir[curr_scope]["constructor"][p[2]][paramsAux[1]] = {"type": paramsAux[0]}
            #class_dir[curr_scope]["method_table"][p[2]][p[4][1]] = {"type":p[4][0]}
            paramsAux = paramsAux[2]

# def p_extension0(p): # quitamos polimorfismo temporalmente
#    '''
#    extension0 : ID
#    '''


def p_attributes(p):
    '''
    attributes : data_access simple_declaration attributes
               | simple_assignment attributes
               | empty
    '''
    if(p[1] != None):
        if(p[1] == "private" or p[1] == "public"):
            #print(curr_scope, p[2][0])
            class_dir[curr_scope]["vars_table"][p[2][0]] = p[2][1]


def p_methods(p):
    '''
    methods : data_access function0 methods
            | empty
    '''
    #for i in p: print(i)
    if(len(p) > 2):
        if(p[2][2] != None):
            class_dir[curr_scope]["method_table"][p[2][1]] = {}
            paramsAux = p[2][2]
            while(paramsAux != None):
                class_dir[curr_scope]["method_table"][p[2][1]
                                                      ][paramsAux[1]] = {"type": paramsAux[0]}
                paramsAux = paramsAux[2]


def p_params0(p):
    '''
    params0 : type ID params1
            | empty
    '''
    
    if(p[1] != None):
        p[0] = (p[1], p[2], p[3])


def p_params1(p):
    '''
    params1 : COMMA params0
            | empty
    '''
    if(p[1] != None):
        p[0] = p[2]


def p_function_block0(p):
    '''
    function_block0 : LBRACKET function_block1 RBRACKET
    '''


def p_function_block1(p):
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
    #global curr_scope, var_id, func_dir
    #print(curr_scope, var_id, p[1])
    #func_dir[curr_scope][var_id] = {"type": p[1]}
    p[0] = p[1]


def p_simple_declaration(p):
    '''
    simple_declaration : ID COLON type SEMICOLON
    '''
    #global curr_scope, var_id, func_dir
    # print(p[3])
    p[0] = (p[1], p[3])
    #func_dir[curr_scope][p[1]] = {"type": p[3]}
    # print(curr_scope)
    #var_id = p[1]


def p_simple_assignment(p):
    '''
    simple_assignment : ID EQUALS expression0 SEMICOLON
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter
    if len(operands_stack):
        value = operands_stack.pop()
        quad = [p[2], value, None, p[1]]
        quadruples.append(quad)
        quadCounter += 1
    #global curr_scope
    #func_dir[curr_scope][p[1]]["value"] = p[3]


def p_complex_type(p):
    '''
    complex_type : ID
    '''
    p[0] = p[1]

# def p_logic_or0(p):
#    '''
#    logic_or0 : logic_and0 logic_or1
#    '''

# def p_logic_or1(p):
#    '''
#    logic_or1 : OR logic_or0
#              | empty
#    '''

# def p_logic_and0(p):
#    '''
#    logic_and0 : logic_operand logic_and1
#    '''

# def p_logic_and1(p):
#    '''
#    logic_and1 : AND logic_and0
#               | empty
#    '''

# def p_logic_operand0(p):
#    '''
#    logic_operand : NOT expression0
#    '''


def p_exp0(p):
    '''
    exp0 : term0 check_last_plus_minus_operator exp1
    '''


def p_exp1(p):
    '''
    exp1 : PLUS push_plus_minus_op exp0
         | MINUS push_plus_minus_op exp0
         | empty
    '''


def p_push_plus_minus_op(p):
    '''
    push_plus_minus_op :
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter
    operators_stack.append(p[-1])


def p_check_last_plus_minus_operator(p):
    '''
    check_last_plus_minus_operator :
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter
    # falta typematching
    if len(operators_stack) and len(operands_stack) and (operators_stack[-1] == '+' or operators_stack[-1] == '-'):
        right_oper = operands_stack.pop()
        left_oper = operands_stack.pop()
        op = operators_stack.pop()
        operands_stack.append(('dir', temp_counter))
        quad = [op, left_oper,
                right_oper, ('dir', temp_counter)]
        quadruples.append(quad)
        quadCounter += 1
        temp_counter += 1


def p_term0(p):
    '''
    term0 : power0 check_last_times_division_operator term1
    '''


def p_term1(p):
    '''
    term1 : MULTIPLY push_times_division_op term0
          | DIVIDE push_times_division_op term0
          | empty
    '''


def p_push_times_division_op(p):
    '''
    push_times_division_op :
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter
    operators_stack.append(p[-1])


def p_check_last_times_division_operator(p):
    '''
    check_last_times_division_operator :
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter
    if len(operators_stack) and len(operands_stack) and (operators_stack[-1] == '*' or operators_stack[-1] == '/'):
        right_oper = operands_stack.pop()
        left_oper = operands_stack.pop()
        op = operators_stack.pop()
        operands_stack.append(('dir', temp_counter))
        quad = [op, left_oper,
                right_oper, ('dir', temp_counter)]
        quadruples.append(quad)
        quadCounter += 1
        temp_counter += 1


'''
def p_factor(p):
    '''''''
    factor : check_last_unary_sign_operator PLUS power0
           | check_last_unary_sign_operator MINUS power0
           | power0 
    ''''''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter
    if (p): # Distinto de None (empty)
        operators_stack.append(p[1])
    print(operators_stack)

def p_check_last_unary_sign_operator(p):
    ''''''
    check_last_unary_sign_operator :
    ''''''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter
    # falta typematching
    if len(operators_stack) > 0 and (operators_stack[-1] == 'u+' or operators_stack[-1] == 'u-'):
        oper = operands_stack.pop()
        operands_stack.append(('dir', temp_counter))
        quad = [operators_stack[-1], oper, None, ('dir', temp_counter)]
        quadruples.append(quad)
        temp_counter += 1
'''


def p_power0(p):
    '''
    power0 : LPAREN open_paren exp0 RPAREN close_paren check_pow_rad_operator power2
           | const_var check_pow_rad_operator power2
           | function_call check_pow_rad_operator power2
           | method_call0 check_pow_rad_operator power2
           | attr_access0 check_pow_rad_operator power2
           | ID LSQRBRACKET exp0 RSQRBRACKET check_pow_rad_operator power1 power2 
    '''

def p_open_paren(p):
    '''
    open_paren : 
    '''
    global operators_stack
    operators_stack.append('(')

def p_close_paren(p):
    '''
    close_paren : 
    '''
    global operators_stack
    operators_stack.pop()

def p_power1(p):
    '''
    power1 : LSQRBRACKET exp0 RSQRBRACKET
           | empty
    '''


def p_power2(p):
    '''
    power2 : POWER push_pow_rad_op power0
           | SQRT push_pow_rad_op power0
           | empty
    '''


def p_push_pow_rad_op(p):
    '''
    push_pow_rad_op :
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter
    operators_stack.append(p[-1])


def p_check_pow_rad_operator(p):
    '''
    check_pow_rad_operator :
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter, Ti, Tf, Tb, To
    # falta typematching
    if len(operators_stack) and len(operands_stack) and (operators_stack[-1] == '\\|' or operators_stack[-1] == '**'):
        right_oper = operands_stack.pop()
        left_oper = operands_stack.pop()
        op = operators_stack.pop()
        print(right_oper, left_oper)
        operands_stack.append(('dir', temp_counter))
        quad = [op, left_oper,
                right_oper, ('dir', temp_counter)]
        quadruples.append(quad)
        quadCounter += 1
        temp_counter += 1


def p_const_var(p):
    '''
    const_var : CONST_INT neurInt
              | CONST_FLOAT neurFloat
              | ID
    '''
    p[0] = p[1]
    operands_stack.append(p[1])

def p_neurInt(p):
    '''
    neurInt :
    '''
    global types_stack
    types_stack.append("int")

def p_neurFloat(p):
    '''
    neurFloat :
    '''
    global types_stack
    types_stack.append("float")

def p_function_call(p):
    '''
    function_call : id_funcCall LPAREN function_call_params0 RPAREN 
    '''
    global quadruples, quadCounter
    quad = ["GOSUB", p[1], None, None]
    quadruples.append(quad)
    quadCounter += 1
    #print(p[3], "AaAa")

def p_id_funcCall(p):
    '''
    id_funcCall : ID
    '''
    global quadruples, quadCounter
    quad = ["ERA", p[1], None, None]
    quadruples.append(quad)
    quadCounter += 1
    p[0] = p[1]


def p_function_call_params0(p):
    '''
    function_call_params0 : expression0 neurFuncCallParams1 function_call_params1
                          | CONST_STRING neurFuncCallParams1 function_call_params1
                          | empty function_call_params1
    '''


def p_neurFuncCallParams1(p):
    '''
    neurFuncCallParams1 : 
    '''
    global quadruples, quadCounter, operands_stack
    aux = operands_stack.pop()
    quadruples.append(["PARAM",None, None, aux])
    quadCounter+=1


def p_function_call_params1(p):
    '''
    function_call_params1 : COMMA function_call_params0
                          | empty 
    '''
    if(p[1] != None):
        p[0] = p[2]


def p_expression0(p):
    '''
    expression0 : exp0 expression1
                | attr_access0 expression1
    '''  # falta soporte para atributos en los cuadruplos


def p_expression1(p):
    '''
    expression1 : LTHAN push_rel_op expression3 
                | GTHAN push_rel_op expression3
                | DIFFERENT push_rel_op expression3
                | EQUIVALENT push_rel_op expression3
                | empty
    '''


def p_push_rel_op(p):
    '''
    push_rel_op :
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter
    operators_stack.append(p[-1])


def p_check_rel_operator(p):
    '''
    check_rel_operator :
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter
    # falta typematching
    if operators_stack and operands_stack and (operators_stack[-1] == '<' or operators_stack[-1] == '>' or operators_stack[-1] == '<>' or operators_stack[-1] == '=='):
        right_oper = operands_stack.pop()
        left_oper = operands_stack.pop()
        op = operators_stack.pop()
        operands_stack.append(('dir', temp_counter))
        quad = [op, left_oper,
                right_oper, ('dir', temp_counter)]
        quadruples.append(quad)
        quadCounter += 1
        temp_counter += 1


def p_expression3(p):
    '''
    expression3 : exp0 check_rel_operator
                | attr_access0
    '''


def p_attr_access0(p):  # eliminamos anidamiento temporalmente
    '''
    attr_access0 : ID DOT ID
    '''


def p_method_call0(p):  # eliminamos anidamiento temporalmente
    '''
    method_call0 : ID DOT function_call
    '''


def p_data_access(p):
    '''
    data_access : PRIVATE
                | PUBLIC
    '''
    p[0] = p[1]
    global curr_scope
    # print(curr_scope)


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
    condition0 : IF LPAREN expression0 condNeur1 RPAREN block0 condition1 SEMICOLON condNeur3
    '''


def p_condNeur1(p):
    '''
    condNeur1 :
    '''
    global pSaltos, quadruples, quadCounter
    pSaltos.append(quadCounter)
    quadruples.append(["GOTOF", None, None, None])
    quadCounter += 1


def p_condNeur3(p):
    '''
    condNeur3 :
    '''
    global pSaltos, quadruples, quadCounter
    temp = pSaltos.pop()
    quadruples[temp][3] = quadCounter + 1


def p_condition1(p):
    '''
    condition1 : ELSE condNeur2 block0
               | empty
    '''


def p_condNeur2(p):
    '''
    condNeur2 :
    '''
    global pSaltos, quadruples, quadCounter
    temp = pSaltos.pop()
    quadruples[temp][3] = quadCounter + 1
    pSaltos.append(quadCounter)
    quadruples.append(["GOTO", None, None, None])
    quadCounter += 1


def p_writing0(p):
    '''
    writing0 : WRITE push_writing_op LPAREN writing1 RPAREN SEMICOLON
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter
    if operands_stack:
        #print('aperro')
        value = operands_stack.pop()
        op = operators_stack.pop()
        quad = [op, None, None, value]
        quadruples.append(quad)
        quadCounter += 1


def p_push_writing_op(p):
    '''
    push_writing_op :
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter
    operators_stack.append(p[-1])


def p_push_string_val(p):
    '''
    push_string_val :
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter
    operands_stack.append(p[-1])


def p_writing1(p):
    '''
    writing1 : expression0 writing2
             | CONST_STRING push_string_val writing2
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
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter
    quad = [p[1], None, None, p[2]]
    quadruples.append(quad)
    quadCounter += 1


def p_return(p):
    '''
    return : RETURN expression0 SEMICOLON
           | RETURN SEMICOLON
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter
    if len(p) == 4 and len(operands_stack):
        value = operands_stack.pop()
        quad = [p[1], None, None, value]
        quadruples.append(quad)
        quadCounter += 1


def p_while(p):
    '''
    while : WHILE wNeur1 LPAREN expression0 RPAREN wNeur2 block0 wNeur3
    '''


def p_wNeur1(p):
    '''
    wNeur1 :
    '''
    global pSaltos, quadruples, quadCounter
    pSaltos.append(quadCounter)
   


def p_wNeur2(p):
    '''
    wNeur2 :
    '''
    global pSaltos, quadruples, quadCounter
    pSaltos.append(quadCounter)
    quadruples.append(["GOTOF", None, None, None])
    quadCounter += 1
    


def p_wNeur3(p):
    '''
    wNeur3 :
    '''
    global pSaltos, quadruples, quadCounter
    temp1 = pSaltos.pop()
    temp2 = pSaltos.pop()
    #print(temp1, temp2)
    quadruples.append(["GOTO", None, None, temp2])
    quadCounter += 1
    #print(quadruples[temp2], end = "\n\n\n")
    quadruples[temp1][3] = quadCounter + 1


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
    global Li, Lf, Lo
    Li = 5000
    Lf = 7001
    Lo = 10001

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
    global curr_scope, func_dir, prev_scope
    prev_scope = curr_scope
    curr_scope = "main"
    func_dir[curr_scope] = {"return_type": "void", "vars_table": {}}


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

            # for lexem in lexer:
            #    print(lexem)

            if parser.parse(source) == 1:
                print("Código válido.")

        except EOFError:
            print(EOFError)
    else:
        print('Se necesita un archivo como argumento.')
