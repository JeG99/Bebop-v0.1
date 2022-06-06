import ply.yacc as yacc
import sys
import json

from pylexer import tokens, lexer

func_dir = {}
class_dir = {}
curr_scope = ''
prev_scope = ""
var_id = ""
<<<<<<< Updated upstream
=======
const_table = {}
dim1Node = {}
dimNodes = [
    {"ls":0, "li":0,"r": 1, "m": 0},
    {"ls":0, "li":0,"r": 1, "m": 0}
]
dimCounter = 0

quadruples = []
quadCounter = 0
operands_stack = []
operators_stack = []
types_stack = []
temp_counter = 0
prev_table = {}
pSaltos = []
paramCounter = 0
paramTableCounter = 0
currFuncCall = ""
dimAssign  = 0
temporalCounter = 0

## Global addresses
Gi = 0
Gf = 2001
Go = 4001

## Local Addresses
Li = 5000
Lf = 7001
Lo = 10001

## Temporal Addresses
Ti = 11000
Tf = 12001
Tb = 13001
To = 14001
Ts = 15001

## Constant Addresses
Ci = 16000
Cf = 17001
Cs = 18001 

## Pointer Address
Tp = 19000


### Aux Function tempCalculator
# params: left_oper, right_oper, op
# Takes operands used to validate the type generated from a certain operation
# Function used to validate constant and variable types with semantic cube
# Return: direc(Temporal direction for saving result), rOperDir(calculated direction of right operand), lOperDir(calculated direction of left operand)

def tempCalculator(left_oper, right_oper, op):
    global Ti, Tf, To, Tb, curr_scope, currFuncCall, temporalCounter
    ### RIGHT
    #Check if constant
    if right_oper in const_table.keys():
        rOperDir = const_table[right_oper]
        if rOperDir >= 16000 and rOperDir < 17001 :
            rOperType = "int"
        elif rOperDir >= 17001 and rOperDir < 18000:
            rOperType = "float"
    else:
        #Check in current scope, go to global, or check temporals
        if right_oper in func_dir[curr_scope]["vars_table"].keys():
           rOperType = func_dir[curr_scope]["vars_table"][right_oper]["type"]
           rOperDir = func_dir[curr_scope]["vars_table"][right_oper]["dirV"]
        elif right_oper in func_dir["global"]["vars_table"].keys():
           rOperType = func_dir["global"]["vars_table"][right_oper]["type"]
           rOperDir = func_dir["global"]["vars_table"][right_oper]["dirV"]
        else:
            if right_oper >= 11000 and right_oper < 12001 :
                rOperType = "int"
            elif right_oper >= 12001 and right_oper < 13001:
                rOperType = "float"
            rOperDir = right_oper

    ### LEFT
    #Check if constant
    if left_oper in const_table.keys():
            lOperDir = const_table[left_oper]
            if lOperDir >= 16000 and lOperDir < 17001 :
                lOperType = "int"
            elif lOperDir >= 17001 and lOperDir < 18000:
                lOperType = "float"
    elif left_oper in const_table.values():
        lOperDir = left_oper
        if lOperDir >= 16000 and lOperDir < 17001 :
            lOperType = "int"
        elif lOperDir >= 17001 and lOperDir < 18000:
            lOperType = "float"
    else:
        #Check in current scope, go to global, or check temporals
        if left_oper in func_dir[curr_scope]["vars_table"].keys():
           lOperType =  func_dir[curr_scope]["vars_table"][left_oper]["type"]
           lOperDir = func_dir[curr_scope]["vars_table"][left_oper]["dirV"]
        elif left_oper in func_dir["global"]["vars_table"].keys():
           lOperType =  func_dir["global"]["vars_table"][left_oper]["type"]
           lOperDir = func_dir["global"]["vars_table"][left_oper]["dirV"]
        else:
            if left_oper >= 11000 and left_oper < 12001 :
                lOperType = "int"
            elif left_oper >= 12001 and left_oper < 13001:
                lOperType = "float"
            lOperDir = left_oper
    #Utilize Semantic Cube to check if types are correct
    if op == "+":
        typeRes = typeMatch("SUM",rOperType, lOperType)
    elif op == "-":
        typeRes = typeMatch("SUB", rOperType, lOperType)
    elif op == "*":
        typeRes = typeMatch("MUL", rOperType, lOperType)
    elif op == "/":
        typeRes = typeMatch("DIV", rOperType, lOperType)
    elif op == "<":
        typeRes = typeMatch("LT", rOperType, lOperType)
    elif op == ">":
        typeRes = typeMatch("GT", rOperType, lOperType)
    elif op == "**":
        typeRes = typeMatch("EXP", rOperType, lOperType)
    elif op == "\\|":
        typeRes = typeMatch("SQRT", rOperType, lOperType)
    elif op == "==":
        typeRes = typeMatch("EQUIVALENT", rOperType, lOperType)
    elif op == "<>":
        typeRes = typeMatch("NEQUIVALENT", rOperType, lOperType)
    if typeRes == "INT":
        if Ti >= 12001:
            raise MemoryError("Temporal integer limit reached")
        else:
            direc = Ti
            Ti += 1
    elif typeRes == "FLOAT":
        if Tf >= 13001:
            raise MemoryError("Temporal float limit reached")
        else:
            direc = Tf
            Tf += 1
    elif typeRes == "BOOL":
        if Tb >= 14001:
            raise MemoryError("Temporal bool limit reached")
        else:
            direc = Tb
            Tb += 1
    else:
        if To >= 15001:
            raise MemoryError("Temporal other limit reached")
        else:
            direc = To
            To += 1
    temporalCounter += 1
    return direc, lOperDir, rOperDir
