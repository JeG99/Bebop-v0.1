from typing_extensions import Self


class VirtualMachine():
    def __init__(self, quads, var_table, func_dir, const_table):
        self.instructions = quads

    def set_global_mem(self):
        pass

    def set_local_mem(self):
        pass

    def set_temp_mem(self):
        pass

    def run(self):   
        pass