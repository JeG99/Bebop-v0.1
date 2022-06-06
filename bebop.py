from aifc import Error
from os import lseek
from semCube import typeMatch
import ply.yacc as yacc
import sys
import json

from vm import VirtualMachine
from pylexer import tokens, lexer

func_dir = {}
class_dir = {}
curr_scope = ''
prev_scope = ""
var_id = ""
const_table = {}
dim1Node = {}
dimNodes = [
    {"ls": 0, "li": 0, "r": 1, "m": 0},
    {"ls": 0, "li": 0, "r": 1, "m": 0}
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
dimAssign = 0
#                 Li,Lf,Ti,Tf,Tb
func_mem = [0, 0, 0, 0, 0]

# Global addresses
Gi = 0
Gf = 2000
Go = 4000

# Local Addresses
Li = 5000
Lf = 7000
Lo = 10000

# Temporal Addresses
Ti = 11000
Tf = 12000
Tb = 13000
To = 14000
Ts = 15000

# Constant Addresses
Ci = 16000
Cf = 17000
Cs = 18000

# Pointer Address
Tp = 19000


# Aux Function tempCalculator
# params: left_oper, right_oper, op
# Takes operands used to validate the type generated from a certain operation
# Function used to validate constant and variable types with semantic cube
# Return: direc(Temporal direction for saving result), rOperDir(calculated direction of right operand), lOperDir(calculated direction of left operand)

def tempCalculator(left_oper, right_oper, op):
    global Ti, Tf, To, Tb, curr_scope, currFuncCall, func_mem
    # RIGHT
    # Check if constant
    if right_oper in const_table.keys():
        rOperDir = const_table[right_oper]
        if rOperDir >= 16000 and rOperDir < 17000:
            rOperType = "int"
        elif rOperDir >= 17000 and rOperDir < 18000:
            rOperType = "float"
    else:
        # Check in current scope, go to global, or check temporals
        if right_oper in func_dir[curr_scope]["vars_table"].keys():
            rOperType = func_dir[curr_scope]["vars_table"][right_oper]["type"]
            rOperDir = func_dir[curr_scope]["vars_table"][right_oper]["dirV"]
        elif right_oper in func_dir["global"]["vars_table"].keys():
            rOperType = func_dir["global"]["vars_table"][right_oper]["type"]
            rOperDir = func_dir["global"]["vars_table"][right_oper]["dirV"]
        else:
            if right_oper >= 11000 and right_oper < 12000 or right_oper >= 5000 and right_oper < 7000 or right_oper >= 16000 and right_oper < 17000:
                rOperType = "int"
                rOperDir = right_oper
            elif right_oper >= 12000 and right_oper < 13000 or right_oper >= 7000 and right_oper < 10000 or right_oper >= 17000 and right_oper < 18000:
                rOperType = "float"
                rOperDir = right_oper
            else:
                rOperDir = right_oper

    # LEFT
    # Check if constant
    print
    if left_oper in const_table.keys():
        lOperDir = const_table[left_oper]
        if lOperDir >= 16000 and lOperDir < 17000:
            lOperType = "int"
        elif lOperDir >= 17000 and lOperDir < 18000:
            lOperType = "float"
    else:
        # Check in current scope, go to global, or check temporals
        if left_oper in func_dir[curr_scope]["vars_table"].keys():
            lOperType = func_dir[curr_scope]["vars_table"][left_oper]["type"]
            lOperDir = func_dir[curr_scope]["vars_table"][left_oper]["dirV"]
        elif left_oper in func_dir["global"]["vars_table"].keys():
            lOperType = func_dir["global"]["vars_table"][left_oper]["type"]
            lOperDir = func_dir["global"]["vars_table"][left_oper]["dirV"]
        else:
            if left_oper >= 11000 and left_oper < 12000 or left_oper >= 5000 and left_oper < 7000 or left_oper >= 16000 and left_oper < 17000:
                lOperType = "int"
                lOperDir = left_oper
            elif left_oper >= 12000 and left_oper < 13000 or left_oper >= 7000 and left_oper < 10000 or left_oper >= 17000 and left_oper < 18000:
                lOperType = "float"
                lOperDir = left_oper
            else:
                lOperDir = left_oper
    # Utilize Semantic Cube to check if types are correct
    if op == "+":
        typeRes = typeMatch("SUM", rOperType, lOperType)
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
        direc = Ti
        Ti += 1
        func_mem[2] += 1
    elif typeRes == "FLOAT":
        direc = Tf
        Tf += 1
        func_mem[3] += 1
    elif typeRes == "BOOL":
        direc = Tb
        Tb += 1
        func_mem[4] += 1
    else:
        direc = To
        To += 1
    return direc, lOperDir, rOperDir

# Routine0: Beginning of program
# Utilizes token ROUTINE to snow the beginning of program


def p_routine0(p):
    '''
    routine0 : goto_main_neur ROUTINE ID SEMICOLON global_scope routine1 main0
    '''
    global quadCounter, quadruples
    p[0] = 1
    quadruples.append(["END", None, None, None])
    quadCounter += 1
    print(json.dumps(func_dir, indent=4))
    # print(operands_stack)
    # print(types_stack)
    # print(operators_stack)
    print(const_table)
    [print(idx, quad) for idx, quad in enumerate(quadruples)]
    vm = VirtualMachine(quadruples, func_dir, const_table)
    vm.mem_init()
    vm.run()


# Neural Point 1
# Generates first quaruple GOTO main
def p_goto_main_neur(p):
    '''
    goto_main_neur :
    '''
    global quadruples, quadCounter
    quadruples.append(["GOTO", "main", None, None])
    quadCounter = quadCounter + 1


# Routine1
# Allows program to generate values, functions, and clases on the global scope.
def p_routine1(p):
    '''
    routine1 : statement routine1
             | class0 routine1 
             | function0 routine1
             | declaration0 routine1
             | assignment0 routine1
             | empty
    '''
    global func_dir, Gi, Gf, Go, Li, Lf, Lo, Ti, To, Tf, Tb, Ts, func_mem

    Li = 5000
    Lf = 7000
    Lo = 10000
    Ti = 11000
    Tf = 12000
    Tb = 13000
    To = 14000
    Ts = 15000
    #                 Li,Lf,Ti,Tf,Tb
    func_mem = [0, 0, 0, 0, 0]

# Global Scope (Neural point 2)
# Converts current scope to "global"
# Generates global scope func_dir entry


def p_global_scope(p):
    '''
    global_scope :
    '''
    global curr_scope, func_dir
    curr_scope = "global"
    func_dir[curr_scope] = {"return_type": "void", "vars_table": {}}

# Class0
# Detects classes and begins class recognition


def p_class0(p):
    '''
    class0 : CLASS class_id_def class1 LBRACKET class2 constructor class3 RBRACKET SEMICOLON revert_global
    '''

# Revert global (Neural point 3 )
# Reverts current scope to global


def p_revert_global(p):
    '''
    revert_global :
    '''
    global curr_scope
    curr_scope = "global"

# Revert scope (Neural point 4)
# Reverts current scope to previous scope


def p_revert_scope(p):
    '''
    revert_scope : 
    '''
    global curr_scope, prev_scope
    curr_scope = prev_scope


# id def (Neural point 5)
# Neural point that checks if an ID for a function is defined to raise an error or to create its entry on func_dir
# and entry on global scope as variable for return
def p_id_def(p):
    '''
    id_def : ID
    '''
    global curr_scope, func_dir, prev_scope, prev_table
    if p[1] in func_dir.keys():
        raise NameError("Function already exists")
    else:
        func_dir["global"]["vars_table"][p[1]] = {
            "type": None, "dirV": None, "value": None}
        func_dir[p[1]] = {"return_type": None, "vars_table": {},
                          "params_table": [], "params_addresses": []}
        prev_scope = curr_scope
        curr_scope = p[1]
        p[0] = p[1]

# Class id def (Neural Point 6)
# Neural point that checks if class already exists to raise error
# Generates constructor(dict), method_table(dict), vars_table(dict)


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

# class1
# Checks for possible extensions, or heritage, in the class


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

# class2
# Checks for the attributes of the class, if any


def p_class2(p):
    '''
    class2 : attributes
           | empty
    '''

# class 3
# Checks for the methods of the class, if any


def p_class3(p):
    '''
    class3 : methods 
           | empty  
    '''

# Function 0
# Checks for the structure of a function to generate it, adds ENDPROC quadruple at end of its excecution
# and resets local and temporal addresses to default address


def p_function0(p):
    '''
    function0 : DEF id_def LPAREN params0 RPAREN endParamNeur ARROW function1 LSQRBRACKET LSQRBRACKET function2 RSQRBRACKET RSQRBRACKET startFuncNeur function_block0 revert_scope
    '''
    global quadruples, quadCounter, prev_table, Li, Lf, Lo, Ti, Tf, Tb, To, Ts, func_mem
    p[0] = (p[1], p[2], p[4], p[7])
    quadruples.append(["ENDPROC", None, None, None])
    func_dir[p[2]]["temporal_counter"] = func_mem
    quadCounter += 1
    Li = 5000
    Lf = 7000
    Lo = 10000
    Ti = 11000
    Tf = 12000
    Tb = 13000
    To = 14000
    Ts = 15000
    #                 Li,Lf,Ti,Tf,Tb
    func_mem = [0, 0, 0, 0, 0]


# endParamNeur (Neural point 7)
#  Neural point to assign number of paramneters to function entry
def p_endParamNeur(p):
    '''
    endParamNeur :
    '''
    global func_dir, curr_scope
    func_dir[curr_scope]["params_number"] = len(
        func_dir[curr_scope]["params_table"])
# startFuncNeur (Neural point 8)
# Neural point to assign the quadruple number of where the function starts in order to jump when function is called


def p_startFuncNeur(p):
    '''
    startFuncNeur :
    '''
    global func_dir, curr_scope, quadCounter
    func_dir[curr_scope]["quad_number"] = quadCounter
# p_function1
# Defines the function's type and grants its direction in memory


def p_function1(p):
    '''
    function1 : type
              | VOID
    '''

    global curr_scope, func_dir, Gi, Gf, Go
    func_dir[p[-6]]["return_type"] = p[1]
    if p[1] != "void":
        func_dir['global']["vars_table"][p[-6]]["type"] = p[1]
        direc = 0
        if(p[1] != "void"):
            if p[1] == "int":
                direc = Gi
                Gi += 1
                value = 0
            elif p[1] == "float":
                direc = Gf
                Gf += 1
                value = 0.0
            else:
                direc = Go
                Go += 1
                value = None
        func_dir['global']["vars_table"][p[-6]]["dirV"] = direc
        func_dir['global']["vars_table"][p[-6]]["isArray"] = False
        func_dir['global']["vars_table"][p[-6]]["value"] = value
    else:
        del func_dir['global']["vars_table"][p[-6]]
    p[0] = p[1]


# function 2
# Defines declarations and assignments
def p_function2(p):
    '''
    function2 : simple_declaration function2    
              | simple_assignment function2
              | empty
    '''

# declaration 0
# Rule used to declare a variable.


def p_declaration0(p):
    '''
    declaration0 : decl_id_def COLON declaration1 SEMICOLON
    '''


# decl_id_def
# Rule used to add the ID to the current scope's vars table
def p_decl_id_def(p):
    '''
    decl_id_def : ID
    '''
    p[0] = p[1]
    global var_id, func_dir, curr_scope
    var_id = p[1]
    func_dir[curr_scope]["vars_table"][p[1]] = {
        "type": None, "dirV": None, "isArray": False}

# declaration1
# Allows different types of declarations, from simple types to complex types(objects) and arrays


def p_declaration1(p):
    '''
    declaration1 : type simpleMemoryNeur
                 | complex_type simpleMemoryNeur
                 | type isArrayNeur LSQRBRACKET exp0 limitNeur RSQRBRACKET declaration2 neurMemory
    '''
    p[0] = p[1]
    global Li, Lf, Lo, func_dir, curr_scope, dimNodes, dimCounter
    func_dir[curr_scope]["vars_table"][p[-2]]["type"] = p[1]

# LimitNeur (Neural Point 9)
# Checks 1st dim array limits and generates m, r, ls, and li. Checks if size type is valid


def p_limitNeur(p):
    '''
    limitNeur : 
    '''
    global operands_stack, types_stack, dimNodes, dimCounter
    aux = operands_stack.pop()
    auxType = types_stack.pop()

    if(auxType != "int"):
        raise TypeError("Index type must be an integer")
    else:

        Ls = aux
        Li = 0
        dimNodes[dimCounter]["ls"] = Ls
        dimNodes[dimCounter]["li"] = Li
        dimNodes[dimCounter]["r"] = 1 * (Ls - Li + 1)
        dimCounter += 1

        #dim1Node["r"] = dim1Node["r"] * (Ls - Li + 1)


# simpleMemoryNeur
# Assigns memory address to simple declarations
def p_simpleMemoryNeur(p):
    '''
    simpleMemoryNeur :
    '''
    global Li, Lf, Lo, func_dir, curr_scope, Gi, Gf, Go
    if(curr_scope == "global"):
        if p[-1] == "int":
            direc = Gi
            Gi += 1
            val = 0
        elif p[-1] == "float":
            direc = Gf
            Gf += 1
            val = 0.0
        else:
            direc = Go
            Go += 1
            val = None
    else:
        if p[-1] == "int":
            direc = Li
            Li += 1
            val = 0
            func_mem[0] += 1
        elif p[-1] == "float":
            direc = Lf
            Lf += 1
            val = 0.0
            func_mem[1] += 1
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
    dimNodes[0] = {"ls": 0, "li": 0, "r": 1, "m": 0}
    dimNodes[1] = {"ls": 0, "li": 0, "r": 1, "m": 0}


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
            direc = Li
            Li += size
        elif p[-7] == "float":
            direc = Lf
            Lf += size
        else:
            direc = Lo
            Lo += size
    else:
        if p[-7] == "int":
            direc = Gi
            Gi += size
        elif p[-7] == "float":
            direc = Gf
            Gf += size
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
        func_dir[curr_scope]["vars_table"][var_id]["m1"] = r / (ls1+1)
        func_dir[curr_scope]["vars_table"][var_id]["m2"] = func_dir[curr_scope]["vars_table"][var_id]["m1"] / \
            (ls2+1)

    func_dir[curr_scope]["vars_table"][var_id]["dirV"] = direc
    func_dir[curr_scope]["vars_table"][var_id]["size"] = size


def p_declaration2(p):
    '''
    declaration2 : dim2Neur LSQRBRACKET exp0 limitNeur2 RSQRBRACKET
                 | empty
    '''


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
        Li = 0
        dimNodes[dimCounter]["ls"] = Ls
        dimNodes[dimCounter]["li"] = Li
        dimNodes[dimCounter]["r"] = dimNodes[dimCounter-1]["r"] * (Ls - Li + 1)
        dimCounter += 1


def p_assignment0(p):
    '''
    assignment0 : ID EQUALS expression0 SEMICOLON
                | assign_id_def lsqrbracket_assign exp0 rsqrbracket_assign EQUALS expression0 SEMICOLON 
                | assign_id_def lsqrbracket_assign exp0 rsqrbracket_assign_2dim1 LSQRBRACKET exp0 RSQRBRACKET arrAccdim2 EQUALS expression0 SEMICOLON
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter, const_table
    print("Length", "=", len(p))
    print(operands_stack)
    if len(p) == 5 and operands_stack:
        print(p[1], "--------------------------")
        if p[1] not in func_dir["global"]["vars_table"] and p[1] not in func_dir[curr_scope]["vars_table"]:
            raise NameError("Variable does not exist")
        else:
            value = operands_stack.pop()
            valType = types_stack.pop()
            print("alv", value, p[1])
            if p[1] in func_dir["global"]["vars_table"]:
                direc = func_dir["global"]["vars_table"][p[1]]["dirV"]
            else:
                direc = func_dir[curr_scope]["vars_table"][p[1]]["dirV"]
            
            if value  in func_dir["global"]["vars_table"]:
                dirVal = func_dir["global"]["vars_table"][value]["dirV"]
            elif(value in const_table.keys()):
                dirVal = const_table[value]
                #dirVal = value
            elif value  in func_dir[curr_scope]["vars_table"]:
                dirVal = func_dir[curr_scope]["vars_table"][value]["dirV"]
            else:
                dirVal = value
            
            quad = [p[2], dirVal, None, direc]
            
            print("Cuadruplo = ", quad)
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
    global quadCounter, quadruples, func_dir, operands_stack, curr_scope, var_id, temp_counter, operators_stack, Tp
    id = p[-6][0]
    idType = p[-6][1]
    dim = p[-6][2]
    if id not in func_dir[curr_scope]["vars_table"].keys():
        ls = func_dir["global"]["vars_table"][id]["lsDim2"]
    else:
        ls = func_dir[curr_scope]["vars_table"][id]["lsDim2"]
    quad = ["VERIFY", operands_stack[-1], 0, ls]
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
        lSup = func_dir["global"]["vars_table"][id]["lsDim1"]
        if aux in func_dir[curr_scope]["vars_table"].keys():
            aux = func_dir[curr_scope]["vars_table"][aux]["dirV"]
        elif aux in func_dir["global"]["vars_table"].keys():
            aux = func_dir["global"]["vars_table"][aux]["dirV"]
        elif aux not in const_table.keys():
            const_table[aux] = Ci
            Ci += 1
            aux = const_table[aux]
        else:
            if aux in const_table.keys():
                aux = const_table[aux]
        m = int(func_dir["global"]["vars_table"][id]["m1"])
        if m not in const_table.keys():
            const_table[m] = Ci
            Ci += 1
        quadruples.append(
            ["VERIFY", aux, 0, lSup])
    else:
        lSup = func_dir[curr_scope]["vars_table"][id]["lsDim1"]
        if aux in func_dir[curr_scope]["vars_table"].keys():
            aux = func_dir[curr_scope]["vars_table"][aux]["dirV"]
        elif aux in func_dir["global"]["vars_table"].keys():
            aux = func_dir["global"]["vars_table"][aux]["dirV"]
        elif aux not in const_table.keys():
            const_table[aux] = Ci
            Ci += 1
            aux = const_table[aux]
        else:
            if aux in const_table.keys():
                aux = const_table[aux]
        m = int(func_dir[curr_scope]["vars_table"][id]["m1"])
        if m not in const_table.keys():
            const_table[m] = Ci
            Ci += 1
        quadruples.append(
            ["VERIFY", aux, 0, lSup])
    quadCounter += 1
    direc, rOperDir, lOperDir = tempCalculator(aux, m, "*")
    quad = ["*", rOperDir, lOperDir, direc]
    quadruples.append(quad)
    operands_stack.append(direc)
    temp_counter += 1
    quadCounter += 1


def p_rsqrbracket_assign(p):
    '''
    rsqrbracket_assign : RSQRBRACKET
    '''
    global quadCounter, quadruples, func_dir, operands_stack, curr_scope, var_id, temp_counter, operators_stack, Tp, Ci
    id = p[-2][0]
    idType = p[-2][1]
    dim = p[-2][2]
    aux = operands_stack.pop()
    if id not in func_dir[curr_scope]["vars_table"].keys():
        if aux in func_dir[curr_scope]["vars_table"].keys():
            aux = func_dir[curr_scope]["vars_table"][aux]["dirV"]
        elif aux in func_dir["global"]["vars_table"].keys():
            aux = func_dir["global"]["vars_table"][aux]["dirV"]
        elif aux not in const_table.keys():
            const_table[aux] = Ci
            Ci += 1
            aux = const_table[aux]
        else:
            if aux in const_table.keys():
                aux = const_table[aux]
        lSup = func_dir["global"]["vars_table"][id]["lsDim1"]
        quadruples.append(["VERIFY", aux, 0, lSup
                          ])
    else:
        if aux in func_dir[curr_scope]["vars_table"].keys():
            aux = func_dir[curr_scope]["vars_table"][aux]["dirV"]
        elif aux in func_dir["global"]["vars_table"].keys():
            aux = func_dir["global"]["vars_table"][aux]["dirV"]
        elif aux not in const_table.keys():
            const_table[aux] = Ci
            Ci += 1
            aux = const_table[aux]
        else:
            if aux in const_table.keys():
                aux = const_table[aux]
        lSup = func_dir[curr_scope]["vars_table"][id]["lsDim1"]
        quadruples.append(["VERIFY", aux, 0,
                          lSup])
    quadCounter += 1
    
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


def p_arrAccNeur1(p):
    '''
    arrAccNeur1 : 
    '''
    global types_stack, operands_stack
    id_type = types_stack.pop()
    id = operands_stack.pop()


def p_constructor(p):
    '''
    constructor : CONSTRUCT ID LPAREN params0 RPAREN function_block0
    '''
    class_dir[curr_scope]["constructor"][p[2]] = {}
    if(p[4] != None):
        paramsAux = p[4]
        while paramsAux != None:
            class_dir[curr_scope]["constructor"][p[2]
                                                 ][paramsAux[1]] = {"type": paramsAux[0]}
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
            class_dir[curr_scope]["vars_table"][p[2][0]] = p[2][1]


def p_methods(p):
    '''
    methods : data_access function0 methods
            | empty
    '''
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
    params0 : type ID paramsNeur params1
            | empty
    '''
    if(p[1] != None):
        p[0] = (p[1], p[2], p[3])


def p_paramsNeur(p):
    '''
    paramsNeur : 
    '''
    global func_dir, quadruples, quadCounter, Li, Lf, Lo, curr_scope
    if p[-2] == "int":
        direc = Li
        Li += 1
        value = 0
        func_mem[0] += 1
    elif p[-2] == "float":
        direc = Lf
        Lf += 1
        value = 0.0
        func_mem[1] += 1
    else:
        direc = Lo
        Lo += 1
        value = None
    if curr_scope in class_dir.keys():
        class_dir[curr_scope]["vars_table"][p[-1]
                                            ] = {"type": p[-2], "dirV": direc, "isArray": False, "value": value}
        class_dir[curr_scope]["params_table"].append(p[-2])
        class_dir[curr_scope]["params_addresses"].append(direc)
    else:
        func_dir[curr_scope]["vars_table"][p[-1]
                                           ] = {"type": p[-2], "dirV": direc, "isArray": False, "value": value}
        func_dir[curr_scope]["params_table"].append(p[-2])
        func_dir[curr_scope]["params_addresses"].append(direc)


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
    '''
    p[0] = p[1]


def p_simple_declaration(p):
    '''
    simple_declaration : decl_id_def COLON type simpleMemoryNeur SEMICOLON
    '''
    p[0] = (p[1], p[3])


def p_simple_assignment(p):
    '''
    simple_assignment : ID EQUALS expression0 SEMICOLON
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter
    if p[1] not in func_dir["global"]["vars_table"] and p[1] not in func_dir[curr_scope]["vars_table"]:
        raise NameError("Variable does not exist")
    else:
        value = operands_stack.pop()
        valType = types_stack.pop()
        if p[1] not in func_dir["global"]["vars_table"]:
            validation = typeMatch(
                "EQUAL", valType, func_dir[curr_scope]["vars_table"][p[1]]["type"])
            direc = func_dir[curr_scope]["vars_table"][p[1]]["dirV"]
        else:
            validation = typeMatch(
                "EQUAL", valType, func_dir["global"]["vars_table"][p[1]]["type"])
            direc = func_dir["global"]["vars_table"][p[1]]["dirV"]
        if(value in const_table.keys()):
            value = const_table[value]
        quad = [p[2], value, None, direc]
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
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter, const_table
    # falta typematching
    # Ci = 16000   Cf = 17000
    if len(operators_stack) and len(operands_stack) and (operators_stack[-1] == '+' or operators_stack[-1] == '-'):
        right_oper = operands_stack.pop()
        left_oper = operands_stack.pop()
        op = operators_stack.pop()
        direc, lOperDir, rOperDir = tempCalculator(left_oper, right_oper, op)
        operands_stack.append(direc)
        quad = [op, lOperDir,
                rOperDir, direc]
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
        direc, lOperDir, rOperDir = tempCalculator(left_oper, right_oper, op)
        operands_stack.append(direc)
        quad = [op, lOperDir,
                rOperDir, direc]
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
           | ID LSQRBRACKET exp0 RSQRBRACKET neurArrayPush check_pow_rad_operator  power1 power2 
    '''

def p_neurArrayPush(p):
    '''
    neurArrayPush :
    '''
    global operands_stack, func_dir, curr_scope, Tp, quadruples, quadCounter
    
    aux = operands_stack.pop()
    print(p[-4], "aaaaaaaaaaaa", aux)
    if p[-4] in func_dir[curr_scope]["vars_table"].keys():
        direc = func_dir[curr_scope]["vars_table"][p[-4]]["dirV"]
    elif p[-4] in func_dir["global"]["vars_table"].keys():
        direc = func_dir["global"]["vars_table"][p[-4]]["dirV"]
    elif p[-4] in const_table.keys:
        direc = const_table[p[-4]]
    else:
        raise Error("Access is not in scope")
    if aux in func_dir[curr_scope]["vars_table"].keys():
        dirAux = func_dir[curr_scope]["vars_table"][aux]["dirV"]
    elif aux in func_dir["global"]["vars_table"].keys():
        dirAux = func_dir["global"]["vars_table"][aux]["dirV"]
    elif aux in const_table.keys():
        dirAux = const_table[aux]
    else:
        raise Error("Access is not in scope")
    print("++++----++++----", ["+", direc, dirAux, Tp], quadCounter)
    quadruples.append(["+", dirAux, direc, Tp])
    quadCounter += 1
    operands_stack.append(Tp)
    Tp += 1
    


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
        direc, lOperDir, rOperDir = tempCalculator(left_oper, right_oper, op)
        operands_stack.append(direc)
        quad = [op, lOperDir,
                rOperDir, direc]
        quadruples.append(quad)
        quadCounter += 1
        temp_counter += 1


def p_const_var(p):
    '''
    const_var : CONST_INT neurInt
              | CONST_FLOAT neurFloat
              | ID neurID
    '''
    p[0] = p[1]
    operands_stack.append(p[1])


def p_neurID(p):
    '''
    neurID :
    '''
    global func_dir, curr_scope
    if(p[-1] not in func_dir[curr_scope]["vars_table"].keys()):
        if (p[-1] not in func_dir["global"]["vars_table"].keys()):
            pass
            #raise NameError("Variable " + p[-1] + " not defined")
        else:
            id_type = func_dir["global"]["vars_table"][p[-1]]["type"]
            types_stack.append(id_type)
    else:
        id_type = func_dir[curr_scope]["vars_table"][p[-1]]["type"]
        types_stack.append(id_type)


def p_neurInt(p):
    '''
    neurInt :
    '''
    global types_stack, const_table, Ci
    if p[-1] not in const_table.keys():
        const_table[p[-1]] = Ci
        Ci += 1
    types_stack.append("int")


def p_neurFloat(p):
    '''
    neurFloat :
    '''
    global types_stack, const_table, Cf
    if p[-1] not in const_table.keys():
        const_table[p[-1]] = Cf
        Cf += 1
    types_stack.append("float")


def p_function_call(p):
    '''
    function_call : id_funcCall LPAREN neurFuncCall function_call_params0 RPAREN 
    '''
    global quadruples, quadCounter, paramCounter, paramTableCounter, currFuncCall, func_dir
    if p[1] in func_dir.keys():
        quad = ["GOSUB", p[1], None, func_dir[currFuncCall]["quad_number"]]
        quadruples.append(quad)
        quadCounter += 1
        paramTableCounter = 0
        currFuncCall = ""
    else:
        raise NameError("Function does not exist")


def p_neurFuncCall(p):
    '''
    neurFuncCall : 
    '''
    global paramCounter
    paramCounter = 0


def p_id_funcCall(p):
    '''
    id_funcCall : ID
    '''
    global quadruples, quadCounter, func_dir, paramCounter, currFuncCall, curr_scope
    if p[1] in func_dir.keys():
        currFuncCall = p[1]
        temp_size = func_dir[currFuncCall]["temporal_counter"]
        local_size = len(list(func_dir[currFuncCall]["vars_table"].keys()))
        quad = ["ERA", p[1], None, temp_size]
        quadruples.append(quad)
        quadCounter += 1
        p[0] = p[1]
    else:
        pass
        #raise NameError('Function not defined')


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
    global quadruples, quadCounter, operands_stack, paramCounter, types_stack, curr_scope, paramTableCounter, const_table, Ci
    aux = operands_stack.pop()
    auxType = types_stack.pop()
    if func_dir[currFuncCall]["params_table"][paramTableCounter] != auxType:
        raise TypeError("Parameter type does not match")
    else:
        if(aux in func_dir[curr_scope]["vars_table"].keys()):
            quadruples.append(["PARAM", func_dir[curr_scope]["vars_table"]
                              [aux]["dirV"], "param$"+str(paramCounter), None])
        else:
            if aux not in const_table:
                const_table[aux] = Ci
                Ci += 1
            quadruples.append(["PARAM", const_table[aux],
                              "param$"+str(paramCounter), None])

        quadCounter += 1
        paramCounter += 1
        paramTableCounter += 1


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
        direc, lOperDir, rOperDir = tempCalculator(left_oper, right_oper, op)
        operands_stack.append(direc)
        quad = [op, lOperDir,
                rOperDir, direc]
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
    condition0 : IF LPAREN expression0 condNeur1 RPAREN block0 condition1 condNeur3
    '''


def p_condNeur1(p):
    '''
    condNeur1 :
    '''
    global operands_stack, pSaltos, quadruples, quadCounter
    pSaltos.append(quadCounter)
    temp = operands_stack.pop()
    quadruples.append(["GOTOF", temp, None, None])
    quadCounter += 1


def p_condNeur3(p):
    '''
    condNeur3 :
    '''
    global pSaltos, quadruples, quadCounter
    temp = pSaltos.pop()
    quadruples[temp][3] = quadCounter


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


def p_push_writing_op(p):
    '''
    push_writing_op :
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter
    operators_stack.append('<<<')


def p_push_string_val(p):
    '''
    push_string_val :
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, Cs
    if p[-1] not in const_table.keys():
        const_table[p[-1]] = Cs
        Cs += 1
    operands_stack.append(const_table[p[-1]])
    types_stack.append("string")


def p_writing1(p):
    '''
    writing1 : expression0 push_writing_val writing2 
             | CONST_STRING push_string_val push_writing_val writing2
    '''


def p_push_writing_val(p):
    '''
    push_writing_val : 
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter
    if operands_stack:
        value = operands_stack.pop()
        op = operators_stack.pop()
        print("Push writing val", value, op)
        if value in func_dir["global"]["vars_table"].keys():
            direc = func_dir["global"]["vars_table"][value]["dirV"]
        elif value in func_dir[curr_scope]["vars_table"].keys():
            direc = func_dir[curr_scope]["vars_table"][value]["dirV"]
        elif value not in const_table.keys():
            if type(value) == int:
                direc = value
            else:
                raise ValueError("Not a valid print")
        else:
            direc = value
        quad = [op, None, None, direc]
        quadruples.append(quad)
        quadCounter += 1


def p_writing2(p):
    '''
    writing2 : COMMA push_writing_op writing1
             | empty
    '''


def p_reading(p):
    '''
    reading : READ ID SEMICOLON
    '''
    global operators_stack, operands_stack, types_stack, quadruples, temp_counter, quadCounter
    if p[2] in func_dir["global"]["vars_table"].keys():
        direc = func_dir["global"]["vars_table"][p[2]]["dirV"]
        allocation_type = func_dir["global"]["vars_table"][p[2]]["type"]
    elif p[2] in func_dir[curr_scope]["vars_table"].keys():
        direc = func_dir[curr_scope]["vars_table"][p[2]]["dirV"]
        allocation_type = func_dir[curr_scope]["vars_table"][p[2]]["type"]
    else:
        raise NameError("Variable does not exist")
    quad = [p[1], None, allocation_type, direc]
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
        quad = ["RETURN", None, None, value]
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
    global operands_stack, pSaltos, quadruples, quadCounter
    pSaltos.append(quadCounter)
    temp = operands_stack.pop()
    quadruples.append(["GOTOF", temp, None, None])
    quadCounter += 1


def p_wNeur3(p):
    '''
    wNeur3 :
    '''
    global pSaltos, quadruples, quadCounter
    temp1 = pSaltos.pop()
    temp2 = pSaltos.pop()
    quadruples.append(["GOTO", None, None, temp2])
    quadCounter += 1
    quadruples[temp1][3] = quadCounter


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
    global Li, Lf, Lo, Ti, Tf, Tb, To, Ts, func_mem
    Li = 5000
    Lf = 7000
    Lo = 10000
    Ti = 11000
    Tf = 12000
    Tb = 13000
    To = 14000
    Ts = 15000
    #                 Li,Lf,Ti,Tf,Tb
    func_mem = [0, 0, 0, 0, 0]


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
    global curr_scope, func_dir, prev_scope, quadruples, quadCounter
    quadruples[0][3] = quadCounter
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
                print("ROUTINE END")

        except EOFError:
            print(EOFError)
    else:
        print('Se necesita un archivo como argumento.')