>>>>>>> Stashed changes

# TYPE CODEs
# int: 0
# float: 1
# 
# OPERATOR CODES
# sum: 0
# sub: 1
# mul: 2
# div: 3
# exp: 4
# sqrt: 5

# RESULTING_TYPE = sem_cube[OPERATOR][OP1][OP2]
# EX:
# RESULTING_TYPE = sem_cube[DIV][INT][FLOAT]
# RESULTING_TYPE = sem_cube[3][0][1] = 1 = FLOAT

sem_cube = (
    ((0, 1), (1, 1)),
    ((0, 1), (1, 1)),
    ((0, 1), (1, 1)),
    ((0, 1), (1, 1)),
    ((0, 1), (1, 1)),
    ((0, 1), (1, 1))
)

def p_routine0(p):
    '''
    routine0 : ROUTINE ID SEMICOLON global_scope routine1 main0
    ''' 
    p[0] = 1
<<<<<<< Updated upstream
    print(json.dumps(func_dir, indent=5))
    #print(json.dumps(class_dir, indent=5))
=======
    quadruples.append(["END", None, None, None])
    quadCounter += 1
    print(json.dumps(func_dir, indent=4))
    #print(operands_stack)
    #print(types_stack)
    #print(operators_stack)
    #print('\nquadruples:')
    #print(const_table)
    [print(idx, quad) for idx, quad in enumerate(quadruples)]
    vm = VirtualMachine(quadruples, func_dir, const_table)
    vm.mem_init()
    vm.run()


### Neural Point 1
# Generates first quaruple GOTO main
def p_goto_main_neur(p):
    '''
    goto_main_neur :
    '''
    global quadruples, quadCounter, const_table, Ci, Cf
    quadruples.append(["GOTO", "main", None, None])
    quadCounter = quadCounter + 1
    const_table[0] = Ci
    Ci += 1
    const_table[0.0] = Cf
    Cf+= 1
>>>>>>> Stashed changes

def p_routine1(p):
    '''
    routine1 : class0 routine1 
             | function0 routine1
             | declaration0 routine1
             | assignment0 routine1
             | empty
    '''
<<<<<<< Updated upstream
    global func_dir
    if(p[1] != None and 'def' in p[1][0]):
        func_dir["global"]["vars_table"][p[1][1]] = {"type":p[1][3]}
        func_dir[p[1][1]] = {"return_type" : None, "vars_table" : {}}
        paramsAux = p[1][2]
        func_dir[p[1][1]]["return_type"] = p[1][3]
        while paramsAux != None:
            func_dir[p[1][1]]["vars_table"][paramsAux[1]] = {"type" : paramsAux[0]}
            paramsAux = paramsAux[2]
   
    

=======
    global func_dir, Gi, Gf, Go, Li, Lf, Lo, Ti, To, Tf, Tb, Ts, Tp, temporalCounter
            
    Li = 5000
    Lf = 7001
    Lo = 10001
    Ti = 11000
    Tf = 12001
    Tb = 13001
    To = 14001
    Ts = 15001
    Tp = 19000
    temporalCounter = 0

