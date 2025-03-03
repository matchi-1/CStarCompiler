from syntax_analyzer import node_body, node_code_block, node_if_stmt, node_loop_stmt, node_switch_stmt, node_case_stmt, node_default_stmt, node_return_block

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
        return {sym_name: sym_content}

    def set_array(self, sym_name, value, dtype, arr_info, priv=False, const=False):
        sym_content = self._create_symbol_entry(value, dtype, priv, const)
        sym_content["arr_info"] = arr_info  
        self.syms[sym_name] = sym_content

    def set_class(self, sym_name, class_info):
        sym_content = {}
        sym_content["class_info"] = class_info 
        self.syms[sym_name] = sym_content

    def set_obj(self, sym_name, initVal, class_name):
        sym_content = {}
        sym_content["init_val"] = initVal
        sym_content["dtype"] = class_name 
        self.syms[sym_name] = sym_content

    def set_function(self, sym_name, return_type, param_types, priv=False, isStd_lib=False):
        # sym_content = self._create_symbol_entry(value=None, dtype=return_type, priv=priv, const=const)
        #removed const from functions, prolly not needed (????)
        sym_content = {}
        sym_content["value"] = None #prolly needed in the future when we implement returning actual value
        sym_content["dtype"] = return_type
        sym_content["priv"] = priv
        sym_content["params"] = param_types 
        sym_content["isStd_lib"] = isStd_lib 
        self.syms[sym_name] = sym_content
        return {sym_name: sym_content}
    
    
    def set_constructor(self, sym_name, param_types):
        sym_content = {}
        sym_content["params"] = param_types
        self.syms[sym_name] = sym_content
        return {sym_name: sym_content}
    
    def print_symbol_tree(self, indent=0):
        """Recursively prints the symbol table from the current scope up to the root."""
        print("\t" * indent + f"Scope Level {indent}: {self.syms}")

        if self.parent:
            self.parent.print_symbol_tree(indent + 1)  # Move up the tree

