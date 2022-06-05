import json
from turtle import clear


class ActivationRecord():
    def __init__(self, param_size, temp_size):
        pass


class VirtualMachine():
    def __init__(self, quads, func_dir, const_table):
        self.func_dir_copy = func_dir.copy()
        self.const_table_copy = const_table.copy()
        self.mem = [None for i in range(19000)]
        self.mem_backup = self.mem
        self.instructions = quads.copy()
        self.prev_ip = 0
        self.curr_ip = 0
        self.execution_stack = [] # Aqui van los activation records
        
        # Mapear memoria (las "declaraciones")
        self.mem_init()

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
                    print("Name : ", var_name)
                    var_val = self.func_dir_copy[scope]['vars_table'][var_name]['value']
                    self.mem[var_dir] = var_val # Setting space for a simple variable
                else: 
                    space_counter = self.func_dir_copy[scope]['vars_table'][var_name]['size']
                    # Setting a place for an array
                    aux = 0
                    while(aux != space_counter):
                        self.mem[var_dir + aux] = 0
                        aux += 1
                    '''while(space_counter > -1):
                        print("+-+-+-+-", var_dir + space_counter)
                        self.mem[var_dir + space_counter] = 0
                        space_counter -= 1'''



        
        # Mapping virtual directions for constants
        const_vals = list(self.const_table_copy.keys())
        while(len(const_vals) > 0):
            const_val = const_vals.pop()
            self.mem[self.const_table_copy[const_val]] = const_val

    def mem_dump(self): # Just to show the current view of memory
        for idx, val in enumerate(self.mem):
            if val != None:
                print(idx, val)
        print('-------------------------------')

    def get_mem(self, idx):
        return self.mem[idx]

    def run(self):
        
        while(self.instructions[self.curr_ip][0] != 'END'):
            print(self.instructions[self.curr_ip])
            if self.instructions[self.curr_ip][0] == '+':
                # Left operand
                left_op_dir = self.instructions[self.curr_ip][1]
                # Right operand
                right_op_dir = self.instructions[self.curr_ip][2]
                if self.instructions[self.curr_ip][3] >= 18000:
                    self.mem[self.instructions[self.curr_ip][3]] = self.mem[left_op_dir] + right_op_dir
                else:
                # Temporal direction
                    print(self.mem[left_op_dir], "+" ,self.mem[right_op_dir])
                    self.mem[self.instructions[self.curr_ip][3]] = self.mem[left_op_dir] + self.mem[right_op_dir]

            elif self.instructions[self.curr_ip][0] == '-':
                # Left operand
                left_op_dir = self.instructions[self.curr_ip][1]
                # Right operand
                right_op_dir = self.instructions[self.curr_ip][2]
                # Temporal direction
                self.mem[self.instructions[self.curr_ip][3]] = self.mem[left_op_dir] - self.mem[right_op_dir]
            
            elif self.instructions[self.curr_ip][0] == '*':
                # Left operand
                left_op_dir = self.instructions[self.curr_ip][1]
                # Right operand
                right_op_dir = self.instructions[self.curr_ip][2]
                # Temporal direction
                self.mem[self.instructions[self.curr_ip][3]] = self.mem[left_op_dir] * self.mem[right_op_dir]
            
            elif self.instructions[self.curr_ip][0] == '/':
                # Left operand
                left_op_dir = self.instructions[self.curr_ip][1]
                # Right operand
                right_op_dir = self.instructions[self.curr_ip][2]
                # Temporal direction
                self.mem[self.instructions[self.curr_ip][3]] = self.mem[left_op_dir] / self.mem[right_op_dir]
            
            elif self.instructions[self.curr_ip][0] == '**':
                # Left operand
                left_op_dir = self.instructions[self.curr_ip][1]
                # Right operand
                right_op_dir = self.instructions[self.curr_ip][2]
                # Temporal direction
                self.mem[self.instructions[self.curr_ip][3]] = self.mem[left_op_dir] ** self.mem[right_op_dir]
            
            elif self.instructions[self.curr_ip][0] == '\\|':
                # Left operand
                left_op_dir = self.instructions[self.curr_ip][1]
                # Right operand
                right_op_dir = self.instructions[self.curr_ip][2]
                # Temporal direction
                self.mem[self.instructions[self.curr_ip][3]] = self.mem[right_op_dir] ** (1 / self.mem[left_op_dir]) 
            
            elif self.instructions[self.curr_ip][0] == '<':
                # Left operand
                left_op_dir = self.instructions[self.curr_ip][1]
                # Right operand
                right_op_dir = self.instructions[self.curr_ip][2]
                # Temporal direction
                self.mem[self.instructions[self.curr_ip][3]] = self.mem[left_op_dir] < self.mem[right_op_dir]
            
            elif self.instructions[self.curr_ip][0] == '>':
                # Left operand
                left_op_dir = self.instructions[self.curr_ip][1]
                # Right operand
                right_op_dir = self.instructions[self.curr_ip][2]
                # Temporal direction
                self.mem[self.instructions[self.curr_ip][3]] = self.mem[left_op_dir] > self.mem[right_op_dir]
            
            elif self.instructions[self.curr_ip][0] == '<>':
                # Left operand
                left_op_dir = self.instructions[self.curr_ip][1]
                # Right operand
                right_op_dir = self.instructions[self.curr_ip][2]
                # Temporal direction
                self.mem[self.instructions[self.curr_ip][3]] = self.mem[left_op_dir] != self.mem[right_op_dir]
            
            elif self.instructions[self.curr_ip][0] == '==':
                # Left operand
                left_op_dir = self.instructions[self.curr_ip][1]
                # Right operand
                right_op_dir = self.instructions[self.curr_ip][2]
                # Temporal direction
                self.mem[self.instructions[self.curr_ip][3]] = self.mem[left_op_dir] == self.mem[right_op_dir]
            
            elif self.instructions[self.curr_ip][0] == '=':
                # Value to be stored
                value = self.mem[self.instructions[self.curr_ip][1]]
                # Memory direction
                dir = self.instructions[self.curr_ip][3]
                if dir >= 18000: # Si la direccion a guardar es un puntero
                    self.mem[self.mem[dir]] = value
                else:
                    self.mem[dir] = value

            elif self.instructions[self.curr_ip][0] == '<<<':
                dir = self.instructions[self.curr_ip][3]
                if type(dir) != str:
                    dir = self.mem[dir]
                print(dir)

            elif self.instructions[self.curr_ip][0] == '>>>':
                dir = self.instructions[self.curr_ip][3]
                value = input()
                self.mem[dir] = value
                #if type(dir) != str:
                #    dir = self.mem[dir]
                #print(dir)
        
            elif self.instructions[self.curr_ip][0] == 'GOTO':
                #print(self.instructions[self.curr_ip][3])
                self.curr_ip = self.instructions[self.curr_ip][3]
                continue
                
            elif self.instructions[self.curr_ip][0] == 'GOTOF':
                cond_dir = self.instructions[self.curr_ip][1] 
                if not self.mem[cond_dir]:
                    self.curr_ip = self.instructions[self.curr_ip][3]
                    continue
                
            elif self.instructions[self.curr_ip][0] == 'GOSUB':
                print(self.instructions[self.curr_ip])
                self.prev_ip = self.curr_ip
                self.curr_ip = self.instructions[self.curr_ip][3]
                continue
            
            elif self.instructions[self.curr_ip][0] == 'ERA':
                pass
            
            elif self.instructions[self.curr_ip][0] == 'PARAM':
                pass
            
            elif self.instructions[self.curr_ip][0] == 'RETURN':
                pass
            
            elif self.instructions[self.curr_ip][0] == 'ENDPROC':
                self.curr_ip = self.prev_ip
            
            elif self.instructions[self.curr_ip][0] == 'VERIFY':
                print(self.instructions[self.curr_ip])
                lower_limit = self.instructions[self.curr_ip][2]
                upper_limit = self.instructions[self.curr_ip][3]
                index = self.instructions[self.curr_ip][1]
                if index >= 11000 and index < 12001:
                    index = self.mem[self.instructions[self.curr_ip][1]]
                    
                if index > upper_limit or index < lower_limit:
                    raise IndexError('Array index out of range.')
            
            self.curr_ip += 1   
        self.mem_dump()