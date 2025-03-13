from syntax_analyzer import node_iden, node_body, node_code_block, node_if_stmt, node_else_stmt, node_else_chain, node_loop_stmt, node_switch_stmt, node_case_stmt, node_default_stmt, node_return_block, node_ctrl_stmt_body, node_class_arr_idx, node_arr_idx, node_class_att, node_num, node_str, node_bool
from decimal import Decimal

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
        return {sym_name: sym_content}

    def set_class(self, sym_name, class_info):
        sym_content = {}
        sym_content["class_info"] = class_info 
        sym_content["dtype"] = ('class', None)
        self.syms[sym_name] = sym_content

    def set_obj(self, sym_name, initVal, class_name, obj_info):
        sym_content = {}
        sym_content["init_val"] = initVal
        sym_content["dtype"] = class_name 
        sym_content["obj_info"] = obj_info 
        self.syms[sym_name] = sym_content
        return {sym_name: sym_content}

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

class ErrorNode:
    def __init__(self, line, startCol):
        self.line = line
        self.startCol = startCol

class SemanticAnalyzer:

    numtypes = ['int', 'long', 'float', 'double']
    default_vals = {
        'string': '',
        'bool' : False,
        'int' : 0,
        'long' : 0,
        'float' : Decimal(0.0),
        'double' : Decimal(0.0)
    }
   
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

            print('---------GLOBAL TABLE---------\n\t\t')
            self.print_symbols(self.curr_scope.syms, indent=2)
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

    def visit_node(self, node, funcExpectedVal = True):
        nodeName = type(node).__name__
        visit_func = getattr(self, f'visit_{nodeName}', None)  # Get the appropriate visit function, or None if it doesn't exist

        if visit_func is None:
            if nodeName == 'node_imports_list':
                print()
            else: print(f"\n(semantic)(dbg) Not implemented yet!!!!!!!!!!!!!!!!!! node name: {nodeName}")
        else:
            print(f'\n(semantic)(dbg) VISITING {nodeName}!!')
            print(f'!!NODE!!: {node}!!')
            if nodeName in ['node_func_call', 'node_class_method_call']:
                return visit_func(node, expected_val=funcExpectedVal)
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

    def logError(self, msg, err_n = None): 
        if isinstance(err_n, ErrorNode):
            full_message = (
                f"Semantic Error ({err_n.line}, {err_n.startCol}): {msg}"
            )
        elif isinstance(err_n, node_iden):
            col = err_n.id_t["tokenCol"] - len(err_n.id_t["tokenName"]) - 1
            full_message = (
                f"Semantic Error ({err_n.id_t['tokenLine']}, {col}): {msg}"
            )
        else:
            full_message = (
                f"Semantic Error (#todo line nums): {msg}"
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
            self.visit_node(statement, funcExpectedVal=False)
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
        err_n = ErrorNode(node.class_id_n.id_t["tokenLine"], node.class_id_n.id_t["tokenCol"] - len(node.class_id_n.id_t["tokenName"]) - 1)
        className = node.class_id_n.id_t["tokenName"]

        if self.curr_scope.get(className, checkParent=False):
            self.logError(f"Symbol '{className}' is already declared.", err_n)
            return
         
        self.visit_node_class_body(node.class_body_n, className, node)


    def visit_node_constructor_dec(self, node, parentClassname): #TODO: be wary of return statements
        className = node.class_id_n.id_t["tokenName"]
        err_n = ErrorNode(node.class_id_n.id_t["tokenLine"], node.class_id_n.id_t["tokenCol"] - len(node.class_id_n.id_t["tokenName"]) - 1)
        # Check if constructor already exists in current scope
        if self.curr_scope.get(className, checkParent=False):
            self.logError(f"Only one constructor allowed for each class. Duplicate constructor definition found at class '{className}'.", err_n)
            return
        param_types = []
        if node.params_n: # if params_n isn't None
            for param in node.params_n:
                if type(param).__name__ == "node_funcpar_class":
                    err_n = ErrorNode(node.class_id_n.id_t["tokenLine"], param.class_id_n.id_t["tokenCol"] - len(param.class_id_n.id_t["tokenName"]) - 1)
                    class_name = param.class_id_n.id_t["tokenName"]
                    if parentClassname == class_name:
                        self.logError(f"Constructors cannot take an object instance of their own class as parameters. Parameter '{class_name} {param.id_n.id_t["tokenName"]}' not allowed for constructor definition for class '{className}'. ", err_n)
                    if not self.curr_scope.get(class_name):
                        self.logError(f"Class '{class_name}' definition not found for parameter '{class_name} {param.id_n.id_t["tokenName"]}' on constructor definition for class '{className}'.", err_n)
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

        # Ensure param_types is set to None if empty
        param_types = param_types if param_types else None
        constructorInfo = {}
        constructorInfo = self.curr_scope.set_constructor(className, param_types)

        #self.enter_scope(type(node).__name__)
        print(f"\n(semantic)(dbg) ENTERING scope Constructor for class '{className}'")
        self.curr_scope = SymbolTable(self.curr_scope)

        # Add parameters to new function scope
        if node.params_n:
            for param in node.params_n:
                param_name = param.id_n.id_t["tokenName"]
                err_n = ErrorNode(node.param.id_n.id_t["tokenLine"], param.param.id_n.id_t["tokenCol"] - len(param.param.id_n.id_t["tokenName"]) - 1)

                # Check if parameter name is duplicated
                if self.curr_scope.get(param_name, checkParent=False):
                    self.logError(f"Parameter '{param_name}' is already declared in constructor for class '{className}'.", err_n)

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
        if node.code_block_n:
            #print(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$${node.code_block_n}")
            self.visit_node(node.code_block_n)

        # has_return = any(self.visit_node(stmt) for stmt in node.body_n)

        # # If function is non-void, ensure at least one return exists
        # if return_type != "void" and not has_return:
        #     self.logError(f"Function '{func_name}' must return a value of type '{return_type}'.", node.id_n)

        #self.exit_scope(type(node).__name__)

        print(f"\n(semantic)(dbg) EXITING scope Constructor for class '{className}', SYMBOL TABLE: ")
        self.print_symbols(self.curr_scope.syms, indent=2)
        self.curr_scope = self.curr_scope.parent


        return constructorInfo


    def visit_node_class_body(self, node, className, parent_node):
        print(f'\n(semantic)(dbg) VISITING {type(node).__name__}!!')

        class_content = []
        constructor_info = None
        
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

                elif type(vardec_n).__name__ == "node_arr_dec":
                    class_content.append(self.visit_node_arr_dec(vardec_n, priv))

            
            if parent_node.constructor_dec_n: constructor_info = self.visit_node_constructor_dec(parent_node.constructor_dec_n, className)
            child_sym = self.curr_scope.syms
            # self.exit_scope(type(node).__name__)
            self.curr_scope = self.curr_scope.parent

        if parent_node.constructor_dec_n and not node.class_body_stmt_n: 
            constructor_info = self.visit_node_constructor_dec(parent_node.constructor_dec_n, className)
        
        print(f"\n(semantic)(dbg) EXITING scope 'Class: {className}', SYMBOL TABLE: ")
        if node.class_body_stmt_n: self.print_symbols(child_sym, indent=2)
        else: self.print_symbols(self.curr_scope.syms, indent=2)


        flattened = [item for sublist in class_content for item in sublist]
        merged_dict = {k: v for d in flattened for k, v in d.items()}
        self.curr_scope.set_class(className, class_info={"constructor_dec" : constructor_info, "class_body_content": merged_dict})
        

    def visit_node_class_inst(self, node):
        class_id = node.class_id_n.id_t["tokenName"]
        obj_id = node.obj_id_n.id_t["tokenName"]
        class_inst_cont = node.class_instcont_n

        if self.curr_scope.get(obj_id, False):
            self.logError(f"Symbol '{obj_id}' has already been declared in local scope.", node.obj_id_n)

        if not self.curr_scope.get(class_id, checkParent=True):
            self.logError(f"Class '{class_id}' definition not found.", node.class_id_n)


        dtype = ('object', class_id)

        if self.curr_scope.get(class_id).get("class_info"): class_elem_info = self.curr_scope.get(class_id)["class_info"]["class_body_content"]
        
        elif self.curr_scope.parent.get(class_id).get("class_info"): class_elem_info = self.curr_scope.parent.get(class_id)["class_info"]["class_body_content"]

        
        class_elem_info = {k: v for k, v in class_elem_info.items() if not v["priv"]}       #filter items
        
        
        if class_inst_cont:
            constructor_call_id = class_inst_cont.class_id_n.id_t["tokenName"]
            class_constructor_info = self.curr_scope.parent.get(class_id)["class_info"]["constructor_dec"]
            err_n_class_inst = ErrorNode(class_inst_cont.class_id_n.id_t["tokenLine"], class_inst_cont.class_id_n.id_t["tokenCol"] - len(class_inst_cont.class_id_n.id_t["tokenName"]) - 1)
            if constructor_call_id != class_id:
                self.logError(f"Constructor call must match class name. Expected '{class_id}', but found '{constructor_call_id}'.", err_n_class_inst)
            
            if not class_constructor_info:
                self.logError(f"Class '{class_id}' has no defined constructor function.",node.class_id_n)
        
            self.check_function_params(class_constructor_info[class_id], class_inst_cont.func_arg_n, class_inst_cont.class_id_n, "constructor")

            
        self.curr_scope.set_obj(obj_id, None, dtype, class_elem_info)


    def visit_node_class_att(self, node):   #iden.iden
        err_n_obj = ErrorNode(node.obj_id_n.id_t["tokenLine"], node.obj_id_n.id_t["tokenCol"] - len(node.obj_id_n.id_t["tokenName"]) - 1)
        err_n_att = ErrorNode(node.att_id_n.id_t["tokenLine"], node.obj_id_n.id_t["tokenCol"] - len(node.obj_id_n.id_t["tokenName"]) - 1)
        obj_name = node.obj_id_n.id_t["tokenName"]
        class_elem = node.att_id_n.id_t["tokenName"]

        obj_info = self.curr_scope.get(obj_name)
        if not obj_info:
            self.logError(f"Object '{obj_name}' is not yet declared.", node.obj_id_n)

        if obj_info.get("class_info"):
            self.logError(f"Cannot use class '{obj_name}' to access attribute '{class_elem}'. Use an object instance of '{obj_name}' instead.", err_n_obj)

        # print(f"Obj_info : {obj_info} \nobj_name: {obj_name} \nclass_elem: {class_elem}")

        if obj_info.get("dtype")[0] != 'object':
            self.logError(f"Symbol '{obj_name}' not an object instance.", err_n_obj)


        class_info = self.curr_scope.parent.get(obj_info["dtype"][1])["class_info"]["class_body_content"]
        class_info_no_privates = {k: v for k, v in class_info.items() if not v["priv"]}

        if class_info_no_privates.get(class_elem) and class_info_no_privates.get(class_elem)["dtype"][0] == 'func':
            self.logError(f"'{class_elem}' is a method of object '{obj_name}', instance of class '{obj_info["dtype"][1]}', and cannot be used as a value. Use a method call instead.", node.att_id_n)
            
            
        if not class_info_no_privates.get(class_elem) and not class_info.get(class_elem):
            self.logError(f"Element '{class_elem}' not found in object '{obj_name}', instance of class '{obj_info["dtype"][1]}'.", node.att_id_n)
        
        elif class_info.get(class_elem) and not class_info_no_privates.get(class_elem):
            self.logError(f"Element '{class_elem}' is a private element within class '{obj_info["dtype"][1]}' and cannot be accessed by any instance of the class.", node.att_id_n)

        print(f"(semantic)(dbg) EXITED node_class_att!! RETURNED: {(class_info[class_elem]["dtype"], obj_info["obj_info"][class_elem]["value"])}")
        return (class_info[class_elem]["dtype"], obj_info["obj_info"][class_elem]["value"], err_n_obj)  

    def visit_node_class_arr_idx(self, node):
        err_n_obj = ErrorNode(node.obj_id_n.id_t["tokenLine"], node.obj_id_n.id_t["tokenCol"] - len(node.obj_id_n.id_t["tokenName"]) - 1)
        obj_name = node.obj_id_n.id_t["tokenName"]
        class_elem = node.att_id_n.id_t["tokenName"]

        obj_info = self.curr_scope.get(obj_name)
        if obj_info.get("class_info"):
            self.logError(f"Cannot use class '{obj_name}' to access attribute '{class_elem}'. Use an object instance of '{obj_name}' instead.", node.obj_id_n)

        if obj_info.get("dtype")[0] != 'object':
            self.logError(f"Symbol '{obj_name}' not an object.", node.obj_id_n)

        print(obj_info)
        if not obj_info:
            self.logError(f"Object '{obj_name}' is not yet declared.", node.obj_id_n)

        class_info = self.curr_scope.parent.get(obj_info["dtype"][1])["class_info"]["class_body_content"]
        class_info_no_privates = {k: v for k, v in class_info.items() if not v["priv"]}

        if not class_info_no_privates.get(class_elem) and not class_info.get(class_elem):
            self.logError(f"Attribute '{class_elem}' not found in object '{obj_name}', instance of class '{obj_info["dtype"][1]}'.", node.att_id_n)
        
        elif class_info.get(class_elem) and not class_info_no_privates.get(class_elem):
            self.logError(f"Attribute '{class_elem}' is a private attribute within class '{obj_info["dtype"][1]}' and cannot be accessed by any instance of the class.", node.att_id_n)

        arr_sym = obj_info["obj_info"][class_elem]
        dtype = arr_sym["dtype"][1]
        idx_type, idx_val, err_n = self.visit_node(node.idx_n)

        if arr_sym["dtype"][0] != 'arr':
            if not node.idx2_n and dtype == 'string':
                if idx_type[1] not in ['int', 'long']:
                    self.logError(f'Type mismatch: expected whole number (integer, long) but got {idx_type[1]}.', err_n)
                if idx_val < 0:
                        self.logError("String index cannot be negative.", err_n)
                if idx_val >= len(arr_sym["value"]):
                    self.logError(f'String index out of bounds: Index {idx_val} is out of bounds for string length {len(arr_sym["value"])}.', err_n)
                return (('lit', 'string'), arr_sym["value"][idx_val], err_n)
            else:
                self.logError(f'Symbol \'{node.obj_id_n.id_t["tokenName"]}\' is not an array.', node.obj_id_n)

        
        
        if idx_type[1] not in ['int', 'long']:
            self.logError(f'Type mismatch: expected whole number (integer, long) but got {idx_type[1]}.', err_n)
        if idx_val < 0:
                self.logError(f"Array index for '{class_elem}' cannot be negative.", node.att_id_n)
        if idx_val >= arr_sym["arr_info"]["size1"]:
            self.logError(f'Array out of bounds: Index {idx_val} is out of bounds for array length {arr_sym["arr_info"]["size1"]}.', err_n)
        idx2_val = None
        if node.idx2_n:
            if arr_sym["arr_info"]["dimension"] == 1:
                self.logError(f'Array \'{class_elem}\' is 1-dimensional but accessed with 2 indices.', err_n)
            idx2_type, idx2_val = self.visit_node(node.idx2_n)
            if idx2_type[1] not in ['int', 'long']:
                self.logError(f'Type mismatch: expected whole number (integer, long) but got {idx2_type[1]}.', err_n)
            if idx2_val < 0:
                self.logError(f"Array index for '{class_elem}' cannot be negative.", node.att_id_n)
            if idx2_val >= arr_sym["arr_info"]["size2"]:
                self.logError(f'Array out of bounds: Index {idx2_val} is out of bounds for array length {arr_sym["arr_info"]["size2"]}.', err_n)
        else:
            if arr_sym["arr_info"]["dimension"] == 2:
                self.logError(f'Array \'{class_elem}\' is 2-dimensional but accessed with 1 index.', err_n)
        return (('var', dtype), arr_sym["value"][idx_val][idx2_val] if idx2_val else arr_sym["value"][idx_val], err_n_obj)

    def visit_node_num(self, node):
        val = 0
        err_n = ErrorNode(node.val_t["tokenLine"], node.val_t["tokenCol"] - len(node.val_t["tokenName"]) - 1)
        match(node.dtype):
            case "int":
                val = int(node.val_t["tokenName"])
                if val > self.MAX_INT or val < self.MIN_INT:
                    self.logError(f"Value {val} is out of 'int' range.", err_n)

            case "long":
                val = int(node.val_t["tokenName"])
                if val > self.MAX_LONG or val < self.MIN_LONG:
                    self.logError(f"Value {val} is out of 'long' range.", err_n)
            
            case "float":
                val = Decimal(node.val_t["tokenName"])
                if val > self.MAX_FLOAT or val < self.MIN_FLOAT:
                    self.logError(f"Value {val} is out of 'float' range.", err_n)
            
            case "double":
                val = Decimal(node.val_t["tokenName"])
                if val > Decimal(self.MAX_DOUBLE) or val < Decimal(self.MIN_DOUBLE):
                    self.logError(f"Value {val} is out of 'double' range.", err_n)

        print(f"RETURNED FROM NODE_NUM: {(node.dtype, val), err_n} using node: {node.val_t}")
        return (('lit', node.dtype), val, err_n) 
        # return (('lit', node.dtype), None)
    
    def visit_node_str(self, node):
        # return (('var', node.dtype), node.val_t["tokenName"][1:-1]
        err_n = ErrorNode(node.val_t["tokenLine"], node.val_t["tokenCol"] - len(node.val_t["tokenName"]) - 1)
        return (('lit', node.dtype), node.val_t["tokenName"][1:-1], err_n)
    
    def visit_node_bool(self, node):
        err_n = ErrorNode(node.val_t["tokenLine"], node.val_t["tokenCol"] - len(node.val_t["tokenName"]) - 1)
        return (('lit', 'bool'), node.val_t["tokenName"]=="true", err_n)
    
    def visit_node_iden(self, node):
        iden_symbol = self.curr_scope.get(node.id_t["tokenName"])
        err_n = ErrorNode(node.id_t["tokenLine"], node.id_t["tokenCol"] - len(node.id_t["tokenName"]) - 1)
        if not iden_symbol:
            self.logError(f"Symbol '{node.id_t["tokenName"]}' hasn't been declared yet.", err_n)
        else:
            # dtype = iden_symbol["dtype"]
            # val = None
            # if dtype[1] in ['int', 'long']:
            #     val = int(iden_symbol["value"])
            # elif dtype[1] in ['float', 'double']:
            #     val = Decimal(iden_symbol["value"])
            # elif dtype[1] == 'string':
            #     val = iden_symbol["value"]
            
            # return (dtype, val)
            match iden_symbol["dtype"][0]:
                case 'func':
                    self.logError(f"Symbol '{node.id_t["tokenName"]}' is a function and needs to be called rather than using it as a value.", err_n)
                case 'class':
                    self.logError(f"Symbol '{node.id_t["tokenName"]}' is a class and needs to be instantiated rather than using it as a value.", err_n)

            print(f'RETURNED FROM NODE_IDEN: iden_symbol["dtype"]: {iden_symbol.get("dtype", None)}, iden_symbol["value"]:{iden_symbol.get("value", None)}')
            return (iden_symbol.get("dtype", None), iden_symbol.get("value", None), err_n)
            # return (('var', iden_symbol["dtype"][1]), None)
        
    def visit_node_arr_idx(self, node):
        arr_sym = self.curr_scope.get(node.id_n.id_t["tokenName"])
        print(f"ARRRRRRRRRRRRRRRR SYMMMMMMMMMM: {arr_sym}")
        arr_id_err = ErrorNode(node.id_n.id_t["tokenLine"], node.id_n.id_t["tokenCol"] - len(node.id_n.id_t["tokenName"])-1)
        print(f"!!@@@@@@@@@@@@@@@@rr_sym: {node.id_n.id_t["tokenName"]}")
        if not arr_sym:
            self.logError(f'Symbol \'{node.id_n.id_t["tokenName"]}\' has not been declared yet.', arr_id_err)
        dtype = arr_sym["dtype"][1]
        idx_type, idx_val, idx_err = self.visit_node(node.idx_n)
        if arr_sym["dtype"][0] != 'arr':
            if not node.idx2_n and dtype == 'string':
                if idx_type[1] not in ['int', 'long']:
                    self.logError(f'Type mismatch: expected whole number (integer, long) but got {idx_type[1]}.', idx_err)
                if idx_val < 0:
                        self.logError("String index cannot be negative.", idx_err)
                if idx_val >= len(arr_sym["value"]):
                    self.logError(f'String index out of bounds: Index {idx_val} is out of bounds for string length {len(arr_sym["value"])}.', idx_err)
                return (('lit', 'string'), arr_sym["value"][idx_val], arr_id_err)
            else:
                self.logError(f'Symbol \'{node.id_n.id_t["tokenName"]}\' is not an array.', arr_id_err)

    
        if idx_type[1] not in ['int', 'long']:
            self.logError(f'Type mismatch: expected whole number (integer, long) but got {idx_type[1]}.'. idx_err)
        if idx_val < 0:
                self.logError("Array index cannot be negative.", idx_err)
        if idx_val >= arr_sym["arr_info"]["size1"]:
            self.logError(f'Array out of bounds: Index {idx_val} is out of bounds for array length {arr_sym["arr_info"]["size1"]}.', idx_err)
        idx2_val = None
        if node.idx2_n:
            idx2_type, idx2_val, idx2_err = self.visit_node(node.idx2_n)
            if arr_sym["arr_info"]["dimension"] == 1:
                self.logError(f'Array \'{node.id_n.id_t["tokenName"]}\' is 1-dimensional but accessed with 2 indices.', idx2_err)
            if idx2_type[1] not in ['int', 'long']:
                self.logError(f'Type mismatch: expected whole number (integer, long) but got {idx2_type[1]}.', idx2_err)
            if idx2_val < 0:
                self.logError("Array index cannot be negative.", idx2_err)
            if idx2_val >= arr_sym["arr_info"]["size2"]:
                self.logError(f'Array out of bounds: Index {idx2_val} is out of bounds for array length {arr_sym["arr_info"]["size2"]}.', idx2_err)
        else:
            if arr_sym["arr_info"]["dimension"] == 2:
                # self.logError(f'Array \'{node.id_n.id_t["tokenName"]}\' is 2-dimensional but accessed with 1 index.')
                return (('arr', dtype), arr_sym["value"][idx_val])
        
        print(f"!!!!!!!!!!!!!!!!!!!arr_sym: {arr_sym}\nidx_val: {idx_val}\nidx2_val: {idx2_val}")
        
        return (('var', dtype), arr_sym["value"][idx_val][idx2_val] if idx2_val else arr_sym["value"][idx_val], arr_id_err)
    #cont...

    def visit_node_func_dec(self, node, priv = False):
        func_name = node.id_n.id_t["tokenName"]
        return_type = ('func', node.dtype_t["tokenName"])

        # Check if function already exists in current scope
        if self.curr_scope.get(func_name, checkParent=False):
            self.logError(f"Symbol '{func_name}' has already been declared.", node.id_n)
            return

        
        # Store func params into function signature in symbol table
        param_types = []

        if node.params_n: # if params_n isn't None
            for param in node.params_n:
                if type(param).__name__ == "node_funcpar_class":
                    class_name = param.class_id_n.id_t["tokenName"]
                    if not self.curr_scope.get(class_name):
                        self.logError(f"Class '{class_name}' hasn't been declared yet.", param.class_id_n)
                    param_types.append({
                        "dtype": ("object", class_name),
                    })  

                elif type(param).__name__ == "node_funcpar_arr":
                    param_types.append({
                        "dtype": ("arr", param.dtype_t["tokenName"] if param.dtype_t else None),  # for any types
                        "dimension": param.arrdim_i if param.arrdim_i else None # for any dimensions
                    })  

                elif type(param).__name__ == "node_funcpar_var":
                    param_types.append({
                        "dtype": ("var", param.dtype_t["tokenName"])
                    })  
        
        # sample parameter format
        # [
        #     {"type": "var", "dtype": "int"},
        #     {"type": "class", "name": "MyClass"},
        #     {"type": "arr", "dimension": 10}
        # ]

        # Ensure param_types is set to None if empty
        param_types = param_types if param_types else None
        print(f">>param types : {param_types}")
        print(f">>>>>>>>>>> {func_name} IS FUNC STD LIB? " + str(node.is_std_lib))

        classReturn = []
        # Store function in symbol table. (for classes only) also returns the resulting dict
        classReturn.append(self.curr_scope.set_function(func_name, return_type, param_types, priv, isStd_lib = node.is_std_lib))
        #add actual value param in da future

        print(f"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^{classReturn}")


        # Enter function scope
        #self.enter_scope(type(node).__name__)
        print(f"\n(semantic)(dbg) ENTERING scope 'Function: {func_name}'")
        self.curr_scope = SymbolTable(self.curr_scope)
        # Add parameters to new function scope
        if node.params_n:
            for param in node.params_n:
                param_name = param.id_n.id_t["tokenName"]
                print(f"\n\nFOUND TYPE '{type(param).__name__}' FOR PARAM '{param_name}'")

                # Check if parameter name is duplicated
                if self.curr_scope.get(param_name, checkParent=False):
                    self.logError(f"Parameter '{param_name}' is already declared in function '{func_name}'.", param.id_n)

                # Handle different parameter types properly
                if type(param).__name__ == "node_funcpar_class":
                    class_name = ('object', param.class_id_n.id_t["tokenName"])
                    class_elem_info = self.curr_scope.get(param.class_id_n.id_t["tokenName"])["class_info"]["class_body_content"]
                    class_elem_info = {k: v for k, v in class_elem_info.items() if not v["priv"]}       #filter items
                    print(f">>>>>>>>>>>>>SET OBJ: {self.curr_scope.set_obj(param_name, None, class_name, class_elem_info)}")

                elif type(param).__name__ == "node_funcpar_arr":
                    arr_dtype = ('arr', param.dtype_t["tokenName"]) if param.dtype_t else None  # for any types -- std lib Carray
                    arr_dim = param.arrdim_i if param.arrdim_i else None   # for any dimensions -- std lib Carray
                    print(arr_dtype)
                    arr_val = None if not arr_dtype else self.default_vals[arr_dtype[1]]
                    print(f'>>>>>>>>>>>>>SET ARR: {self.curr_scope.set_array(param_name, value=arr_val, dtype=arr_dtype, arr_info={"dimension": arr_dim, "size1": 1, "size2": 2 if arr_dim == 2 else None}, const=False)}')

                elif type(param).__name__ == "node_funcpar_var":
                    var_dtype = ('var', param.dtype_t["tokenName"])
                    print(f'>>>>>>>>>>>>>SET VAR: {self.curr_scope.set(param_name, value=self.default_vals[var_dtype[1]], dtype=var_dtype, const=False)}')

        
        # Visit function body
        if not node.is_std_lib:
            self.function_return_stack.append(return_type[1])
            if not node.body_n:
                self.logError(f"Function '{func_name}' must have a return statement.", node.id_n)

            self.count_return = 0
            has_return = self.check_return_in_body(node.body_n)
            if not has_return:
                if self.count_return:
                    self.logError(f"Function '{func_name}' must have a return statement in all possible code paths.", node.id_n)
                else:
                    self.logError(f"Function '{func_name}' must have a return statement.", node.id_n)
                
            self.visit_node(node.body_n)

            self.function_return_stack.pop()
            print(f"(semantic)(dbg) Popped return type, Stack after pop = {self.function_return_stack}")
            self.current_function_name = None
 

        # Exit function scope, back to program constructs
        print(f"\n(semantic)(dbg) EXITING scope 'Function: {func_name}', SYMBOL TABLE: ")
        self.print_symbols(self.curr_scope.syms, indent=2)
        self.curr_scope = self.curr_scope.parent
        return classReturn

    # assign_stmt  -- need to refactor nodes in ast bc 
    def visit_node_assign_stmt_var(self, node):
        iden = node.id_n
        value = node.value_n
        iden_name = iden.id_t["tokenName"]
        iden_symbol = self.curr_scope.get(iden_name)

        if not iden_symbol: self.logError(f"Symbol '{iden_name}' hasn't been declared yet.", iden)

        if iden_symbol["dtype"][0] in ["arr", "object"]:
            if iden_symbol["dtype"][0] == "arr":
                self.logError(f"Symbol '{iden_name}' is an array and cannot be reassigned. Try accessing its elements instead.", iden)
            elif iden_symbol["dtype"][0] == "object":
                self.logError(f"Symbol '{iden_name}' is an object and cannot be reassigned. Try accessing its attributes instead.", iden)

            
        if iden_symbol["const"]:
            self.logError(f"Symbol '{iden_name}' is a constant and cannot be reassigned.", iden)
        dtype = iden_symbol["dtype"][1]
        val_type, val = self.visit_node(value)
        print(f" ------------------------------------------->{val_type[1]}")
        #if dtype != val_type[1]:
        #    self.logError(f"Type Mismatch: expected '{dtype}' for variable '{iden_name}' but found '{val_type[1]}'", iden)
        
        match(dtype):
            case "int":
                if val_type[1] not in ["string", "bool"]:
                    if val > self.MAX_INT or val < self.MIN_INT:
                        self.logError(f"Value '{val}' is out of 'int' range for variable '{iden_name}'.", iden)
                
                if val_type and dtype != val_type[1]:    
                    self.logError(f"Type Mismatch: expected '{dtype}' for variable '{iden_name}' but found '{val_type[1]}'.", iden)   
    
            case "long":
                if val_type[1] not in ["string", "bool"]:
                    if val > self.MAX_LONG or val < self.MIN_LONG:
                        self.logError(f"Value '{val}' is out of 'long' range for variable '{iden_name}'.", iden)
                
                if val_type and dtype != val_type[1]:
                    if val_type[1] != "int":
                        self.logError(f"Type Mismatch: expected '{dtype}' for variable '{iden_name}' but found '{val_type[1]}'.", iden)
    
            case "float":
                if val_type[1] not in ["string", "bool"]:
                    if val > self.MAX_FLOAT or val < self.MIN_FLOAT:
                        self.logError(f"Value '{val}' is out of 'float' range for variable '{iden_name}'.", iden)
                
                if val_type and dtype != val_type[1]:
                    if val_type[1] != "int":
                        self.logError(f"Type Mismatch: expected '{dtype}' for variable '{iden_name}' but found '{val_type[1]}'.", iden)

            case "double":
                if val_type[1] not in ["string", "bool"]:
                    if val > self.MAX_DOUBLE or val < self.MIN_DOUBLE:
                        self.logError(f"Value '{val}' is out of 'double' range for variable '{iden_name}'.", iden)
                
                if val_type and dtype != val_type[1]:
                    if val_type[1] not in ["int", "float", "long"]:
                        self.logError(f"Type Mismatch: expected '{dtype}' for variable '{iden_name}' but found '{val_type[1]}'.", iden)

            case _:
                if val_type and dtype != val_type[1]:
                    self.logError(f"Type Mismatch: expected '{dtype}' for variable '{iden_name}' but found '{val_type[1]}'.", iden)

        self.curr_scope.set(iden_name, val, dtype=('var', f'{dtype}'))


    def visit_node_assign_stmt_array_elem(self, node): 
        # visit_node_assign_stmt_object_att_arr REFERENCES THIS, CHANGE BOTH FUNCS WHEN U CHANGE THIS ONE THANK U
        arr_node = node.id_arr_n   # current node
        arr_name = arr_node.id_n.id_t["tokenName"]
        arr_symbol = self.curr_scope.get(arr_name)  # reference node in sym table

        if not arr_symbol:
            self.logError(f"Array '{arr_name}' hasn't been declared yet.", arr_node.id_n)

        if arr_symbol["const"]:
            self.logError(f"Array '{arr_name}' is a constant and cannot be modified.", arr_node.id_n)

        arr_dtype = arr_symbol["dtype"][1]
        arr_dim = arr_symbol["arr_info"]["dimension"]

        if arr_dim == 1 and arr_node.idx2_n:
            self.logError(f"Array '{arr_name}' is 1-dimensional but accessed with 2 indices.", arr_node.id_n)
        elif arr_dim == 2 and not arr_node.idx2_n:
            self.logError(f"Array '{arr_name}' is 2-dimensional but accessed with 1 index.", arr_node.id_n)

        idx1_type, idx1_val, _ = self.visit_node(arr_node.idx_n)
        if idx1_type[1] not in ['int', 'long']:
            self.logError(f"Array index must be an integer, but found '{idx1_type[1]}'.", arr_node.id_n)

        if idx1_val is not None and (idx1_val < 0 or (arr_symbol["arr_info"]["size1"] is not None and idx1_val >= arr_symbol["arr_info"]["size1"])):  # code gen    
            self.logError(f"Array index '{idx1_val}' out of bounds for array '{arr_name}'.", arr_node.id_n)

        if arr_dim == 2:
            idx2_type, idx2_val = self.visit_node(arr_node.idx2_n)
            if idx2_type[1] not in ['int', 'long']:
                self.logError(f"Array index must be an integer, but found '{idx2_type[1]}'.", arr_node.id_n)

            if idx2_val is not None and (idx2_val < 0 or (arr_symbol["arr_info"]["size2"] is not None and idx2_val >= arr_symbol["arr_info"]["size2"])):
                self.logError(f"Array index '{idx2_val}' out of bounds for array '{arr_name}'.", arr_node.id_n)

        value_type, value, _ = self.visit_node(node.value_n)
        if value_type[1] != arr_dtype:
            self.logError(f"Type Mismatch: expected '{arr_dtype}' for array '{arr_name}' but found '{value_type[1]}'.", node.id_arr_n.id_n)

        # Update the array value in the symbol table (for code generation purposes)
        # if arr_dim == 1:
        #     arr_symbol["value"][idx1_val] = value
        # else:
        #     arr_symbol["value"][idx1_val][idx2_val] = value
        


    def visit_node_assign_stmt_object_att(self,node):
        self.visit_node(node.class_att_n)

        obj_name = node.class_att_n.obj_id_n.id_t["tokenName"]
        att_name = node.class_att_n.att_id_n.id_t["tokenName"]
        value = node.value_n
        print(f"\nOBJ INFO: {self.curr_scope.get(obj_name)} \n{obj_name}")
        att_info = self.curr_scope.get(obj_name)["obj_info"].get(att_name)
        #print(f"!!!!!!!!!!!!!found att_info for '{att_name}' in '{obj_name}': {att_info}")   

        if att_info["dtype"][0] == 'var' and att_info["const"]:
            self.logError(f"Attribute '{att_name}' is a constant and cannot be reassigned.", node.class_att_n.att_id_n)
        
        if att_info["dtype"][0] == 'arr':
            self.logError(f"Cannot assign to class array attribute '{att_name}' without providing index.", node.class_att_n.att_id_n)
        
        if att_info["dtype"][0] != 'var':
            self.logError(f"Cannot assign to class element '{att_name}' because it is not an attribute.", node.class_att_n.att_id_n)


        dtype = att_info["dtype"][1]
        val_type, val = self.visit_node(value)
        print(f">>>>>>>>>>>>>>>>dtype: {dtype}, val_type: {val_type}, val: {val}")


        if dtype != val_type[1]:
            self.logError(f"Type Mismatch: expected '{dtype}' for attribute '{att_name}' but found '{val_type[1]}'", node.class_att_n.att_id_n)

        # self.curr_scope.set(att_name, val, dtype=dtype) #for code gen na e2 ryt TODO
        att_info["value"] = val

        print(f"\n(semantic)(dbg) EXITED node_assign_stmt_object_att!! New local object '{obj_name}' info: {self.curr_scope.get(obj_name)}")

        
    def visit_node_assign_stmt_object_att_arr(self, node): # # iden.iden[1][2] = val
        print(node.class_arr_n)
        # node_assign_stmt_object_att_arr:
            # self.op_t         #assign_op
            # self.value_n       #lit/var/func  
            # self.class_arr_n   # iden.iden[1][]
                # node_class_arr_idx
                    # self.obj_id_n     #iden
                    # self.att_id_n     #iden
                    # self.idx_n        #1stD
                    # self.idx2_n       #2ndD
        print('\n(semantic)(dbg) VISITING node_class_att!!')
        print(f'!!NODE!!: {node.class_arr_n}!!')
        self.visit_node_class_att(node.class_arr_n)


        obj_name = node.class_arr_n.obj_id_n.id_t["tokenName"]
        att_name = node.class_arr_n.att_id_n.id_t["tokenName"]
        val_to_be_assigned = node.value_n
        att_info = self.curr_scope.get(obj_name)["obj_info"].get(att_name)
        print(f"\nOBJ INFO: {self.curr_scope.get(obj_name)} \n{obj_name}\n{att_info}\n{val_to_be_assigned}")

        if att_info["dtype"][0] != 'arr' :      # todo add string!!!
            self.logError(f"Class element '{att_name}' cannot be indexed because it is not an array.", node.class_arr_n.att_id_n)

        if att_info["const"]:
            self.logError(f"Array attribute '{att_name}' is a constant and cannot be reassigned.", node.class_arr_n.att_id_n)

        att_arr_dtype = att_info["dtype"][1]
        att_arr_dim = att_info["arr_info"]["dimension"]
        att_arr_idx1 = node.class_arr_n.idx_n
        att_arr_idx2 = node.class_arr_n.idx2_n

        if att_arr_dim == 1 and att_arr_idx2:
            self.logError(f"Array attribute '{att_name}' is 1-dimensional but accessed with 2 indices.", node.class_arr_n.att_id_n)
        elif att_arr_dim == 2 and not att_arr_idx2:
            self.logError(f"Array attribute '{att_name}' is 2-dimensional but accessed with 1 index.", node.class_arr_n.att_id_n)

        idx1_type, idx1_val = self.visit_node(att_arr_idx1)
        if idx1_type[1] not in ['int', 'long']:
            self.logError(f"Array index must be an integer, but found '{idx1_type[1]}'.", node.class_arr_n.att_id_n)

        if idx1_val is not None and (idx1_val < 0 or (att_info["arr_info"]["size1"] is not None and idx1_val >= att_info["arr_info"]["size1"])):  # code gen    
            self.logError(f"Array index '{idx1_val}' out of bounds for array '{att_name}'.", node.class_arr_n.att_id_n)

        if att_arr_dtype == 2:
            idx2_type, idx2_val = self.visit_node(att_arr_idx2)
            if idx2_type[1] not in ['int', 'long']:
                self.logError(f"Array index must be an integer, but found '{idx2_type[1]}'.", node.class_arr_n.att_id_n)

            if idx2_val is not None and (idx2_val < 0 or (att_info["arr_info"]["size2"] is not None and idx2_val >= att_info["arr_info"]["size2"])):
                self.logError(f"Array index '{idx2_val}' out of bounds for array '{att_name}'.", node.class_arr_n.att_id_n)

        value_type, value, err_n = self.visit_node(node.value_n)
        if value_type[1] != att_arr_dtype:
            self.logError(f"Type Mismatch: expected '{att_arr_dtype}' for array '{att_name}' but found '{value_type[1]}'.", err_n)

        # Update the array value in the symbol table (for code generation purposes)
        # if arr_dim == 1:
        #     arr_symbol["value"][idx1_val] = value
        # else:
        #     arr_symbol["value"][idx1_val][idx2_val] = value


        print(f"\n(semantic)(dbg) EXITED node_assign_stmt_object_att_arr!! New local object '{{' info: {{")


    
    # func calls
    def visit_node_func_call(self, node, expected_val):
        func_name = node.id_n.id_t["tokenName"]
        func_symbol = self.curr_scope.get(func_name)
        if not func_symbol:
            self.logError(f"Function '{func_name}' hasn't been declared yet.", node.id_n)
        if func_symbol["dtype"][0] != 'func':
            self.logError(f"Symbol '{func_name}' is not a function.")
        
        self.check_function_params(func_symbol, node.args_n, node.id_n, "function")
        #print(f"RETURNED FROM FUNC CALL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{(func_symbol["dtype"], None)}")
        #temp vals
        val = None
        if func_symbol["dtype"][1] == 'void':
            if expected_val:
                self.logError("Function '{func_name}' is void and cannot return any value, it cannot be used as a value.", node.id_n)
        else:
            val = self.default_vals[func_symbol["dtype"][1]]


        print(f"RETURNED FROM FUNC_CALL: {('lit', f'{func_symbol["dtype"][1]}'), val}")
        return (('lit', f'{func_symbol["dtype"][1]}'), val, node.id_n) 

    
    def check_function_params(self, func_symbol, args, node_id, call_string):
        print(f"(semantic)(dbg) CHECKING PARAMS from {call_string}!!")
        """
        Checks params vs args -- used for func calls / method calls / constructors.
        params:
            func_symbol (dict): function's symbol information, including expected parameters  -- check usage in visit_node_func_call
            args (list): args_n from func/method call
            node_id (int): id of the node where the function call is made

            NOTE: u can add a flag if function/method/constructor then change error msgs
        """
        
        if func_symbol["params"]:
            if len(func_symbol["params"]) != len(args):
                param_count = len(func_symbol['params'])
                self.logError(f"{call_string.capitalize()} call '{node_id.id_t['tokenName']}' requires {param_count} parameter{'s' if param_count > 1 else ''} but got {len(args)}.", node_id)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++ args: " + str(args))
            for i, (arg_node, param_type) in enumerate(zip(args, func_symbol["params"])):
                arg_sym = None
                arg_val_type = None
                arg_arr_att_flag = False # flag for checking if arg is a value or not (not a whole array or a whole object)

                print(">>>>>>>>>>>>>>>>>>>>>> arg_node: " + str(arg_node))
                
                if hasattr(arg_node, 'id_t'):
                    arg_sym = self.curr_scope.get(arg_node.id_t["tokenName"])
                    if not arg_sym:
                        self.logError(f"[Argument {i+1}] Symbol '{arg_node.id_t['tokenName']}' has not been declared yet.", arg_node)
                    arg_val_type = arg_sym["dtype"]
                else:
                    current_node = arg_node
                    while not hasattr(current_node, 'id_t') and hasattr(current_node, 'id_n'):  # loop until it finds an identifier in the nodes (if there are any)
                        if isinstance(current_node, (node_arr_idx, node_class_att, node_class_arr_idx)):
                            arg_arr_att_flag = True # value -- array element or object attribute or object att arr element
                        current_node = current_node.id_n
                    if hasattr(current_node, 'id_t'):
                        arg_sym = self.curr_scope.get(current_node.id_t["tokenName"])
                        if not arg_sym:
                            self.logError(f"[Argument {i+1}] Symbol '{current_node.id_t['tokenName']}' is not declared.", current_node)
                        arg_val_type = arg_sym["dtype"]
                    else: # if the current node doesn't have an iden 
                        arg_val_type = self.visit_node(arg_node)[0]

                print(">>>>>>>>>>>>>>>>>>>>>> PARAM TYPE: " + str(param_type))
                print(">>>>>>>>>>>>>>>>>>>>>> arg_sym: " + str(arg_sym))
                print(">>>>>>>>>>>>>>>>>>>>>> arg_val_type: " + str(arg_val_type))
                print(">>>>>>>>>>>>>>>>>>>>>> param_type: " + str(param_type))
                print(">>>>>>>>>>>>>>>>>>>>>> arg_value_flag: " + str(arg_arr_att_flag))
                print(">>>>>>>>>>>>>>>>>>>>>> node type: " + str(type(arg_node).__name__))

                self.visit_node(arg_node)

                if param_type["dtype"][0] == "var":
                    if arg_val_type[0] != "lit" or arg_arr_att_flag:  # values and vars are treated the sme type
                        if arg_val_type[0] == 'arr' : # value  vs  array 
                            if not arg_arr_att_flag: # value  vs  array as a whole
                                self.logError(f"Type mismatch for {call_string} call '{node_id.id_t['tokenName']}' parameter {i+1}: expected a value of type '{param_type['dtype'][1]}' but found an array of type '{arg_val_type[1]}'.", node_id)

                        elif arg_val_type[0] == 'object': # value  vs  object
                            self.logError(f"Type mismatch for {call_string} call '{node_id.id_t['tokenName']}' parameter {i+1}: expected a value of type '{param_type['dtype'][1]}' but found an object of class '{arg_val_type[1]}'.", node_id)
                   
                    if param_type["dtype"][1] != arg_val_type[1]: # value vs value but not correct dtype
                        self.logError(f"Type mismatch for {call_string} call '{node_id.id_t['tokenName']}' parameter {i+1}: expected '{param_type['dtype'][1]}' but found '{arg_val_type[1]}'.", node_id)
                
                elif param_type["dtype"][0] == "arr":
                    if arg_arr_att_flag and arg_sym["arr_info"]["dimension"] == 2: # array with 2 dimensions and the array value in 1d is trying to be accessed and passed
                        if param_type["dtype"][1] is None or param_type["dimension"] is None:
                            continue  # Accept any dtype and dimension for std libs

                        if param_type["dtype"][1] != arg_val_type[1]: # arr vs arr -- wrong dtype
                            self.logError(f"Type mismatch for {call_string} call '{node_id.id_t['tokenName']}' parameter {i+1}: expected array of type '{param_type['dtype'][1]}' but found array of type '{arg_val_type[1]}'.", node_id)
                        
                    elif arg_val_type[0] != "arr" or arg_arr_att_flag:  # arr vs incorrect value types (or array elements too)
                        print("ARRAYYYYYYYYYYYYYYYYYY ARR VS NOT ARR OR ARR ELEM")
                        if arg_val_type[0] in ["var", "lit"] or arg_arr_att_flag: # arr vs value
                            self.logError(f"Type mismatch for {call_string} call '{node_id.id_t['tokenName']}' parameter {i+1}: expected an array but found a value of type '{arg_val_type[1]}'.", node_id)
                        elif arg_val_type[0] == "object": # arr vs object 
                            self.logError(f"Type mismatch for {call_string} call '{node_id.id_t['tokenName']}' parameter {i+1}: expected an array but found an object instance of class '{arg_val_type[1]}'.", node_id)
                      
                    elif arg_val_type[0] == "arr":  # arr vs arr
                        print("ARRAYYYYYYYYYYYYYYYYYY ARR VS ARR")
                        if param_type["dtype"][1] is None or param_type["dimension"] is None:
                            continue  # Accept any dtype and dimension for std libs

                        if param_type["dtype"][1] != arg_val_type[1]: # arr vs arr -- wrong dtype
                            self.logError(f"Type mismatch for {call_string} call '{node_id.id_t['tokenName']}' parameter {i+1}: expected array of type '{param_type['dtype'][1]}' but found array of type '{arg_val_type[1]}'.", node_id)
                        
                        else:
                            arg_sym = self.curr_scope.get(arg_node.id_t["tokenName"])

                        print("ARRAYYYYYYYYYYYYYYYYYY CHECK IN ARGS ARR INFO: " + str(arg_sym["arr_info"]))

                        if arg_sym["arr_info"]["dimension"] != param_type["dimension"]: # arr vs arr -- wrong dimension
                            self.logError(f"Dimension mismatch for {call_string} call '{node_id.id_t['tokenName']}' parameter {i+1}: expected {param_type['dimension']} dimensions but found {arg_sym['arr_info']['dimension']}.", node_id)
                
                elif param_type["dtype"][0] == "object":
                    if arg_val_type[0] != "object":
                        if arg_val_type[0] == "arr" and not arg_arr_att_flag: # object vs arr
                            self.logError(f"Type mismatch for function call '{node_id.id_t['tokenName']}' parameter {i+1}: expected an object but found an array of type '{arg_val_type[1]}'.", node_id)
                        else: # object vs value
                            self.logError(f"Type mismatch for {call_string} call '{node_id.id_t['tokenName']}' parameter {i+1}: expected an object but found a value of type '{arg_val_type[1]}'.", node_id)
                    
                    elif param_type["dtype"][1] != arg_val_type[1]:  # object vs object -- wrong classname
                        self.logError(f"Class type mismatch for {call_string} call '{node_id.id_t['tokenName']}' parameter {i+1}: expected instance of class '{param_type['dtype'][0]}' but found '{arg_val_type[1]}'.", node_id)
                else:
                        self.logError(f"Unknown parameter type for {call_string} call '{node_id.id_t['tokenName']}' parameter {i+1}: '{param_type['dtype'][1]}'", node_id)
            
        else:
            if args:
                self.logError(f"{call_string.capitalize()} call '{node_id.id_t['tokenName']}' requires 0 parameters but got {len(args)}.", node_id)

        print(f"(semantic)(dbg) FINISHED CHECKING PARAMS from {call_string}!!!!!")
    
    
    def visit_node_class_method_call(self,node, expected_val):
        obj_name = node.obj_id_n.id_t["tokenName"]
        class_elem = node.method_id_n.id_t["tokenName"]

        obj_info = self.curr_scope.get(obj_name)
        if not obj_info:
            self.logError(f"Object '{obj_name}' is not yet declared.", node.obj_id_n)
        if obj_info["dtype"][0] != "object":    
            self.logError(f"Symbol '{obj_name}' is not an object.", node.obj_id_n)
        class_info = self.curr_scope.parent.get(obj_info["dtype"][1])["class_info"]["class_body_content"]
        class_info_no_privates = {k: v for k, v in class_info.items() if not v["priv"]}

        if not class_info_no_privates.get(class_elem) and not class_info.get(class_elem):
            self.logError(f"Method '{class_elem}' not found in object '{obj_name}', instance of class '{obj_info["dtype"][1]}'.", node.method_id_n)
        
        elif class_info.get(class_elem) and not class_info_no_privates.get(class_elem):
            self.logError(f"Method '{class_elem}' is a private method within class '{obj_info["dtype"][1]}' and cannot be accessed by any instance of the class.", node.method_id_n)

        # self.obj_id_n = class_id_n
        # self.method_id_n = method_id_n
        # self.args_n = args_n
        self.check_function_params(class_info_no_privates[class_elem], node.args_n, node.method_id_n, "method")
        print(node)

        val = None
        if class_info[class_elem]["dtype"][1] == 'void':
            if expected_val:
                self.logError(f"Class method '{class_elem}' is void and cannot return any value, it cannot be used as a value.", node.method_id_n)
        else:
            val = self.default_vals[class_info[class_elem]["dtype"][1]]

        return (class_info[class_elem]["dtype"], val, node.obj_id_n)
    
    # var / arr dec helper function for type and range checking
    def check_type_and_range(self, dec_type, dtype, val_type, id_n, value, index_1D = None, index_2D = None, err_n = None):
        id = id_n.id_t["tokenName"]
        print("PRINT >>>>>>>>>>>>>>>>> DEC_TYPE: " + dec_type)
        print("PRINT >>>>>>>>>>>>>>>>> DTYPE: " + str(dtype))
        print("PRINT >>>>>>>>>>>>>>>>> VAL_TYPE: " + str(val_type))
        print("PRINT >>>>>>>>>>>>>>>>> ID_N: " + str(id_n))
        print("PRINT >>>>>>>>>>>>>>>>> VALUE: " + str(value))
        print("PRINT >>>>>>>>>>>>>>>>> INDEX_1D: " + str(index_1D))
        print("PRINT >>>>>>>>>>>>>>>>> INDEX_2D: " + str(index_2D))

        index = None
        if index_1D != None:
            index = f" at index [{index_1D}]"
            if index_2D != None:
                index += f"[{index_2D}]"
        
        print("PRINT >>>>>>>>>>>>>>>>> index: " + str(index))

        match dtype[1]:
            case "int":
                if val_type[1] not in ["string", "bool"]:
                    if value > self.MAX_INT or value < self.MIN_INT:
                       self.logError(f"Value '{value}' is out of 'int' range for {dec_type} '{id}'{index if index else ""}.", err_n)
                
                if val_type and dtype[1] != val_type[1]:    
                    self.logError(f"Type Mismatch: expected '{dtype[1]}' for {dec_type} '{id}'{index if index else ""} but found '{val_type[1]}'." , err_n)

            case "long":
                if val_type[1] not in ["string", "bool"]:
                    if value > self.MAX_LONG or value < self.MIN_LONG:
                        self.logError(f"Value '{value}' is out of 'long' range for {dec_type} '{id}'{index if index else ""}.", err_n)
                
                if val_type and dtype[1] != val_type[1]:
                    if val_type[1] != "int":
                        self.logError(f"Type Mismatch: expected '{dtype[1]}' for {dec_type} '{id}'{index if index else ""} but found '{val_type[1]}'.", err_n)

            case "float":
                if val_type[1] not in ["string", "bool"]:
                    if value > self.MAX_FLOAT or value < self.MIN_FLOAT:
                        self.logError(f"Value '{value}' is out of 'float' range for {dec_type} '{id}'{index if index else ""}.", err_n)
                
                if val_type and dtype[1] != val_type[1]:
                    if val_type[1] != "int":
                        self.logError(f"Type Mismatch: expected '{dtype[1]}' for {dec_type} '{id}'{index if index else ""} but found '{val_type[1]}'.", err_n)

            case "double":
                if val_type[1] not in ["string", "bool"]:
                    if value > self.MAX_DOUBLE or value < self.MIN_DOUBLE:
                        self.logError(f"Value '{value}' is out of 'double' range for {dec_type} '{id}'{index if index else ""}.", err_n)
                
                if val_type and dtype[1] != val_type[1]:
                    if val_type[1] not in ["int", "float", "long"]:
                        self.logError(f"Type Mismatch: expected '{dtype[1]}' for {dec_type} '{id}'{index if index else ""} but found '{val_type[1]}'.", err_n)

            case _:
                if val_type and dtype[1] != val_type[1]:
                    self.logError(f"Type Mismatch: expected '{dtype[1]}' for {dec_type} '{id}'{index if index else ""} but found '{val_type[1]}'.", err_n) 

    #node_var_dec
    def visit_node_vardec(self, node, priv = False):
        err_n = ErrorNode(node.id_n.id_t["tokenLine"], node.id_n.id_t["tokenCol"] - len(node.id_n.id_t["tokenName"]) - 1)

        if self.curr_scope.get(node.id_n.id_t["tokenName"], False):
            self.logError(f"Symbol '{node.id_n.id_t["tokenName"]}' has already been declared.", err_n)
        const = node.const_b
        dtype = ('var', node.dtype_t["tokenName"])
        id = node.id_n.id_t["tokenName"]
        val_type = None
        value = None
        idec_rec = None
        if node.vardec_cont_n:
            if node.vardec_cont_n.value_n:
                val_type, value, err_n = self.visit_node(node.vardec_cont_n.value_n)
            if val_type: print('(semantic)(dbg) dec valtype: ', val_type)
            idec_rec = node.vardec_cont_n.idec_rec_n

        defaultVal = self.default_vals[dtype[1]]

        if not val_type and not value:
            val_type = ('lit', f'{dtype[1]}')
            value = defaultVal
            
        if val_type: print(f" -------------------------------------------> val_type: {val_type[1]} d_type: {dtype[1]}")
        
        self.check_type_and_range("variable", dtype, val_type, node.id_n, value, err_n = err_n)

        classReturn = []
        classReturn.append(self.curr_scope.set(id, value, dtype=dtype, priv = priv, const=const))

        for dec_node in idec_rec or []:
            err_n = ErrorNode(dec_node.id_n.id_t["tokenLine"], dec_node.id_n.id_t["tokenCol"] - len(dec_node.id_n.id_t["tokenName"]) - 1)
            
            if self.curr_scope.get(dec_node.id_n.id_t["tokenName"], False):
                self.logError(f"Symbol '{dec_node.id_n.id_t["tokenName"]}' has already been declared.", err_n)
            classReturn.append(self.curr_scope.set(dec_node.id_n.id_t["tokenName"], dec_node.value_n if dec_node.value_n != None else defaultVal, dtype=dtype, priv = priv, const=const))

        return classReturn

    #array declaration
    def visit_node_arr_dec(self, node, priv = False):
        print(f'\n(semantic)(dbg) VISITING {type(node).__name__}!!')
        print(f'!!NODE!!: {node}!!')
        id = node.id_n.id_t["tokenName"]

        if self.curr_scope.get(id, checkParent=False):
            self.logError(f"Symbol '{id}' has already been declared.", node.id_n)

        dtype = ('arr', node.dtype_t["tokenName"])

        baseVal = self.default_vals[dtype[1]]

        dim = 2 if node.size2_n else 1

        size_1_type, size_1, size1_err = self.visit_node(node.size1_n)

        if size_1_type[1] not in ['int', 'long']:
            self.logError(f"Type mismatch: expected whole number (integer, long) for array 1st Dimension size, but got '{size_1_type[1]}'.", node.id_n)
        
        if size_1 < 1:
            self.logError(f"Cannot declare array '{id}' with 1st Dimension size less than 1.", node.id_n)
        size_2_type, size_2, size2_err = self.visit_node(node.size2_n) if node.size2_n else (None, None, None)

        if size_2_type and size_2_type[1] not in ['int', 'long']:
            self.logError(f"Type mismatch: expected whole number (integer, long) for array 2nd Dimension size, but got '{size_2_type[1]}'.", node.id_n)
        print(size_2 and size_2 < 1)
        
        try:
            if size_2 < 1:
                self.logError(f"Cannot declare array '{id}' with 2nd Dimension size less than 1.", node.id_n)
        except TypeError:
            pass


        values_list = None
        
        arr_rec = None
        
        classReturn = []
        
        if node.arr_dec_cont_n:
            if type(node.arr_dec_cont_n[0]).__name__ == "node_arr_dec_rec":
                arr_rec = node.arr_dec_cont_n
                #print(f'##########################arr_rec@!!@!@!@: {arr_rec} size_1: {size_1} dim = {dim}')
                values_list = []
                
                for i in range(size_1):
                     values_list.append(baseVal)
            
            else:
                values_list = node.arr_dec_cont_n
        
        else:
            values_list = []
            for i in range(size_1):
                values_list.append(baseVal)
        
       #print(f'##########################values_list@!!@!@!@: {values_list if values_list else arr_rec} dim = {dim}')
                

        arr_vals = []
        if dim == 1:
            if node.arr_dec_cont_n and not arr_rec:
                
                for index_1D, value_node in enumerate(values_list or []):
                    val_type, val, err_n = self.visit_node(value_node)
                    print(f'arr init valtype: {val_type[1]}')
                    
                    #error for arr size in code gen
                    # if val_type[1] != node.dtype_t["tokenName"]:
                    #     self.logError(f"Array contents of '{id}' can only be of type '{node.dtype_t["tokenName"]}', but found '{val_type[1]}'.", node.id_n)
                    
                    self.check_type_and_range("array", dtype, val_type, node.id_n, val, index_1D, err_n = err_n)

                    arr_vals.append(val)
                
                if arr_vals and len(arr_vals) > size_1:
                    singplur = 'element' if size_1 == 1 else 'elements'
                    self.logError(f"Expected {size_1} {singplur} for array '{id}', but got {len(arr_vals)} elements instead.", node.id_n)
                
                elif arr_vals and len(arr_vals) < size_1:
                    for i in range(size_1 - len(arr_vals)):
                        arr_vals.append(baseVal)
  
            else: arr_vals = values_list
        
        else:
            
            for index_1D, inner_arr in enumerate(values_list or []):
                temp_arr = []
                
                for index_2D, value_node in enumerate(inner_arr or []):
                    val_type, val, err_n = self.visit_node(value_node)
                    print(f'arr init valtype: {val_type}, val = {val}')
                    
                    #error for arr size in code gen
                    # if val_type[1] != node.dtype_t["tokenName"]:
                    #     self.logError(f"Array contents of '{id}'  can only be of type '{node.dtype_t["tokenName"]}', but found '{val_type[1]}.", node.id_n)
                    
                    self.check_type_and_range("array", dtype, val_type, node.id_n, val, index_1D, index_2D, err_n = err_n)

                    temp_arr.append(val)
                
                if len(temp_arr) > size_2:
                        singplur = 'element' if size_2 == 1 else 'elements'
                        self.logError(f"Expected {size_2} {singplur} for inner array element of array '{id}', but got {len(temp_arr)} elements instead.", node.id_n)
                
                elif len(temp_arr) < size_2:
                    for i in range(size_2 - len(temp_arr)):
                        temp_arr.append(baseVal)

                #print(f"_____________________________{temp_arr}")
                arr_vals.append(temp_arr)
            
            if len(arr_vals) > size_1:
                singplur = 'element' if size_1 == 1 else 'elements'
                self.logError(f"Expected {size_1} {singplur} for array '{id}', but got {len(arr_vals)}.", node.id_n)
            
            elif len(arr_vals) < size_1:
                    for i in range(size_1 - len(arr_vals)):
                        arr_vals.append([baseVal]*(size_2 if size_2 else size_1))
        classReturn.append(self.curr_scope.set_array(id, arr_vals, dtype=dtype, arr_info={'dimension': dim, 'size1': size_1, 'size2':size_2}, priv=priv, const = node.const_b))
        
        for arrdec_node in arr_rec or []:
            arrdec_vals = []
            
            size_1_type, size_1, _ = self.visit_node(arrdec_node.size1_n)
            
            if size_1_type[1] not in ['int', 'long']:
                self.logError(f"Type mismatch: expected whole number (integer, long) for array 1st Dimension size, but got '{size_1_type[1]}'.", arrdec_node.id_n)
            if size_1 < 1:
                self.logError(f"Cannot declare array '{arrdec_node.id_n.id_t["tokenName"]}' with 1st Dimension size less than 1.", arrdec_node.id_n)
            size_2_type, size_2, _ = self.visit_node(arrdec_node.size2_n) if node.size2_n else (None, None)
            
            if size_2_type and size_2_type[1] not in ['int', 'long']:
                self.logError(f"Type mismatch: expected whole number (integer, long) for array 2nd Dimension size, but got '{size_2_type[1]}'.", arrdec_node.id_n)
            
            if size_2 and size_2 < 1:
                self.logError(f"Cannot declare array '{arrdec_node.id_n.id_t["tokenName"]}' with 2nd Dimension size less than 1.", arrdec_node.id_n)


            if self.curr_scope.get(arrdec_node.id_n.id_t["tokenName"], checkParent=False):
                self.logError(f"Symbol '{arrdec_node.id_n.id_t["tokenName"]}' has already been declared.", node.id_n)

            for i in range(size_1):
                temp_arr = []
                if size_2:
                    for j in range(size_2):
                        temp_arr.append(baseVal)
                arrdec_vals.append(temp_arr if temp_arr else baseVal)
            #print(f"_____________________________{arrdec_vals}")

            classReturn.append(self.curr_scope.set_array(arrdec_node.id_n.id_t["tokenName"], arrdec_vals, dtype=dtype, arr_info={'dimension': dim, 'size1': size_1, 'size2':size_2}, priv=priv, const = node.const_b))
        
        return classReturn

    # binary and unary operations
    def visit_node_bi_op(self, node):
        
        left_type, left_val, left_err = self.visit_node(node.left_n)
        right_type, right_val, right_err = self.visit_node(node.right_n)
        dtype = ('lit', 'int')

        if (left_type[0] == 'arr' and right_type[0] == 'object') or (left_type[0] == 'object' and right_type[0] == 'arr'):
            self.logError("Direct operations between entire arrays and objects are not allowed. Perform element-wise evaluations instead.", left_err)

        elif left_type[0] == 'arr' or right_type[0] == 'arr':
            if left_type[0] == 'arr' and right_type[0] == 'arr':
                err_n = left_err
            elif right_type[0] == 'arr':
                err_n = right_err
            else:
                err_n =left_err
            self.logError("Direct operations on entire arrays are not allowed. Access individual elements or use vectorized computations.", err_n)

        elif left_type[0] == 'object' or right_type[0] == 'object':
            if left_type[0] == 'object' and right_type[0] == 'object':
                err_n = left_err
            elif right_type[0] == 'object':
                err_n = right_err
            else:
                err_n =left_err
            self.logError("Direct operations on entire objects are not allowed. Access specific properties instead.", err_n)

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
                        self.logError(f"Type mismatch for string expression, expected a string for both operands, but got {right_type[1]}.", right_err)
                    else:
                        return (('lit', 'string'), (left_val or "") + (right_val or ""), left_err ) #or empty string for nontypes
                        # return (('lit', 'string'), None)
                elif left_type[1] in self.numtypes and right_type[1] in self.numtypes:
                    return (dtype, left_val + right_val, left_err)
                    # return (dtype, None)
                else:
                     self.logError(f"Type mismatch for arithmetic expression, expected numeric value (int, long, float, double) for both operands, but got {left_type[1]} and {right_type[1]}.", left_err)

            case '-':
                if left_type[1] in self.numtypes and right_type[1] in self.numtypes:
                    return (dtype, left_val - right_val, left_err)
                    # return (dtype, None)
                else:
                    self.logError(f"Type mismatch for arithmetic expression, expected numeric value (int, long, float, double) for both operands, but got {left_type[1]} and {right_type[1]}.", left_err)
            case '/':
                if right_val == 0: #todo
                    # print("(semantic)(dbg) ERROR: DIVIDE BY 0")
                    self.logError("Division by 0 is not allowed.", right_err)
                if left_type[1] in self.numtypes and right_type[1] in self.numtypes:
                    return (dtype, int(left_val / right_val), left_err)
                    # return (dtype, None)
                else:
                    self.logError(f"Type mismatch for arithmetic expression, expected numeric value (int, long, float, double) for both operands, but got {left_type[1]} and {right_type[1]}.", left_err)
            case '*':
                if left_type[1] in self.numtypes and right_type[1] in self.numtypes:
                    return (dtype, left_val * right_val, left_err)
                    # return (dtype, None)
                else:
                    self.logError(f"Type mismatch for arithmetic expression, expected numeric value (int, long, float, double) for both operands, but got {left_type[1]} and {right_type[1]}.", left_err)
            case '%':
                if dtype[1] in ['float', 'double'] or right_type[1] in ['float', 'double']:
                    self.logError("Type mismatch for arithmetic expression, modulo operation only supports whole numbers (int, long)", left_err)
                else:
                    if right_val == 0: #todo err
                        self.logError("Modulo by 0 is not allowed.", right_err)
                    if left_type[1] in self.numtypes and right_type[1] in self.numtypes:
                        return (dtype, left_val % right_val, left_err)
                        # return (dtype, None)
                    else:
                        self.logError(f"Type mismatch for arithmetic expression, expected numeric value (int, long, float, double) for both operands, but got {left_type[1]} and {right_type[1]}.", left_err)

            #relational
            case '==':
                if left_type[1] in self.numtypes:
                    if right_type[1] not in self.numtypes:
                        self.logError(f"Type mismatch for relational expression, numeric values can only be compared with other numeric values (int, long, float, double), but got {right_type[1]}.", right_err)
                elif left_type[1] == 'string':
                    if right_type[1] != 'string':
                        self.logError("Type mismatch for relational expression, strings an can only be compared with other strings.", right_err)
                elif left_type[1] == 'bool':
                    if right_type[1] != 'bool':
                        self.logError("Type mismatch for relational expression, bools can only be compared with other bools.", right_err)
                return (('lit', 'bool'), left_val == right_val, left_err)
                # return (('lit', 'bool'), None)
            
            case '!=':
                if left_type[1] in self.numtypes:
                    if right_type[1] not in self.numtypes:
                        self.logError(f"Type mismatch for relational expression, numeric values can only be compared with other numeric values (int, long, float, double), but got {right_type[1]}.", right_err)
                elif left_type[1] == 'string':
                    if right_type[1] != 'string':
                        self.logError("Type mismatch for relational expression, strings an can only be compared with other strings.", right_err)
                elif left_type[1] == 'bool':
                    if right_type[1] != 'bool':
                        self.logError("Type mismatch for relational expression, bools can only be compared with other bools.", right_err)
                return (('lit', 'bool'), left_val != right_val, left_err)
                # return (('lit', 'bool'), None)
            
            case '<':
                if left_type[1] not in self.numtypes or right_type[1] not in self.numtypes:
                    self.logError(f"Type mismatch for relational expression, expected numeric value (int, long, float, double) for both operands, but got {left_type[1]} and {right_type[1]}.", left_err)

                return (('lit', 'bool'), left_val < right_val, left_err)  
                # return (('lit', 'bool'), None)
            case '<=':
                if left_type[1] not in self.numtypes or right_type[1] not in self.numtypes:
                    self.logError(f"Type mismatch for relational expression, expected numeric value (int, long, float, double) for both operands, but got {left_type[1]} and {right_type[1]}.", left_err)

                return (('lit', 'bool'), left_val <= right_val, left_err)  
                # return (('lit', 'bool'), None)
            case '>':
                if left_type[1] not in self.numtypes or right_type[1] not in self.numtypes:
                    self.logError(f"Type mismatch for relational expression, expected numeric value (int, long, float, double) for both operands, but got {left_type[1]} and {right_type[1]}.", left_err)

                return (('lit', 'bool'), left_val > right_val, left_err)  
                # return (('lit', 'bool'), None)
            case '>=':
                if left_type[1] not in self.numtypes or right_type[1] not in self.numtypes:
                    self.logError(f"Type mismatch for relational expression, expected numeric value (int, long, float, double) for both operands, but got {left_type[1]} and {right_type[1]}.", left_err)

                return (('lit', 'bool'), left_val >= right_val, left_err)  
                # return (('lit', 'bool'), None)
            
            #logical
            case '&&':
                if left_type[1] != 'bool' or right_type[1] != 'bool':
                    self.logError(f"Type mismatch for logical expression, expected bool value for both operands, but got {left_type[1]} and {right_type[1]}.", left_err)

                return (('lit', 'bool'), left_val and right_val, left_err)
                # return (('lit', 'bool'), None)
            case '||':
                if left_type[1] != 'bool' or right_type[1] != 'bool':
                    self.logError(f"Type mismatch for logical expression, expected bool value for both operands, but got {left_type[1]} and {right_type[1]}.", left_err)

                return (('lit', 'bool'), left_val or right_val, left_err)
                # return (('lit', 'bool'), None)

    #unary ops
    def visit_node_un_op(self, node):
        right_type, right_val, right_err = self.visit_node(node.id_right_n)
        left_err = ErrorNode(node.left_t["tokenLine"], node.left_t["tokenCol"] - len(node.left_t["tokenName"])-1)
        match node.left_t["tokenName"]:
            case '!':
                if right_type[1] != 'bool':
                    self.logError(f"Type mismatch for logical expression, expected bool value for operand, but got {right_type[1]}.", right_err)
                return (('lit', 'bool'), not right_val, left_err)
                # return (('lit', 'bool'), None)
            case '-':
                if right_type[1] not in self.numtypes:
                    self.logError(f"Type mismatch for arithmetic expression, expected numeric value (int, long, float, double), but got {right_type[1]}.", right_err)

                adjusted_type = right_type
                match (-right_val):
                    case self.MIN_INT: 
                        if right_type[1] == "long":
                            adjusted_type = (right_type[0], "int")
                    
                    case self.MIN_LONG:
                        if right_type[1] == "double":
                            adjusted_type = (right_type[0], "long")

                return (adjusted_type, -right_val, left_err)
                # return (right_type, None)
            case '++':
                if right_type[1] not in ["int", "long"]:
                    self.logError(f"Type mismatch for increment operation, expected numeric variable (int, long, float, double), but got {right_type[1]}.", right_err)
                self.curr_scope.syms[node.id_right_n.id_t["tokenName"]]["value"] += 1
                return (right_type, right_val + 1, left_err)
                # return (right_type, None)
            case '--':
                if right_type[1] not in ["int", "long"]:
                    self.logError(f"Type mismatch for decrement operation, expected numeric variable (int, long, float, double), but got {right_type[1]}.", right_err)
                self.curr_scope.syms[node.id_right_n.id_t["tokenName"]]["value"] -= 1
                return (right_type, right_val - 1 , left_err)
                # return (right_type, None)
        
        if node.left_t["tokenName"] in ["bool", "string", "int", "long", "double", "float"]:
            if right_type[1] not in ["bool", "string", "int", "long", "double", "float"]:
                self.logError(f'{node.id_right_n.id_t["tokenName"]} cannot be typecasted.', right_err)
            match node.left_t["tokenName"] :
                case 'bool':
                    match right_type[1]:
                        case 'bool':
                            return (('lit', 'bool'), right_val, left_err)
                        case 'string':
                            return (('lit', 'bool'), right_val != '', left_err)
                        case 'int':
                            return (('lit', 'bool'), right_val != 0, left_err)
                        case 'long':
                            return (('lit', 'bool'), right_val != 0, left_err)
                        case 'float':
                            return (('lit', 'bool'), right_val != 0.0, left_err)
                        case 'double':
                            return (('lit', 'bool'), right_val != 0.0, left_err)
                    # return (('lit', 'bool'), None)
                case 'string':
                    return (('lit', 'string'), str(right_val), left_err)
                    # return (('lit', 'string',), None)
                case 'int':
                    match right_type[1]:
                        case 'bool':
                            return (('lit', 'int'), int(right_val), left_err)
                        case 'string':
                            self.logError(f'Strings cannot be casted into integers.', right_err)

                        case 'int':
                            return (('lit', 'int'), right_val, left_err)
                        case 'long':
                            if right_val <= self.MAX_INT and right_val >= self.MIN_INT:
                                return (('lit', 'int'), right_val, left_err )
                            else:
                                self.logError(f'Value {right_val} is out of integer range.', right_err)
                        case 'float':
                            return (('lit', 'int'), int(right_val), left_err)
                        case 'double':
                            if int(right_val) <= self.MAX_INT and int(right_val) >= self.MIN_INT:
                                return (('lit', 'int'), right_val, left_err)
                            else:
                                self.logError(f'Value {right_val} is out of integer range.', right_err)
                case 'long':
                    match right_type[1]:
                        case 'bool':
                            return (('lit', 'long'), int(right_val), left_err)
                        case 'string':
                            self.logError(f'Strings cannot be casted into long.', right_err)
                        case 'int':
                            return (('lit', 'long'), right_val, left_err)
                        case 'long':
                            return (('lit', 'long'), right_val, left_err)
                        case 'float':
                            return (('lit', 'long'), int(right_val), left_err)
                        case 'double':
                            return (('lit', 'long'), int(right_val), left_err)
                case 'float':
                    match right_type[1]:
                        case 'bool':
                            return (('lit', 'float'), Decimal(right_val), left_err)
                        case 'string':
                            self.logError(f'Strings cannot be casted into float.', right_err)
                        case 'int':
                            return (('lit', 'float'), Decimal(right_val), left_err)
                        case 'long':
                            if right_val <= self.MAX_FLOAT and right_val >= self.MIN_FLOAT:
                                return (('lit', 'float'), Decimal(right_val), left_err)
                            else:
                                self.logError(f'Value {right_val} is out of float range.', right_err)
                        case 'float':
                            return (('lit', 'float'), right_val, left_err)
                        case 'double':
                            if right_val <= self.MAX_FLOAT and right_val >= self.MIN_FLOAT:
                                return (('lit', 'float'), right_val, left_err)
                            else:
                                self.logError(f'Value {right_val} is out of float range.', right_err)
                case 'double':
                    match right_type[1]:
                        case 'bool':
                            return (('lit', 'double'), Decimal(right_val), left_err)
                        case 'string':
                            self.logError(f'Strings cannot be casted into double.', right_err)
                        case 'int':
                            return (('lit', 'double'), Decimal(right_val), left_err)
                        case 'long':
                            return (('lit', 'double'), Decimal(right_val), left_err)
                        case 'float':
                            return (('lit', 'double'), right_val, left_err)
                        case 'double':
                            return (('lit', 'double'), right_val, left_err)
                        
    def visit_node_post_un_op(self, node):
        left_type, left_val, left_err = self.visit_node(node.id_left_n)
        iden_name = node.id_left_n.id_t["tokenName"]
        if not self.curr_scope.get(iden_name):
            self.logError(f"Symbol '{node.id_t["tokenName"]}' hasn't been declared yet.", node.id_left_n, left_err)
        
        match node.right_t["tokenName"]:
            case '++':
                print(f"LLLLLEEEEEFFFFTTT: {left_type[1]}")
                if left_type[1] not in ["int", "long"]:
                    self.logError(f"Type mismatch for increment operation, expected whole numeric variable (int, long), but got {left_type[1]}.", left_err)
                self.curr_scope.syms[node.id_left_n.id_t["tokenName"]]["value"] += 1
                return (left_type, left_val, left_err)
                # return (left_type, None)
            case '--':
                print(f"LLLLLEEEEEFFFFTTT: {left_type[1]}")
                if left_type[1] not in ["int", "long"]:
                    self.logError(f"Type mismatch for decrement operation, expected whole numeric variable (int, long), but got {left_type[1]}.", left_err)
                self.curr_scope.syms[node.id_left_n.id_t["tokenName"]]["value"] -= 1
                return (left_type, left_val, left_err)
            
    def visit_node_pre_un_op(self, node):
        right_type, right_val, right_err = self.visit_node(node.iden_n)
        left_err = ErrorNode(node.left_t["tokenLine"], node.left_t["tokenCol"] - len(node.left_t["tokenName"])-1)
        iden_name = node.iden_n.id_t["tokenName"]

        if not self.curr_scope.get(iden_name):
            self.logError(f"Symbol '{node.id_t["tokenName"]}' hasn't been declared yet.", right_err)

        match node.left_t["tokenName"]:
            case '++':
                print(f"RRRRRRRIIIIIIIIGHT: {right_type[1]}")
                if right_type[1] not in ["int", "long"]:
                    self.logError(f"Type mismatch for increment operation, expected whole numeric variable (int, long), but got {right_type[1]}.", right_err)
                self.curr_scope.syms[node.iden_n.id_t["tokenName"]]["value"] += 1
                return (right_type, right_val + 1, left_err)
                # return (right_type, None)
            case '--':
                print(f"RRRRRRRIIIIIIIIGHT: {right_type[1]}")
                if right_type[1] not in ["int", "long"]:
                    self.logError(f"Type mismatch for decrement operation, expected whole numeric variable (int, long), but got {right_type[1]}.", right_err)
                self.curr_scope.syms[node.iden_n.id_t["tokenName"]]["value"] -= 1
                return (right_type, right_val - 1, left_err)
                # return (right_type, None)
                    
    def visit_node_loop_stmt(self, node):
        node_loop = node.loop_stmt_n
        loop_name = type(node_loop).__name__
        self.loop_depth += 1

        self.enter_scope(loop_name)
        if loop_name == 'node_forloop':    
            self.visit_node(node_loop.init_arg_n)
            
            self.visit_node(node_loop.condition_n)
            print(f"CONDITION was found from: {loop_name}")
            #print(f"(semantic)(dbg) FOUND CONDITION for {loop_name} -> {node_loop.condition_n.condition_value_n} = {self.visit_node(node_loop.condition_n.condition_value_n)}")
            
            self.visit_node(node_loop.inc_arg_n, funcExpectedVal=False) 
            self.visit_node(node_loop.ctrl_stmt_body_n)

        elif loop_name == 'node_while' or loop_name == 'node_do':
            self.visit_node(node_loop.condition_n)
            print(f"CONDITION was found from: {loop_name}")
            #print(f"(semantic)(dbg) FOUND CONDITION for {loop_name} -> {node_loop.condition_n.condition_value_n} = {self.visit_node(node_loop.condition_n.condition_value_n)}")
            
            self.visit_node(node_loop.ctrl_stmt_body_n)

        elif loop_name == 'node_repeat':
            repeat_type, repeat_val, err_n = self.visit_node(node_loop.repeat_value_n)
            
            if repeat_type[1] not in ['int', 'long']:
                self.logError(f"Invalid data type for repeat value. Expected 'int' or 'long', but found '{repeat_type[1]}' instead.", err_n)
            
            if repeat_val < 0:
                self.logError(f"Invalid value for repeat statement. Expected positive 'int' or 'long' values, but found '{repeat_val}' instead.", err_n)
            
            print(f"(semantic)(dbg) FOUND REPEAT VALUE -> {node_loop.repeat_value_n} = {repeat_type}, {repeat_val}")
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
    #             value = Decimal(user_input)
    #         elif expected_dtype == 'double':
    #             value = Decimal(`user_input)
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

        # print(f"(semantic)(dbg) Expected Data Type: {expected_dtype}")

        if expected_dtype not in ["int", "long", "float", "double", "string", "bool"]:
            self.logError(f"Unsupported data type for input: {expected_dtype}", node)
            return None
        value = self.default_vals[expected_dtype]
        print(f"RETURNED FROM NODE_INPUT: {(('lit', expected_dtype), value)}")
        return (('lit', expected_dtype), value, None)
    
    def visit_node_output(self, node):
        print_stmts_n = node.print_stmts_n 
        print_params_n = node.print_params_n  

        # if not print_params_n:
        #     self.logError("Output statement requires at least one parameter (format string).")
        #     return None
        first_param = print_params_n[0]
        first_param_type, first_param_val, err_n = self.visit_node(first_param)
        formatted_output = ""

        if first_param_type is None or first_param_type[1] != "string":
           # self.logError("First parameter in output statement must be a string (format string).", first_param)
            if len(print_params_n) > 1:
                self.logError("Print statements can only have one parameter, unless a string with format specifiers is used in the first parameter.", err_n)
            formatted_output = str(first_param_val)

        # check if any of the parameters are entire arrays, entire objects, classnames, function reference (just the func name)
        for param in print_params_n:
            param_type, param_value, err_n = self.visit_node(param)
            for i, param in enumerate(print_params_n):
                param_type, param_value, err_n  = self.visit_node(param)
                # entire arrays and objects are not allowed as direct output
                if param_type[0] == 'arr':
                    self.logError(f"(Output Parameter {i+1}) Direct output of entire arrays is not allowed. Access specific elements instead.", err_n)
                    return None
                elif param_type[0] == 'object':
                    self.logError(f"(Output Parameter {i+1}) Direct output of entire objects is not allowed. Access specific properties instead.", err_n)
                    return None
                formatted_output += str(param_value)
        
            # return None
        else:
            format_specifiers = self._extract_format_specifiers(str(first_param_val))
            
            if len(format_specifiers) != len(print_params_n) - 1:
                if not format_specifiers:
                    self.logError(f"String '{first_param_val}' does not contain any format specifiers.", err_n)
                else:
                    self.logError(f"Number of format specifiers ({len(format_specifiers)}) does not match number of parameters ({len(print_params_n) - 1}).", err_n)
                    return None

            formatted_output = first_param_val
            for i, specifier in enumerate(format_specifiers):
                param_node = print_params_n[i + 1] 
                param_type, param_value, err_n  = self.visit_node(param_node)

            
                if not self._validate_format_specifier(specifier, param_type[1]):
                    err_n = ErrorNode(first_param.id_t["tokenLine"], first_param.id_t["tokenCol"] - len(first_param.id_t["tokenName"]) - 1)
                    self.logError(f"Format specifier '{specifier}' does not match argument {i+1} of type '{param_type[1]}'.", err_n)
                    return None
                formatted_output = formatted_output.replace(specifier, str(param_value), 1)

        if print_stmts_n == "println":
            print(f'\n\n(semantic)(OUTUPT)\t{formatted_output}\n\n') #TEMPORARY 
        else:
            print(f'\n\n(semantic)(OUTUPT)\t{formatted_output}\n\n', end='') #TEMPORARY

        return None

    def _extract_format_specifiers(self, format_string):
        import re
        return re.findall(r'%[sdf]|%l[df]', format_string or "")  # matches %s, %d, %f, %ld, %lf
                                                        #or statement so that we dont throw an exeption on None returns

    def _validate_format_specifier(self, specifier, param_type):
        if specifier == "%s":
            return param_type == "string"
        elif specifier == "%d":
            return param_type == "int"
        elif specifier == "%ld":
            return param_type == "long"
        elif specifier == "%f":
            return param_type == "float"
        elif specifier == "%lf":
            return param_type == "double"
        else:
            return False
    # def visit_node_output(self, node):
    #     print_stmts_n = node.print_stmts_n 
    #     print_params_n = node.print_params_n  

    #     if not print_params_n:
    #         self.logError("Output statement requires at least one parameter.", node)
    #         return None

    #     first_param = print_params_n[0]
    #     first_param_type, _ = self.visit_node(first_param)

    #     # if first_param_type != "string":
    #     #     self.logError("First parameter in output statement must be a string.", first_param)
    #     #     return None
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
    
    # ALEX HERE
    def visit_node_ctrl_stmt_body(self, node):
        self.enter_scope(type(node).__name__)
        statements_n = node.statements_n
        
        for statement in statements_n:
            ctrl_stmt = type(statement).__name__

            if ctrl_stmt == "node_break_stmt":
                err_n = ErrorNode(statement.id_t["tokenLine"], statement.id_t["tokenCol"] - len(statement.id_t["tokenName"]) - 1)
                if self.loop_depth == 0 and self.switch_depth == 0:
                    self.logError("'break' statement may only be used within the scope of a 'loop' or 'switch' statement.", err_n)
                print("(semantic)(dbg) FOUND 'break' !!!")
                continue
            
            elif ctrl_stmt == "node_continue_stmt":
                err_n = ErrorNode(statement.id_t["tokenLine"], statement.id_t["tokenCol"] - len(statement.id_t["tokenName"]) - 1)
                if self.loop_depth == 0:
                    self.logError("'continue' statement may only be used within the scope of a 'loop' statement.", err_n)
                print("(semantic)(dbg) FOUND 'continue' !!!")
                continue
            
            else:
                self.visit_node(statement)

        print("(semantic)(dbg) EXITING scope 'ctrl_stmt_body', TABLE: ")
        self.exit_scope(type(node).__name__)
        return
    
    def visit_node_condition_value(self, node):
        condition = self.visit_node(node.condition_value_n)
        err_n = condition[2]

        if condition[0][1] != 'bool':
            self.logError(f"Invalid data type for loop condition. Expected 'bool', but found '{condition[0][1]}' instead.", err_n)
        print(f"(semantic)(dbg) FOUND CONDITION for {type(node).__name__} -> {node.condition_value_n} = {self.visit_node(node.condition_value_n)[0]}, {self.visit_node(node.condition_value_n)[1]}")

        return

    def visit_node_if_stmt(self, node):
        self.enter_scope(type(node).__name__)

        self.visit_node(node.condition_n)
        print(f"CONDITION was found from: {type(node).__name__}")

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
        
        switch_type, switch_val, err_n = self.visit_node(node.value_n)
        if switch_type[1] not in ["string", "int", "long"]:
            self.logError("Invalid data type for 'switch' value. Expected: 'string', 'int', 'long' data types.", err_n)
        
        # CASE
        case_n = node.case_n
        case_value_list = []

        for case_stmt in case_n.case_stmt_n:

            self.enter_scope(case_stmt)
            case_type, case_val, err_n = self.visit_node(case_stmt.case_value_n)

            if case_val in case_value_list:
                self.logError(f"'switch' statement already contains case value '{case_val}'.", err_n)
            
            if case_type[1] != switch_type[1]:
                if (switch_type[1] != "long") and (case_type[1] != "int"):
                    self.logError(f"'switch' value and 'case' value must be of the same data type. Expected: '{switch_type[1]}' data type for case value, but got '{case_type[1]}'.", err_n)

            case_value_list.append(case_val)
            print(f"(semantic)(dbg) FOUND CASE VALUE: '{case_val}'")

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
                rettype, result, err_n = self.visit_node(node.ret_value_n)
                print(f"RETURN VALUE: {result}\n RETTYPE: {rettype}")
                if rettype[0] == 'arr':
                    self.logError(f"Function '{self.current_function_name}' cannot return an array.", err_n)
                
                if rettype[0] == 'object':
                    self.logError(f"Function '{self.current_function_name}' cannot return an object.", err_n)

                #TODO: add class error
                actual_return_type = self.visit_node(node.ret_value_n)[0][1]

                match(expected_return_type):
                    case "void":
                        self.logError(f"Function '{self.current_function_name}' is void and cannot return a value.", err_n)
                    
                    case "int":
                        if actual_return_type not in ["string", "bool"]:
                            if result > self.MAX_INT or result < self.MIN_INT:
                               self.logError(f"Value '{result}' is out of 'int' range for 'return' value.", err_n)
                        
                        if expected_return_type != actual_return_type:    
                            self.logError(f"Function '{self.current_function_name}' must return a value of type '{expected_return_type}', but got '{actual_return_type}'.", err_n)  
            
                    case "long":
                        if actual_return_type not in ["string", "bool"]:
                            if result > self.MAX_LONG or result < self.MIN_LONG:
                                self.logError(f"Value '{result[1]}' is out of 'long' range for 'return' value.", err_n)
                        
                        if expected_return_type != actual_return_type:
                            if actual_return_type != "int":
                                self.logError(f"Function '{self.current_function_name}' must return a value of type '{expected_return_type}', but got '{actual_return_type}'.", err_n)
            
                    case "float":
                        if actual_return_type not in ["string", "bool"]:
                            if result > self.MAX_FLOAT or result < self.MIN_FLOAT:
                                self.logError(f"Value '{result[1]}' is out of 'float' range for 'return' value.", err_n)
                        
                        if expected_return_type != actual_return_type:
                            if actual_return_type != "int":
                                self.logError(f"Function '{self.current_function_name}' must return a value of type '{expected_return_type}', but got '{actual_return_type}'.", err_n)

                    case "double":
                        if actual_return_type not in ["string", "bool"]:
                            if result > self.MAX_DOUBLE or result < self.MIN_DOUBLE:
                                self.logError(f"Value '{result[1]}' is out of 'double' range for 'return' value.", err_n)
                        
                        if expected_return_type != actual_return_type:
                            if actual_return_type not in ["int", "float", "long"]:
                                self.logError(f"Function '{self.current_function_name}' must return a value of type '{expected_return_type}', but got '{actual_return_type}'.", err_n)

                    case _:
                        if expected_return_type != actual_return_type:
                            self.logError(f"Function '{self.current_function_name}' must return a value of type '{expected_return_type}', but got '{actual_return_type}'.", err_n)

                return result
            else:
                if expected_return_type != "void":
                    self.logError(f"Function '{self.current_function_name}' must return a value of type '{expected_return_type}', but got none.", err_n)

    def check_return_in_body(self, node):
        print(f"(semantic)(dbg) Checking return in {type(node).__name__}")

        if node is None:
            return False

        if isinstance(node, node_body):
            return self.check_return_in_body(node.body_codeblock_n) or self.check_return_in_body(node.return_stmt_n)

        if isinstance(node, node_code_block):
            return any(self.check_return_in_body(stmt) for stmt in node.code_block_statement_n)

        if isinstance(node, node_ctrl_stmt_body):
            return any(self.check_return_in_body(stmt) for stmt in node.statements_n)

        if isinstance(node, node_if_stmt):
            print(f"(semantic)(dbg) Checking return in IF statement")

            has_return_in_if = self.check_return_in_body(node.body_n)
            has_return_in_else = False

            if node.else_chain_n:
                has_return_in_else = self.check_return_in_body(node.else_chain_n)

            print(f"(semantic)(dbg) has_return_in_if={has_return_in_if}, has_return_in_else={has_return_in_else}")

            return has_return_in_if and has_return_in_else 

        if isinstance(node, node_else_stmt):
            return self.check_return_in_body(node.body_n)

        if isinstance(node, node_else_chain):
            return any(self.check_return_in_body(stmt) for stmt in node.else_chain_n)

        if isinstance(node, node_loop_stmt):
            return self.check_return_in_body(node.loop_stmt_n.ctrl_stmt_body_n)

        if isinstance(node, node_switch_stmt):
            print(f"(semantic)(dbg) Checking return in SWITCH statement")

            case_returns = [self.check_return_in_body(case) for case in node.case_n.case_stmt_n]

            has_default = node.default_n is not None
            has_return_in_default = self.check_return_in_body(node.default_n) if has_default else False

            print(f"(semantic)(dbg) Switch case returns: {case_returns}, has_default={has_default}, has_return_in_default={has_return_in_default}")

            if not all(case_returns) or (has_default and not has_return_in_default):
                return False

            return True 

        if isinstance(node, node_case_stmt):
            return self.check_return_in_body(node.ctrl_stmt_body_n)

        if isinstance(node, node_default_stmt):
            return self.check_return_in_body(node.ctrl_stmt_body_n)

        if isinstance(node, node_return_block):
            print(f"(semantic)(dbg) Found return statement")
            self.count_return += 1
            return True

        return False