#### Global Scope (Neural point 2)
# Converts current scope to "global"
# Generates global scope func_dir entry
>>>>>>> Stashed changes
def p_global_scope(p):
    '''
    global_scope :
    '''
    global curr_scope, func_dir
    curr_scope = "global"
    func_dir[curr_scope] = {"return_type" : "void", "vars_table" : {}}

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
    class_dir[curr_scope] = {"constructor" : {},"method_table": {}, "vars_table" : {}}
    p[0] = p[1]

def p_class1(p):
    '''
    class1 : COLON ID
           | empty
    '''
    if(p[1] == ':'):
        #pass
        for i in class_dir[p[2]]["vars_table"].keys(): 
                class_dir[curr_scope]["vars_table"][i] = class_dir[p[2]]["vars_table"][i]
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
<<<<<<< Updated upstream
    p[0] = (p[1], p[2],p[4], p[7])
=======
    global quadruples, quadCounter, prev_table, Li, Lf, Lo, temporalCounter, Ti, Tf, Tb, To, Ts, Tp
    p[0] = (p[1], p[2], p[4], p[7])
    quadruples.append(["ENDPROC",None,None,None])
    func_dir[p[2]]["temporal_counter"] = temporalCounter
    quadCounter += 1
    Li = 5000
    Lf = 7001
    Lo = 10001
    Ti = 11000
    Tf = 12001
    Tb = 13001
    To = 14001
    Ts = 15001
    Tp = 19000
    temporalCounter = 0

