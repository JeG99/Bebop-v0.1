from multiprocessing.sharedctypes import Value
import operator


class VirtualMachine():
    def __init__(self, quads, func_dir, const_table):
        # Limits for stack reference
        self.Li = 5000
        self.Lf = 7000
        self.Ti = 11000
        self.Tf = 12000
        self.Tb = 13000

        self.func_dir_copy = func_dir.copy()
        self.const_table_copy = const_table.copy()
        self.mem = [None for i in range(20000)]
        self.mem_backup = self.mem
        self.instructions = quads.copy()
        self.curr_ip = 0
        self.ip_saltos = []
        self.execution_stack = []  # Aqui van los activation records
        self.curr_func = ""
        self.params_counter = 0

        # Mapear memoria (las "declaraciones")
        self.mem_init()

    def activation_record_dir_translator(self, dir):
        if dir >= self.Li and dir < self.Lf:
            stack_dir = (0, dir - self.Li)
        elif dir >= self.Lf and dir < self.Ti:
            stack_dir = (1, dir - self.Lf)
        elif dir >= self.Ti and dir < self.Tf:
            stack_dir = (2, dir - self.Ti)
        elif dir >= self.Tf and dir < self.Tb:
            stack_dir = (3, dir - self.Tf)
        elif dir >= self.Tb and dir < self.Tb + 1000:
            stack_dir = (4, dir - self.Tb)
        else:
            return 0
        return stack_dir

    def mem_init(self):
        # Mapping virtual directions for simple variables (and arrays)
        scopes = list(self.func_dir_copy.keys())
        while(len(scopes) > 0):
            scope = scopes.pop()
            scope_vars = list(self.func_dir_copy[scope]['vars_table'].keys())
            while(len(scope_vars) > 0):
                var_name = scope_vars.pop()
                var_dir = self.func_dir_copy[scope]['vars_table'][var_name]['dirV']
                if not self.func_dir_copy[scope]['vars_table'][var_name]['isArray']:
                    var_val = self.func_dir_copy[scope]['vars_table'][var_name]['value']
                    # Setting space for a simple variable
                    self.mem[var_dir] = var_val
                else:
                    space_counter = self.func_dir_copy[scope]['vars_table'][var_name]['size']
                    # Setting a place for an array
                    aux = 0
                    while(aux != space_counter):
                        self.mem[var_dir + aux] = 0
                        aux += 1

        # Mapping virtual directions for constants
        const_vals = list(self.const_table_copy.keys())
        while(len(const_vals) > 0):
            const_val = const_vals.pop()
            self.mem[self.const_table_copy[const_val]] = const_val

    def stack_operation(self, op, ip):
        left_op_dir = self.instructions[ip][1]
        right_op_dir = self.instructions[ip][2]
        res_dir = self.activation_record_dir_translator(
            self.instructions[ip][3])

        if not ((left_op_dir >= 16000 and left_op_dir < 19000) or (left_op_dir >= 0 and left_op_dir < 4000)):
            # Left operand
            left_op_dir = self.activation_record_dir_translator(left_op_dir)
            left_op = self.execution_stack[-1][left_op_dir[0]][left_op_dir[1]]
        else:
            left_op = self.mem_backup[left_op_dir]

        if not ((right_op_dir >= 16000 and right_op_dir < 19000) or (right_op_dir >= 0 and right_op_dir < 4000)):
            # Right operand
            right_op_dir = self.activation_record_dir_translator(right_op_dir)
            right_op = self.execution_stack[-1][right_op_dir[0]
                                                ][right_op_dir[1]]
        else:
            right_op = self.mem_backup[right_op_dir]
        # Temporal direction
        self.execution_stack[-1][res_dir[0]
                                 ][res_dir[1]] = op(left_op, right_op)

    def stack_assignation(self, ip):
        value_dir = self.instructions[ip][1]
        dir = self.instructions[ip][3]
        if not ((value_dir >= 16000 and value_dir < 19000) or (value_dir >= 0 and value_dir < 4000)):
            # Left operand
            value_dir = self.activation_record_dir_translator(value_dir)
            value = self.execution_stack[-1][value_dir[0]][value_dir[1]]
        else:
            value = self.mem_backup[value_dir]
        # Temporal direction
        if not (dir >= 0 and dir < 4000):
            dir = self.activation_record_dir_translator(dir)
            self.execution_stack[-1][dir[0]][dir[1]] = value
        else:
            self.mem_backup[dir] = value

    def stack_out(self, ip):
        value_dir = self.instructions[ip][3]

        if not ((value_dir >= 16000 and value_dir < 19000) or (value_dir >= 0 and value_dir < 4000)):
            # Left operand
            value_dir = self.activation_record_dir_translator(value_dir)
            value = self.execution_stack[-1][value_dir[0]][value_dir[1]]
        else:
            value = self.mem_backup[value_dir]
        # Temporal direction
        print(value)

    def stack_in(self, ip):
        talloc = self.instructions[ip][2]
        dir = self.instructions[ip][3]
        value = eval(talloc + '( input() )')
        try:
            if not ((dir >= 16000 and dir < 19000) or (dir >= 0 and dir < 4000)):
                # Read allocation
                dir = self.activation_record_dir_translator(dir)
                self.execution_stack[-1][dir[0]][dir[1]] = value
            else:
                self.mem_backup[dir] = value
        except:
            raise ValueError('This input must be of type ' + talloc)

    def stack_return(self, ip):
        dir = self.instructions[ip][3]
        if not ((dir >= 16000 and dir < 19000) or (dir >= 0 and dir < 4000)):
            # Read allocation
            dir = self.activation_record_dir_translator(dir)
            value = self.execution_stack[-1][dir[0]][dir[1]]
        else:
            value = self.mem_backup[dir]
        return value
        

    def mem_dump(self):  # Just to show the current view of memory
        for idx, val in enumerate(self.mem):
            if val != None:
                print(idx, val)
        print('-----------------DEBUG-----------------')

    def mem_backup_dump(self):  # Just to show the current view of memory
        for idx, val in enumerate(self.mem_backup):
            if val != None:
                print(idx, val)
        print('-----------------DEBUG-----------------')

    def get_mem(self, idx):
        return self.mem[idx]

    def run(self):
        print("ROUTINE START")
        while(self.instructions[self.curr_ip][0] != 'END'):
            #print("B4",self.instructions[self.curr_ip])
            if type(self.instructions[self.curr_ip][1]) == int:
                if self.instructions[self.curr_ip][1] >= 19000:
                    self.instructions[self.curr_ip][1] = self.mem[self.instructions[self.curr_ip][1]]
            if type(self.instructions[self.curr_ip][2]) == int:
                if self.instructions[self.curr_ip][2] >= 19000:
                    self.instructions[self.curr_ip][2] = self.mem[self.instructions[self.curr_ip][2]]
            #print(self.instructions[self.curr_ip])
            if self.instructions[self.curr_ip][0] == '+':
                #print("---",self.instructions[self.curr_ip])
                if len(self.execution_stack) > 0:
                    self.stack_operation(operator.add, self.curr_ip)
                else:
                    # Left operand
                    left_op_dir = self.instructions[self.curr_ip][1]
                    # Right operand
                    right_op_dir = self.instructions[self.curr_ip][2]
                    #print(self.mem[left_op_dir], "+", self.mem[right_op_dir])
                    if self.instructions[self.curr_ip][3] >= 19000:
                        
                        self.mem[self.instructions[self.curr_ip][3]
                                 ] = self.mem[left_op_dir] + right_op_dir
                        #print(self.mem[self.instructions[self.curr_ip][3]
                        #         ],self.mem[left_op_dir] + right_op_dir, "+++++++++++++")
                        #self.mem_dump()
                    else:
                        # Temporal direction
                        self.mem[self.instructions[self.curr_ip][3]
                                 ] = self.mem[left_op_dir] + self.mem[right_op_dir]
                        #print(self.mem[left_op_dir] + self.mem[right_op_dir], "-----------------")

            elif self.instructions[self.curr_ip][0] == '-':
                if len(self.execution_stack) > 0:
                    self.stack_operation(operator.sub, self.curr_ip)
                else:
                    # Left operand
                    left_op_dir = self.instructions[self.curr_ip][1]
                    # Right operand
                    right_op_dir = self.instructions[self.curr_ip][2]
                    # Temporal direction
                    self.mem[self.instructions[self.curr_ip][3]
                             ] = self.mem[left_op_dir] - self.mem[right_op_dir]

            elif self.instructions[self.curr_ip][0] == '*':
                if len(self.execution_stack) > 0:
                    self.stack_operation(operator.mul, self.curr_ip)
                else:
                    # Left operand
                    left_op_dir = self.instructions[self.curr_ip][1]
                    # Right operand
                    right_op_dir = self.instructions[self.curr_ip][2]
                    # Temporal direction
                    self.mem[self.instructions[self.curr_ip][3]
                             ] = self.mem[left_op_dir] * self.mem[right_op_dir]

            elif self.instructions[self.curr_ip][0] == '/':
                if len(self.execution_stack) > 0:
                    self.stack_operation(operator.truediv, self.curr_ip)
                else:
                    # Left operand
                    left_op_dir = self.instructions[self.curr_ip][1]
                    # Right operand
                    right_op_dir = self.instructions[self.curr_ip][2]
                    # Temporal direction
                    self.mem[self.instructions[self.curr_ip][3]
                             ] = self.mem[left_op_dir] / self.mem[right_op_dir]

            elif self.instructions[self.curr_ip][0] == '**':
                if len(self.execution_stack) > 0:
                    self.stack_operation(operator.pow, self.curr_ip)
                else:
                    # Left operand
                    left_op_dir = self.instructions[self.curr_ip][1]
                    # Right operand
                    right_op_dir = self.instructions[self.curr_ip][2]
                    # Temporal direction
                    self.mem[self.instructions[self.curr_ip][3]
                             ] = self.mem[left_op_dir] ** self.mem[right_op_dir]

            elif self.instructions[self.curr_ip][0] == '\\|':
                # Left operand
                left_op_dir = self.instructions[self.curr_ip][1]
                # Right operand
                right_op_dir = self.instructions[self.curr_ip][2]
                # Temporal direction
                self.mem[self.instructions[self.curr_ip][3]
                         ] = self.mem[right_op_dir] ** (1 / self.mem[left_op_dir])

            elif self.instructions[self.curr_ip][0] == '<':
                if len(self.execution_stack) > 0:
                    self.stack_operation(operator.lt, self.curr_ip)
                else:
                    # Left operand
                    left_op_dir = self.instructions[self.curr_ip][1]
                    # Right operand
                    right_op_dir = self.instructions[self.curr_ip][2]
                    # Temporal direction
                    self.mem[self.instructions[self.curr_ip][3]
                             ] = self.mem[left_op_dir] < self.mem[right_op_dir]

            elif self.instructions[self.curr_ip][0] == '>':
                if len(self.execution_stack) > 0:
                    self.stack_operation(operator.gt, self.curr_ip)
                else:
                    # Left operand
                    left_op_dir = self.instructions[self.curr_ip][1]
                    # Right operand
                    right_op_dir = self.instructions[self.curr_ip][2]
                    # Temporal direction
                    self.mem[self.instructions[self.curr_ip][3]
                             ] = self.mem[left_op_dir] > self.mem[right_op_dir]

            elif self.instructions[self.curr_ip][0] == '<>':
                #print(self.instructions[self.curr_ip][1], self.instructions[self.curr_ip][2], self.instructions[self.curr_ip][3])
                #print(self.mem[self.instructions[self.curr_ip][1]], self.mem[self.instructions[self.curr_ip][2]], self.mem[self.instructions[self.curr_ip][3]])
                if len(self.execution_stack) > 0:
                    self.stack_operation(operator.ne, self.curr_ip)
                else:
                    # Left operand
                    left_op_dir = self.instructions[self.curr_ip][1]
                    # Right operand
                    right_op_dir = self.instructions[self.curr_ip][2]
                    # Temporal direction
                    self.mem[self.instructions[self.curr_ip][3]
                             ] = self.mem[left_op_dir] != self.mem[right_op_dir]

            elif self.instructions[self.curr_ip][0] == '==':
                if len(self.execution_stack) > 0:
                    self.stack_operation(operator.eq, self.curr_ip)
                else:
                    # Left operand
                    left_op_dir = self.instructions[self.curr_ip][1]
                    # Right operand
                    right_op_dir = self.instructions[self.curr_ip][2]
                    # Temporal direction
                    #print(self.mem[left_op_dir], "==", self.mem[right_op_dir], "=", self.mem[left_op_dir] == self.mem[right_op_dir] ,"///////")
                    self.mem[self.instructions[self.curr_ip][3]
                             ] = self.mem[left_op_dir] == self.mem[right_op_dir]

            elif self.instructions[self.curr_ip][0] == '=':
                if len(self.execution_stack) > 0:
                    self.stack_assignation(self.curr_ip)
                else:
                    # print(self.instructions[self.curr_ip])

                    # Value to be stored
                    value = self.mem[self.instructions[self.curr_ip][1]]
                    # Memory direction
                    dir = self.instructions[self.curr_ip][3]
                    if dir >= 19000 and self.instructions[self.curr_ip][1] >= 19000:
                        self.mem[self.mem[dir]] = self.mem[value]
                        
                    elif self.instructions[self.curr_ip][1] >= 19000:
                        #print("Entra 2")
                        self.mem[dir] = self.mem[value]
                    elif  dir >= 19000:
                        #print("Entra 3")
                        self.mem[self.mem[dir]] = value
                    else:
                        self.mem[dir] = value
                    # self.mem_dump()

            elif self.instructions[self.curr_ip][0] == '<<<':
                #print(self.instructions[self.curr_ip], self.mem[self.instructions[self.curr_ip][3]])
                if len(self.execution_stack) > 0:
                    self.stack_out(self.curr_ip)
                else:
                    dir = self.instructions[self.curr_ip][3]
                    dirAux = dir
                    if type(dir) != str:
                        dir = self.mem[dir]
                    if dirAux >= 19000:
                        print(self.mem[dir])
                    else:
                        print(dir)

            elif self.instructions[self.curr_ip][0] == '>>>':
                if len(self.execution_stack) > 0:
                    self.stack_in(self.curr_ip)
                else:
                    talloc = self.instructions[self.curr_ip][2]
                    dir = self.instructions[self.curr_ip][3]
                    try:
                        value = eval(talloc + '( input() )')
                        self.mem[dir] = value
                    except:
                        raise ValueError(
                            'This input must be of type ' + talloc)

            elif self.instructions[self.curr_ip][0] == 'GOTO':
                self.curr_ip = self.instructions[self.curr_ip][3]
                continue

            elif self.instructions[self.curr_ip][0] == 'GOTOF':
                cond_dir = self.instructions[self.curr_ip][1]
                if not self.mem[cond_dir]:
                    self.curr_ip = self.instructions[self.curr_ip][3]
                    continue

            elif self.instructions[self.curr_ip][0] == 'GOSUB':
                self.ip_saltos.append(self.curr_ip)
                self.curr_ip = self.instructions[self.curr_ip][3]
                continue

            elif self.instructions[self.curr_ip][0] == 'ERA':
                self.curr_func = self.instructions[self.curr_ip][1]
                reserved_chunk = self.instructions[self.curr_ip][3]
                if len(reserved_chunk) == 0:
                    self.instructions[self.curr_ip][3] = self.func_dir_copy[self.curr_func]['temporal_counter']
                    i = self.curr_ip
                    while(self.instructions[i][0] != 'ENDPROC'):
                        i += 1
                    self.curr_ip = i + 1
                    continue

                activation_record = [
                    [None for i in range(reserved_chunk[0])],
                    [None for i in range(reserved_chunk[1])],
                    [None for i in range(reserved_chunk[2])],
                    [None for i in range(reserved_chunk[3])],
                    [None for i in range(reserved_chunk[4])]
                ]
                self.execution_stack.append(activation_record)
                self.mem_backup = self.mem.copy()

            elif self.instructions[self.curr_ip][0] == 'PARAM':
                pass

            elif self.instructions[self.curr_ip][0] == 'RETURN':                
                func = self.instructions[self.curr_ip][1]
                value = self.stack_return(self.curr_ip)
                dir = self.func_dir_copy["global"]["vars_table"][func]["dirV"] 
                self.mem_backup[dir] = value

            elif self.instructions[self.curr_ip][0] == 'ENDPROC':
                activation_record = self.execution_stack.pop()
                self.mem = self.mem_backup
                salto = self.ip_saltos.pop()
                self.curr_ip = salto

            elif self.instructions[self.curr_ip][0] == 'VERIFY':
                lower_limit = self.instructions[self.curr_ip][2]
                upper_limit = self.instructions[self.curr_ip][3]
                index = self.instructions[self.curr_ip][1]
                
                if (index >= 11000 and index < 12001) or (index >= 5000 and index < 7000) or (index >= 16000 and index < 17000):
                    index = self.mem[self.instructions[self.curr_ip][1]]
                #print(">>>>>>>>>>>>>>>>>>>>>>",index, upper_limit, lower_limit)
                if index > upper_limit or index < lower_limit:
                    raise IndexError('Array index out of range.')

            self.curr_ip += 1
        # self.mem_dump()
