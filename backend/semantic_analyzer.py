class SymbolTable:
    def __init__(self, parent=None):
        self.syms = {} #key: string val: dict
        self.parent = parent


    def get(self, sym_name, checkParent = True):
        sym = self.syms.get(sym_name, None)
        if not sym and self.parent and checkParent:
            return self.parent.get(sym_name)
        return sym
    
        
    # ALWAYS NAME ARGS FOR DTYPE PRIV AND CONST WHEN CALLING SET
    def _create_symbol_entry(self, value, dtype, priv, const):
        return {
            "value": value,
            "dtype": dtype,
            "priv": priv,
            "const": const,
        }

    def set(self, sym_name, value, dtype=None, priv=False, const=False):
        sym_content = self._create_symbol_entry(value, dtype, priv, const)
        self.syms[sym_name] = sym_content

    def set_array(self, sym_name, value, dtype, arr_info, priv=False, const=False):
        sym_content = self._create_symbol_entry(value, dtype, priv, const)
        sym_content["arr_info"] = arr_info  
        self.syms[sym_name] = sym_content

    def set_class(self, sym_name, value, dtype, class_info, priv=False, const=False):
        sym_content = self._create_symbol_entry(value, dtype, priv, const)
        sym_content["class_info"] = class_info 
        self.syms[sym_name] = sym_content

    def set_function(self, sym_name, return_type, param_types, priv=False, const=False, isStd_lib=True):
        sym_content = self._create_symbol_entry(value=None, dtype=return_type, priv=priv, const=const)
        sym_content["params"] = param_types 
        sym_content["isStd_lib"] = isStd_lib 
        self.syms[sym_name] = sym_content