>>>>>>> Stashed changes

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
    func_dir[curr_scope]["vars_table"][p[1]] = {"type" : p[3]}

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
                 | type LSQRBRACKET exp0 RSQRBRACKET declaration2
    '''
    p[0] = p[1]
<<<<<<< Updated upstream
=======
    global Li, Lf, Lo, func_dir, curr_scope, dimNodes, dimCounter
    func_dir[curr_scope]["vars_table"][p[-2]]["type"] = p[1]

### LimitNeur (Neural Point 9)
# Checks 1st dim array limits and generates m, r, ls, and li. Checks if size type is valid
def p_limitNeur(p):
    '''
    limitNeur : 
    '''
    global operands_stack, types_stack, dimNodes, dimCounter
    aux = operands_stack.pop()
    auxType = types_stack.pop()

    if(auxType != "int"):
        raise Error("Index type is not valid")
    else:
        
        Ls = aux
        Linf = 0
        dimNodes[dimCounter]["ls"] = Ls
        dimNodes[dimCounter]["li"] = Linf
        dimNodes[dimCounter]["r"] = 1 * (Ls - Linf + 1)
        dimCounter += 1
        
        #dim1Node["r"] = dim1Node["r"] * (Ls - Li + 1)


### simpleMemoryNeur
# Assigns memory address to simple declarations
def p_simpleMemoryNeur(p):
    '''
    simpleMemoryNeur :
    '''
    global Li, Lf, Lo, func_dir, curr_scope, Gi, Gf, Go
    if(curr_scope == "global"):
        if p[-1] == "int":
            if Gi >= 2001:
                raise MemoryError("Global integer limit reached")
            else:
                direc = Gi
                Gi += 1
                val = 0
        elif p[-1] == "float":
            if Gf >= 4001:
                raise MemoryError("Global float limit reached")
            else:
                direc = Gf
                Gf += 1
                val = 0.0
        else:
            if Go >= 5000:
                raise MemoryError("Global other limit reached")
            else:
                direc = Go
                Go += 1
                val = None
    else:
        if p[-1] == "int":
            if Li >= 7001:
                raise MemoryError("Local integer limit reached")
            else:
                direc = Li
                Li += 1
                val = 0
        elif p[-1] == "float":
            if Lf >= 10001:
                raise MemoryError("Local Float limit reached")
            else:
                direc = Lf
                Lf += 1
                val = 0.0
        else:
            if Lo >= 11000:
                raise MemoryError("Local other limit reached")
            else:
                direc = Lo
                Lo += 1
                val = None

    func_dir[curr_scope]["vars_table"][p[-3]]["dirV"] = direc
    func_dir[curr_scope]["vars_table"][p[-3]]["value"] = val
    func_dir[curr_scope]["vars_table"][p[-3]]["type"] = p[-1]



###isArrayNeur (Neural )
def p_isArrayNeur(p):
    '''
    isArrayNeur :
    '''
    global func_dir, curr_scope, operands_stack, dimCounter
    func_dir[curr_scope]["vars_table"][p[-3]]["isArray"] = True
    dimCounter = 0
    dimNodes[0] = {"ls":0, "li":0, "r":1, "m":0}
    dimNodes[1] = {"ls":0, "li":0, "r":1, "m":0}


def p_neurMemory(p):
    '''
    neurMemory :
    '''
    global Li, Lf, Lo, func_dir, curr_scope, var_id, Gi, Gf, Go, operands_stack, dimCounter, dimNodes
    if(dimCounter > 1):
        size = dimNodes[1]["r"]
    else:
        size = dimNodes[0]["r"]

    if curr_scope != "global":
        if p[-7] == "int":
            if Li >= 7001:
                raise MemoryError("Local integer limit reached")
            else:
                direc = Li
                Li += 1
        elif p[-7] == "float":
            if Lf >= 10001:
                raise MemoryError("Local float limit reached")
            else:
                direc = Lf
                Lf += 1
        else:
            if Lo >= 11000:
                raise MemoryError("Local other limit reached")
            else:
                direc = Lo
                Lo += 1
    else:
        if p[-7] == "int":
            if Gi >= 2001:
                raise MemoryError("Global integer limit reached")
            else:
                direc = Gi
                Gi += size
        elif p[-7] == "float":
            if Gf >= 4001:
                raise MemoryError("Global float limit reached")
            else:
                direc = Gf
                Gf += size
        else:
            if Gi >= 5000:
                raise MemoryError("Global other limit reached")
            else:
                direc = Go
                Go += size
    
    if dimCounter == 1:
        ls1 = dimNodes[0]["ls"]
        r = dimNodes[0]["r"]
        func_dir[curr_scope]["vars_table"][var_id]["lsDim1"] = ls1
        func_dir[curr_scope]["vars_table"][var_id]["lsDim2"] = 0
        func_dir[curr_scope]["vars_table"][var_id]["dim"] = dimCounter
        func_dir[curr_scope]["vars_table"][var_id]["m1"] = r / (ls1+1)
    elif dimCounter == 2:
        ls1 = dimNodes[0]["ls"]
        ls2 = dimNodes[1]["ls"]
        r = dimNodes[1]["r"]
        func_dir[curr_scope]["vars_table"][var_id]["lsDim1"] = ls1
        func_dir[curr_scope]["vars_table"][var_id]["lsDim2"] = ls2
        func_dir[curr_scope]["vars_table"][var_id]["dim"] = dimCounter
        func_dir[curr_scope]["vars_table"][var_id]["m1"] = r/ (ls1+1)
        func_dir[curr_scope]["vars_table"][var_id]["m2"] = func_dir[curr_scope]["vars_table"][var_id]["m1"]/ (ls2+1)

    func_dir[curr_scope]["vars_table"][var_id]["dirV"] = direc
    func_dir[curr_scope]["vars_table"][var_id]["size"] = size

>>>>>>> Stashed changes

def p_declaration2(p):
    '''
    declaration2 : LSQRBRACKET exp0 RSQRBRACKET
                 | empty
    '''

<<<<<<< Updated upstream
def p_assignment0(p):
    '''
    assignment0 : ID EQUALS expression0 SEMICOLON
                | ID LSQRBRACKET exp0 RSQRBRACKET EQUALS expression0 SEMICOLON
                | ID LSQRBRACKET exp0 RSQRBRACKET LSQRBRACKET exp0 RSQRBRACKET EQUALS expression0 SEMICOLON
    '''
    #global curr_scope
    #if(p[2] != "["):
    #    func_dir[curr_scope][p[1]]["value"] = p[3]    
=======
def p_dim2Neur(p):
    '''
    dim2Neur :
    '''
    


def p_limitNeur2(p):
    '''
    limitNeur2 : 
    '''
    global dimNodes, dimCounter, operands_stack, types_stack
    aux = operands_stack.pop()
    auxType = types_stack.pop()
    if(auxType != "int"):
        raise IndexError("Index Type not valid")
    else:
        Ls = aux
        Linf = 0
        dimNodes[dimCounter]["ls"] = Ls
        dimNodes[dimCounter]["li"] = Linf
        dimNodes[dimCounter]["r"] = dimNodes[dimCounter-1]["r"] * (Ls - Linf + 1)
        dimCounter += 1

def p_assignment0(p):
    '''
    assignment0 : ID EQUALS expression0 SEMICOLON
                | assign_id_def lsqrbracket_assign exp0 rsqrbracket_assign EQUALS expression0 SEMICOLON 
                | assign_id_def lsqrbracket_assign exp0 rsqrbracket_assign_2dim1 LSQRBRACKET exp0 RSQRBRACKET arrAccdim2 EQUALS expression0 SEMICOLON
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter, const_table
    if len(p) == 5 and operands_stack:
        if p[1] not in func_dir["global"]["vars_table"] and p[1] not in func_dir[curr_scope]["vars_table"]:
            raise NameError("Variable does not exist")
        else:
            value = operands_stack.pop()
            valType = types_stack.pop()
            if p[1] not in func_dir["global"]["vars_table"]:
                validation = typeMatch("EQUAL",valType,func_dir[curr_scope]["vars_table"][p[1]]["type"])
                direc = func_dir[curr_scope]["vars_table"][p[1]]["dirV"]
            else:
                validation = typeMatch("EQUAL",valType,func_dir["global"]["vars_table"][p[1]]["type"])
                direc = func_dir["global"]["vars_table"][p[1]]["dirV"]
            if(value in const_table.keys()):
                value = const_table[value]
            quad = [p[2], value, None, direc]
            quadruples.append(quad)
            quadCounter += 1
    elif len(p) == 8 and operands_stack:
        valAssign = operands_stack.pop()
        assignee = operands_stack.pop()
        if valAssign in const_table.keys():
            vAssign = const_table[valAssign]
        elif valAssign in func_dir["global"]["vars_table"].keys():
            vAssign = func_dir["global"]["vars_table"][valAssign]["dirV"]
        elif valAssign in func_dir[curr_scope]["vars_table"].keys():
            vAssign = func_dir[curr_scope]["vars_table"][valAssign]["dirV"]
        else:
            vAssign = valAssign
        quad = [p[5], vAssign, None, assignee]
        quadruples.append(quad)
        quadCounter += 1
    elif len(p) == 12 and operands_stack:
        valAssign = operands_stack.pop()
        assignee = operands_stack.pop()
        quad = [p[9], const_table[valAssign], None, assignee]
        quadruples.append(quad)
        quadCounter += 1