class SemanticAnalyzer:

    numtypes = ['int', 'long', 'float', 'double']
   
    MIN_INT =       -   2147483648
    MAX_INT =           2147483647
    MIN_LONG =      -   9223372036854775808
    MAX_LONG =          9223372036854775807
    MIN_FLOAT =     -   999999990.0
    MAX_FLOAT =         999999990
    MIN_DOUBLE =    -   9999999999999999000
    MAX_DOUBLE =        9999999999999999000

    def interpret(self, node):
        try:
            self.visit_node(node)
            self.errors.append("Semantic analysis completed successfully. No Semantic Errors found.")
            print("Semantic checking completed successfully. No Semantic Errors found.")
            #print('(semantic)(dbg) global table: ')
            #print global dbg #wont be seen until prog construts is implemented
            for s in self.curr_scope.syms:
                print(f'\t\t{s} : {self.curr_scope.syms[s]}')
        except SyntaxError as e:
            print (e)

        return self.errors

    def __init__(self):
        self.curr_scope = SymbolTable()
        self.errors = []
        self.loop_depth = 0
        self.switch_depth = 0
        self.function_return_stack = []

    def enter_scope(self, nodeName):
        print(F'\n(semantic)(dbg) ENTERING scope {nodeName}')
        self.curr_scope = SymbolTable(self.curr_scope)
    
    def exit_scope(self, nodeName):
        print(F'\n(semantic)(dbg) EXITING scope {nodeName}, table: ')
        #print table dbg
        self.print_symbols(self.curr_scope.syms, indent=2)
        self.curr_scope = self.curr_scope.parent

    def visit_node(self, node):
        nodeName = type(node).__name__
        visit_func = getattr(self, f'visit_{nodeName}', None)  # Get the appropriate visit function, or None if it doesn't exist

        if visit_func is None:
            print(f"\n(semantic)(dbg) Not implemented yet!!!!!!!!!!!!!!!!!! node name: {nodeName}")
        else:
            print(f'\n(semantic)(dbg) VISITING {nodeName}!!')
            return visit_func(node)
        
    def print_symbols(self, d, indent=2):
        """Recursively prints dictionaries with {} and lists with [] using proper indentation."""

        if isinstance(d, dict):
            if not d:
                print("\t" * indent + "{ }")  # Print {} for empty dictionary
                return

            for key, value in d.items():
                print("\t" * indent + f"{key} :", end=" ")

                if isinstance(value, dict):
                    print("{")  # Open brace for dictionary
                    self.print_symbols(value, indent + 1)  # Recursive call for nested dict
                    print("\t" * indent + "}")  # Closing brace

                elif isinstance(value, list):
                    if not value:
                        print("[ ]")  # Print [] for empty list
                    else:
                        print("[")  # Open bracket for list
                        for item in value:
                            if isinstance(item, dict):  # Fix indentation for dicts inside lists
                                self.print_symbols(item, indent + 1)
                            else:
                                print("\t" * (indent + 1) + str(item))
                        print("\t" * indent + "]")  # Closing bracket

                else:
                    print(value)  # Print primitive values

        elif isinstance(d, list):  # Handle standalone lists
            if not d:
                print("\t" * indent + "[ ]")  # Print [] for empty list
            else:
                print("\t" * indent + "[")  # Open bracket for list
                for item in d:
                    if isinstance(item, dict):  # Fix indentation for dicts inside lists
                        self.print_symbols(item, indent + 1)
                    else:
                        print("\t" * (indent + 1) + str(item))
                print("\t" * indent + "]")  # Closing bracket

        else:
            print(d)  # Print non-dictionary/list values





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
        #print(full_message)
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

        if node.body_codeblock_n:
            self.visit_node(node.body_codeblock_n)
        
        if node.return_stmt_n:
            self.visit_node(node.return_stmt_n)
        
        self.exit_scope(type(node).__name__)
        

    #code_block PLACEHODLER
    def visit_node_code_block(self, node):
        # PLACEHODLER!! idk if correct
        for statement in node.code_block_statement_n:
            #print("++++ CODE BLOCK STATEMENT: " + str(statement))
            self.visit_node(statement)
            print("\n(semantic)(dbg) CURRENT LOCAL SCOPE TABLE: ")
            self.print_symbols(self.curr_scope.syms, indent=2)
        
        
        

    def visit_node_program_constructs(self, node):
        self.enter_scope(type(node).__name__)
        
        for global_declarations in node.program_constructs_statement_n:
            if global_declarations:
                self.visit_node(global_declarations)

        print("\n(semantic)(dbg) DONE VISITNG scope 'node_program_constructs', GLOBAL TABLE: ")
        self.print_symbols(self.curr_scope.syms, indent=2)

        



    def visit_node_class_dec(self, node):
        className = node.class_id_n.id_t["tokenName"]

        if self.curr_scope.get(className, checkParent=False):
            self.logError(f"Class '{className}' is already declared.", node.class_id_n)
            return
        constructorInfo = None
        if node.constructor_dec_n: constructorInfo = self.visit_node_constructor_dec(node.constructor_dec_n) 
        self.visit_node_class_body(node.class_body_n, className, constructorInfo)



    def visit_node_constructor_dec(self, node): #TODO: be wary of return statements
        className = node.class_id_n.id_t["tokenName"]

        param_types = []
        if node.params_n: # if params_n isn't None
            for param in node.params_n:
                if type(param).__name__ == "node_funcpar_class":
                    param_types.append({
                        "type": "class",
                        "classname": param.class_id_n.id_t["tokenName"]
                    })  

                elif type(param).__name__ == "node_funcpar_arr":
                    param_types.append({
                        "type": "arr",
                        "dtype": param.dtype_t["tokenName"] if param.dtype_t else None,  # for any types
                        "dimension": param.arrdim_i if param.arrdim_i else None # for any dimensions
                    })  

                elif type(param).__name__ == "node_funcpar_var":
                    param_types.append({
                        "type": "var",
                        "dtype": param.dtype_t["tokenName"]
                    }) 

        # Ensure param_types is set to None if empty
        param_types = param_types if param_types else None
        constructorInfo = self.curr_scope.set_constructor(className, param_types)

        self.enter_scope(type(node).__name__)

        # Add parameters to new function scope
        if node.params_n:
            for param in node.params_n:
                param_name = param.id_n.id_t["tokenName"]

                # Check if parameter name is duplicated
                if self.curr_scope.get(param_name, checkParent=False):
                    self.logError(f"Parameter '{param_name}' is already declared in function '{className}'.", param.id_n)

                # Handle different parameter types properly
                if type(param).__name__ == "node_funcpar_class":
                    class_name = param.class_id_n.id_t["tokenName"]
                    self.curr_scope.set_class(param_name, class_info={"classname": class_name})

                elif type(param).__name__ == "node_funcpar_arr":
                    arr_dtype = param.dtype_t["tokenName"] if param.dtype_t else None,  # for any types -- std lib Carray
                    arr_dim = param.arrdim_i if param.arrdim_i else None   # for any dimensions -- std lib Carray

                    self.curr_scope.set_array(param_name, value=None, dtype=arr_dtype, arr_info={"dimension": arr_dim}, const=False)

                elif type(param).__name__ == "node_funcpar_var":
                    var_dtype = param.dtype_t["tokenName"]
                    self.curr_scope.set(param_name, value=None, dtype=var_dtype, const=False)


        # Visit function body
        # has_return = any(self.visit_node(stmt) for stmt in node.body_n)

        # # If function is non-void, ensure at least one return exists
        # if return_type != "void" and not has_return:
        #     self.logError(f"Function '{func_name}' must return a value of type '{return_type}'.", node.id_n)

        self.exit_scope(type(node).__name__)
        return constructorInfo


    def visit_node_class_body(self, node, className, constructorInfo):
        class_content = []
        
        if node.class_body_stmt_n:
            class_body_stmt = node.class_body_stmt_n
        
            #self.enter_scope(type(node).__name__)
            print(f"\n(semantic)(dbg) ENTERING scope 'Class: {className}'")
            self.curr_scope = SymbolTable(self.curr_scope)

            for class_body_stmt_n in class_body_stmt:
                priv = class_body_stmt_n.is_private_b
                vardec_n = class_body_stmt_n.vardec_n
                
                if type(vardec_n).__name__ == "node_vardec":
                    class_content.append(self.visit_node_vardec(vardec_n, priv))

                elif type(vardec_n).__name__ == "node_func_dec":
                    class_content.append(self.visit_node_func_dec(vardec_n, priv))

            # self.exit_scope(type(node).__name__)
            print(f"\n(semantic)(dbg) EXITING scope 'Class: {className}', SYMBOL TABLE: ")
            self.print_symbols(self.curr_scope.syms, indent=2)
            self.curr_scope = self.curr_scope.parent

        flattened = [item for sublist in class_content for item in sublist]
        merged_dict = {k: v for d in flattened for k, v in d.items()}
        self.curr_scope.set_class(className, class_info={"constructor_dec" : constructorInfo, "class_body_content": merged_dict})
        

    def visit_node_class_inst(self, node):
        class_id = node.class_id_n.id_t["tokenName"]
        class_inst_cont = node.class_instcont_n
        dtype = ('object', class_id)
        
        if not self.curr_scope.get(class_id, checkParent=True):
            self.logError(f"Class '{class_id}' definition not found.", node.class_id_n)

        if class_inst_cont:
            constructor_call_id = class_inst_cont.class_id_n.id_t["tokenName"]
            if constructor_call_id != class_id:
                self.logError(f"Constructor call must match class name. Expected '{class_id}', but found '{constructor_call_id}'.", class_inst_cont.class_id_n)

            #TODO: add params and to scope and custom scope hahahahahahahhahahajfdhkasdhflkjawdh;geiurswthnbjoernbiop;las

        self.curr_scope.set_obj(node.obj_id_n.id_t["tokenName"], None, dtype)



    def visit_node_class_att(self, node):
        obj_name = node.obj_id_n.id_t["tokenName"]
        class_elem = node.att_id_n.id_t["tokenName"]
        print(obj_name)

        obj_info = self.curr_scope.get(obj_name)
        if not obj_info:
            self.logError(f"'{obj_name}' object is not yet declared.", node.obj_id_n)

        class_info = self.curr_scope.parent.get(obj_info["dtype"][1])["class_info"]["class_body_content"]

        if class_elem not in class_info:
            self.logError(f"Attribute '{class_elem}' not found in '{obj_name}', instance of class '{obj_info["class_name"]}'.", node.att_id_n)
        print(class_info)
        print(class_elem)

        return (class_info[class_elem]["dtype"], None)   #None is TODO for code gen


    def visit_node_num(self, node):
        val = 0
        # if node.dtype in ['int', 'long']:
        #     val = int(node.val_t["tokenName"])
        # elif node.dtype in ['float', 'double']:
        #     val = float(node.val_t["tokenName"])
        # return (('var', node.dtype), val) 
        return (('lit', node.dtype), None)
    
    def visit_node_str(self, node):
        # return (('var', node.dtype), node.val_t["tokenName"][1:-1])
        return (('lit', node.dtype), None)
    
    def visit_node_bool(self, node):
        # return (node.dtype, node.val_t["tokenName"]=="true")
        return (('lit', node.dtype), None)
    
    def visit_node_iden(self, node):
        iden_symbol = self.curr_scope.get(node.id_t["tokenName"])
        if not iden_symbol:
            self.logError(f"Symbol '{node.id_t["tokenName"]}' hasn't been declared yet.", node)
        else:
            # dtype = iden_symbol["dtype"]
            # val = 0
            # if dtype in ['int', 'long']:
            #     val = int(iden_symbol["value"])
            # elif dtype in ['float', 'double']:
            #     val = float(iden_symbol["value"])
            # return (dtype, val)
            return (('var', iden_symbol["dtype"][1]), None)
        
    def visit_node_arr_idx(self, node):
        arr_sym = self.curr_scope.get(node.id_n.id_t["tokenName"])
        if arr_sym["dtype"][0] != 'arr':
            self.logError(f'Symbol {node.id_n.id_t["tokenName"]} is not an array.')
        dtype = arr_sym["dtype"][1]
        if node.idx2_n:
            if arr_sym["arr_info"]["dimension"] == 1:
                self.logError(f'Array {node.id_n.id_t["tokenName"]} only has 1 dimension.')
        else:
            if arr_sym["arr_info"]["dimension"] == 2:
                self.logError(f'Array {node.id_n.id_t["tokenName"]} has 2 dimensions.')
        return (('var', dtype), None) #for now, since seman
    #cont...

    def visit_node_func_dec(self, node, priv = False):
        func_name = node.id_n.id_t["tokenName"]
        return_type = node.dtype_t["tokenName"]

        # Check if function already exists in current scope
        if self.curr_scope.get(func_name, checkParent=False):
            self.logError(f"Function '{func_name}' is already declared.", node.id_n)
            return

        
        # Store func params into function signature in symbol table
        param_types = []

        if node.params_n: # if params_n isn't None
            for param in node.params_n:
                if type(param).__name__ == "node_funcpar_class":
                    class_name = param.class_id_n.id_t["tokenName"]
                    if not self.curr_scope.get(class_name):
                        self.logError(f"Class '{class_name}' hasnt been declared yet.", param.class_id_n)
                    param_types.append({
                        "type": "object",
                        "dtype": class_name,
                        "class_name": class_name
                    })  

                elif type(param).__name__ == "node_funcpar_arr":
                    param_types.append({
                        "type": "arr",
                        "dtype": param.dtype_t["tokenName"] if param.dtype_t else None,  # for any types
                        "dimension": param.arrdim_i if param.arrdim_i else None # for any dimensions
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

        # Ensure param_types is set to None if empty
        param_types = param_types if param_types else None

        print(f">>>>>>>>>>> {func_name} IS FUNC STD LIB? " + str(node.is_std_lib))

        classReturn = []
        # Store function in symbol table. (for classes only) also returns the resulting dict
        classReturn.append(self.curr_scope.set_function(func_name, return_type, param_types, priv, isStd_lib = node.is_std_lib))
        #add actual value param in da future


        # Enter function scope
        #self.enter_scope(type(node).__name__)
        print(f"\n(semantic)(dbg) ENTERING scope 'Function: {func_name}'")
        self.curr_scope = SymbolTable(self.curr_scope)

        # Add parameters to new function scope
        if node.params_n:
            for param in node.params_n:
                param_name = param.id_n.id_t["tokenName"]

                # Check if parameter name is duplicated
                if self.curr_scope.get(param_name, checkParent=False):
                    self.logError(f"Parameter '{param_name}' is already declared in function '{func_name}'.", param.id_n)

                # Handle different parameter types properly
                if type(param).__name__ == "node_funcpar_class":
                    class_name = ('object', param.class_id_n.id_t["tokenName"])
                    self.curr_scope.set_obj(param_name, None, class_name)

                elif type(param).__name__ == "node_funcpar_arr":
                    arr_dtype = ('arr', param.dtype_t["tokenName"]) if param.dtype_t else None  # for any types -- std lib Carray
                    arr_dim = param.arrdim_i if param.arrdim_i else None   # for any dimensions -- std lib Carray
                    self.curr_scope.set_array(param_name, value=None, dtype=arr_dtype, arr_info={"dimension": arr_dim}, const=False)

                elif type(param).__name__ == "node_funcpar_var":
                    var_dtype = ('var', param.dtype_t["tokenName"])
                    self.curr_scope.set(param_name, value=None, dtype=var_dtype, const=False)

        self.function_return_stack.append(return_type)
        print(f"Return stack = {self.function_return_stack}")
        
        # Visit function body
        has_return = self.check_return_in_body(node.body_n)
        self.visit_node(node.body_n)

        # Ensure non-void functions return a value
        if return_type != "void" and not has_return:
            self.logError(f"Function '{func_name}' must return a value of type '{return_type}'.")

        self.function_return_stack.pop()
        print(f"(semantic)(dbg) Popped return type, Stack after pop = {self.function_return_stack}")

        # Exit function scope, back to program constructs
        print(f"\n(semantic)(dbg) EXITING scope 'Function: {func_name}', SYMBOL TABLE: ")
        self.print_symbols(self.curr_scope.syms, indent=2)
        self.curr_scope = self.curr_scope.parent
        return classReturn

    # assign_stmt  -- need to refactor nodes in ast bc stephen :skull:
    def visit_node_assign_stmt_var(self, node):
        iden = node.id_n
        value = node.value_n
        iden_name = iden.id_t["tokenName"]
        iden_symbol = self.curr_scope.get(iden_name)
        if not iden_symbol:
            self.logError(f"Symbol '{iden_name}' hasn't been declared yet.", iden)
        if iden_symbol["const"]:
            self.logError(f"Symbol '{iden_name}' is a constant and cannot be reassigned.", iden)
        dtype = iden_symbol["dtype"]
        val_type, val = self.visit_node(value)
        if dtype != val_type:
            self.logError(f"Type mismatch: expected '{dtype}' but found '{val_type}'", iden)
        self.curr_scope.set(iden_name, val, dtype=dtype)

    def visit_node_assign_stmt_arr(self, node):
        iden = node.id_n
        value = node.value_n
        iden_name = iden.id_t["tokenName"]
        iden_symbol = self.curr_scope.get(iden_name)
        if not iden_symbol:
            self.logError(f"Symbol '{iden_name}' hasn't been declared yet.", iden)
        if iden_symbol["const"]:
            self.logError(f"Symbol '{iden_name}' is a constant and cannot be reassigned.", iden)
        dtype = iden_symbol["dtype"][4:]
        val_type, val = self.visit_node(value)
        if dtype != val_type:
            self.logError(f"Type mismatch: expected '{dtype}' but found '{val_type}'", iden)

        # Check dimensions
        if node.idx2_n:
            if iden_symbol["arr_info"]["dimension"] != 2:
                self.logError(f"Array '{iden_name}' is not 2-dimensional.", iden)
            idx1_type, idx1_val = self.visit_node(node.idx1_n)
            idx2_type, idx2_val = self.visit_node(node.idx2_n)
            if idx1_type not in ['int', 'long'] or idx2_type not in ['int', 'long']:
                self.logError(f"Array indices must be of type 'int' or 'long'.", iden)
            if idx1_val >= iden_symbol["arr_info"]["size1"] or idx2_val >= iden_symbol["arr_info"]["size2"]:  # this wont work for expressions yet
                self.logError(f"Array index out of bounds.", iden)
        else:
            if iden_symbol["arr_info"]["dimension"] != 1:
                self.logError(f"Array '{iden_name}' is not 1-dimensional.", iden)
            idx1_type, idx1_val = self.visit_node(node.idx1_n)
            if idx1_type not in ['int', 'long']:
                self.logError(f"Array index must be of type 'int' or 'long", iden)
            if idx1_val >= iden_symbol["arr_info"]["size1"]:
                self.logError(f"Array index out of bounds.", iden)
        


    # func calls
    def visit_node_func_call(self, node):
        func_name = node.id_n.id_t["tokenName"]
        func_symbol = self.curr_scope.get(func_name)
        if not func_symbol:
            self.logError(f"Function '{func_name}' hasn't been declared yet.", node.id_n)
        
        if func_symbol["params"]:
            if len(func_symbol["params"]) != len(node.args_n):
                param_count = len(func_symbol['params'])
                self.logError(f"Function '{func_name}' expects {param_count} parameter{'s' if param_count > 1 else ''} but got {len(node.args_n)}.", node.id_n)
            for arg_node, param_type in zip(node.args_n, func_symbol["params"]):
                arg_val_type, arg_val = self.visit_node(arg_node)
                print(">>>>>>>>>>>>>>>>>>>>>> arg_val_type: " + str(arg_val_type))
                print(">>>>>>>>>>>>>>>>>>>>>> param_type: " + str(param_type))
                print(">>>>>>>>>>>>>>>>>>>>>> arg_val: " + str(arg_val))
                print(">>>>>>>>>>>>>>>>>>>>>> arg_node: " + str(arg_node))
                
                if arg_val_type[0] in ["var", "lit"]:
                    if arg_val_type[1] != param_type["dtype"]:
                        self.logError(f"Type mismatch for function call of '{func_name}' parameter: expected '{param_type['dtype']}' but found '{arg_val_type[1]}'", None)
                
                elif arg_val_type[0] == "arr":
                    if arg_val_type[1] != param_type["dtype"]:
                        self.logError(f"Type mismatch for function '{func_name}' parameters: expected array of '{param_type['dtype']}' but found '{arg_val_type[1]}'", None)
                    elif arg_node.dimension != param_type["dimension"]:
                        self.logError(f"Dimension mismatch for function call of '{func_name}' parameter: expected {param_type['dimension']} dimensions but found {arg_node.dimension}", None)
                
                elif arg_val_type[0] == "object":
                    if arg_val_type[1] != param_type["class_name"]:
                        self.logError(f"Type mismatch for function call of '{func_name}' parameter: expected instance of class '{param_type['class_name']}' but found '{arg_val_type[1]}'", None)
                
                else:
                    self.logError(f"Unknown parameter type for function '{func_name}' parameter: '{param_type['dtype']}'", None)
        else:
            if node.args_n:
                self.logError(f"Function '{func_name}' does not take any parameters.", node.id_n)

        return (func_symbol["dtype"], None) 


    #var_dec
    def visit_node_vardec(self, node, priv = False):
        if self.curr_scope.get(node.id_n.id_t["tokenName"], False):
            self.logError(f"Symbol '{node.id_n.id_t["tokenName"]}' has already been declared.", node.id_n)
        const = node.const_b
        dtype = ('var', node.dtype_t["tokenName"])
        id = node.id_n.id_t["tokenName"]
        val_type = None
        value = None
        idec_rec = None
        if (node.vardec_cont_n):
            if node.vardec_cont_n.value_n:
                val_type, value = self.visit_node(node.vardec_cont_n.value_n)
            print('(semantic)(dbg) dec valtype: ', val_type[1])
            idec_rec = node.vardec_cont_n.idec_rec_n
                    
        if val_type and dtype[1] != val_type[1]:
            if dtype[1] not in ['float', 'double'] or val_type not in ['int', 'long']:
                self.logError(f"Type mismatch: expected '{dtype[1]}' but found '{val_type[1]}'", node.id_n)
        # if not value:
        #     match dtype:
        #         case 'bool':
        #             value = False
        #         case 'int':
        #             value = 0
        #         case 'long':
        #             value = 0
        #         case 'float':
        #             value = 0.0
        #         case 'double':
        #             value = 0.0
        #         case 'string':
        #             value = ''
        classReturn = []
        classReturn.append(self.curr_scope.set(id, value, dtype=dtype, priv = priv, const=const))
        for dec_node in idec_rec or []:
            classReturn.append(self.curr_scope.set(dec_node.id_n.id_t["tokenName"], self.visit_node(dec_node.value_n) if dec_node.value_n else None, dtype=dtype, priv = priv, const=const))

        return classReturn

    #array declaration
    def visit_node_arr_dec(self, node):
        id = node.id_n.id_t["tokenName"]
        if self.curr_scope.get(id, checkParent=False):
            self.logError(f"Symbol '{id}' has already been declared.", node.id_n)
        dtype = ('arr', node.dtype_t["tokenName"])
        dim = 2 if node.size2_n else 1
        size_1_type, size_1 = self.visit_node(node.size1_n)
        if size_1_type[1] not in ['int', 'long']:
            self.logError('Expected whole number.')
        size_2_type, size_2 = self.visit_node(node.size2_n) if node.size2_n else (None, None)
        if size_2_type and size_2_type[1] not in ['int', 'long']:
            self.logError('Expected whole number.')
        values_list = None
        arr_rec = None
        if node.arr_dec_cont_n:
            if type(node.arr_dec_cont_n[0]).__name__ == "node_arr_dec_rec":
                arr_rec = node.arr_dec_cont_n
            else:
                values_list = node.arr_dec_cont_n
        arr_vals = []
        if dim == 1:
            for value_node in values_list or []:
                val_type, val = self.visit_node(value_node)
                print(f'arr init valtype: {val_type[1]}')
                #error for arr size in code gen
                if val_type[1] != node.dtype_t["tokenName"]:
                    self.logError(f'Array contents can only be of type \'{node.dtype_t["tokenName"]}\'')
                else:
                    arr_vals.append(val)
        else:
            for inner_arr in values_list or []:
                temp_arr = []
                for value_node in inner_arr or []:
                    val_type, val = self.visit_node(value_node)
                    print(f'arr init valtype: {val_type[1]}')
                    #error for arr size in code gen
                    if val_type[1] != node.dtype_t["tokenName"]:
                        self.logError(f'Array contents can only be of type {node.dtype_t["tokenName"]}')
                    else:
                        temp_arr.append(val)
                arr_vals.append(temp_arr)
        self.curr_scope.set_array(id, arr_vals, dtype=dtype, arr_info={'dimension': dim, 'size1': size_1, 'size2':size_2})
        for arrdec_node in arr_rec or []:
            size_1_type, size_1 = self.visit_node(arrdec_node.size1_n)
            if size_1_type[1] not in ['int', 'long']:
                self.logError('Expected whole number.')
            size_2_type, size_2 = self.visit_node(arrdec_node.size2_n) if node.size2_n else (None, None)
            if size_2_type and size_2_type[1] not in ['int', 'long']:
                self.logError('Expected whole number.')
            if self.curr_scope.get(arrdec_node.id_n.id_t["tokenName"], checkParent=False):
                self.logError(f"Symbol '{arrdec_node.id_n.id_t["tokenName"]}' has already been declared.", node.id_n)
            self.curr_scope.set_array(arrdec_node.id_n.id_t["tokenName"], None, dtype=dtype, arr_info={'dimension': dim, 'size1': size_1, 'size2':size_2})
        

    # binary and unary operations
    def visit_node_bi_op(self, node):
        
        left_type, left_val = self.visit_node(node.left_n)
        right_type, right_val = self.visit_node(node.right_n)
        dtype = ('lit', 'int')
        if (left_type[1] == 'long' or right_type[1] == 'long'):
            dtype = ('lit', 'long')
        if (left_type[1] == 'float' or right_type[1] == 'float'):
            dtype = ('lit', 'float')
        if (left_type[1] == 'double' or right_type[1] == 'double'):
            dtype = ('lit', 'double')
        match node.op_t["tokenName"]:
            case '+': 
                if left_type[1] == 'string':
                    if right_type[1] != 'string':
                        print('(semantic)(dbg) ERROR: string exp only strings')
                    else:
                        # return ('string', left_val + right_val)
                        return (('lit', 'string'), None)
                elif left_type[1] in self.numtypes and right_type[1] in self.numtypes:
                    # return (dtype, left_val + right_val)
                    return (dtype, None)
                else:
                     print('(semantic)(dbg) ERROR: only numerics')

            case '-':
                if left_type[1] in self.numtypes and right_type[1] in self.numtypes:
                    # return (dtype, left_val - right_val)
                    return (dtype, None)
                else:
                    print('(semantic)(dbg) ERROR: only numerics')
            case '/':
                if right_val == 0: #todo
                    print("(semantic)(dbg) ERROR: DIVIDE BY 0")
                if left_type[1] in self.numtypes and right_type[1] in self.numtypes:
                    # return (dtype, left_val / right_val)
                    return (dtype, None)
                else:
                    print('(semantic)(dbg) ERROR: only numerics')
            case '*':
                if left_type[1] in self.numtypes and right_type[1] in self.numtypes:
                    # return (dtype, left_val * right_val)
                    return (dtype, None)
                else:
                    print('(semantic)(dbg) ERROR: only numerics')
            case '%':
                if dtype[1] in ['float', 'double']:
                    print('(semantic)(dbg) ERROR : MODULO FLOATING POINT')
                else:
                    if left_type[1] in self.numtypes and right_type[1] in self.numtypes:
                        # return (dtype, left_val % right_val)
                        return (dtype, None)
                    else:
                        print('(semantic)(dbg) ERROR: only numerics')

            #relational
            case '==':
                if left_type[1] in self.numtypes:
                    if right_type[1] not in self.numtypes:
                        print('(semantic)(dbg) ERROR: comparison with numeric can only be with another numeric')
                elif left_type[1] == 'string':
                    if right_type[1] != 'string':
                        print('(semantic)(dbg) ERROR: comparisong with string can only be with another string')
                elif left_type[1] == 'bool':
                    if right_type[1] != 'bool':
                        print('(semantic)(dbg) ERROR: comparisong with bool can only be with another bool')
                # return ('bool', left_val == right_val)
                return (('lit', 'bool'), None)
            
            case '!=':
                if left_type[1] in self.numtypes:
                    if right_type[1] not in self.numtypes:
                        print('(semantic)(dbg) ERROR: comparison with numeric can only be with another numeric')
                elif left_type[1] == 'string':
                    if right_type[1] != 'string':
                        print('(semantic)(dbg) ERROR: comparisong with string can only be with another string')
                elif left_type[1] == 'bool':
                    if right_type[1] != 'bool':
                        print('(semantic)(dbg) ERROR: comparisong with bool can only be with another bool')
                # return ('bool', left_val != right_val)
                return (('lit', 'bool'), None)
            
            case '<':
                if left_type[1] not in self.numtypes or right_type[1] not in self.numtypes:
                    print('(semantic)(dbg) ERROR: only numerics allowed')

                # return ('bool', left_val < right_val)  
                return (('lit', 'bool'), None)
            case '<=':
                if left_type[1] not in self.numtypes or right_type[1] not in self.numtypes:
                    print('(semantic)(dbg) ERROR: only numerics allowed')

                # return ('bool', left_val <= right_val)  
                return (('lit', 'bool'), None)
            case '>':
                if left_type[1] not in self.numtypes or right_type[1] not in self.numtypes:
                    print('(semantic)(dbg) ERROR: only numerics allowed')

                # return ('bool', left_val > right_val)  
                return (('lit', 'bool'), None)
            case '>=':
                if left_type[1] not in self.numtypes or right_type[1] not in self.numtypes:
                    print('(semantic)(dbg) ERROR: only numerics allowed')

                # return ('bool', left_val >= right_val)  
                return (('lit', 'bool'), None)
            
            #logical
            case '&&':
                if left_type[1] != 'bool' or right_type[1] != 'bool':
                    print('(semantic)(dbg) ERROR: booleans only!!')

                # return ('bool', left_val and right_val)
                return (('lit', 'bool'), None)
            case '||':
                if left_type[1] != 'bool' or right_type[1] != 'bool':
                    print('(semantic)(dbg) ERROR: booleans only!!')

                # return ('bool', left_val or right_val)
                return (('lit', 'bool'), None)

    #unary ops
    def visit_node_un_op(self, node):
        right_type, right_val = self.visit_node(node.id_right_n)
        match node.left_t["tokenName"]:
            case '!':
                if right_type[1] != 'bool':
                    print('(semantic)(dbg) ERROR: only bool')
                # return ('bool', not right_val)
                return (('lit', 'bool'), None)
            case '-':
                if right_type[1] not in self.numtypes:
                    print('(semantic)(dbg) ERROR: invalid data type')
                # return (right_type, -right_val)
                return (right_type, None)
            case '++':
                if right_type[1] not in self.numtypes:
                    print('(semantic)(dbg) ERROR: invalid data type')
                # self.curr_scope[node.id_right_n.id_n.id_t["tokenName"]] += 1
                # return (right_type, right_val + 1)
                return (right_type, None)
            case '--':
                if right_type[1] not in self.numtypes:
                    print('(semantic)(dbg) ERROR: invalid data type')
                # self.curr_scope[node.id_right_n.id_n.id_t["tokenName"]] -= 1
                # return (right_type, right_val - 1 )
                return (right_type, None)
        if node.left_t["tokenName"] in ["bool", "string", "int", "long", "double", "float"]:
            if right_type[1] not in ["bool", "string", "int", "long", "double", "float"]:
                self.logError(f'{node.id_right_n.id_t["tokenName"]} cannot be typecasted.')
            match node.left_t["tokenName"] :
                case 'bool':
                    # match right_type:
                    #     case 'bool':
                    #         return ('bool', right_val)
                    #     case 'string':
                    #         return ('bool', right_val != '')
                    #     case 'int':
                    #         return ('bool', right_val != 0)
                    #     case 'long':
                    #         return ('bool', right_val != 0)
                    #     case 'float':
                    #         return ('bool', right_val != 0.0)
                    #     case 'double':
                    #         return ('bool', right_val != 0.0)
                    return (('lit', 'bool'), None)
                case 'string':
                    # return ('string', str(right_val))
                    return (('lit', 'string',), None)
                case 'int':
                    match right_type[1]:
                        # case 'bool':
                        #     return ('int', int(right_val))
                        case 'string':
                            self.logError(f'Strings cannot be casted into integers.')
                        case _:
                            return (('lit', 'int'), None)
                        # case 'int':
                        #     return ('int', right_val)
                        # case 'long':
                        #     if right_val <= self.MAX_INT and right_val >= self.MIN_INT:
                        #         return ('int', right_val)
                        #     else:
                        #         self.logError(f'Value {right_val} is out of integer range.')
                        # case 'float':
                        #     return ('int', int(right_val))
                        # case 'double':
                        #     if int(right_val) <= self.MAX_INT and int(right_val) >= self.MIN_INT:
                        #         return ('int', right_val)
                        #     else:
                        #         self.logError(f'Value {right_val} is out of integer range.')
                case 'long':
                    match right_type[1]:
                        # case 'bool':
                        #     return ('long', int(right_val))
                        case 'string':
                            self.logError(f'Strings cannot be casted into long.')
                        case _:
                            return (('lit', 'long'), None)
                        # case 'int':
                        #     return ('long', right_val)
                        # case 'long':
                        #     return ('long', right_val)
                        # case 'float':
                        #     return ('long', int(right_val))
                        # case 'double':
                        #     return ('long', int(right_val))
                case 'float':
                    match right_type[1]:
                        # case 'bool':
                        #     return ('float', float(right_val))
                        case 'string':
                            self.logError(f'Strings cannot be casted into float.')
                        case _:
                            return (('lit', 'float'), None)
                        # case 'int':
                        #     return ('float', float(right_val))
                        # case 'long':
                        #     if right_val <= self.MAX_FLOAT and right_val >= self.MIN_FLOAT:
                        #         return ('float', float(right_val))
                        #     else:
                        #         self.logError(f'Value {right_val} is out of float range.')
                        # case 'float':
                        #     return ('float', right_val)
                        # case 'double':
                        #     if right_val <= self.MAX_FLOAT and right_val >= self.MIN_FLOAT:
                        #         return ('float', right_val)
                        #     else:
                        #         self.logError(f'Value {right_val} is out of float range.')
                case 'double':
                    match right_type[1]:
                        # case 'bool':
                        #     return ('double', float(right_val))
                        case 'string':
                            self.logError(f'Strings cannot be casted into double.')
                        case _:
                            return (('lit', 'double'), None)
                        # case 'int':
                        #     return ('double', float(right_val))
                        # case 'long':
                        #     return ('double', float(right_val))
                        # case 'float':
                        #     return ('double', right_val)
                        # case 'double':
                        #     return ('double', right_val)
                    
    def visit_node_loop_stmt(self, node):
        node_loop = node.loop_stmt_n
        loop_name = type(node_loop).__name__
        self.loop_depth += 1

        self.enter_scope(loop_name)
        if loop_name == 'node_forloop':    
            self.visit_node(node_loop.init_arg_n)
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

        self.loop_depth -= 1
        self.exit_scope(loop_name)

    # input
    # def visit_node_input(self, node):
    #     expected_dtype = node.type_t["tokenName"]
    #     prompt_n = node.prompt_n
    #     count_n = node.count_n

    #     promp_text = ""
    #     if prompt_n:
    #         promp_type, promp_text = self.visit_node(prompt_n)
    #         if promp_type != "string":
    #             print("(semantic)(dbg) ERROR: Prompt must be a string")
    #             return None
    #     if count_n:
    #         count_type, count = self.visit_node(count_n)
    #         if count_type not in ["int", "long"]:
    #             print("(semantic)(dbg) ERROR: Count must be an integer or long")
    #             return None
    #         if count <= 0:
    #             print("(semantic)(dbg) ERROR: Count must be greater than 0")
    #             return None
            
    #     user_input = input(promp_text)

    #     try:
    #         if expected_dtype == 'int':
    #             value = int(user_input) 
    #         elif expected_dtype == 'long':
    #             value = int(user_input)
    #         elif expected_dtype == 'float':
    #             value = float(user_input)
    #         elif expected_dtype == 'double':
    #             value = float(user_input)
    #         elif expected_dtype == 'string':
    #             value = user_input
    #         elif expected_dtype == 'bool':
    #             value = user_input.lower() == 'true'
    #         else:
    #             print("(semantic)(dbg) ERROR: Unsupported data type for input")
    #             return None
    #     except ValueError:
    #         print("(semantic)(dbg) ERROR: Input does not match expected data type")
    #         return None
        
    #     if count_n:
    #        _, count = self.visit_node(count_n) 
    #        if not isinstance(count, int) or count <= 0:
    #            print("(semantic)(dbg) ERROR: Invalid count for input")
    #            return None
           
    #     return (expected_dtype, value)
    def visit_node_input(self, node):
        if not hasattr(node, 'type_t'):
            self.logError("Input node is missing the 'type_t' attribute.", node)
            return None

        expected_dtype = node.type_t["tokenName"] 


        print(f"(semantic)(dbg) Expected Data Type: {expected_dtype}")


        if expected_dtype not in ["int", "long", "float", "double", "string", "bool"]:
            self.logError(f"Unsupported data type for input: {expected_dtype}", node)
            return None

        return (('lit', expected_dtype), None)
    
    # def visit_node_output(self, node):
    #     print_stmts_n = node.print_stmts_n 
    #     print_params_n = node.print_params_n  

    #     if not print_params_n:
    #         self.logError("Output statement requires at least one parameter (format string).")
    #         return None
    #     format_string_node = print_params_n[0]
    #     format_string_type, format_string_value = self.visit_node(format_string_node)


    #     if format_string_type != "string":
    #         self.logError("First parameter in output statement must be a string (format string).", format_string_node)
    #         return None

    #     format_specifiers = self._extract_format_specifiers(format_string_value)

    #     if len(format_specifiers) != len(print_params_n) - 1:
    #         self.logError(f"Number of format specifiers ({len(format_specifiers)}) does not match number of parameters ({len(print_params_n) - 1}).", format_string_node)
    #         return None

    #     formatted_output = format_string_value
    #     for i, specifier in enumerate(format_specifiers):
    #         param_node = print_params_n[i + 1] 
    #         param_type, param_value = self.visit_node(param_node)

        
    #         if not self._validate_format_specifier(specifier, param_type):
    #             self.logError(f"Format specifier '{specifier}' does not match parameter type '{param_type}'.", param_node)
    #             return None
    #         formatted_output = formatted_output.replace(specifier, str(param_value), 1)

    #     if print_stmts_n == "println":
    #         print(formatted_output)
    #     else:
    #         print(formatted_output, end='')

    #     return None

    # def _extract_format_specifiers(self, format_string):
    #     import re
    #     return re.findall(r'%[sdf]|%l[df]', format_string)  # matches %s, %d, %f, %ld, %lf

    # def _validate_format_specifier(self, specifier, param_type):
    #     if specifier == "%s":
    #         return param_type == "string"
    #     elif specifier == "%d":
    #         return param_type == "int"
    #     elif specifier == "%ld":
    #         return param_type == "long"
    #     elif specifier == "%f":
    #         return param_type == "float"
    #     elif specifier == "%lf":
    #         return param_type == "double"
    #     else:
    #         return False
    def visit_node_output(self, node):
        print_stmts_n = node.print_stmts_n 
        print_params_n = node.print_params_n  

        if not print_params_n:
            self.logError("Output statement requires at least one parameter.", node)
            return None

        format_string_node = print_params_n[0]
        format_string_type, _ = self.visit_node(format_string_node)

        if format_string_type != "string":
            self.logError("First parameter in output statement must be a string.", format_string_node)
            return None
        return None
    
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
    
    # ALEX HERE
    def visit_node_ctrl_stmt_body(self, node):
        self.enter_scope(type(node).__name__)
        statements_n = node.statements_n
        
        for statement in statements_n:
            ctrl_stmt = type(statement).__name__

            if ctrl_stmt == "node_break_stmt":
                if self.loop_depth == 0 and self.switch_depth == 0:
                    self.logError("'break' statements may only be used within the scope of 'loop' and 'switch' statements.")
                print("(semantic)(dbg) FOUND 'break' !!!")
                continue
            
            elif ctrl_stmt == "node_continue_stmt":
                if self.loop_depth == 0 and self.switch_depth == 0:
                    self.logError("'continue' statements may only be used within the scope of 'loop' and 'switch' statements.")
                print("(semantic)(dbg) FOUND 'continue' !!!")
                continue
            
            else:
                self.visit_node(statement)

        print("(semantic)(dbg) EXITING scope 'ctrl_stmt_body', TABLE: ")
        self.exit_scope(type(node).__name__)

        return

    def visit_node_if_stmt(self, node):
        self.enter_scope(type(node).__name__)

        if_condition = self.visit_node(node.condition_n.condition_value_n)
        
        if if_condition[0] != 'bool':
            self.logError(f"Invalid data type for loop condition. Expected 'bool', but found '{if_condition[0]}' instead.")
        print(f"(semantic)(dbg) FOUND CONDITION for {type(node).__name__} -> {node.condition_n.condition_value_n} = {self.visit_node(node.condition_n.condition_value_n)}")
        
        if node.body_n:
            self.visit_node(node.body_n)

        if node.else_chain_n:
            self.visit_node(node.else_chain_n)

        self.exit_scope(type(node).__name__)
        return
    
    def visit_node_else_chain(self, node):
        self.enter_scope(type(node).__name__)

        else_chain_n = node.else_chain_n

        for chain_stmt in else_chain_n:
            chain_type = type(chain_stmt).__name__

            print(f"CHAAAAAAAAINNNNNNNN TYPE: {chain_type}")
            self.visit_node(chain_stmt)

        self.exit_scope(type(node).__name__)
        return

    def visit_node_else_stmt(self, node):
        self.enter_scope(type(node).__name__)

        if node.body_n:
            self.visit_node(node.body_n)

        self.exit_scope(type(node).__name__)
        return
    
    def visit_node_switch_stmt(self, node):
        self.enter_scope(type(node).__name__)
        self.switch_depth += 1
        
        switch_value = self.visit_node(node.value_n)
        if switch_value[0] not in ["string", "int", "long"]:
            self.logError("Invalid data type for 'switch' value. Expected: 'string', 'int', 'long' data types.")
        
        # CASE
        case_n = node.case_n

        for case_stmt in case_n.case_stmt_n:

            self.enter_scope(case_stmt)
            case_value_type = case_stmt.case_value_n
            case_value = self.visit_node(case_value_type)
            print(f"(semantic)(dbg) FOUND 'case_value'")
            
            if case_value[0] != switch_value[0]:
                self.logError(f"'switch' value and 'case' value must be of same data type. Expected: '{switch_value[0]}' data type for case value.")

            if case_stmt.ctrl_stmt_body_n:
                self.visit_node(case_stmt.ctrl_stmt_body_n)

            print(f"(semantic)(dbg) FOUND 'case_body'")
            self.exit_scope(case_stmt)
            
        
        # DEFAULT
        default_stmt = node.default_n

        if default_stmt:
            self.enter_scope(default_stmt)
            
            if default_stmt.ctrl_stmt_body_n:
                self.visit_node(default_stmt.ctrl_stmt_body_n)
                print(f"(semantic)(dbg) FOUND 'default_body'")

            self.exit_scope(default_stmt)

        self.switch_depth -= 1
        self.exit_scope(type(node).__name__)
        return
    
    def visit_node_return_block(self, node):

        print("ENTERED RETURN BLOCK")

        if self.function_return_stack:

            # Get current function return type
            expected_return_type = self.function_return_stack[-1]  

            if node.ret_value_n:
                result = self.visit_node(node.ret_value_n)
                print(result)
        
                actual_return_type = self.visit_node(node.ret_value_n)[0]

                if expected_return_type == "void":
                    self.logError("Semantic Error: 'void' functions cannot return a value.")

                if expected_return_type != actual_return_type:
                    self.logError(f"Semantic Error: Expected return type '{expected_return_type}', but got '{actual_return_type}'.")

            else:
                if expected_return_type != "void":
                    self.logError(f"Semantic Error: Function must return a value of type '{expected_return_type}', but got none.")