class SemanticAnalyzer:

    numtypes = ['int', 'long', 'float', 'double']
   
    MIN_INT = -2147483648
    MAX_INT = 2147483647
    MIN_LONG = -9223372036854775808
    MAX_LONG = 9223372036854775807
    MIN_FLOAT = -999999990.0
    MAX_FLOAT = 999999990
    MIN_DOUBLE = -9999999999999999000
    MAX_DOUBLE = 9999999999999999000

    def interpret(self, node):
        try:
            self.visit_node(node)
            self.errors.append("Semantic analysis completed successfully. No Semantic Errors found.")
            print("Semantic checking completed successfully. No Semantic Errors found.")
            print('(semantic)(dbg) global table: ')
            #print global dbg #wont be seen until prog construts is implemented
            for s in self.curr_scope.syms:
                print(f'(semantic)(dbg)\t\t{s} : {self.curr_scope.syms[s]}')
        except SyntaxError as e:
            print (e)

        return self.errors

    def __init__(self):
        self.curr_scope = SymbolTable()
        self.errors = []

    def enter_scope(self, nodeName):
        print(F'(semantic)(dbg) ENTERING scope {nodeName}')
        self.curr_scope = SymbolTable(self.curr_scope)
    
    def exit_scope(self, nodeName):
        print(F'(semantic)(dbg) EXITING scope {nodeName}, table: ')
        #print table dbg
        for s in self.curr_scope.syms:
            print(f'(semantic)(dbg)\t\t{s} : {self.curr_scope.syms[s]}')
        self.curr_scope = self.curr_scope.parent

    def visit_node(self, node):
        nodeName = type(node).__name__
        visit_func = getattr(self, f'visit_{nodeName}', None)  # Get the appropriate visit function, or None if it doesn't exist

        if visit_func is None:
            print(f"(semantic)(dbg) Not implemented yet!!!!!!!!!!!!!!!!!! node name: {nodeName}")
        else:
            print(f'(semantic)(dbg) VISITING {nodeName}!!')
            return visit_func(node)
        
    def logError(self, msg, idenNode = None): #only works on node_iden
        if idenNode:
            currLine = idenNode.id_t["tokenLine"]
            currCol = idenNode.id_t["tokenCol"]
            full_message = (
                f"Semantic Error ({currLine}, {currCol}): {msg}"
            )
        else:
            full_message = (
                f"Semantic Error(#todo line nums): {msg}"
            )
        self.errors.append(full_message)
        print(full_message)
        raise SyntaxError(full_message)



    # ------------------------------------ NODE VISITATION FUNCS----------------------------------
    # FORMAT: visit_{node_name}
    # VALUE nodes always return tuple of dtype and value
    
    #program PLACEHODLER
    def visit_program_node(self, node):
        #PLACEHOLDER! the real thing would iterate through      
        #self.visit_node(node.program_structure_stmts[2])

        for statement in node.program_structure_stmts:
            self.visit_node(statement)
    
    #body PLACEHOLDER
    def visit_node_body(self, node):
        self.enter_scope(type(node).__name__)
        # PLACEHOLDER! idk if it's correct
        self.visit_node(node.body_codeblock_n)
        self.exit_scope(type(node).__name__)

    #code_block PLACEHODLER
    def visit_node_code_block(self, node):
        # PLACEHODLER!! idk if correct
        for statement in node.code_block_statement_n:
            self.visit_node(statement)

    def visit_node_program_constructs(self, node):
        self.enter_scope(type(node).__name__)
        
        for global_declarations in node.program_constructs_statement_n:
            self.visit_node(global_declarations)
        
        print("(semantic)(dbg) EXITING scope 'Program Constructs', GLOBAL TABLE: ", self.curr_scope.syms)
        self.curr_scope = self.curr_scope.parent

    def visit_node_num(self, node):
        val = 0
        if node.dtype in ['int', 'long']:
            val = int(node.val_t["tokenName"])
        elif node.dtype in ['float', 'double']:
            val = float(node.val_t["tokenName"])
        return (node.dtype, val) 
    
    def visit_node_str(self, node):
        return (node.dtype, node.val_t["tokenName"][1:-1])
    
    def visit_node_bool(self, node):
        return (node.dtype, node.val_t["tokenName"]=="true")
    
    def visit_node_iden(self, node):
        iden_symbol = self.curr_scope.get(node.id_t["tokenName"])
        if not iden_symbol:
            self.logError(f"Symbol '{node.id_t["tokenName"]}' hasn't been declared yet.", node)
        else:
            dtype = iden_symbol["dtype"]
            val = 0
            if dtype in ['int', 'long']:
                val = int(iden_symbol["value"])
            elif dtype in ['float', 'double']:
                val = float(iden_symbol["value"])
            return (dtype, val)
    #cont...
    def visit_node_func_dec(self, node):
        func_name = node.id_n.id_t["tokenName"]
        return_type = node.dtype_t["tokenName"]

        # Check if function already exists in current scope
        if self.curr_scope.get(func_name, checkParent=False):
            self.logError(f"Function '{func_name}' is already declared.", node.id_n)
            return

        # Store func params into function signature in symbol table
        param_types = []

        for param in node.params_n:
            if type(param).__name__ == "node_funcpar_class":
                param_types.append({
                    "type": "class",
                    "classname": param.class_id_n.id_t["tokenName"]
                })  

            elif type(param).__name__ == "node_funcpar_arr":
                param_types.append({
                    "type": "arr",
                    "dtype": param.dtype_t["tokenName"],  # Include the data type
                    "dimension": param.arrdim_i
                })  

            elif type(param).__name__ == "node_funcpar_var":
                param_types.append({
                    "type": "var",
                    "dtype": param.dtype_t["tokenName"]
                })  
        
        # sample parameter format
        # [
        #     {"type": "var", "dtype": "int"},
        #     {"type": "class", "name": "MyClass"},
        #     {"type": "arr", "dimension": 10}
        # ]

        # Store function in symbol table
        self.curr_scope.set_function(func_name, return_type, param_types, isStd_lib = False)  # const bc functions are not reassignable

        # Enter function scope
        self.enter_scope(type(node).__name__)

        # Add parameters to new function scope
        for param in node.params_n:
            param_name = param.id_n.id_t["tokenName"]

            # Check if parameter name is duplicated
            if self.curr_scope.get(param_name, checkParent=False):
                self.logError(f"Parameter '{param_name}' is already declared in function '{func_name}'.", param.id_n)

            # Handle different parameter types properly
            if type(param).__name__ == "node_funcpar_class":
                class_name = param.class_id_n.id_t["tokenName"]
                self.curr_scope.set_class(param_name, value=None, dtype="class", class_info={"classname": class_name}, const=False)

            elif type(param).__name__ == "node_funcpar_arr":
                arr_dtype = param.dtype_t["tokenName"]
                arr_dim = param.arrdim_i
                self.curr_scope.set_array(param_name, value=None, dtype=arr_dtype, arr_info={"dimension": arr_dim}, const=False)

            elif type(param).__name__ == "node_funcpar_var":
                var_dtype = param.dtype_t["tokenName"]
                self.curr_scope.set(param_name, value=None, dtype=var_dtype, const=False)


        # Visit function body
        # has_return = any(self.visit_node(stmt) for stmt in node.body_n)

        # # If function is non-void, ensure at least one return exists
        # if return_type != "void" and not has_return:
        #     self.logError(f"Function '{func_name}' must return a value of type '{return_type}'.", node.id_n)

        # Exit function scope, back to program constructs
        print(f"(semantic)(dbg) EXITING scope 'Function: {func_name}', SYMBOL TABLE: ", self.curr_scope.syms)
        self.curr_scope = self.curr_scope.parent


    #var_dec
    def visit_node_vardec(self, node):
        if self.curr_scope.get(node.id_n.id_t["tokenName"], False):
            self.logError(f"Symbol '{node.id_n.id_t["tokenName"]}' has already been declared.", node.id_n)
        const = node.const_b
        dtype = node.dtype_t["tokenName"]
        id = node.id_n.id_t["tokenName"]
        val_type = None
        value = None
        idec_rec = None
        if (node.vardec_cont_n):
            val_type, value = self.visit_node(node.vardec_cont_n.value_n)
            idec_rec = node.vardec_cont_n.idec_rec_n
                    
        if value and dtype != val_type:
            self.logError(f"Type mismatch: expected '{dtype}' but found '{val_type}'", node.id_n)
        if not value:
            match dtype:
                case 'bool':
                    value = False
                case 'int':
                    value = 0
                case 'long':
                    value = 0
                case 'float':
                    value = 0.0
                case 'double':
                    value = 0.0
                case 'string':
                    value = ''
        self.curr_scope.set(id, value, dtype=dtype, const=const)
        for dec_node in idec_rec or []:
            self.curr_scope.set(dec_node.id_n.id_t["tokenName"], self.visit_node(dec_node.value_n) if dec_node.value_n else None, dtype=dtype, const=const)

    # binary and unary operations
    def visit_node_bi_op(self, node):
        
        left_type, left_val = self.visit_node(node.left_n)
        right_type, right_val = self.visit_node(node.right_n)
        dtype = 'int'
        if (left_type == 'long' or right_type == 'long'):
            dtype = 'long'
        if (left_type == 'float' or right_type == 'float'):
            dtype = 'float'
        if (left_type == 'double' or right_type == 'double'):
            dtype = 'double'
        match node.op_t["tokenName"]:
            case '+': 
                if left_type == 'string':
                    if right_type != 'string':
                        print('(semantic)(dbg) ERROR: string exp only strings')
                    else:
                        return ('string', left_val + right_val)
                elif left_type in self.numtypes and right_type in self.numtypes:
                    return (dtype, left_val + right_val)
                else:
                     print('(semantic)(dbg) ERROR: only numerics')

            case '-':
                if left_type in self.numtypes and right_type in self.numtypes:
                    return (dtype, left_val - right_val)
                else:
                    print('(semantic)(dbg) ERROR: only numerics')
            case '/':
                if right_val == 0: #todo
                    print("(semantic)(dbg) ERROR: DIVIDE BY 0")
                if left_type in self.numtypes and right_type in self.numtypes:
                    return (dtype, left_val / right_val)
                else:
                    print('(semantic)(dbg) ERROR: only numerics')
            case '*':
                if left_type in self.numtypes and right_type in self.numtypes:
                    return (dtype, left_val * right_val)
                else:
                    print('(semantic)(dbg) ERROR: only numerics')
            case '%':
                if dtype in ['float', 'double']:
                    print('(semantic)(dbg) ERROR : MODULO FLOATING POINT')
                else:
                    if left_type in self.numtypes and right_type in self.numtypes:
                        return (dtype, left_val % right_val)
                    else:
                        print('(semantic)(dbg) ERROR: only numerics')

            #relational
            case '==':
                if left_type in self.numtypes:
                    if right_type not in self.numtypes:
                        print('(semantic)(dbg) ERROR: comparison with numeric can only be with another numeric')
                elif left_type == 'string':
                    if right_type != 'string':
                        print('(semantic)(dbg) ERROR: comparisong with string can only be with another string')
                elif left_type == 'bool':
                    if right_type != 'bool':
                        print('(semantic)(dbg) ERROR: comparisong with bool can only be with another bool')
                return ('bool', left_val == right_val)
            
            case '!=':
                if left_type in self.numtypes:
                    if right_type not in self.numtypes:
                        print('(semantic)(dbg) ERROR: comparison with numeric can only be with another numeric')
                elif left_type == 'string':
                    if right_type != 'string':
                        print('(semantic)(dbg) ERROR: comparisong with string can only be with another string')
                elif left_type == 'bool':
                    if right_type != 'bool':
                        print('(semantic)(dbg) ERROR: comparisong with bool can only be with another bool')
                return ('bool', left_val != right_val)
            
            case '<':
                if left_type not in self.numtypes or right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: only numerics allowed')

                return ('bool', left_val < right_val)  
            case '<=':
                if left_type not in self.numtypes or right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: only numerics allowed')

                return ('bool', left_val <= right_val)  
            case '>':
                if left_type not in self.numtypes or right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: only numerics allowed')

                return ('bool', left_val > right_val)  
            case '>=':
                if left_type not in self.numtypes or right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: only numerics allowed')

                return ('bool', left_val >= right_val)  
            
            #logical
            case '&&':
                if left_type != 'bool' or right_type != 'bool':
                    print('(semantic)(dbg) ERROR: booleans only!!')

                return ('bool', left_val and right_val)
            case '||':
                if left_type != 'bool' or right_type != 'bool':
                    print('(semantic)(dbg) ERROR: booleans only!!')

                return ('bool', left_val or right_val)

    #unary ops
    def visit_node_un_op(self, node):
        right_type, right_val = self.visit_node(node.id_right_n)
        match node.left_t["tokenName"]:
            case '!':
                if right_type != 'bool':
                    print('(semantic)(dbg) ERROR: only bool')
                return ('bool', not right_val)
            case '-':
                if right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: invalid data type')
                return (right_type, -right_val)
            case '++':
                if right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: invalid data type')
                self.curr_scope[node.id_right_n.id_n.id_t["tokenName"]] += 1
                return (right_type, right_val + 1)
            case '--':
                if right_type not in self.numtypes:
                    print('(semantic)(dbg) ERROR: invalid data type')
                self.curr_scope[node.id_right_n.id_n.id_t["tokenName"]] -= 1
                return (right_type, right_val - 1 )
        if node.left_t["tokenName"] in ["bool", "string", "int", "long", "double", "float"]:
            match node.left_t["tokenName"] :
                case 'bool':
                    match right_type:
                        case 'bool':
                            return ('int', right_val)
                        case 'string':
                            return ('bool', right_val != '')
                        case 'int':
                            return ('bool', right_val != 0)
                        case 'long':
                            return ('bool', right_val != 0)
                        case 'float':
                            return ('bool', right_val != 0.0)
                        case 'double':
                            return ('bool', right_val != 0.0)
                case 'string':
                    return ('string', str(right_val))
                case 'int':
                    match right_type:
                        case 'bool':
                            return ('int', int(right_val))
                        case 'string':
                            self.logError(f'Strings cannot be casted into integers.')
                        case 'int':
                            return ('int', right_val)
                        case 'long':
                            if right_val <= self.MAX_INT and right_val >= self.MIN_INT:
                                return ('int', right_val)
                            else:
                                self.logError(f'Value {right_val} is out of integer range.')
                        case 'float':
                            return ('int', int(right_val))
                        case 'double':
                            if int(right_val) <= self.MAX_INT and int(right_val) >= self.MIN_INT:
                                return ('int', right_val)
                            else:
                                self.logError(f'Value {right_val} is out of integer range.')
                case 'long':
                    match right_type:
                        case 'bool':
                            return ('long', int(right_val))
                        case 'string':
                            self.logError(f'Strings cannot be casted into long.')
                        case 'int':
                            return ('long', right_val)
                        case 'long':
                            return ('long', right_val)
                        case 'float':
                            return ('long', int(right_val))
                        case 'double':
                            return ('long', int(right_val))
                case 'float':
                    match right_type:
                        case 'bool':
                            return ('float', float(right_val))
                        case 'string':
                            self.logError(f'Strings cannot be casted into float.')
                        case 'int':
                            return ('float', float(right_val))
                        case 'long':
                            if right_val <= self.MAX_FLOAT and right_val >= self.MIN_FLOAT:
                                return ('float', float(right_val))
                            else:
                                self.logError(f'Value {right_val} is out of float range.')
                        case 'float':
                            return ('float', right_val)
                        case 'double':
                            if right_val <= self.MAX_FLOAT and right_val >= self.MIN_FLOAT:
                                return ('float', right_val)
                            else:
                                self.logError(f'Value {right_val} is out of float range.')
                case 'double':
                    match right_type:
                        case 'bool':
                            return ('double', float(right_val))
                        case 'string':
                            self.logError(f'Strings cannot be casted into double.')
                        case 'int':
                            return ('double', float(right_val))
                        case 'long':
                            return ('double', float(right_val))
                        case 'float':
                            return ('double', right_val)
                        case 'double':
                            return ('double', right_val)
                        
    def visit_node_loop_stmt(self, node):
        node_loop = node.loop_stmt_n
        loop_name = type(node_loop).__name__

        self.enter_scope(loop_name)
        if loop_name == 'node_forloop':    
            self.visit_node_vardec(node_loop.init_arg_n)
            loop_condition = self.visit_node(node_loop.condition_n.condition_value_n)
            if loop_condition[0] != 'bool':
                self.logError(f"Invalid data type for loop condition. Expected 'bool', but found '{loop_condition[0]}' instead.")
            print(f"(semantic)(dbg) FOUND CONDITION for {loop_name} -> {node_loop.condition_n.condition_value_n} = {self.visit_node(node_loop.condition_n.condition_value_n)}")
            self.visit_node(node_loop.inc_arg_n) 
            self.visit_node(node_loop.ctrl_stmt_body_n)

        elif loop_name == 'node_while' or loop_name == 'node_do':
            loop_condition = self.visit_node(node_loop.condition_n.condition_value_n)
            if loop_condition[0] != 'bool':
                self.logError(f"Invalid data type for loop condition. Expected 'bool', but found '{loop_condition[0]}' instead.")

            print(f"(semantic)(dbg) FOUND CONDITION for {loop_name} -> {node_loop.condition_n.condition_value_n} = {self.visit_node(node_loop.condition_n.condition_value_n)}")
            self.visit_node(node_loop.ctrl_stmt_body_n)

        elif loop_name == 'node_repeat':
            repeat_val_result = self.visit_node(node_loop.repeat_value_n)
            if repeat_val_result[0] not in ['int', 'long']:
                self.logError(f"Invalid data type for repeat value. Expected 'int' or 'long', but found '{repeat_val_result[0]}' instead.")
            print(f"(semantic)(dbg) FOUND REPEAT VALUE -> {node_loop.repeat_value_n} = {repeat_val_result}")
            self.visit_node(node_loop.ctrl_stmt_body_n)

        self.exit_scope(loop_name)

    # input
    def visit_node_input(self, node):
        expected_dtype = node.type_t["tokenName"]
        prompt_n = node.prompt_n
        count_n = node.count_n

        promp_text = ""
        if prompt_n:
            promp_type, promp_text = self.visit_node(prompt_n)
            if promp_type != "string":
                print("(semantic)(dbg) ERROR: Prompt must be a string")
                return None
        if count_n:
            count_type, count = self.visit_node(count_n)
            if count_type not in ["int", "long"]:
                print("(semantic)(dbg) ERROR: Count must be an integer or long")
                return None
            if count <= 0:
                print("(semantic)(dbg) ERROR: Count must be greater than 0")
                return None
            
        user_input = input(promp_text)

        try:
            if expected_dtype == 'int':
                value = int(user_input) 
            elif expected_dtype == 'long':
                value = int(user_input)
            elif expected_dtype == 'float':
                value = float(user_input)
            elif expected_dtype == 'double':
                value = float(user_input)
            elif expected_dtype == 'string':
                value = user_input
            elif expected_dtype == 'bool':
                value = user_input.lower() == 'true'
            else:
                print("(semantic)(dbg) ERROR: Unsupported data type for input")
                return None
        except ValueError:
            print("(semantic)(dbg) ERROR: Input does not match expected data type")
            return None
        
        if count_n:
           _, count = self.visit_node(count_n) 
           if not isinstance(count, int) or count <= 0:
               print("(semantic)(dbg) ERROR: Invalid count for input")
               return None
           
        return (expected_dtype, value)
    
    # def visit_node_output(self, node):
    #     print_stmts_n = node.print_stmts_n
    #     print_params_n = node.print_params_n

    #     output_values = []
    #     for param in print_params_n:
    #         _, value = self.visit_node(param)
    #         output_values.append(str(value))

    #     output_text = " ".join(output_values)

    #     if print_stmts_n == "println":
    #         print(output_text)
    #     else:
    #         print(output_text, end='')
 
    #     return None

    
    #code block
    # def visit_code_block(self, node, isVoid=False):
    #     statements_n = node.code_block_statement_n  
    #     self.enter_scope()

    #     for stmt in statements_n:
    #         if isinstance(stmt, str):  
    #             self.visit_ctrl_stmt(stmt)
    #         elif isinstance(stmt, node_iden): 
    #             self.visit_var_decl(stmt)
    #         elif isinstance(stmt, node_pre_un_op):  
    #             self.visit_pre_un_op(stmt)
    #         elif isinstance(stmt, node_output):  
    #             self.visit_output(stmt)
    #         elif isinstance(stmt, node_conditional_stmt):  
    #             self.visit_conditional_stmt(stmt)
    #         elif isinstance(stmt, node_loop_stmt): 
    #             self.visit_loop_stmt(stmt)
    #         elif isinstance(stmt, node_code_block):  
    #             self.visit_code_block(stmt, isVoid)
    #         else:
    #             print("(semantic)(dbg) ERROR: Unrecognized statement type inside code block.")
        
    #     self.exit_scope()