def p_arrAccdim2(p):
    '''
    arrAccdim2 :
    '''
    global quadCounter, quadruples, func_dir, operands_stack, curr_scope, var_id, temp_counter, operators_stack, Tp, Ci
    id = p[-6][0]
    idType = p[-6][1]
    dim = p[-6][2]
    if id not in func_dir[curr_scope]["vars_table"].keys():
        ls = func_dir["global"]["vars_table"][id]["lsDim2"]
    else:
        ls = func_dir[curr_scope]["vars_table"][id]["lsDim2"]
    aux = operands_stack[-1]
    if aux in func_dir[curr_scope]["vars_table"].keys():
        aux = func_dir[curr_scope]["vars_table"][aux]["dirV"]
    elif aux in func_dir["global"]["vars_table"].keys():
        aux = func_dir["global"]["vars_table"][aux]["dirV"]
    else:
        if aux not in const_table.keys():
            const_table[aux] = Ci
            Ci += 1
        aux = const_table[aux]
    print(aux, "asdasdasds")
    if ls not in const_table.keys():
        const_table[ls] = Ci
        Ci += 1
    ls = const_table[ls]
    quad = ["VERIFY",aux , const_table[0], ls]
    quadruples.append(quad)
    quadCounter += 1
    left_oper = operands_stack.pop()
    right_oper = operands_stack.pop()
    direc, lOperDir, rOperDir = tempCalculator(left_oper, right_oper, "+")
    operands_stack.append(direc)
    quadruples.append(["+", lOperDir, rOperDir, direc])
    operands_stack.append(direc)
    temp_counter += 1
    quadCounter += 1
    aux3 = operands_stack.pop()
    if id not in func_dir[curr_scope]["vars_table"].keys():
        direc, lOperDir, rOperDir = tempCalculator(aux3, id, "+")
    else:
        direc, lOperDir, rOperDir = tempCalculator(aux3, id, "+")
    
    operands_stack.append(Tp)
    quadruples.append(["+", lOperDir, rOperDir, Tp])
    Tp += 1
    temp_counter += 1
    quadCounter += 1
    
    operators_stack.pop()

def p_rsqrbracket_assign_2dim1(p):
    '''
    rsqrbracket_assign_2dim1 : RSQRBRACKET
    '''
    global quadCounter, quadruples, func_dir, operands_stack, curr_scope, var_id, temp_counter, operators_stack, const_table, Ci
    aux = operands_stack.pop()
    id = p[-2][0]
    
    if id not in func_dir[curr_scope]["vars_table"].keys():
        ls = func_dir["global"]["vars_table"][id]["lsDim1"]
        m = int(func_dir["global"]["vars_table"][id]["m1"])
        if m not in const_table.keys():
            const_table[m] = Ci
            Ci += 1
        if ls not in const_table.keys():
            const_table[ls] = Ci
            Ci += 1
        if aux in func_dir[curr_scope]["vars_table"].keys():
            aux = func_dir[curr_scope]["vars_table"][aux]["dirV"]
        elif aux in func_dir["global"]["vars_table"].keys():
            aux = func_dir["global"]["vars_table"][aux]["dirV"]
        else:
            if aux not in const_table.keys():
                const_table[aux] = Ci
                Ci += 1
                aux = const_table[aux]
            aux = const_table[aux]
        quadruples.append(["VERIFY",aux , const_table[0],const_table[ls]])
    else:
        ls = func_dir[curr_scope]["vars_table"][id]["lsDim1"]
        m = int(func_dir[curr_scope]["vars_table"][id]["m1"])
        if m not in const_table.keys():
            const_table[m] = Ci
            Ci += 1
        if ls not in const_table.keys():
            const_table[ls] = Ci
            Ci += 1
        if aux in func_dir[curr_scope]["vars_table"].keys():
            aux = func_dir[curr_scope]["vars_table"][aux]["dirV"]
        elif aux in func_dir["global"]["vars_table"].keys():
            aux = func_dir["global"]["vars_table"][aux]["dirV"]
        else:
            if aux not in const_table.keys():
                const_table[aux] = Ci
                Ci += 1
                aux = const_table[aux]
            aux = const_table[aux]
        print(aux, "putamadreyamatenmealv")
        quadruples.append(["VERIFY",aux , const_table[0],const_table[ls]])
    quadCounter += 1
    direc, rOperDir, lOperDir = tempCalculator(aux, m, "*")
    quad = ["*", rOperDir, lOperDir,direc]
    quadruples.append(quad)
    operands_stack.append(direc)
    temp_counter += 1
    quadCounter +=1

    

def p_rsqrbracket_assign(p):
    '''
    rsqrbracket_assign : RSQRBRACKET
    '''
    global quadCounter, quadruples, func_dir, operands_stack, curr_scope, var_id, temp_counter, operators_stack, Tp, Ci
    id = p[-2][0]
    idType = p[-2][1]
    
    if id in func_dir[curr_scope]["vars_table"].keys():
        aux = operands_stack[-1]
        ls = func_dir[curr_scope]["vars_table"][id]["lsDim1"]
        if aux in func_dir[curr_scope]["vars_table"].keys():
            aux = func_dir[curr_scope]["vars_table"][aux]["dirV"]
        elif aux in func_dir["global"]["vars_table"].keys():
            aux = func_dir["global"]["vars_table"][aux]["dirV"]
        else:
            if aux not in const_table.keys():
                const_table[aux] = Ci
                Ci += 1
            aux = const_table[aux]
        if ls not in const_table.keys():
            const_table[ls] = Ci
            Ci += 1
        ls = const_table[ls]
        quadruples.append(["VERIFY",aux , const_table[0], ls])
    else:
        aux = operands_stack[-1]
        ls = func_dir["global"]["vars_table"][id]["lsDim1"]
        if aux in func_dir[curr_scope]["vars_table"].keys():
            aux = func_dir[curr_scope]["vars_table"][aux]["dirV"]
        elif aux in func_dir["global"]["vars_table"].keys():
            aux = func_dir["global"]["vars_table"][aux]["dirV"]
        else:
            if aux not in const_table.keys():
                const_table[aux] = Ci
                Ci += 1
            aux = const_table[aux]
        if ls not in const_table.keys():
            const_table[ls] = Ci
            Ci += 1
        ls = const_table[ls]
        print(aux)
        quadruples.append(["VERIFY",aux , const_table[0], ls])
    quadCounter += 1
    aux = operands_stack.pop()
    direc, lOperDir, rOperDir = tempCalculator(aux, id, "+")
    operands_stack.append(Tp)
    quadruples.append(["+", lOperDir, rOperDir, Tp])
    Tp += 1
    temp_counter += 1
    quadCounter += 1
    operators_stack.pop()


def p_lsqrbracket_assign(p):
    '''
    lsqrbracket_assign : LSQRBRACKET
    '''
    global operands_stack, types_stack, operators_stack, dimAssign
    
    id = operands_stack.pop()
    idType = types_stack.pop()
    operators_stack.append("(")
    dimAssign = 1
    p[0] = (id, idType, dimAssign)

        

def p_assign_id_def(p):
    '''
    assign_id_def : ID
    '''
    global operands_stack, types_stack
    p[0] = p[1]
    if p[1] not in func_dir[curr_scope]["vars_table"].keys():
        operands_stack.append(p[1])
        types_stack.append(func_dir["global"]["vars_table"][p[1]]["type"])
    else:
        operands_stack.append(p[1])
        types_stack.append(func_dir[curr_scope]["vars_table"][p[1]]["type"])

>>>>>>> Stashed changes
    

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
                class_dir[curr_scope]["method_table"][p[2][1]][paramsAux[1]] = {"type":paramsAux[0]}
                paramsAux = paramsAux[2]
    


def p_params0(p):
    '''
    params0 : type ID params1
            | empty
    '''
    if(p[1] != None):
        p[0] = (p[1], p[2], p[3])

<<<<<<< Updated upstream
=======
def p_paramsNeur(p):
    '''
    paramsNeur : 
    '''
    global func_dir, quadruples, quadCounter, Li, Lf, Lo, curr_scope
    if p[-2] == "int":
        if Li >= 7001:
            raise MemoryError("Local integer limit reached")
        else:
            direc = Li
            Li += 1
            value = 0
    elif p[-2] == "float":
        if Lf >= 10001:
            raise MemoryError("Local float limit reached")
        else:
            direc = Lf
            Lf += 1
            value = 0.0
    else:
        if Lo >= 11000:
            raise MemoryError("Local other limit reached")
        else:
            direc = Lo
            Lo += 1
            value = None
    if curr_scope in class_dir.keys():
        class_dir[curr_scope]["vars_table"][p[-1]] = {"type" : p[-2], "dirV" : direc, "isArray":False, "value" : value}
        class_dir[curr_scope]["params_table"].append(p[-2])
        class_dir[curr_scope]["params_addresses"].append(direc)
    else:
        func_dir[curr_scope]["vars_table"][p[-1]] = {"type" : p[-2], "dirV" : direc, "isArray":False, "value" : value}
        func_dir[curr_scope]["params_table"].append(p[-2])
        func_dir[curr_scope]["params_addresses"].append(direc)
>>>>>>> Stashed changes



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
    #print(p[3])
    p[0] = (p[1], p[3])
    #func_dir[curr_scope][p[1]] = {"type": p[3]}
    #print(curr_scope)
    #var_id = p[1]

def p_simple_assignment(p):
    '''
    simple_assignment : ID EQUALS expression0 SEMICOLON
    '''
    #global curr_scope
    #func_dir[curr_scope][p[1]]["value"] = p[3]

def p_complex_type(p):
    '''
    complex_type : ID
    '''
    p[0] = p[1]

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
    p[0] = p[1]
    global curr_scope
    #print(curr_scope)

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
<<<<<<< Updated upstream
=======
    global Li, Lf, Lo, temporalCounter, Ti, Tf, Tb, To, Ts
    Li = 5000
    Lf = 7001
    Lo = 10001
    Ti = 11000
    Tf = 12001
    Tb = 13001
    To = 14001
    Ts = 15001
    temporalCounter = 0

>>>>>>> Stashed changes

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
    func_dir[curr_scope] = {"return_type" : "void", "vars_table" : {}}

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