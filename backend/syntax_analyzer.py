from lexical_analyzer import Token

#-------------------- PREDICT SETS --------------------
PREDICT_SETS = {
    "program":["import", "Identifier", "const", "void", "bool", "string", "int", "long", "float", "double", "private", "class"],
    "imports_rec": ["import", "private", "class", "int", "long", "bool", "float", "double", "string", "const", "void", "Identifier"],
    "std_lib": ["Cmath", "Cstring", "Carray"],
    "program_constructs": ["private", "class", "int", "long", "bool", "float", "double", "string", "const", "void", "Identifier"],
    "data_type": ["bool", "string", "int", "long", "double", "float"],
    "class_body": [ "private" , "const", "int", "long", "bool", "float", "double", "string" , "void"],
    "print_stmts" : ["print", "println"],
    "conditional_stmt" : ["if", "switch"],
    "loop_stmt" : ["for", "while", "do", "repeat"],
    "unary_operator" : ["++", "--", "Identifier"],
    "init_arg" : ["Identifier", "bool", "string", "int", "long", "double", "float"],
    "switch_value" : ["whole_lit", "string_lit", "Identifier", "(", "-"], # TO ADD other exps
    "ctrl_stmt_body" : ["break", "continue"], 
    "arith_operator" : ["+", "-", "*", "/", "%"],
    "inc_arg" : ["Identifier", "--", "++", "print", "println"],
    "func_arg" : ["!", "(", "++", "-", "--", "Identifier", "bool_lit", "frac_lit", "in", "string_lit", "whole_lit", ")"],
    "value":["!", "(", "++", "-", "--", "Identifier", "bool_lit", "frac_lit", "in", "string_lit", "whole_lit"],
    "rel_operator" : ["==", "!=", "<", "<=", ">", ">="],
    "logic_operator" : ["&&", "||"],
    "iden_mods" : ["(", "[", "."],  # TO ADD 
    "int_val" : ["whole_lit", "Identifier", "-", "(", "in"],
    "lit_type": ["whole_lit", "frac_lit", "string_lit", "bool_lit"],
    "assign_operator" : ["=", "+=", "-=", "*=", "/=", "%="],
    "var_init": ["=", ",", ";"],
    "string_value": ["string_lit", "Identifier", "(", "in"],
    "expression":["!", "(", "++", "-", "--", "Identifier", "bool_lit", "frac_lit", "in", "string_lit", "whole_lit"],
    "output":["print", "println"],
    "code_block": [ "const", "++", "--", "Identifier", "bool", "const", "do", "double", "float", "for", "if", "int", "long", "print", "println", "repeat", "string", "switch", "while" ],
    "iden_as_var_mods": ["[","."],
    "body": [],  # Placeholder for now
    "add_min_cont":["+", "-"],
    "mult_div_modulo_cont":["*", "/", "%"],
    "atom":["in", "--", "++", "Identifier", "bool_lit", "whole_lit", "frac_lit", "string_lit"],
    "mods_post_op":["[", "(", "++", "--", "."],
    "iden_dec": [ "const", "void", "bool", "string", "int", "long", "double", "float" ],
    "iden_dec_cont": [ "=", ",", "[" ],
    "term_join_operators": ["+", "-", "*", "/", "%", "==", "!=", "<", "<=", ">", ">=", "&&", "||"],
    "class_as_func_post": ["Identifier", "++", "--", ],
    "assign_func_method_mods": ["[", "(", ".",],
    "assign_func_method_mods_cont": ["[", "("],
    "inc_arg_post": ["++", "--"],
    "case_value": ["whole_lit", "string_lit", "-"],
    "input_params": ["string_lit"]
}
PREDICT_SETS["body"] = PREDICT_SETS["code_block"] + ["return"]  #bruh
PREDICT_SETS["ctrl_stmt_body"] = PREDICT_SETS["ctrl_stmt_body"] + PREDICT_SETS["body"] #bruh pt.2
PREDICT_SETS["assign_func_method_mods"] = PREDICT_SETS["assign_func_method_mods"]+ PREDICT_SETS["assign_operator"]
PREDICT_SETS["class_as_func_post"] = PREDICT_SETS["class_as_func_post"] + PREDICT_SETS["assign_func_method_mods"] 

# reminders for predict sets:
 
# two ways to use predict sets errors (u may add mroe)
#    - for general errors: use matchPredictSet( for general errors (like may unexpected token for a specific part of the grammar, this method will generate the general error na)
#    - for custom errors: just use " in PREDICT_SETS["<non_terminal>"]  "  this will return true/false then use a custom error nalang sa else

# note: not every prod have to use predict sets cos some of em just branch to 1 token

#---------------FOR CHECKNG DTYPE------------
MIN_INT = -2147483648
MAX_INT = 2147483647
MIN_LONG = -9223372036854775808
MAX_LONG = 9223372036854775807
MIN_FLOAT = -999999990.0
MAX_FLOAT = 999999990
MIN_DOUBLE = -9999999999999999000
MAX_DOUBLE = 9999999999999999000

def typeFracLit(frac_lit):
    if len(frac_lit.split('.')[1]) < 8:
        return "float"
    elif len(frac_lit.split('.')[1]) < 16:
        return "double"
    else:
        return "err"
    

#-----------------AST FOR VALUE------------------
# #_t suffix = token, #_n suffix = node
#----------------NODE OBJECTS---------------------
class node_num:
    def __init__(self, val_t):
        self.val_t = val_t
        if (self.val_t["tokenType"] == "whole_lit"):
            if int(self.val_t["tokenName"]) >= MIN_INT and int(self.val_t["tokenName"]) <= MAX_INT:
                self.dtype = "int"
            elif int(self.val_t["tokenName"]) >= MIN_LONG and int(self.val_t["tokenName"]) <= MAX_LONG:
                self.dtype = "long"
            else:
                self.dtype = "err"
        elif (self.val_t["tokenType"] == "frac_lit"):
            if float(self.val_t["tokenName"]) >= MIN_FLOAT and float(self.val_t["tokenName"]) <= MAX_FLOAT:
                self.dtype = typeFracLit(self.val_t["tokenName"])
            elif float(self.val_t["tokenName"]) >= MIN_DOUBLE and float(self.val_t["tokenName"]) <= MAX_DOUBLE:
                    self.dtype = "double" if typeFracLit(self.val_t["tokenName"]) != "err" else "err"
            else:
                self.dtype = "err"
            
    def __repr__(self):
        return self.val_t["tokenName"]

class node_str:
    def __init__(self, val_t):
        self.val_t = val_t
        self.dtype = "string"
    def __repr__(self):
        return self.val_t["tokenName"]

class node_bool:
    def __init__(self, val_t):
        self.val_t = val_t
        self.dtype = "boolean"
    def __repr__(self):
        return self.val_t["tokenName"]

class node_iden:
    def __init__(self, id_t):
        self.id_t = id_t
        # self.type = sema.curr_scope.get(id_t["tokenName"])["dtype"]
    def __repr__(self):
        return self.id_t["tokenName"]

class node_func_call:
    def __init__(self, id_n, args_n = None):
        self.id_n = id_n
        self.args_n = args_n
    def __repr__(self):
        return f'{self.id_n}({self.args_n})'

class node_arr_idx:
    def __init__(self, id_n, idx_n, idx2_n = None):
        self.id_n = id_n
        self.idx_n = idx_n
        self.idx2_n = idx2_n
    def __repr__(self):
        return f'{self.id_n}[{self.idx_n}]' + (f'[{self.idx2_n}]' if self.idx2_n else '') 

class node_class_att:
    def __init__(self, id_n, att_n):
        self.id_n = id_n
        self.att_n = att_n
    def __repr__(self):
        return f'{self.id_n}.{self.att_n}'

class node_class_func_call:
    def __init__(self, id_n, att_n, args_n = None):
        self.id_n = id_n
        self.att_n = att_n
        self.args_n = args_n
    def __repr__(self):
        return f'{self.id_n}.{self.att_n}({self.args_n})'

class node_class_arr_idx:
    def __init__(self, id_n, att_n, idx_n, idx2_n = None):
        self.id_n = id_n
        self.att_n = att_n
        self.idx_n = idx_n
        self.idx2_n = idx2_n
    def __repr__(self):
        return f'{self.id_n}.{self.att_n}[{self.idx_n}]' + (f'[{self.idx_n}]' if self.idx2_n else '')

class node_func_args:
    def __init__(self, args_n, args_rec_n = None):
        self.args_n = args_n
        self.args_rec_n = args_rec_n
    def __repr__(self):
        return f'{self.args_n}' + f', {self.args_rec_n}' if self.args_rec_n else ''
        
class node_bi_op:
    def __init__(self, left_n, op_t, right_n):
        self.left_n = left_n
        self.op_t = op_t
        self.right_n = right_n
    def __repr__(self):
        return f'node_bi_op: ({self.left_n} {self.op_t["tokenName"]} {self.right_n})'

class node_un_op:
    def __init__(self, left_t, id_right_n):
        self.left_t = left_t
        self.id_right_n = id_right_n
    def __repr__(self):
        return f'node_un_op: (unary_op: {self.left_t["tokenName"]}, id_n: {self.id_right_n})'

class node_post_un_op:
    def __init__(self, id_left_n, right_t):
        self.id_left_n = id_left_n
        self.right_t = right_t
    def __repr__(self):
        return f'node_post_un_op: (id_n: {self.id_left_n}, unary_op: {self.right_t["tokenName"]})'

class node_pre_un_op:
    def __init__(self, left_t, iden_n):
        self.left_t = left_t
        self.iden_n = iden_n
    def __repr__(self):
        return f'node_pre_un_op: (unary_op: {self.left_t["tokenName"]}, id_n: {self.iden_n})'

class node_input:
    def __init__(self, type_t, prompt_n = None, count_n = None):
        self.type_t = type_t
        self.prompt_n = prompt_n
        self.count_n = count_n
    def __repr__(self):
        return f'in<{self.type_t}>({self.prompt_n}, {self.count_n})'

class node_vardec:
    def __init__ (self, const_b, dtype_t, id_n, vardec_cont_n):
        self.const_b = const_b
        self.dtype_t = dtype_t
        self.id_n = id_n
        self.vardec_cont_n = vardec_cont_n
    def __repr__(self):
        return f'node_vardec: \n\t(const_b: {self.const_b}, dtype_t: {self.dtype_t["tokenName"]}, id_n: {self.id_n}, {self.vardec_cont_n})'

class node_vardec_cont:
    def __init__(self, value_n, idec_rec_n):
        self.value_n = value_n
        self.idec_rec_n = idec_rec_n
    
    def __repr__(self):
        return f"node_vardec_cont: (value_n: {self.value_n}, \n\tidec_rec_n: {self.idec_rec_n})\n"

class node_idec_rec_stmt:
    def __init__(self, id_n, value_n):
        self.id_n = id_n
        self.value_n = value_n

    def __repr__(self):
        return f"\n\t(id_n: {self.id_n}, value_n: {self.value_n})"

class node_idec_rec:
    def __init__(self, node_idec_rec_stmt_n):
        self.node_idec_rec_stmt_n = node_idec_rec_stmt_n

    def __repr__(self):
        statements = ",\n".join(map(str, self.node_idec_rec_stmt_n))    
        return f"{self.__class__.__name__}(\n{statements}\n\n)"

class node_arr_dec:
    def __init__(self, dtype_t, id_n, size1_n, size2_n, arr_dec_cont_n):
        self.size1_n = size1_n
        self.size2_n = size2_n
        self.arr_dec_cont_n = arr_dec_cont_n

    def __repr__(self):
        if all(isinstance(elem, node_arr_dec_rec) for elem in self.arr_dec_cont_n):
            # Case 1: List of node_arr_dec_rec objects → Format with newlines
            arr_dec_str = ",\n\t".join(str(elem) for elem in self.arr_dec_cont_n)

        elif all(isinstance(elem, list) for elem in self.arr_dec_cont_n):
            # Case 3: 2D List (List of lists of numbers) → Format each inner list with newlines
            arr_dec_str = "values: " + ",\n\t".join(str(sublist) for sublist in self.arr_dec_cont_n)

        else:
            # Case 2: Regular list of numbers → Format as a normal list
            arr_dec_str = "values: " + str(self.arr_dec_cont_n)
        return f"node_arr_dec: (size1_n: {self.size1_n}, size2_n: {self.size2_n}, arr_dec_cont_n: {arr_dec_str})"

class node_arr_dec_rec:
    def __init__(self, id_n, size1_n, size2_n):
        self.id_n = id_n
        self.size1_n = size1_n
        self.size2_n = size2_n
    
    def __repr__(self):
        return f"(id_n: {self.id_n}, size1_n: {self.size1_n}, size2_n: {self.size2_n})"

class node_func_dec:
    def __init__(self, dtype_t, iden_n, params_n, body_n, is_std_lib = False):
        self.dtype_t = dtype_t
        self.iden_n = iden_n
        self.params_n = params_n
        self.body_n = body_n
        self.is_std_lib = is_std_lib
    def __repr__(self):
        return f"node_func_dec: (\n\tdtype_t: {self.dtype_t["tokenName"]}, id_n: {self.iden_n}, params_n: {self.params_n}, body_n: {self.body_n}, is_std_lib: {self.is_std_lib})"

class node_funcpar_class:
    def __init__(self, class_id_n, obj_id_n):
        self.class_id_n = class_id_n
        self.obj_id_n = obj_id_n
    def __repr__(self):
        return f"node_funcpar_class: (class_id_n: {self.class_id_n}, obj_id_n: {self.obj_id_n}"

class node_funcpar_arr:
    def __init__(self, dtype_t, id_n, arrdim_i):
        self.dtype_t = dtype_t
        self.id_n = id_n
        self.arrdim_i = arrdim_i
    
    def __repr__(self):
        return f"node_funcpar_arr: (dtype_t: {self.dtype_t["tokenName"] if self.dtype_t else 'None'}, id_n: {self.id_n}, arr_dim_i: {self.arrdim_i if self.arrdim_i else 'None'})"

class node_funcpar_var:
    def __init__(self, dtype_t, id_n):
        self.dtype_t = dtype_t
        self.id_n = id_n
    def __repr__(self):
        return f"node_funcpar_var: (dtype_t: {self.dtype_t["tokenName"]}, id_n: {self.id_n})"

class node_output:
    def __init__(self, print_stmts_n, print_params_n):
        self.print_stmts_n = print_stmts_n
        self.print_params_n = print_params_n
    def __repr__(self):
        return f'node_output: (print_stmts_n: {self.print_stmts_n}, print_params_n: {self.print_params_n})'

class node_body:
    def __init__(self,body_codeblock_n, return_stmt_n):
        self.body_codeblock_n = body_codeblock_n
        self.return_stmt_n = return_stmt_n
        
    def __repr__(self):
        return f'node_body: {{ body_codeblock_n: {self.body_codeblock_n}, \nbody_return_stmt_n: {self.return_stmt_n} }}\n'

class node_assign_func_method_mods:
    def __init__(self, iden_n, as_array_n, assign_stmt_op_n, func_arg_n, class_elem_iden_n, assign_func_method_mods_cont_n):
        self.iden_n = iden_n
        self.as_array_n = as_array_n
        self.assign_stmt_op_n = assign_stmt_op_n
        self.func_arg_n = func_arg_n
        self.class_elem_iden_n = class_elem_iden_n
        self.assign_func_method_mods_cont_n = assign_func_method_mods_cont_n

    def __repr__(self):
        attrs = {key: value for key, value in vars(self).items() if value is not None}
        attr_str = ", ".join(f"{key}: {value}" for key, value in attrs.items())
        return f"{self.__class__.__name__}({attr_str})"

class node_assign_func_method_mods_cont:
    def __init__(self, as_array_n, assign_stmt_op_n, func_arg_n):
        self.as_array_n = as_array_n
        self.assign_stmt_op_n = assign_stmt_op_n 
        self.func_arg_n = func_arg_n

    def __repr__(self):
        attrs = {key: value for key, value in vars(self).items() if value is not None}
        attr_str = ", ".join(f"{key}: {value}" for key, value in attrs.items())
        return f"{self.__class__.__name__}({attr_str})"

class node_return_block:
    def __init__(self, ret_value_n=None):
        self.ret_value_n = ret_value_n
    def __repr__(self):
        return f'node_return_block: (ret_value_n: {self.ret_value_n})'

class node_if_stmt:
    def __init__(self, condition_n, body_n, else_chain_n=None):
        self.condition_n = condition_n
        self.body_n = body_n
        self.else_chain_n = else_chain_n
    def __repr__(self):
        return f'node_if_stmt( \n{self.condition_n} \n ctrl_body_n( {self.body_n} ) {self.else_chain_n if self.else_chain_n else "node_else_chain( None )"}'

class node_else_chain:
    def __init__(self, else_stmt_n):
        self.else_stmt_n = else_stmt_n
    def __repr__(self):
        return f'\nnode_else_chain( {self.else_stmt_n} )'

class node_else_stmt:
    def __init__(self, body_n):
        self.body_n = body_n
    def __repr__(self):
        return f'node_else( \n ctrl_body_n( {self.body_n} ) \n)'

class node_ctrl_stmt_body:
    def __init__(self, statements_n):
        self.statements_n = statements_n
        
    def __repr__(self):
        return "\n\t" + "\n\t".join(map(str, self.statements_n))

#class node_break_stmt:
#    def __repr__(self):
#        return 'break;'

#class node_continue_stmt:
#    def __repr__(self):
#        return 'continue;'

class node_class_inst:
    def __init__(self, class_id_n, obj_id_n, class_instcont_n):
        self.class_id_n = class_id_n
        self.obj_id_n = obj_id_n
        self.class_instcont_n = class_instcont_n

    def __repr__(self):
        return (f"node_class_inst: (class_id_n: {self.class_id_n}, "
                f"obj_id_n: {self.obj_id_n}, "
                f"\nclass_instcont_n: {self.class_instcont_n})")

class node_classinst_cont:
    def __init__(self, class_id_n, func_arg_n):
        self.class_id_n = class_id_n
        self.func_arg_n = func_arg_n

    def __repr__(self):
        return f"node_classinst_cont: (class_id_n: {self.class_id_n}, func_arg_n: {self.func_arg_n})"

class node_class_dec:
    def __init__(self, is_private_b, class_id_n, constructor_dec_n, class_body_n):
        self.is_private_b = is_private_b
        self.class_id_n = class_id_n
        self.constructor_dec_n = constructor_dec_n
        self.class_body_n = class_body_n

    def __repr__(self):
        return (f"node_class_dec: (private_b: {self.is_private_b}, "
                f"class_id_n: {self.class_id_n}, "
                f"\n\tconstructor_dec_n: {self.constructor_dec_n},"
                f"\n\tclass_body_n: {self.class_body_n}) ")

class node_class_body:
    def __init__(self, class_body_stmt_n):
        self.class_body_stmt_n = class_body_stmt_n

    def __repr__(self):
        statements = ",\n\t".join(map(str, self.class_body_stmt_n))
        return f"{self.__class__.__name__}(\n\t\t{statements}\n)"
    
   

class node_class_body_stmt:
    def __init__(self, is_private_b, vardec_n):
        self.is_private_b = is_private_b
        self.vardec_n = vardec_n

    def __repr__(self):
        return (f"private_b: {self.is_private_b}, "
                f"{self.vardec_n}"
                )
    
class node_constructor_dec:
    def __init__(self, class_id_n, params_dec_n, code_block_n):
        self.class_id_n = class_id_n
        self.params_dec_n = params_dec_n
        self.code_block_n = code_block_n

    def __repr__(self):
        return (f"node_constructor_dec: (class_id_n: {self.class_id_n}, "
                f"params_dec_n: {self.params_dec_n}, "
                f"\n\t\tcode_block_n: {self.code_block_n})")

class node_code_block:
    def __init__(self, code_block_statement_n):
        self.code_block_statement_n = code_block_statement_n

    def __repr__(self):
        statements = ",\n".join(map(str, self.code_block_statement_n))
        return f"{self.__class__.__name__}({statements}\n)"

class node_program_constructs:
    def __init__(self, program_constructs_statement_n):
        self.program_constructs_statement_n = program_constructs_statement_n

    def __repr__(self):
        # Filter out None values
        filtered_statements = [stmt for stmt in self.program_constructs_statement_n if stmt is not None]
        statements = ",\n\n".join(map(str, filtered_statements))
        return f"{self.__class__.__name__}: ({statements}\n)"

class program_node:
    def __init__(self, program_structure_stmts):
        self.program_structure_stmts = program_structure_stmts

    def __repr__(self):
        statements = ",\n\n".join(map(str, self.program_structure_stmts))
        return f"program: {{ \n{statements} \n}}"

# alex here
class node_condition_value:
    def __init__(self, condition_value_n):
        self.condition_value_n = condition_value_n
    def __repr__(self):
        return f"condition_value_n -> {self.condition_value_n}, Type: {type(self.condition_value_n).__name__}"

class node_switch_stmt:
    def __init__(self, value_n, case_n, default_n):
        self.value_n = value_n
        self.case_n = case_n
        self.default_n = default_n

    def __repr__(self):
        return f"\nnode_switch ( \n switch_value_n: {self.value_n} \n {self.case_n} \n {self.default_n if self.default_n else "node_default: ( None )"} \n)"

class node_case:
    def __init__(self, case_stmt_n):
        self.case_stmt_n = case_stmt_n
        
    def __repr__(self):
        return "\n ".join(map(str, self.case_stmt_n))

class node_case_stmt:
    def __init__(self, case_value_n, ctrl_stmt_body_n):
        self.case_value_n = case_value_n
        self.ctrl_stmt_body_n = ctrl_stmt_body_n

    def __repr__(self):
        return f"node_case_stmt( \n case_value_n: {self.case_value_n["tokenName"]} \n case_body_n( {self.ctrl_stmt_body_n} ) \n)"
        
class node_default_stmt:
    def __init__(self, ctrl_stmt_body_n):
        self.ctrl_stmt_body_n = ctrl_stmt_body_n

    def __repr__(self):
        return f"node_default( \n default_body_n( {self.ctrl_stmt_body_n} ) \n)"

class node_loop_stmt:
    def __init__(self, loop_stmt_n):
        self.loop_stmt_n = loop_stmt_n
    def __repr__(self):
        return f"\nnode_loop_stmt -> {self.loop_stmt_n}\n"

class node_forloop:
    def __init__(self, init_arg_n, condition_n, inc_arg_n, ctrl_stmt_body_n):
        self.init_arg_n = init_arg_n
        self.condition_n = condition_n
        self.inc_arg_n = inc_arg_n
        self.ctrl_stmt_body_n = ctrl_stmt_body_n

    def __repr__(self):
        return f"node_forloop: ( \n init_arg_n: {self.init_arg_n} \n {self.condition_n} \n inc_arg_n: {self.inc_arg_n} \n)\n ctrl_body_n( {self.ctrl_stmt_body_n} )\n)"

class node_while:
    def __init__(self, condition_n, ctrl_stmt_body_n):
        self.condition_n = condition_n
        self.ctrl_stmt_body_n = ctrl_stmt_body_n

    def __repr__(self):
        return f"node_while ( \n {self.condition_n} \n ctrl_body_n( {self.ctrl_stmt_body_n} )\n)"

class node_do:
    def __init__(self, condition_n, ctrl_stmt_body_n):
        self.condition_n = condition_n
        self.ctrl_stmt_body_n = ctrl_stmt_body_n

    def __repr__(self):
        return f"node_do (\n ctrl_body_n( {self.ctrl_stmt_body_n} )\n {self.condition_n} \n)"

class node_repeat:
    def __init__(self, repeat_value_n, ctrl_stmt_body_n):
        self.repeat_value_n = repeat_value_n
        self.ctrl_stmt_body_n = ctrl_stmt_body_n

    def __repr__(self):
        return f"node_repeat ( \n repeat_value_n: {self.repeat_value_n} \n ctrl_body_n( {self.ctrl_stmt_body_n} ) \n)"

class node_assign_stmt:
    def __init__(self, id_n, assign_op_n, assign_value_n):
        self.id_n = id_n
        self.assign_op_n = assign_op_n
        self.assign_value_n = assign_value_n

    def __repr__(self):
        return f"assign stmt: id_n:'{self.id_n}', op:'{self.assign_op_n}', val:'{self.assign_value_n}'"

class node_imports_list:
    def __init__(self, stdlib_n):
        self.stdlib_n = stdlib_n

    def __repr__(self):
        return f"imports_list: (stdlib_n: {self.stdlib_n})"

#-------------------- PARSER --------------------
class SyntaxAnalyzer:
    # Takes tokens, initializes current token and its index
    def __init__(self, tokens):
        self.classNames = []            #for checking if constructor name matches class name
        self.errors = []
        self.parse_tree = None
        self.tokens = [token.to_dict() 
               for token in tokens 
               if token.token_type not in {"single_comment", "multi-line comment"}]   # comments will be ignored by the parser
        # print(self.tokens) #uncomment to check tokens that the parser accepted
        
        # if not self.tokens:
        #     message = "\n\tNo tokens to parse."
        #     self.errors.append(message)
        #     raise SyntaxError(message)

        self.currToken_index = 0
        self.currToken = self.tokens[self.currToken_index] if self.tokens else None

        self.lineContent = ''
        self.hasMainFunction = False  # Track if main function is found
        self.hasMainReturn = False
        self.hasFunctionReturned = False

    #-------------------- HELPER FUNCTIONS --------------------
    # Advancer for the next token
    def nextToken(self):
        # print("(parser)(dbg)currtoken: " + str(self.currToken))
        self.currToken_index += 1
        if self.currToken_index < len(self.tokens):
            self.currToken = self.tokens[self.currToken_index]
        else:
            self.currToken = None

    # Peeks at a token at the current index + offset.
    def peek(self, offset=1):
        peek_index = self.currToken_index + offset
        if 0 <= peek_index < len(self.tokens):
            print("('peek' function) current token:'",        #hahahahha idk how to format strings (too lazy to gpt)
            self.currToken["tokenName"], "' peeked [", offset, "] token/s further and found:'",
            self.tokens[peek_index]["tokenName"], "'")
            return self.tokens[peek_index]
        return None

    # Matches the current token with the expected type. Returns True if matched, False otherwise.
    def match(self, expected_token, hasSpecError=True):
        if self.currToken is not None and self.currToken["tokenType"] == expected_token:
            # print(f"('match' function) token {expected_token} matched")
            retToken = self.currToken
            self.nextToken()
            return retToken
        elif hasSpecError:
            # print("('match' function) deactivating default expected token error")
            return None
        else:
            # print("('match' function) activating default expected token error")
            self.ERROR_expected_token(expected_token)
            return None

    def matchPredictSet(self, non_terminal, hasSpecError=True):
        if self.currToken is None:  # EOF
            self.ERROR_unexpected("", "Unexpected EOF", PREDICT_SETS.get(non_terminal, []))
            return False

        expected_predict_set = PREDICT_SETS.get(non_terminal, [])

        if self.currToken["tokenType"] not in expected_predict_set:
            if not hasSpecError:
                self.ERROR_unexpected("", "Unexpected Token", expected_predict_set)
                return False
            else:
                return False
        return True

    
    #-------------------- SYNTAX ERRORS --------------------
    # Common Syntax Errors:    
    #   - Unexpected EOF
    #   - Unexpected token
    #   - list down more here

    # REMINDERS
    # 1. when generating errors, make sure they adhere to C, or create ur own basta make sure theyre real / expected compiler errors for our rules
    # 2. reuse already set errors if they have the same syntax error
    # 3. use logError for ONCE and/or SPECIFIC errors that require line,col
    # 4. directly append error / make another error if u dont need line, col but have a general error message
    # 5. avoid using logError if the error that you'll generate would be a 1.) repeat of a previous error 2.) a new error that will be reused more than once [in this case, make a new error]
    
    def ERROR_unexpected(self, expected_token, error_type, expected_predict_set=[]):
        if self.currToken:
            currToken = self.currToken["tokenName"]
            currLine = self.currToken["tokenLine"]
            currCol = self.currToken["tokenCol"]
        else: 
            currToken = self.tokens[self.currToken_index - 1]
            currLine = currToken["tokenLine"]
            currCol = currToken["tokenCol"]

        # Determine the expected message
        if expected_predict_set:
            # Format the list of expected tokens
            expected_tokens = ", ".join(f"'{token}'" for token in expected_predict_set)
            expected_message = f"{expected_tokens}"
        else:
            expected_message = f"'{expected_token}'"

        # Construct the error message
        if self.currToken:
            message = (
                f"\tSyntax Error: Unexpected Token '{currToken}' at line {currLine}, column {currCol}"
                f"\n\tExpected: {expected_message}\n"
            )
        else:
            message = (
                f"\tSyntax Error: Unexpected EOF at line {currLine}, column {currCol}"
                f"\n\tExpected: {expected_message}\n"
            )

        self.errors.append(message)

        raise SyntaxError(message) # will cause hault in producing other syntax errors


    # Helper function to log a syntax error with line and column information.
    def logError(self, message, context=""):
        if not self.currToken:
            # If the current token is None, use the last valid token for line/column info
            currToken = self.tokens[self.currToken_index - 1]
            currLine = currToken["tokenLine"]
            currCol = currToken["tokenCol"]
            tokenName = "<EOF>"
        else:
            # Use current token's details
            currLine = self.currToken["tokenLine"]
            currCol = self.currToken["tokenCol"]
            tokenName = self.currToken["tokenName"]

        # full error message
        full_message = (
            f"Syntax Error ({currLine}, {currCol}): {message}"
            + (f"\n{context}" if context else "")
        )
        self.errors.append(full_message)
        print(full_message)
        raise SyntaxError(full_message)
    
        # TODO: add error highlighter per line of code like  ______ ^



    # -------- Error-specific methods --------
    # Handles missing terminators like ';'.
    def ERROR_terminating_token(self, expected_token):
        if self.currToken:
            actual_token = self.currToken["tokenName"]
            message = f"Statement is expected to be terminated by '{expected_token}', but found '{actual_token}'."
        else:
            message = f"Statement is expected to be terminated by '{expected_token}', but reached EOF."
        self.logError(message)


    # Handles unexpected tokens when expecting a specific type.
    def ERROR_expected_token(self, expected_token):
        if self.currToken is None:
            self.logError(f"Unexpected EOF: Expected {expected_token}, but reached EOF.")
        else:
            self.logError(
                f"Unexpected token '{self.currToken['tokenName']}'. Expected {expected_token}."
            )

    # If no main function was found throughout the whole program
    def ERROR_no_main_func(self):
        message = "Syntax Error: Missing void 'main' function to execute the program.\nThe program must include a void 'main' function as the entry point."
        self.errors.append(message)
        raise SyntaxError(message)

    def ERROR_unclosed_angled_bracket(self):
        self.logError(f"Unclosed angled bracket: Expected '>', found '{self.currToken["tokenName"] if self.currToken else "EOF"}' instead. ") ## should we add line no. + col. num sa mga error d2

    def ERROR_unclosed_parentheses(self):
        self.logError(f"Unclosed parentheses: Expected ')', found '{self.currToken["tokenName"] if self.currToken else "EOF"}' instead. ")
    
    def ERROR_unclosed_curly_braces(self):
        self.logError(f"Unclosed curly braces: Expected '}}', found '{self.currToken["tokenName"] if self.currToken else "EOF"}' instead. ")

    def ERROR_unclosed_square_bracket(self):
        self.logError(f"Unclosed square bracket: Expected ']', found '{self.currToken["tokenName"] if self.currToken else "EOF"}' instead. ")

    def ERROR_expected_Identifier_classes(self):
        if not self.currToken:  # EOF case
            self.logError("Expected constructor call after '=', but reached EOF (End of File).")
        elif not self.match("Identifier"):  # Invalid token case
            current_value = self.currToken["tokenName"] if self.currToken else "EOF"
            self.logError(f"Expected constructor call after '=', but found '{current_value}' instead.")

    def ERROR_missing_initializer(self):
        if self.currToken:
            prev_token = self.tokens[self.currToken_index-1]
            error_message = f"Expected initializer object after '{prev_token['tokenName']}', instead got '{self.currToken['tokenName']}'."
        else:
            error_message = "Expected initializer object but reached EOF (End of File)"
        
        self.logError(error_message)

    def ERROR_expected_constructor_param_closing(self):
        if self.currToken is None:
            self.logError("Expected constructor parameter or closing ')', but reached EOF.")
        else:
            self.logError(f"Expected constructor parameter or closing ')', but found '{self.currToken['tokenName']}'.")


    def ERROR_missing_condition(self, condType):
        self.logError(f"Expected condition after '{condType}' statement")

    def ERROR_invalid_condition(self, condType):
        self.logError(f"Invalid condition for '{condType}' statement")

    def ERROR_empty_condition(self, condType):
        self.logError(f"Condition cannot be empty for '{condType}' statement")

    def ERROR_expected_num_value(self):
        self.logError(f"Expected numerical value. Found '{self.currToken["tokenType"] if self.currToken else "EOF"}' instead.")
    
    def ERROR_expected_pos_integer_value(self, expected_tokens = [t for t in PREDICT_SETS["int_val"] if t != "-"]):
        current_value = self.currToken["tokenType"] if self.currToken else "EOF"
        self.logError(
            f"Expected an integer value. Allowed tokens: {', '.join(expected_tokens)}. "
            f"Encountered: '{current_value}'."
        )

    def ERROR_main_void_return(self):
        if not self.currToken:
            self.logError("Expected ';' to terminate the return statement, but reached end of file. Use 'return;' to exit the main function successfully.")
        elif self.currToken["tokenType"] != ";":
            self.logError(f"Expected ';' to terminate the return statement, but found '{self.currToken['tokenName']}' instead. Use 'return;' to exit the main function successfully.")

    def ERROR_main_missing_return(self):
        self.logError("Missing return statement in main function. Use 'return;' to exit the main function successfully.")

    def ERROR_array_as_param_no_val(self):
        if self.currToken:
            self.logError(f"Dimensions in arrays as parameters should not have any value. Expected closing bracket ']', but found '{self.currToken['tokenName']}'.")
        else:
            self.logError("Expected closing bracket ']', but reached EOF.")
    def ERROR_inc_dec_constant(self):
        self.logError("Increment or decrement operation is not allowed on constants.")
    def ERROR_expected_valid_value(self):
        if self.currToken:
            self.logError(f"Expected a valid value, instead got '{self.currToken['tokenName']}'.")
        else:
            self.logError("Expected a valid value, instead reached EOF.")
    def ERROR_inc_dec_not_int(self):
        self.logError("Increment or decrement operation is only allowed for identifiers of type 'int' or 'long'.")
    def ERROR_expected_operator(self):
        self.logError(f"Expected a valid operator before '{self.currToken['tokenName'] if self.currToken else "EOF"}'.\nEnsure that there is a valid operator before a valid operand.")
    def ERROR_further_class_access(self):
        self.logError("Cstar doesn't allow subclasses. An attempt to access a subclass and/or its attributes or methods is not supported.")

    def ERROR_expected_int_value_in_stmt(self):
        if self.currToken:
            self.logError(f"'in' statement character limit parameter must be of \"int\" type. Instead got '{self.currToken['tokenName']}'.")
        else:
            self.logError(f"'in' statement character limit parameter must be of \"int\" type. Instead reached EOF.")

    #-------------------- PARSER START --------------------
    def parse(self):
        try:
            self.parse_tree = self.program()
            print(self.parse_tree)
            #self.value()
            self.errors.append("Parsing completed successfully. No Syntax Errors found.")
            print("Parsing completed successfully. No Syntax Errors found.")
        except SyntaxError as e:
            #print(f"Parsing incomplete with error/s: {e}")
            print (e)
        return (self.errors, self.parse_tree)

    #-------------------- CFG START --------------------
    # for semantic stuff, instead of using "if not", just add else clause to add functionality in if match clause

    def program(self):
        program_stmts = []
        
        print("(parser) production: \"program\" detected")
        """<program> → <imports_list><program_constructs> int main(){ <main_body> return 0;}"""
        if not self.tokens:
            message = "\n\tNo tokens to parse."
            self.errors.append(message)
            raise SyntaxError(message)
        
        if self.matchPredictSet("program", False):
            imports_list_node, std_lib_func_dec_nodes = self.imports_list([], [])
            program_stmts.append(imports_list_node)
            
            """<program> → <program_constructs> int main(){ <main_body> return 0;}"""
            # Parse constructs
            program_stmts.append(self.program_constructs(std_lib_func_dec_nodes))
           
            print(f"BACK AT MAIN PROGRAM : {self.hasMainFunction}")

            # Check for main function presence
            if not self.hasMainFunction:
                self.ERROR_no_main_func()
            else:
                while self.currToken:
                    #self.match("(", False)
                    if not self.match(")"):
                        self.ERROR_unclosed_parentheses()
                    self.match("{", False)
                    print("(parser) production: \"main_body\" detected")
                    program_stmts.append(self.body(["}"], True)) # isVoid = True here

                    if not self.match("return") and not self.hasMainReturn:
                        self.ERROR_main_missing_return()

                    # if not self.currToken or self.currToken["tokenType"] != ";" and not self.hasMainReturn:
                    #     self.ERROR_main_void_return()
                    
                    if not self.match(";") and not self.hasMainReturn:
                        self.ERROR_main_void_return()  # prolly wont throw this error bc return is now in body

                    if not self.match("}"):
                        self.ERROR_unclosed_curly_braces()

                    # TODO: might have to be revisited, for some reason it's off by one line
                    if self.currToken: 
                        currLine = self.currToken["tokenLine"]
                        currCol = self.currToken["tokenCol"]

                        print(f"warning: ({currLine}, {currCol}): Unreachable code detected")
                        self.errors.append(f"Warning at line {currLine}: Unreachable code detected.")
                        break
            return program_node(program_stmts)


    # CODE BLOCKS START HERE
    def code_block(self, code_block_statement_n = [], isVoid = False):       
        print(f"(parser) Processing <code_block>: {self.currToken['tokenName'] if self.currToken else 'None'}")
        
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["code_block"]:
            currentTokenType = self.currToken["tokenType"]


            if currentTokenType == "Identifier":
                iden_temp_n = node_iden(self.match("Identifier",False))
                code_block_statement_n.append(self.class_as_func_post(iden_temp_n))
                if not self.match(";", True):
                    self.ERROR_terminating_token(";")

            elif currentTokenType in ["const"] + PREDICT_SETS["data_type"]: 
                const_b = False   
                if currentTokenType == "const":
                    self.match("const")
                    const_b = True
                dtype_t = self.data_type()
                iden_temp_n = node_iden(self.match("Identifier",False))
                vardec_cont_n = self.var_dec_cont(dtype_t, iden_temp_n, const_b)
                if not self.match(";"):
                    self.ERROR_terminating_token(";")

                code_block_statement_n.append(vardec_cont_n)

            elif currentTokenType == "++":
                left_t = self.match("++")
                iden_temp_n = node_iden(self.match("Identifier",False))
                if not self.match(";"):
                    self.ERROR_terminating_token(";")
                code_block_statement_n.append(node_pre_un_op(left_t, iden_temp_n))

            elif currentTokenType == "--":
                left_t = self.match("--")
                iden_temp_n = node_iden(self.match("Identifier",False))
                if not self.match(";"):
                    self.ERROR_terminating_token(";")
                code_block_statement_n.append(node_pre_un_op(left_t, iden_temp_n))
            
            elif currentTokenType in PREDICT_SETS["output"]:
                code_block_statement_n.append(self.output())
                if not self.match(";"):
                    self.ERROR_terminating_token(";")

            elif currentTokenType in PREDICT_SETS["conditional_stmt"]:
                code_block_statement_n.append(self.conditional_stmt(isVoid))
                
            elif currentTokenType in PREDICT_SETS["loop_stmt"]:
                code_block_statement_n.append(self.loop_stmt(isVoid))
        
            else: self.logError("You're not supposed to see this.")
            print("AMBATURETURNNNNNNN")
            self.code_block(code_block_statement_n, isVoid)
            

        return node_code_block(code_block_statement_n)
        

    def class_as_func_post(self, iden_temp_n):       
        print("(parser) production: \"class_as_func_post\" detected")

        if self.currToken:
            currentTokenType = self.currToken["tokenType"]
            if currentTokenType in PREDICT_SETS["class_as_func_post"]:
                if currentTokenType == "Identifier":
                    class_id_n = iden_temp_n
                    obj_id_n = node_iden(self.match("Identifier", False))
                    class_instcont_n = self.classinst_cont()
                    if self.currToken:
                        if self.currToken["tokenType"] == "[":
                            self.logError("Array of objects is not supported. Expected '=' or ';'")
                        if self.currToken["tokenType"] == "." or self.currToken["tokenType"] == "(":
                            self.logError(f"Unexpected Token '{self.currToken["tokenType"]}' for object declaration. Expected '=' or ';'")
                    
                    return node_class_inst(class_id_n, obj_id_n, class_instcont_n)

                elif currentTokenType == "++":
                    right_t = self.match("++")
                    return node_post_un_op(iden_temp_n, right_t)
                elif currentTokenType == "--":
                    right_t = self.match("--")
                    return node_post_un_op(iden_temp_n, right_t)

                else: 
                    return self.assign_func_method_mods(iden_temp_n)
            else: self.ERROR_expected_token(PREDICT_SETS["class_as_func_post"])
        else: self.ERROR_expected_token(PREDICT_SETS["class_as_func_post"])

    def assign_func_method_mods(self, iden_temp_n):
        print("(parser) production: \"assign_func_method_mods\" detected")

        if self.currToken:
            currentTokenType = self.currToken["tokenType"]
            if currentTokenType in PREDICT_SETS["assign_func_method_mods"]:
                if currentTokenType in (PREDICT_SETS["assign_operator"] + ["["]):
                    as_array_n = self.as_array()
                    assign_stmt_op_n = self.assign_stmt_op()
                    return node_assign_func_method_mods(iden_temp_n, as_array_n, assign_stmt_op_n, None, None, None)

                elif currentTokenType == "(":
                    self.match("(", False)
                    func_arg_n = self.func_arg()
                    if not self.match(")"):
                        self.ERROR_unclosed_parentheses()
                    return node_assign_func_method_mods(iden_temp_n, None, None, func_arg_n, None, None)

                elif currentTokenType == ".":
                    self.match(".")
                    attribute_iden_n = node_iden(self.match("Identifier", False))
                    assign_func_method_mods_cont_n = self.assign_func_method_mods_cont()
                    return node_assign_func_method_mods(iden_temp_n, None, None, None, attribute_iden_n, assign_func_method_mods_cont_n)
                
            else: self.ERROR_expected_token(PREDICT_SETS["assign_func_method_mods"])
        else: self.ERROR_expected_token(PREDICT_SETS["assign_func_method_mods"])


    def assign_func_method_mods_cont(self):
        print("(parser) production: \"assign_func_method_mods_cont\" detected")

        if self.currToken:
            currentTokenType = self.currToken["tokenType"]
            if currentTokenType in (PREDICT_SETS["assign_func_method_mods_cont"] + PREDICT_SETS["assign_operator"]):
                if currentTokenType == "[" or currentTokenType in PREDICT_SETS["assign_operator"]:
                    as_array_n = self.as_array()
                    if not self.currToken or self.currToken["tokenType"] not in PREDICT_SETS["assign_operator"]:
                        self.ERROR_expected_token(PREDICT_SETS["assign_operator"])
                    assign_stmt_op_n = self.assign_stmt_op()
                    return node_assign_func_method_mods_cont(as_array_n, assign_stmt_op_n, None)

                elif currentTokenType == "(":
                    self.match("(")
                    func_arg_n = self.func_arg()
                    if not self.match(")"):
                        self.ERROR_unclosed_parentheses()
                    return node_assign_func_method_mods_cont(None, None, func_arg_n)

                elif self.currToken and self.currToken["tokenType"] == ".":
                    self.logError(f"Further accessing of object elements is not allowed. Expected '[' or '(', found '{self.currToken["tokenType"]}'.")    
            elif self.currToken and self.currToken["tokenType"] == ".":
                self.logError(f"Further accessing of object elements is not allowed. Expected '[' or '(', found '{self.currToken["tokenType"]}'.")  
            else: self.ERROR_expected_token(["[", "("] + PREDICT_SETS["assign_operator"])
        else: self.ERROR_expected_token(["[", "("] + PREDICT_SETS["assign_operator"])


    def body(self, stopChars, isVoid = False, inControlStruct = False):     # TODO: Check for return statements reachable only within if/code_blocks, thats one semantic error
        print(f"(parser) Processing <body>: {self.currToken['tokenName'] if self.currToken else 'None'}")
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["body"]:
            
            statements_n = self.code_block([], isVoid)
            return_stmt_n = None

            if self.currToken and self.currToken["tokenType"] == "return":
                  return_stmt_n = self.return_block(isVoid)
                  self.hasFunctionReturned = True     
                  if self.hasMainFunction:
                      self.hasMainReturn = True
            #     # TODO: DEAD CODE (CODE AFTER RETURN) ERROR IMPLEMENTATION\

                
            self.body(stopChars, isVoid, inControlStruct)
            return node_body(statements_n, return_stmt_n)

        if self.currToken and self.currToken["tokenType"] not in stopChars:
            self.logError(f"Unexpected Token '{self.currToken["tokenName"]}' found. Expected {PREDICT_SETS["body"]}.")

        if not self.hasFunctionReturned and not inControlStruct and not self.hasMainFunction:
                self.logError(f"Expected 'return' for all functions, instead got '{self.currToken["tokenName"]}'")
                #placeholder hehehehehhehehehehheyhueh

        
        print("(parser) production: \"body\" exited!!!!!!")
        return None
        

    def imports_list(self, stdlibs=[], std_lib_func_dec_nodes = []):
        print("(parser) production: \"imports_list\" detected")

        # should return tuple, stdlibs node and array of stdlibs func dec nodes to be passed to program constructs' statements

        # Only parse if the current token is "import"
        if self.currToken and self.currToken["tokenType"] == "import":
            self.match("import", False)
            self.match("<", False)

            # Process content inside '<>'  -- no more header files import
            if self.currToken["tokenName"] in PREDICT_SETS["std_lib"]:
                print("STANDARD LIBRARY FOUND: " + str(self.currToken["tokenName"]))
                std_lib_header_line = self.currToken["tokenLine"]
                std_lib_header_col = self.currToken["tokenCol"]
                std_lib_header = self.match("Identifier")["tokenName"]  
                

                if std_lib_header not in stdlibs:
                    stdlibs.append(std_lib_header)  # Avoid duplicate appends of stdlib stdlibs
                    
                    # data type tokens
                    string_type_t = Token("string", "string", std_lib_header_line, std_lib_header_col).to_dict()
                    int_type_t = Token("int", "int", std_lib_header_line, std_lib_header_col).to_dict()
                    bool_type_t = Token("bool", "bool", std_lib_header_line, std_lib_header_col).to_dict()

                    # default parameter identifier tokens
                    str_iden = Token("str_param1", "Identifier", std_lib_header_line, std_lib_header_col).to_dict() 
                    str_iden_n = node_iden(str_iden)
                    int_iden = Token("int_param1", "Identifier", std_lib_header_line, std_lib_header_col).to_dict() 
                    int_iden_n = node_iden(int_iden)
                    array_iden = Token("array_param1", "Identifier", std_lib_header_line, std_lib_header_col).to_dict()
                    array_iden_n = node_iden(array_iden)

                    if std_lib_header == "Cstring":
                        # str_isEmpty built-in Cstring stdlib function
                        str_isEmpty_iden_t = Token("str_isEmpty", "Identifier", std_lib_header_line, std_lib_header_col).to_dict() 
                        str_isEmpty_iden_n = node_iden(str_isEmpty_iden_t) 
                        str_isEmpty_params_n = [node_funcpar_var(string_type_t, str_iden_n)]
                        std_lib_func_dec_nodes.append(node_func_dec(bool_type_t, str_isEmpty_iden_n, str_isEmpty_params_n, None, True))

                        # str_length built-in Cstring stdlib function
                        str_length_iden_t = Token("str_length", "Identifier", std_lib_header_line, std_lib_header_col).to_dict()
                        str_length_iden_n = node_iden(str_length_iden_t)
                        str_length_params_n = [node_funcpar_var(string_type_t, str_iden_n)]
                        std_lib_func_dec_nodes.append(node_func_dec(int_type_t, str_length_iden_n, str_length_params_n, None, True))

                        # str_popAlpha built-in Cstring stdlib function
                        str_popAlpha_iden_t = Token("str_popAlpha", "Identifier", std_lib_header_line, std_lib_header_col).to_dict()
                        str_popAlpha_iden_n = node_iden(str_popAlpha_iden_t)
                        str_popAlpha_params_n = [node_funcpar_var(string_type_t, str_iden_n)]
                        std_lib_func_dec_nodes.append(node_func_dec(string_type_t, str_popAlpha_iden_n, str_popAlpha_params_n, None, True))

                        # str_popDigits built-in Cstring stdlib function
                        str_popDigits_iden_t = Token("str_popDigits", "Identifier", std_lib_header_line, std_lib_header_col).to_dict()
                        str_popDigits_iden_n = node_iden(str_popDigits_iden_t)
                        str_popDigits_params_n = [node_funcpar_var(string_type_t, str_iden_n)]
                        std_lib_func_dec_nodes.append(node_func_dec(string_type_t, str_popDigits_iden_n, str_popDigits_params_n, None, True))

                        # str_popSpecial built-in Cstring stdlib function
                        str_popSpecial_iden_t = Token("str_popSpecial", "Identifier", std_lib_header_line, std_lib_header_col).to_dict()
                        str_popSpecial_iden_n = node_iden(str_popSpecial_iden_t)
                        str_popSpecial_params_n = [node_funcpar_var(string_type_t, str_iden_n)]
                        std_lib_func_dec_nodes.append(node_func_dec(string_type_t, str_popSpecial_iden_n, str_popSpecial_params_n, None, True))

                        # str_slice built-in Cstring stdlib function
                        str_slice_iden_t = Token("str_slice", "Identifier", std_lib_header_line, std_lib_header_col).to_dict()
                        str_slice_iden_n = node_iden(str_slice_iden_t)
                        str_slice_params_n = [node_funcpar_var(string_type_t, str_iden_n), node_funcpar_var(int_type_t, int_iden_n), node_funcpar_var(int_type_t, int_iden_n)]
                        std_lib_func_dec_nodes.append(node_func_dec(string_type_t, str_slice_iden_n, str_slice_params_n, None, True))

                        # str_toLower built-in Cstring stdlib function
                        str_toLower_iden_t = Token("str_toLower", "Identifier", std_lib_header_line, std_lib_header_col).to_dict()
                        str_toLower_iden_n = node_iden(str_toLower_iden_t)
                        str_toLower_params_n = [node_funcpar_var(string_type_t, str_iden_n)]
                        std_lib_func_dec_nodes.append(node_func_dec(string_type_t, str_toLower_iden_n, str_toLower_params_n, None, True))

                        # str_toUpper built-in Cstring stdlib function
                        str_toUpper_iden_t = Token("str_toUpper", "Identifier", std_lib_header_line, std_lib_header_col).to_dict()
                        str_toUpper_iden_n = node_iden(str_toUpper_iden_t)
                        str_toUpper_params_n = [node_funcpar_var(string_type_t, str_iden_n)]
                        std_lib_func_dec_nodes.append(node_func_dec(string_type_t, str_toUpper_iden_n, str_toUpper_params_n, None, True))

                    if std_lib_header == "Carray":
                        # array_isEmpty built-in Carray stdlib function
                        array_isEmpty_iden_t = Token("array_isEmpty", "Identifier", std_lib_header_line, std_lib_header_col).to_dict()
                        array_isEmpty_iden_n = node_iden(array_isEmpty_iden_t)
                        array_isEmpty_params_n = [node_funcpar_arr(None, array_iden_n, None)]
                        std_lib_func_dec_nodes.append(node_func_dec(bool_type_t, array_isEmpty_iden_n, array_isEmpty_params_n, None, True))

                        # array_length built-in Carray stdlib function
                        array_length_iden_t = Token("array_length", "Identifier", std_lib_header_line, std_lib_header_col).to_dict()
                        array_length_iden_n = node_iden(array_length_iden_t)
                        array_length_params_n = [node_funcpar_arr(None, array_iden_n, None)]
                        std_lib_func_dec_nodes.append(node_func_dec(int_type_t, array_length_iden_n, array_length_params_n, None, True))


                else:
                    error_msg = f"Duplicate library import: Standard library '{std_lib_header}' has already been imported."
                    self.errors.append(error_msg)
                    raise SyntaxError(error_msg)
                    
            else:
                 self.logError(
                    f"Expected a standard library (Cstring or Carray), found '{self.currToken['tokenName']}'"
                    if self.currToken else "Expected a standard library (Cstring or Carray), but reached EOF instead.")

            if not self.match(">"):
                self.ERROR_unclosed_angled_bracket()

            if not self.match(";"):
                self.ERROR_terminating_token(";")

            # Handle potential recursive imports
            if self.currToken and self.currToken["tokenType"] == "import":
                self.imports_list(stdlibs)

        return (node_imports_list(stdlibs), std_lib_func_dec_nodes)


    # ----- TODO:REVISIT!! can't complete errors here yet bc errors would be found in each prod first, then check if there are external errors left 
    # ex of unimplemented error: if there's a sole variable (it can be considered a class inst, pero if not yet defined, it should throw another type of error)
    def program_constructs(self, program_constructs_statement_n = []):
        
        print("(parser) production: \"program_constructs\" detected: currtoken is \""
      + str(self.currToken["tokenName"])+"\"" if self.currToken else "None" + "\"")
        
        if self.currToken:
            if self.matchPredictSet("program_constructs", False):  # Token is a valid start for program constructs
                currentTokenType = self.currToken["tokenType"]
                if currentTokenType in ["private", "class"]:
                    program_constructs_statement_n.append(self.class_declaration([]))
                    self.program_constructs(program_constructs_statement_n)
                elif currentTokenType in PREDICT_SETS["iden_dec"]:
                    program_constructs_statement_n.append(self.iden_dec())
                    
                else:
                    program_constructs_statement_n.append(self.class_inst())    #initial prog construct ast
                    
            if not self.hasMainFunction:
                self.program_constructs(program_constructs_statement_n)
                
            print(f"######################### AST FOR PROGRAM_CONSTRUCTS #########################")
            return node_program_constructs(program_constructs_statement_n)

    def iden_dec(self, inClassBody = False):
        print("(parser) production: \"iden_dec\" detected (current token: " + str(self.currToken["tokenName"]) + ")")
        

        if self.currToken:
            currentTokenType = self.currToken["tokenType"]
            const_b = False
            if currentTokenType == "const":
                self.match("const")
                const_b = True
                if self.currToken["tokenType"] == "void":
                    self.logError("Void function cannot be preceded by 'const'.")
                elif self.currToken["tokenType"] in PREDICT_SETS["data_type"]:
                    dtype_temp_t = self.data_type()
                    iden_temp_n = node_iden(self.match("Identifier",False))
                    vardec_cont_temp_n = self.var_dec_cont(dtype_temp_t, iden_temp_n)
                    if not self.match(";"):
                        self.ERROR_terminating_token(";")
                    
                    return node_vardec(const_b, dtype_temp_t, iden_temp_n, vardec_cont_temp_n)
                else: self.ERROR_expected_token(PREDICT_SETS["data_type"])

            elif currentTokenType not in PREDICT_SETS["data_type"] and currentTokenType != "void":
                self.logError(f"Expected data type or void, found '{currentTokenType}' instead.")

            elif currentTokenType == "void":
                void_t = self.match("void")
                id_temp_n = None
                isVoid = True
                if self.currToken:
                    if self.currToken["tokenName"] == "main" and not inClassBody:
                        self.hasMainFunction = True
                        print("MAIN FUNCTION FOUND!!!!")
                    id_temp_n = self.match("Identifier", False)
                else:
                    self.logError("Expected Identifier for function declaration.")
                self.match("(", False)
                if not self.hasMainFunction:
                    return self.params_dec_start(void_t, id_temp_n, isVoid)
                else:
                    if self.currToken:
                        if self.currToken["tokenType"] != ")":
                            self.ERROR_unclosed_parentheses()
                        return self.params_dec_start(void_t, id_temp_n, isVoid)
                    else: self.logError("Expected ')', but reached EOF.")

            elif currentTokenType in PREDICT_SETS["data_type"]:
                dtype_temp_t = self.data_type()
                id_temp_n = node_iden(self.match("Identifier", False))
                # return node_vardec(const_b, dtype_temp_t, id_temp_n, self.iden_dec_cont(dtype_temp_t, id_temp_n)) 
                return self.iden_dec_cont(dtype_temp_t, id_temp_n)
                
            
            else:
                self.ERROR_expected_token(PREDICT_SETS["iden_dec"])


    def iden_dec_cont(self, dtype_temp_t, id_temp_n):
        print("(parser) production: \"iden_dec_cont\" detected")

        if self.currToken:

            if self.currToken["tokenType"] == "(":
                return self.params_dec_start(dtype_temp_t, id_temp_n)
            else:
                node_temp = self.var_dec_cont(dtype_temp_t, id_temp_n)
                if not self.match(";"):
                    self.ERROR_terminating_token(";")
                
                return node_temp
            # else: self.ERROR_expected_token(["("] + PREDICT_SETS["iden_dec_cont"])

        else: self.ERROR_expected_token(["("] + PREDICT_SETS["iden_dec_cont"])


    def var_dec_cont(self, dtype_temp_t, id_temp_n, const_b = False):
        print("(parser) production: \"var_dec_cont\" detected")
        value_temp_n = None
        idec_rec_temp_n = None
        vardec_cont_temp_n = None
        node_idec_rec_stmt = []

        if self.currToken:
            if self.currToken["tokenType"] == "[":
                self.match("[", False)
                size1_temp_n = self.arith_exp(["]"])
                if not self.match("]"):
                    self.ERROR_unclosed_square_bracket()
                return self.var_id_arr1D(dtype_temp_t, id_temp_n, size1_temp_n)

            else:
                value_temp_n = self.var_init()
                idec_rec_temp_n = self.var_iden_rec(node_idec_rec_stmt)
        
        # none arr var dec
        if value_temp_n or idec_rec_temp_n:
            vardec_cont_temp_n = node_vardec_cont(value_temp_n, idec_rec_temp_n)

        return node_vardec(const_b, dtype_temp_t, id_temp_n, vardec_cont_temp_n)
        # return node_vardec_cont(value_temp_n, idec_rec_temp_n)



    def params_dec_start(self, dtype_tempt_t, id_temp_n, isVoid = False):
        
        if not self.hasMainFunction:
            print(f"(parser) production: \"params_dec_start\" detected , isVoid = {isVoid}")
            self.match("(")
            params_n = self.params_dec([])
            if not self.match(")", True):
                self.ERROR_unclosed_parentheses()
        
            self.match("{", False)
            body_n = self.body(["}"], isVoid)
            if not self.match("}"):
                self.ERROR_unclosed_curly_braces()
            self.hasFunctionReturned = False
            
            return node_func_dec(dtype_tempt_t, id_temp_n, params_n, body_n)


    # TODO
    def class_declaration(self, class_body_stmt_n = []):
        print("(parser) production: \"class_declaration\" detected")

        is_private_b = False
        class_body_stmt_n = []

        if self.currToken["tokenType"] == "private":
             self.match("private")
             is_private_b = True

        self.match("class", False)

        if self.currToken and self.currToken["tokenType"] == "Identifier":
            self.classNames.append(self.currToken["tokenName"])      # handles constructor name logic of recursive classes within classes
            class_id_n = node_iden(self.match("Identifier"))
        else:
            self.ERROR_expected_token("Identifier")
        
        self.match("{", False)
        self.class_body(class_body_stmt_n)
        constructor_dec_n = self.constructor_dec()
        self.class_body(class_body_stmt_n)

        if self.currToken and self.currToken["tokenType"] == "Identifier":
            self.logError(f"Only one constructor per class allowed. Expected: {PREDICT_SETS['class_body']}")

        if not self.match("}"):
            self.ERROR_expected_token(PREDICT_SETS['class_body'] + ['}'])

        if not self.match(";", True):
            self.logError("Class Declaration is expected to be terminated by ';' after '}'.")

        print(f"######################### AST FOR CLASS DEC #########################")
        class_body_n = node_class_body(class_body_stmt_n)
        return node_class_dec(is_private_b, class_id_n, constructor_dec_n, class_body_n)
        

    
    def class_body(self, class_body_stmt_n = []): # all of these are just 'if's because class_body can be null
        print("(parser) production: \"class_body\" detected")
        
        is_private_b = False
        inClassBody = True
        if self.matchPredictSet("class_body", True):   #throws no error if currToken not in here
            
            if self.currToken:
                if self.currToken["tokenType"] == "private":
                    self.match("private")
                    is_private_b = True
                    if self.currToken and self.currToken["tokenType"] == "class":
                        self.logError(f"Classes cannot be nested within classes. Expected {PREDICT_SETS['iden_dec']} or constructor declaration.")
                    if not self.currToken or self.currToken["tokenType"] not in PREDICT_SETS["iden_dec"]:
                        self.ERROR_expected_token(PREDICT_SETS["iden_dec"])
                
                node_vardec = self.iden_dec(inClassBody)
                class_body_stmt_n.append(node_class_body_stmt(is_private_b, node_vardec))
                self.class_body(class_body_stmt_n)
                return class_body_stmt_n
            inClassBody = False 

        if self.currToken and self.currToken["tokenType"] == "class":
            self.logError(f"Classes cannot be nested within classes. Expected {PREDICT_SETS['class_body']} or constructor declaration.")
        return class_body_stmt_n

    def constructor_dec(self): 
        
        if self.currToken:
            if self.currToken["tokenType"] == "Identifier":
                params_dec_n = None
                code_block_n = None
                print("(parser) production: \"constructor_dec\" detected")
                if self.currToken["tokenName"] != self.classNames[-1]: 
                    self.logError("Constructors must have the same name as its class.") 
                    #TODO: maybe fix error message here, just a placeholder

                class_id_n = node_iden(self.match("Identifier", False))
                self.classNames.pop()
                self.match("(", False)
                params_dec_n = self.params_dec()
                if not self.match(")"):
                    self.ERROR_unclosed_parentheses()

                self.match("{", False)
                code_block_n = self.code_block()
                
                if self.currToken and self.currToken["tokenType"] == "return":
                    self.logError(f"Constructors cannot have return statements. Expected {PREDICT_SETS['code_block']} or }} ")


                if not self.match("}"):
                    self.ERROR_unclosed_curly_braces()

                print("(parser) production: \"constructor_dec\" exited!!!!!")
                return node_constructor_dec(class_id_n, params_dec_n, code_block_n)

                


    def class_inst(self, code_block_statement_n = None):
        print("(parser) production: \"class_inst\" detected")

        class_instcont_n = None

        if self.currToken:
            # Parse the first Identifier (class name or type)
            if self.currToken["tokenType"] != "Identifier":
                self.logError("Expected an identifier for class instantiation.")
                # This error is just a placeholder habang wala pang semantic, cos normally it should identify if existing na ung class
            
            class_id_n = node_iden(self.match("Identifier", False))
            # Parse the second Identifier (variable name)
            if self.currToken and self.currToken["tokenType"] == "Identifier":
                obj_id_n = node_iden(self.match("Identifier", False))
            else:
                self.ERROR_missing_initializer()
            
            if self.currToken and self.currToken["tokenType"] == '=': # check if there is object instantiation
                class_instcont_n = self.classinst_cont()

            # Match terminating symbol
            if self.currToken and self.currToken["tokenType"] == ';':
                self.match(";")
                print(f"######################### AST FOR CLASS INST #########################")
                return node_class_inst(class_id_n, obj_id_n, class_instcont_n)
            else:
                self.ERROR_terminating_token(";")

            
    
    # Handle <classinst_cont>
    def classinst_cont(self):
        print("(parser) production: \"classinst_cont\" detected")
        # object instantiation
        if self.currToken and self.currToken["tokenType"] == "=":
            self.match("=")
            if self.currToken and self.currToken["tokenType"] != "Identifier": # should be the same name as the class name [SEMANTIC]
                self.ERROR_expected_Identifier_classes()

            class_id_n = node_iden(self.match("Identifier",False))

            if not self.currToken or self.currToken["tokenType"] != '(':
                self.logError(f"Expected '(' for constructor call after Identifier. Found '{self.currToken["tokenType"] if self.currToken else "EOF"}' instead.")
            self.match('(')
            func_arg_n = self.func_arg()
            if self.currToken and self.currToken["tokenType"] == ")":
                self.match(')')
            elif (self.currToken is None or self.currToken["tokenType"] not in PREDICT_SETS["func_arg"]):
                self.ERROR_expected_constructor_param_closing()
            else:
                self.ERROR_expected_token([")", ","])

            return node_classinst_cont(class_id_n, func_arg_n)

        return None

    def func_arg(self, func_arg_n=[]):
        print("(parser) production: \"func_arg\" detected")

        # Check if there's a value to parse
        if self.currToken and self.currToken["tokenType"]in PREDICT_SETS["value"]:
            val_n = self.value([',',')'])
            func_arg_n.append(val_n)
            if self.currToken and self.currToken["tokenType"] == ',':
                self.func_arg_rec(func_arg_n)
        else:
            if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["data_type"]:
                self.logError(f"Unexpected token: '{self.currToken["tokenName"]}'. Function call arguments cannot accept declarations.")
            elif self.currToken and self.currToken["tokenType"] != ")":
                self.ERROR_expected_token(PREDICT_SETS["value"]+[")"])
            else: 
                print("(parser) λ-production for <func_arg>")  # Handle λ (empty production)
        
        return func_arg_n

    

    def func_arg_rec(self, func_arg_n):
        print("(parser) production: \"func_arg_rec\" detected")

        self.match(',')

        if self.currToken:
            if self.currToken["tokenType"] not in PREDICT_SETS["value"]:
                self.logError(f"Expected another value after ',' but got '{self.currToken['tokenName']}'.")
            self.func_arg(func_arg_n)
        else: self.logError("Expected another value after ',' but reached EOF.")
        


    def func_method_call(self):    
        print("(parser) production: \"func_method_call\" detected")
        self.match("Identifier")      
        self.func_method_call_mods()      

    def func_method_call_mods(self):
        print("(parser) production: \"func_method_call_mods\" detected")
        if self.currToken and self.currToken["tokenType"] == "(":
            # Handle (<func_arg>) -- direct func call
            self.match("(")
            self.func_arg()
            if not self.match(")"):
                self.ERROR_unclosed_parentheses()
        elif self.currToken and self.currToken["tokenType"] == ".":
            # .Identifier(<func_arg>) -- method call
            self.match(".")
            self.match("Identifier", False)
            self.match("(", False)
            self.func_arg()
            if not self.match(")", False):
                self.ERROR_unclosed_parentheses()
        elif self.currToken and self.currToken["tokenType"] == "[":
            # method of an object in an array of object (and recurse up til it reaches method calling)
            self.as_array()
            self.match(".", False)
            self.match("Identifier", False)
            self.func_method_call_mods()
        else:
            # Handle λ-production (no further modifications)
            self.ERROR_expected_token([".","(","["])
            print("(parser) λ-production for <func_method_call_mods>")


    # Uses of predict sets in value:
    #  - when checking for cont. if the next operator is any of the expressions, only enter cont prods
    def stopCharOrOperatorCheck(self, stopChars):
        if self.currToken["tokenType"] not in PREDICT_SETS["term_join_operators"] + stopChars and self.currToken["tokenType"] in PREDICT_SETS["value"]:  # throw an error for missing operator
            self.ERROR_expected_operator()
    
    def value(self, stopChars):
        # print("(parser-value-chain): Entered \"value\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        return self.logic_exp(stopChars)

    def logic_exp(self, stopChars):
        # print("(parser-value-chain): Entered \"logic_exp\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        left_n = self.rel_exp(stopChars)
        
        if self.currToken:
            if self.currToken["tokenType"] in PREDICT_SETS["logic_operator"]:
                left_n = self.logic_exp_cont(left_n, stopChars)
            self.stopCharOrOperatorCheck(stopChars)
                
        return left_n
    
    def logic_exp_cont(self, left_n, stopChars):
        # print("(parser-value-chain): Entered \"logic_exp_cont\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        op_t = None
        match self.currToken["tokenType"]:
            case "&&":
                op_t = self.match("&&")
            case "||":
                op_t = self.match("||")
        new_left_n = node_bi_op(left_n, op_t, self.rel_exp(stopChars))
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["logic_operator"]:
            new_left_n = self.logic_exp_cont(new_left_n, stopChars)
        return new_left_n

    def rel_exp(self, stopChars):
        # print("(parser-value-chain): Entered \"rel_exp\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        left_n = self.arith_exp(stopChars)

        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["rel_operator"]:
            left_n = self.rel_exp_cont(left_n, stopChars)
        
        return left_n
    
    def rel_exp_cont(self, left_n, stopChars):
        # print("(parser-value-chain): Entered \"rel_exp_cont\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        op_t = None
        match self.currToken["tokenType"]:
            case "==":
                op_t = self.match("==")
            case "!=":
                op_t = self.match("!=")
            case ">":
                op_t = self.match(">")
            case ">=":
                op_t = self.match(">=")
            case "<":
                op_t = self.match("<")
            case "<=":
                op_t = self.match("<=")

        new_left_n = node_bi_op(left_n, op_t, self.arith_exp(stopChars))

        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["rel_operator"]:
            new_left_n = self.rel_exp_cont(new_left_n, stopChars)
        
        return new_left_n
    
    def arith_exp(self, stopChars):
        # print("(parser-value-chain): Entered \"arith_exp\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        left_n = self.term(stopChars)

        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["add_min_cont"]:
            left_n = self.add_min_cont(left_n, stopChars)

        return left_n

    def add_min_cont(self, left_n, stopChars):
        # print("(parser-value-chain): Entered \"add_min_cont\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        op_t = None
        match self.currToken["tokenType"]:
            case "+":
                op_t = self.match("+")
            case "-":
                op_t = self.match("-")
        new_left_n = node_bi_op(left_n, op_t, self.term(stopChars))

        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["add_min_cont"]:
            new_left_n = self.add_min_cont(new_left_n, stopChars)

        return new_left_n

    def term(self, stopChars):
        # print("(parser-value-chain): Entered \"term\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        left_n = self.factor(stopChars)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["mult_div_modulo_cont"]:
            left_n = self.mult_div_modulo_cont(left_n, stopChars)

        return left_n

    def mult_div_modulo_cont(self, left_n, stopChars):
        # print("(parser-value-chain): Entered \"mult_div_modulo_cont\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        op_t = None
        match self.currToken["tokenType"]:
            case "*":
                op_t = self.match("*")
            case "/":
                op_t = self.match("/")
            case "%":
                op_t = self.match("%")
        new_left_n = node_bi_op(left_n, op_t, self.factor(stopChars))
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["mult_div_modulo_cont"]:
            new_left_n = self.mult_div_modulo_cont(new_left_n, stopChars)

        return new_left_n
    
    def factor(self, stopChars):
        # print("(parser-value-chain): Entered \"factor\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        if self.currToken and self.currToken["tokenType"] == "-":
            return node_un_op(self.match("-"), self.factor(stopChars))
        elif self.currToken and self.currToken["tokenType"] == "!":
            return node_un_op(self.match("!"), self.factor(stopChars))
        elif self.currToken and self.currToken["tokenType"] == "(":
            self.match("(")
            return self.cast_val(stopChars)
        elif self.currToken and self.currToken["tokenType"] in PREDICT_SETS["atom"]:
            return self.atom()
        else:
            is_valid_value = False
            self.ERROR_expected_valid_value()

        return is_valid_value
    
    def cast_val(self, stopChars):
        # print("(parser-value-chain): Entered \"cast_val\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        is_valid_value = True
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["data_type"]:
            dtype = self.data_type()
            if not self.match(")"):
                is_valid_value = False
                self.ERROR_unclosed_parentheses()
            return node_un_op(dtype, self.factor(stopChars))
        elif self.currToken and self.currToken["tokenType"] in PREDICT_SETS["value"]:
            val_temp = self.value([")"])
            if not self.match(")"):
                is_valid_value = False
                self.ERROR_unclosed_parentheses()
            return val_temp
        else:
            if self.currToken:
                self.logError(f"Expected a data type for typecasting or a valid value, instead got '{self.currToken["tokenName"]}'.")
            else:
                self.logError(f"Expected a data type for typecasting or a valid value, instead reached EOF.")
        return is_valid_value

    def atom(self):
        # print("(parser-value-chain): Entered \"atom\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        is_valid_value = True
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["lit_type"]:
            return self.lit_type()
        elif self.currToken and self.currToken["tokenType"] == "in":
            return self.input()
        elif self.currToken and self.currToken["tokenType"] == "--":
            left_t = self.match("--")
            temp_id = self.match("Identifier")
            if not temp_id:
                is_valid_value = False
                if self.currToken and self.currToken["tokenType"] == "whole_lit":
                    self.ERROR_inc_dec_constant()
                elif self.currToken and self.currToken["tokenType"] in ["frac_lit", "string_lit", "bool_lit"]:
                    self.ERROR_inc_dec_not_int()
                else:
                    self.ERROR_expected_token("Identifier")
            else:
                return node_un_op(left_t, node_iden(temp_id))
        elif self.currToken and self.currToken["tokenType"] == "++":
            left_t = self.match("++")
            temp_id = self.match("Identifier")
            if not temp_id:
                is_valid_value = False
                if self.currToken and self.currToken["tokenType"] == "whole_lit":
                    self.ERROR_inc_dec_constant()
                elif self.currToken and self.currToken["tokenType"] in ["frac_lit", "string_lit", "bool_lit"]:
                    self.ERROR_inc_dec_not_int()
                else:
                    self.ERROR_expected_token("Identifier")
            else:
                return node_un_op(left_t, node_iden(temp_id))
        elif self.currToken and self.currToken["tokenType"] == "Identifier":
            temp_id = self.match("Identifier")
            temp_node = node_iden(temp_id)
            # print("(parser-value-chain): Entered \"atom\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
            if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["mods_post_op"]:
                temp_node = self.mods_post_op(node_iden(temp_id))
            return temp_node

        return is_valid_value

    def mods_post_op(self, temp_id):
        # print("(parser-value-chain): Entered \"mods_post_op\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["iden_mods"]:
            temp_node = self.iden_mods(temp_id)
        elif self.currToken and self.currToken["tokenType"] in ["++", "--"]:
            temp_node = self.mods_post_op_con(temp_id)
        return temp_node
    
    def mods_post_op_con(self, temp_id):
        # print("(parser-value-chain): Entered \"mods_post_op_con\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        match self.currToken["tokenType"]:
            case "++":
                return node_post_un_op(temp_id, self.match("++"))
            case "--":
                return node_post_un_op(temp_id, self.match("--"))

    def data_type(self):
        match self.currToken["tokenType"]:
            case "int":
                return self.match("int", False)
            case "long":
                return self.match("long", False)
            case "float":
                return self.match("float", False)
            case "double":
                return self.match("double", False)
            case "bool":
                return self.match("bool", False)
            case "string":
                return self.match("string", False)

    def lit_type(self):
        print('(parser) production: "lit_type" detected')
        if (self.currToken and self.currToken["tokenType"] == "whole_lit"):
            return node_num(self.match("whole_lit"))
        elif (self.currToken and self.currToken["tokenType"] == "frac_lit"):
            return node_num(self.match("frac_lit"))
        elif (self.currToken and self.currToken["tokenType"] == "string_lit"):
            return node_str(self.match("string_lit"))
        elif (self.currToken and self.currToken["tokenType"] == "bool_lit"):
            return node_bool(self.match("bool_lit"))


    def iden_mods(self, temp_id):
        print('(parser) production: "iden_mods" detected')
        is_valid_value = True
        if self.currToken and self.currToken["tokenType"] in ['(', '[']:
            return self.is_func_method_arr(temp_id)
        elif (self.currToken and self.currToken["tokenType"] == "."):
            self.match(".")
            tmp_att_id_n = node_iden(self.match("Identifier", False))
            node_temp = node_class_att(temp_id, tmp_att_id_n)
            if self.currToken and self.currToken["tokenType"] in ['(', '[']:
                node_temp = self.is_func_method_arr(temp_id, tmp_att_id_n)
            elif self.currToken and self.currToken["tokenType"] == '.':
                self.ERROR_further_class_access()

            return node_temp
        return is_valid_value 

    def is_func_method_arr(self, temp_id, tmp_att_id_n = None):
        if (self.currToken and self.currToken["tokenType"] == "("):
            self.match("(")
            if not tmp_att_id_n:
                node_temp = node_func_call(temp_id, self.func_arg())
            else:
                node_temp = node_class_func_call(temp_id, tmp_att_id_n, self.func_arg())
            if not self.match(")"):
                is_valid_value = False
                self.ERROR_unclosed_parentheses()
            else:
                return node_temp
        elif (self.currToken and self.currToken["tokenType"] == "["):
            return self.as_array(temp_id, tmp_att_id_n)
        
        return is_valid_value

    def as_array(self, temp_id = None, tmp_att_id_n = None):
        print('(parser) production: "as_array" detected')
        is_valid_value = True
        node_temp = None
        if (self.currToken and self.currToken["tokenType"] == "["):
            self.match("[")
            if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["int_val"]:
                val_temp = self.arith_exp(["]"])
                if not val_temp:
                    is_valid_value = False
                    self.ERROR_expected_pos_integer_value()
                else:
                    if not tmp_att_id_n:
                        node_temp = node_arr_idx(temp_id, val_temp)
                    else:
                        node_temp = node_class_arr_idx(temp_id, tmp_att_id_n, val_temp)
                
                if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["value"]:
                    self.ERROR_expected_operator()
                elif not self.match("]"):
                    is_valid_value = False
                    self.ERROR_unclosed_square_bracket()
                if (self.currToken and self.currToken["tokenType"] == "["):
                    if temp_id:
                        if not tmp_att_id_n:
                            node_temp = self.is_2d_arr(temp_id, val_temp)
                        else:
                            node_temp = self.is_2d_arr(temp_id, val_temp, tmp_att_id_n)
                    else:
                        node_temp = self.is_2d_arr()
            else:
                self.ERROR_expected_pos_integer_value()

        return node_temp 

    def is_2d_arr(self, temp_id = None, val1 = None, tmp_att_id_n = None):
        is_valid_value = True
        print('(parser) production: "is_2d_arr" detected')
        if (self.currToken and self.currToken["tokenType"] == "["):
            self.match("[")
            val_temp = self.arith_exp(["]"])
            if not val_temp:
                is_valid_value = False
                self.ERROR_expected_pos_integer_value()
            else:
                if (temp_id and val1):
                    if not tmp_att_id_n:
                        node_temp = node_arr_idx(temp_id, val1, val_temp)
                    else:
                        node_temp = node_class_arr_idx(temp_id, tmp_att_id_n, val1, val_temp)
                else:
                    node_temp = True
            if not self.match("]"):
                is_valid_value = False
                self.ERROR_unclosed_square_bracket()
            if self.currToken and self.currToken["tokenType"] == "[":
                is_valid_value = False
                self.logError("Only up to 2 dimensions of arrays are allowed.")
        return node_temp

    
    # def ret_type(self):
    #     print("(parser) production: \"ret_type\" detected")

    #     if self.currToken["tokenType"] in PREDICT_SETS["data_type"]:
    #         self.data_type()
    #     else:
    #         if not self.match("Identifier"):
    #             self.logError("Expected data type or Identifier (Class name).")

    #     print("(parser) production: \"ret_type\" exited!!!!!")


    # def params_var(self):
    #     print("(parser) production: \"params_var\" detected")

    #     if self.currToken:
    #         if not self.match("Identifier"):
    #             self.logError("Expected Identifier (variable declaration or class name).")
    #         if self.currToken:
    #             if self.peek(-2)["tokenType"] == "Identifier" and self.currToken:
    #                 if self.currToken["tokenType"] == "=":
    #                     self.logError("Default values for object parameters are not supported. Expected ')' or ','. Found '=' instead.")
    #                 elif self.currToken["tokenType"] == "[":  # array
    #                     self.logError("Array of objects is not supported. Expected ')' or ','. Found '[' instead.")
    #         self.params_var_cont()
    #     else:
    #         self.ERROR_expected_token("Identifier")

    #     print("(parser) production: \"params_var\" exited!!!!!")

    #TODO: harley continue here
    def params_var_cont(self, dtype_temp_t, id_temp_n, params_n):
        print("(parser) production: \"params_var_cont\" detected")
        if self.currToken:
            if self.currToken["tokenType"] == "[":
                params_n.append(node_funcpar_arr(dtype_temp_t, id_temp_n, self.is_array()))
                self.params_var_rec(params_n)
                # self.is_array()
            elif self.currToken["tokenType"] == ",":
                params_n.append(node_funcpar_var(dtype_temp_t, id_temp_n))
                self.params_var_rec(params_n)
            else:
                params_n.append(node_funcpar_var(dtype_temp_t, id_temp_n))

        print("(parser) production: \"params_var_cont\" exited!!!!!")

    def params_var_rec(self, params_n):
        print("(parser) production: \"params_var_rec\" detected")

        if self.currToken:
            if self.currToken["tokenType"] == ",":
                self.match(",")
                if not self.currToken or self.currToken and self.currToken["tokenType"] not in PREDICT_SETS["data_type"] and self.currToken["tokenType"] != "Identifier":
                    self.logError(f"Expected data type or Identifier (Class name), instead got '{self.currToken["tokenName"]}'.")
                return self.params_dec(params_n)
    
        print("(parser) production: \"params_var_rec\" exited!!!!!")


    def is_array(self):
        print("(parser) production: \"is_array\" detected")
        arrdim = 1
        self.match("[")
        if not self.match("]"):
            self.ERROR_array_as_param_no_val()

        if self.currToken and self.currToken["tokenType"] == "[":
            self.match("[")
            if not self.match("]"):
                self.ERROR_array_as_param_no_val()
            arrdim = 2

        if self.currToken and self.currToken["tokenType"] == "[":
            self.logError("Only up to 2-dimensional arrays are supported.")

        if self.currToken and self.currToken["tokenType"] == "=":
            self.logError("Default array values are not supported.")
        print("(parser) production: \"is_array\" exited!!!!!")
        return arrdim

    def params_dec(self, params_n = []):
        print(f"(parser) production: \"params_dec\" detected, {self.currToken["tokenType"] if self.currToken else "EOF"}")
        
        if self.currToken and self.currToken["tokenType"] != ")":
            if self.currToken["tokenType"] in PREDICT_SETS["data_type"]:
                dtype_temp_t = self.data_type()
                id_temp_n = node_iden(self.match("Identifier", False))
                # traverse data type iden or iden[][] and append inside that
                self.params_var_cont(dtype_temp_t, id_temp_n, params_n)
                
                # check if there is another parameter
                self.params_var_rec(params_n)

            elif self.currToken["tokenType"] == "Identifier":
                # self.match("Identifier", False)
                # self.match("Identifier", False)
                # self.params_var_rec()
                param_class_temp_n =  node_funcpar_class(node_iden(self.match("Identifier", False)), node_iden(self.match("Identifier", False)))
                params_n.append(param_class_temp_n)
                print("Entering params_var_rec after iden iden") 

                # check if there is another parameter
                self.params_var_rec(params_n)

        return params_n  
        # if self.currToken and self.currToken["tokenType"] != ")":
        #     if self.currToken and self.currToken["tokenType"] not in PREDICT_SETS["data_type"] and self.currToken["tokenType"] != "Identifier":
        #         self.logError(f"Expected data type or class name. Found '{self.currToken["tokenType"]}' instead.")
        #     self.ret_type()
        #     self.params_var()
        
  
  # ALEX start here
    def condition(self, condType, stopChar):  
        '''<condition> → <value>'''
        print("(parser) entered production: \"condition\"")

        if self.currToken:
            condition_temp_n = self.value(stopChar)
            if not condition_temp_n:
                if self.currToken["tokenType"] == stopChar:
                    self.ERROR_missing_condition(condType)
                else:
                    self.ERROR_invalid_condition(condType)
        
        print("(parser) exited production: \"condition\"")
        return node_condition_value(condition_temp_n)
        
    def output(self):
        '''<output> → <print_stmts>(<print_params>);'''
        print("(parser) entered production: \"output\"")
        
        '''<print_stmts> → print | println'''
        # <print_stmts> are already expected to be here before it entered func
        print_stmts_n = None
        print_params_n = []
        if self.matchPredictSet("print_stmts", False):
            match self.currToken["tokenType"]:
                case "print":
                    print_stmts_n = "print"
                    self.match("print")
                case "println":
                    print_stmts_n = "println"
                    self.match("println")

        self.match("(", False)
        
        # won't enter print_params if null
        if self.currToken and self.currToken["tokenType"] != ")":
            print_params_n = self.print_params(print_params_n)
        
        if not self.match(")"): 
            self.ERROR_unclosed_parentheses()

        print("(parser) exited production: \"output\"")
        return node_output(print_stmts_n, print_params_n)

    def print_params(self,print_params_n):
        '''<print_params> → <value> <output_rec> | null'''
        print("(parser) entered production: \"print_params\"")
        
        # if <print_params> are not null
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["value"]:
            if self.currToken and self.currToken["tokenType"] != ")":
                value_n = self.value([",", ")"])
                if not value_n: #gets commented out for dbg
                    self.logError("Invalid 'print' statement parameter.")
                print_params_n.append(value_n)

                if self.currToken and self.currToken["tokenType"] == ",":
                    self.output_rec(print_params_n)

        else:
            print("entered else")
            self.ERROR_expected_valid_value()
        
        print("(parser) exited production: \"print_params\"")
        return print_params_n

    def output_rec(self, print_params_n):
        '''<output_rec> → ,<value> <output_rec> | null'''
        print("(parser) entered production: \"output_rec\"")
        
        self.match(",", False)
        
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["value"]:
            value_n = self.value([",", ")"]) 
            if not value_n:
                message = f"Expected value after ',', got '{self.currToken['tokenType'] if self.currToken else 'EOF'}' instead."
                self.logError(message)
            print_params_n.append(value_n)

            if self.currToken and self.currToken["tokenType"] == ",":
                self.output_rec(print_params_n)
            
        else:
            self.ERROR_expected_valid_value()

        print("(parser) exited production: \"output_rec\"")
        return print_params_n
    
    def conditional_stmt(self, isVoid = False):
        '''<conditional_stmt> → <if_stmt> | <swicth_stmt>'''
        print("(parser) entered production: \"conditional_stmt\"")

        if self.currToken and self.currToken["tokenType"] == "if":
            node = self.if_stmt(isVoid)
            return node
        elif self.currToken and self.currToken["tokenType"] == "switch":
            node = self.switch_stmt(isVoid)
            return node

        print("(parser) exited production: \"conditional_stmt\"")
    
    def if_stmt(self, isVoid = False): 
        '''<if_stmt> → if(<condition) {<ctrl_stmt_body>} <else_chain>'''
        print(f"(parser) entered production: \"if_stmt\" , isVoid = {isVoid}")

        # if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["init_arg"]:

        body_n = None
        else_chain_n = None

        self.match("if", False)
        if not self.match("("):
            self.ERROR_missing_condition("if")
        condition_n = self.condition("if",[")"])
        if not self.match(")"): 
            self.ERROR_unclosed_parentheses()
        
        self.match("{", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"] + PREDICT_SETS["body"]:
            body_n = node_ctrl_stmt_body(self.ctrl_stmt_body(isVoid))
        if not self.match("}"):
            self.ERROR_unclosed_curly_braces()
        self.hasFunctionReturned = False

        if self.currToken and self.currToken["tokenType"] == "else":
            else_chain_n = self.else_chain()

        print("(parser) entered production: \"if_stmt\"")
        return node_if_stmt(condition_n, body_n, else_chain_n)
    
    def ret_value(self, isVoid = False):
        '''<ret_value> → <value> | null'''
        print("(parser) entered production: \"ret_value\", isVoid: ", isVoid)

        if self.hasFunctionReturned:
            self.logError("Function already has a return statement.")

        ret_value_n = None
        if self.currToken:
            if not isVoid and self.currToken["tokenType"] == ";" and not self.hasMainFunction:
                self.logError("Non-Void functions must return a value.")
            
            elif isVoid and self.currToken["tokenType"] != ";":
                self.logError(f"Void functions cannot return a value and must be terminated by ';', but found '{self.currToken["tokenName"] if self.currToken else "EOF"}'.")
        
        if not isVoid:
            ret_value_n = self.value([";"])

        print("(parser) exited production: \"ret_value\"")
        return ret_value_n

    # bare-minimum tested
    def break_stmt(self):
        '''<break_stmt> → break;'''
        print("(parser) entered production: \"break_stmt\"")

        self.match("break", False)
        if not self.match(";"):
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"break_stmt\"")
        return f"break;"

    # bare-minimum tested
    def continue_stmt(self):
        '''<continue_stmt> → continue;'''
        print("(parser) entered production: \"continue_stmt\"")

        self.match("continue", False)
        if not self.match(";"):
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"continue_stmt\"")
        return f"continue;"

    # bare-minimum tested
    def init_arg(self):
        '''<init_arg> → <data_type> <var_iden>| <assign_stmt> | null'''

        print("(parser) entered production: \"init_arg\"")
        
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["init_arg"]:
            currentTokenType = self.currToken["tokenType"]

            if currentTokenType == "Identifier":
                init_arg_n = self.assign_stmt()

            elif currentTokenType in PREDICT_SETS["data_type"]:
                dtype_temp_t = self.data_type()
                iden_temp_n = node_iden(self.match("Identifier",False))
                init_arg_n = self.var_dec_cont(dtype_temp_t, iden_temp_n)

            return init_arg_n 
        print("(parser) exited production: \"init_arg\"")
        return None

    # to continue testing
    def inc_arg(self):
        '''<inc_arg> → Identifier <inc_arg_post>
                        ++Identifier
                        --Identifier
                        <assign_func_method_mods>
                        ++
                        -- '''
        print("(parser) entered production: \"inc_arg\"")

        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["inc_arg"]:
            currentTokenType = self.currToken["tokenType"]
        
            if currentTokenType == "++":
                inc_arg_temp_n = node_un_op(self.match("++"), node_iden(self.match("Identifier", False)))

            elif currentTokenType == "--":
                inc_arg_temp_n = node_un_op(self.match("--"), node_iden(self.match("Identifier", False)))

            elif currentTokenType == "Identifier":
                id_temp_t = self.match("Identifier")
                if self.currToken["tokenType"] in PREDICT_SETS["inc_arg_post"]:
                    if self.currToken["tokenType"] == "++": 
                        inc_arg_temp_n = node_post_un_op(node_iden(id_temp_t), self.match("++"))
                    elif self.currToken["tokenType"] == "--": 
                        inc_arg_temp_n = node_post_un_op(node_iden(id_temp_t), self.match("--"))
                        
                elif self.currToken["tokenType"] in PREDICT_SETS["assign_func_method_mods"]:
                    inc_arg_temp_n = self.assign_func_method_mods(id_temp_t)

                else: self.logError("Expected: unary operation, assignment statement, function call, method call.")

            elif currentTokenType in PREDICT_SETS["print_stmts"]:
                inc_arg_temp_n = self.output()
            
            return inc_arg_temp_n

        print("(parser) exited production: \"inc_arg\"")
        return None

    # bare-minimum tested
    def else_chain(self):
        '''<else_stmt> → <if_stmt> | { <ctrl_stmt_body> }'''
        print("(parser) entered production: \"else_chain\"")
        
        if self.currToken:
            self.match("else", False)
            else_stmt_n = self.else_stmt()
            return node_else_chain(else_stmt_n)
        
        print("(parser) exited production: \"else_chain\"")
        return None

    def else_stmt(self, isVoid = False):
        print(f"(parser) entered production: \"else_stmt\", isVoid = {isVoid}")

        if self.currToken:

            body_n = None

            if self.currToken and self.currToken["tokenType"] == "if":
                return self.if_stmt()

            elif self.currToken and self.currToken["tokenType"] == "{":
                self.match("{", False)
                if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"] + PREDICT_SETS["body"]:
                    body_n = node_ctrl_stmt_body(self.ctrl_stmt_body(isVoid))
                if not self.currToken:
                    self.ERROR_unclosed_curly_braces()
                self.match("}", False)
                self.hasFunctionReturned = False
                return node_else_stmt(body_n)
            
            else:
                self.logError("Expected: else if statement or else body")

        print("(parser) exited production: \"else_stmt\"")
        return None

    # bare-minimum tested
    def switch_stmt(self, isVoid = False):
        '''<switch_stmt> → switch (<value>) {<case_stmt> <default_stmt>}'''
        print("(parser) entered production: \"switch_stmt\"")

        if self.currToken:
            default_temp_n = None
        
            self.match("switch", False)

            if not self.match("("):
                self.ERROR_missing_condition("switch")
            
            ## TODO: FIX!!!!!
            value_temp_n = None
            if self.currToken["tokenType"] in PREDICT_SETS["switch_value"]:
                value_temp_n = self.value([")", "{"])
            
            if not value_temp_n:
                self.ERROR_empty_condition("switch")
            
            if not self.match(")"): 
                self.ERROR_unclosed_parentheses()
            
            self.match("{", False)
            case_temp_n = node_case(self.case_stmt(isVoid))
            
            if self.currToken["tokenType"] == "default":
                default_temp_n = self.default_stmt(isVoid)

            if not self.currToken:
                self.ERROR_unclosed_curly_braces()
            self.match("}", False)
            self.hasFunctionReturned = False

        print("(parser) exited production: \"switch_stmt\"")
        
        return node_switch_stmt(value_temp_n, case_temp_n, default_temp_n)

    # bare-minimum tested
    def case_stmt(self, isVoid = False):
        '''<case_stmt> → case <case_value>: <ctrl_stmt_body> <case_stmt_rec>'''
        print("(parser) entered production: \"case_stmt\"")

        if self.currToken:
            ctrl_stmt_body_temp_n = None
            case_stmt_n = []

            self.match("case", False)
            case_value_temp_n = self.case_value()
            self.match(":", False)
            
            if self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
                ctrl_stmt_body_temp_n = node_ctrl_stmt_body(self.ctrl_stmt_body(isVoid))
            
            case_stmt_n.append(node_case_stmt(case_value_temp_n, ctrl_stmt_body_temp_n))

            if self.currToken["tokenType"] == "case":
                case_stmt_n += self.case_stmt()
            
        print("(parser) exited production: \"case_stmt\" !!!!!!!!!!!")
        return case_stmt_n
    

    # bare-minimum tested
    def case_value(self):
        '''<switch_value> → string_lit | whole_lit | <negative_exp> '''
        print("(parser) entered production: \"case_value\"") 

        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["case_value"]:
            currentTokenType = self.currToken["tokenType"]
        
            if currentTokenType == "string_lit": 
                case_value_temp_t = self.match("string_lit", False)
                
            elif currentTokenType == "whole_lit": 
                case_value_temp_t = self.match("whole_lit", False)
            
            elif currentTokenType == "-":
                case_value_temp_t = node_un_op(self.match("-", False), self.match("whole_lit"))
                
                #if not case_value_temp_t:
                #    self.logError("Expected negative numerical constant.")
            
            else:
                self.logError("Invalid value for 'case' statement.")

        else: self.logError("'case' must be preceded with a valid value (Whole Number or String).")

        print("(parser) exited production: \"case_value\"")
        return case_value_temp_t


    # bare-minimum tested
    def default_stmt(self, isVoid = False):
        ctrl_stmt_body_temp_n = None
        
        self.match("default", False)
        self.match(":", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
            ctrl_stmt_body_temp_n = node_ctrl_stmt_body(self.ctrl_stmt_body(isVoid))

        return node_default_stmt(ctrl_stmt_body_temp_n)
    
    # bare-minimum tested
    def loop_stmt(self, isVoid = False):
        print("(parser) entered production: \"loop_stmt\"")
        
        match self.currToken["tokenType"]:
            case "while": 
                loop_stmt_temp_n = self.while_stmt(isVoid)
            case "do": 
                loop_stmt_temp_n = self.do_stmt(isVoid)
            case "for": 
                loop_stmt_temp_n = self.forloop_stmt(isVoid)
            case "repeat": 
                loop_stmt_temp_n = self.repeat_stmt(isVoid) 

        print("(parser) exited production: \"loop_stmt\"")
        print (node_loop_stmt(loop_stmt_temp_n))
        return node_loop_stmt(loop_stmt_temp_n)
        
    
    # bare-minimum tested
    def forloop_stmt(self, isVoid = False):
        print("(parser) entered production: \"forloop_stmt\"")

        if self.currToken:

            init_arg_temp_n = None
            inc_arg_temp_n = None
            ctrl_stmt_body_temp_n = None

            self.match("for", False)
            if not self.match("("):
                self.logError("Missing forloop arguments.")

            ## INIT ARG
            if self.currToken["tokenType"] in PREDICT_SETS["init_arg"]:
                init_arg_temp_n = self.init_arg()
            else: 
                print("(parser) empty init_arg detected")
            
            if not self.match(";"):
                self.logError(f"Initialization argument is expected to be terminated by ';', but found '{self.currToken["tokenType"] if self.currToken else "EOF"}'.")
            
            ## CONDITION
            condition_temp_n = self.condition("for-loop",[";"])
            if not condition_temp_n:
                self.ERROR_empty_condition("for-loop")
            
            if not self.match(";"):
                self.logError(f"Condition argument is expected to be terminated by ';', but found '{self.currToken["tokenType"] if self.currToken else "EOF"}'.")

            ## INC ARG
            if self.currToken["tokenType"] in PREDICT_SETS["inc_arg"]:
                inc_arg_temp_n = self.inc_arg()
            else: 
                print("(parser) empty inc_arg detected")

            if not self.match(")"):
                self.ERROR_unclosed_parentheses()

            ## CTRL STMT BODY
            self.match("{", False)
            if self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
                ctrl_stmt_body_temp_n = node_ctrl_stmt_body(self.ctrl_stmt_body(isVoid))
            
            if not self.currToken:
                self.ERROR_unclosed_curly_braces()
            self.match("}", False)
            self.hasFunctionReturned = False
                
        print("(parser) exited production: \"forloop_stmt\"")
        return node_forloop(init_arg_temp_n, condition_temp_n, inc_arg_temp_n, ctrl_stmt_body_temp_n)
    
    # bare-minimum tested
    def while_stmt(self, isVoid = False):
        print("(parser) entered production: \"while_stmt\"")

        if self.currToken:

            ctrl_stmt_body_temp_n = None
            self.match("while", False)
            
            if not self.match("("):
                self.ERROR_missing_condition("while")

            condition_temp_n = self.condition("while",[")"])

            if not self.match(")"):
                self.ERROR_unclosed_parentheses()
            
            self.match("{", False)
            if self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
                ctrl_stmt_body_temp_n = node_ctrl_stmt_body(self.ctrl_stmt_body(isVoid))
            
            if not self.currToken:
                self.ERROR_unclosed_curly_braces()
            self.match("}", False)
            self.hasFunctionReturned = False
        
        print("(parser) exited production: \"while_stmt\"")
        return node_while(condition_temp_n, ctrl_stmt_body_temp_n)

    # bare-minimum tested
    def do_stmt(self, isVoid = False):
        print("(parser) entered production: \"do_stmt\"")
        
        if self.currToken:
            
            self.match("do", False)
            self.match("{", False)
            
            ## CTRL STMT BODY
            ctrl_stmt_body_temp_n = None
            if self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
                ctrl_stmt_body_temp_n = node_ctrl_stmt_body(self.ctrl_stmt_body(isVoid))

            if not self.match("}"):
                self.ERROR_unclosed_curly_braces()

            self.hasFunctionReturned = False
            
            ## WHILE STMT
            if not self.match("while"):
                self.logError("'do' statement must include 'while' condition after '}'.")
            
            ## CONTINUE
            if not self.match("("):
                self.ERROR_missing_condition("do-while")
            condition_temp_n = self.condition("do-while",[")"])
            if not self.match(")"):
                self.ERROR_unclosed_parentheses()
            
            if not self.match(";", True):
                self.logError("'while' statements must be terminated by ';' in a do-while statement.")

        print("(parser) exited production: \"do_stmt\"")
        return node_do(condition_temp_n, ctrl_stmt_body_temp_n)

    # bare-minimum tested
    def repeat_stmt(self, isVoid = False):
        print("(parser) entered production: \"repeat_stmt\"")

        if self.currToken:

            self.match("repeat", False)
            if not self.match("("):
                self.logError("Expected argument for 'repeat' statement")

            repeat_value_temp_n = self.arith_exp([")"])

            if not repeat_value_temp_n:
                self.ERROR_expected_pos_integer_value()

            if not self.match(")"):
                self.ERROR_unclosed_parentheses()
            
            self.match("{", False)

            ctrl_stmt_body_temp_n = None
            if self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
                ctrl_stmt_body_temp_n = node_ctrl_stmt_body(self.ctrl_stmt_body(isVoid))

            if not self.match("}"):
                self.ERROR_unclosed_curly_braces()

            self.hasFunctionReturned = False
        
        print("(parser) exited production: \"repeat_stmt\"")
        return node_repeat(repeat_value_temp_n, ctrl_stmt_body_temp_n)
    
    
    def return_block(self, isVoid = False):
        print("(parser) entered production: \"return_block\"")
        
        self.match("return", False)
        ret_value_n = self.ret_value(isVoid)
        if not self.match(";"):
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"return_block\"")
        return node_return_block(ret_value_n)
    
    # bare-minimum tested
    def ctrl_stmt_body(self, isVoid = False):
        print("(parser) entered production: \"ctrl_stmt_body\"")
        
        statements_n = []
        if self.currToken:
            currentTokenType = self.currToken["tokenType"]

            if currentTokenType == "break":
                statements_n.append(self.break_stmt())
            elif currentTokenType == "continue":
                statements_n.append(self.continue_stmt())
            elif currentTokenType in PREDICT_SETS["code_block"]:
                # statements_n.append(self.body(["break", "continue", "case", "}", "default"], isVoid, True))
                statements_n.extend(self.code_block([], isVoid).code_block_statement_n)
            elif currentTokenType == "return":
                statements_n.append(self.return_block(isVoid))
            if self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"] and currentTokenType not in ["}", "case", "default"]:
                statements_n += self.ctrl_stmt_body(isVoid)

        print("(parser) exited production: \"ctrl_stmt_body\"")
        
        return statements_n

#jeh
    def input(self):
        print("(parser) entered production: \"input\"")
        '''<input> → in<data_type>(<input_params>)'''
        
        if self.currToken:
            self.match("in", False)
            self.match("<", False)

            if self.currToken["tokenType"] in PREDICT_SETS["data_type"]:
                type_t = self.data_type()
            else:
                self.ERROR_expected_token(PREDICT_SETS["data_type"])
            
            if not self.match(">"):
                self.ERROR_unclosed_angled_bracket()
            node_temp = node_input(type_t)
            self.match("(", False)

            if self.currToken and self.currToken["tokenType"] != ")":
                if self.currToken["tokenType"] in PREDICT_SETS["string_value"]:
                    node_temp = self.input_params(type_t)
                else:  # semantic check if string or syntax error
                    self.logError("Expected a valid value of type \"string\" for an input function's first parameter.")

            
            if not self.match(")"):
                self.ERROR_unclosed_parentheses()
            
            #else: self.logError("Invalid value for 'in' statement message.")
        
        print("(parser) exited production: \"input\"")
        return node_temp

    def input_params(self, type_t):
        print("(parser) entered production: \"input_params\"")
        """<input_params> → <value> <in_param_two> | λ"""
        count_n = None
        print(f'(parser)(dbg) in input params prod, current token is {self.currToken}')
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["string_value"]:
            prompt_n = self.value([")", ","])
            if self.currToken and self.currToken["tokenType"] == ",":
                count_n = self.in_param_two()
        
        print("(parser) exited production: \"input_params\"")
        return node_input(type_t, prompt_n, count_n)

    def in_param_two(self):
        print("(parser) entered production: \"in_param_two\"")
        
        if self.currToken:
            self.match(",")
            if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["int_val"]:
                ret = self.arith_exp([")"])
                if not ret:
                    self.ERROR_expected_int_value_in_stmt()
                else:
                    return ret
            else:
                self.ERROR_expected_int_value_in_stmt()

        
        print("(parser) exited production: \"in_param_two\"")


    def var_init(self):
        """<var_init> → = <value> | λ"""
        print("(parser) entered production: \"var_init\"")
        
        if self.currToken:
            currentTokenType = self.currToken["tokenType"]

            if currentTokenType == "=":
                self.match("=", False)
                value_temp_n = self.value(PREDICT_SETS["var_init"])
                if not value_temp_n:
                    self.logError("Invalid value for variable declaration.")
                return value_temp_n
        print("(parser) exited production: \"var_init\"")
        return None

    
    def var_iden_rec(self, idec_rec_stmt_n = []):
        """<var_iden_rec> → , Identifier <var_init> <var_iden_rec> | λ"""
        print("(parser) entered production: \"var_iden_rec\"")
        
        if self.currToken:
            if self.currToken["tokenType"] == ",":
                self.match(",")
                id_temp_t = self.match("Identifier")
                if id_temp_t:
                    id_temp_n = node_iden(id_temp_t)
                    value_temp_n = self.var_init()
                    idec_rec_stmt_n.append(node_idec_rec_stmt(id_temp_n, value_temp_n))
                    if self.currToken["tokenType"] == ",":
                        self.var_iden_rec(idec_rec_stmt_n)
                else:
                    self.ERROR_expected_token("Identifier")
                return idec_rec_stmt_n
            
        print("(parser) exited production: \"var_iden_rec\"")
        return idec_rec_stmt_n

    def var_id_arr1D(self, dtype_temp_t, id_temp_n, size1_temp_n):
        '''<var_id_arr1D> → <array1D_iden_rec> | <array1D_init>'''
        
        print("(parser) entered production: \"var_id_arr1D\"")
        
        if self.currToken:
            currentTokenType = self.currToken["tokenType"]

            if currentTokenType == ",":
                return node_arr_dec(dtype_temp_t, id_temp_n, size1_temp_n, None, self.array1D_iden_rec([]))

            elif currentTokenType == "=":
                return node_arr_dec(dtype_temp_t, id_temp_n, size1_temp_n, None, self.array1D_init([]))

            elif currentTokenType == "[":
                self.match("[", False)
                size2_temp_n = self.arith_exp(["]"])
                if not size2_temp_n:
                    self.ERROR_expected_pos_integer_value()
                if not self.match("]"):
                    self.ERROR_unclosed_square_bracket()
                if self.currToken["tokenType"] == "[":
                    self.logError("Only up to 2 dimensions of arrays are allowed.")
                return self.var_id_arr2D(dtype_temp_t, id_temp_n, size1_temp_n, size2_temp_n)
        
        print("(parser) exited production: \"var_id_arr1D\"")
        return node_arr_dec(dtype_temp_t, id_temp_n, size1_temp_n, None, None)


    def array1D_iden_rec(self, arr_dec_rec_temp_n = []):
        '''<array1D_iden_rec> → , Identifier [<int_val>] <array1D_iden_rec> | λ'''
        print("(parser) entered production: \"array1D_iden_rec\"")
        if self.currToken:
            self.match(",")
            id_temp_n = node_iden(self.match("Identifier", False))
            self.match("[", False)
            size1_temp_n = self.arith_exp(["]"])
            arr_dec_rec_temp_n.append(node_arr_dec_rec(id_temp_n, size1_temp_n, None))
            if not size1_temp_n:
                self.ERROR_expected_pos_integer_value()
            if not self.match("]"):
                self.ERROR_unclosed_square_bracket()
            if self.currToken["tokenType"] == ",":
                self.array1D_iden_rec(arr_dec_rec_temp_n)

        print("(parser) exited production: \"array1D_iden_rec\"")
        return arr_dec_rec_temp_n

    def array1D_init(self, val_list = []):
            '''<array1D_init> → = {<arr_value_1D>}'''
            print("(parser) entered production: \"array1D_init\"")
            if self.currToken:
                self.match("=", False)
                self.match("{", False)
                self.arr_value_1D(val_list)
                if not self.match("}"):
                    self.ERROR_unclosed_curly_braces()
            
            print("(parser) exited production: \"array1D_init\"")
            return val_list

    def arr_value_1D(self, val_list):
            '''<arr_value_1D> → <value> <arr_value_1D_rec>'''
            print("(parser) entered production: \"arr_value_1D\"")
            if self.currToken:
                
                if self.currToken["tokenType"] in PREDICT_SETS["value"]:
                    val_list.append(self.value(["}", ","]))
                    if self.currToken["tokenType"] == ",":
                        self.arr_value_1D_rec(val_list)
                else:
                    self.ERROR_expected_token("value")

            print("(parser) exited production: \"arr_value_1D\"")
            return val_list

    def arr_value_1D_rec(self, val_list):
            '''<arr_value_1D_rec> → , <value> <arr_value_1D_rec> | λ'''
            print("(parser) entered production: \"arr_value_1D_rec\"")
            if self.currToken:

                if self.currToken["tokenType"] == ",":
                    self.match(",")
                    if self.currToken["tokenType"] in PREDICT_SETS["value"]:
                        val_list.append(self.value(["}", ","]))
                        self.arr_value_1D_rec(val_list)
                    else:
                        self.ERROR_expected_token("value")
            
            print("(parser) exited production: \"arr_value_1D_rec\"")
            
    
    def var_id_arr2D(self, dtype_temp_t, id_temp_n, size1_temp_n, size2_temp_n):
            '''<var_id_arr2D> → <array2D_iden_rec> | <array2D_init>'''
            print("(parser) entered production: \"var_id_arr2D\"")
            
            if self.currToken:
                currentTokenType = self.currToken["tokenType"]

                if currentTokenType == ",":
                    return node_arr_dec(dtype_temp_t, id_temp_n, size1_temp_n, size2_temp_n, self.array2D_iden_rec([])) 
                elif currentTokenType == "=":
                    return node_arr_dec(dtype_temp_t, id_temp_n, size1_temp_n, size2_temp_n, self.array2D_init())
                #else:
                #    self.ERROR_expected_token([",", "="])

            print("(parser) exited production: \"var_id_arr2D\"")
            return node_arr_dec(dtype_temp_t, id_temp_n, size1_temp_n, size2_temp_n, None)

    def array2D_iden_rec(self, arr_dec_rec_temp_n = []):
            '''<array2D_iden_rec> → , Identifier [<int_val>] [<int_val>] <array2D_iden_rec> | λ'''
            print("(parser) entered production: \"array2D_iden_rec\"")
            if self.currToken:

                self.match(",")
                id_temp_n = node_iden(self.match("Identifier", False))
                
                self.match("[", False)
                size1_temp_n = self.arith_exp(["]"])
                if not size1_temp_n:
                    self.ERROR_expected_pos_integer_value()
                if not self.match("]"):
                    self.ERROR_unclosed_square_bracket()
                
                self.match("[", False)
                size2_temp_n = self.arith_exp(["]"])
                if not size2_temp_n:
                    self.ERROR_expected_pos_integer_value()
                if not self.match("]"):
                    self.ERROR_unclosed_square_bracket()
                if self.currToken["tokenType"] == "[":
                    self.logError("Only up to 2 dimensions of arrays are allowed.")
                arr_dec_rec_temp_n.append(node_arr_dec_rec(id_temp_n, size1_temp_n, size2_temp_n))
                if self.currToken["tokenType"] == ",":
                    self.array2D_iden_rec(arr_dec_rec_temp_n)
                
                #else:
                #    self.ERROR_unclosed_square_bracket()

            print("(parser) exited production: \"array2D_iden_rec\"")
            return arr_dec_rec_temp_n

    def array2D_init(self, val_2dlist = []):
            '''<array2D_init> → = {<arr_value_2D>}'''
            print("(parser) entered production: \"array2D_init\"")
            if self.currToken:
                self.match("=", False)
                self.match("{", False)
                self.arr_value_2D(val_2dlist)
                if not self.match("}"):
                    self.ERROR_unclosed_curly_braces()
            
            print("(parser) exited production: \"array2D_init\"")
            return val_2dlist
    
    def arr_value_2D(self, val_2dlist):
            '''<arr_value_2D> → {<arr_value_1D>} <arr_value_2D_rec>'''
            print("(parser) entered production: \"arr_value_2D\"")
            if self.currToken:
                self.match("{", False)
                val_2dlist.append(self.arr_value_1D([]))
                if not self.match("}"):
                    self.ERROR_unclosed_curly_braces()
                self.arr_value_2D_rec(val_2dlist)

            print("(parser) exited production: \"arr_value_2D\"")

    def arr_value_2D_rec(self, val_2dlist):
            '''<arr_value_2D_rec> → , {<arr_value_1D>} <arr_value_2D_rec> | λ'''
            print("(parser) entered production: \"arr_value_2D_rec\"")
            if self.currToken:
                self.match(",")
                self.match("{", False)
                val_2dlist.append(self.arr_value_1D([]))
                if not self.match("}"):
                    self.ERROR_unclosed_curly_braces()
                if self.currToken["tokenType"] == ",":
                    self.arr_value_2D_rec(val_2dlist)
        
            print("(parser) exited production: \"arr_value_2D_rec\"")


    def assign_stmt(self):
        print("(parser) production: \"assign_stmt\" detected")
        """<assign_stmt> → Identifier <iden_as_var_mods> <assign_stmt_op>"""
        node_temp = None
        temp_id = node_iden(self.match("Identifier", False))

        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["iden_as_var_mods"]:
            node_temp = self.iden_as_var_mods(temp_id) # match iden mods if there are any
            print("NODE TEMP1!!!!" + str(node_temp))

        if self.matchPredictSet("assign_operator", False):
            assign_stmt_temp_op_n, assign_stmt_temp_val_n = self.assign_stmt_op() # get & match assign operator and value

        print("(parser) exited production: \"assign_stmt\"")
        return node_assign_stmt(node_temp if node_temp else temp_id, assign_stmt_temp_op_n, assign_stmt_temp_val_n)

    def assign_stmt_op(self):
        print('(parser) production: "assign_stmt_op" detected')

        assign_stmt_temp_op_n = self.currToken["tokenType"]
        
        self.match(self.currToken["tokenName"])

        assign_stmt_temp_val_n = self.value([";",")"])

        if not assign_stmt_temp_val_n:  # check valid value
            self.ERROR_expected_token("value")

        return (assign_stmt_temp_op_n, assign_stmt_temp_val_n)

    def iden_as_var_mods(self, temp_id = None):
        print("(parser) production: \"iden_as_var_mods\" detected")
        node_temp = None
        if self.currToken and self.currToken["tokenType"] == "[":
            print("(parser) production: INSIDE \"iden_as_var_mods\" going to as_array")
            # array element
            print("FOUND ARRAY INASSIGN STMHMT ARR[1]")
            node_temp = self.as_array(temp_id)  # returns node_arr_idx = arr[1] or arr[1][1]

        elif self.currToken and self.currToken["tokenType"] == ".":
            # object attribute (can be object attribute of an array element upon recursion)
            print("(parser) production: INSIDE \"iden_as_var_mods\" now checking identifier")
            self.match(".")
            temp_att_id = self.match("Identifier", False)["tokenName"]
            if self.currToken and self.currToken["tokenType"] == "[":
                print("FOUND ARRAY INASSIGN STMHMT IDEN.ARR[1]")
                print("(parser) production: INSIDE \"iden_as_var_mods\" going to as_array")
                # object array element
                node_temp = self.as_array(temp_id, temp_att_id) # returns node_class_arr_idx = obj.arr[1] or obj.arr[1][1]
                print(node_temp)
            elif self.currToken and self.currToken["tokenType"] in PREDICT_SETS["assign_operator"]:
                # object attribute
                print("(parser) production: INSIDE \"iden_as_var_mods\" now checking assign_stmt_op")
                node_temp = node_class_att(temp_id, temp_att_id) # returns node_class_att = obj.att
        else:
            print("(parser-debug): assign statement variable has no var mods")
            pass
        
        print("(parser) exited production: \"iden_as_var_mods\"")
        return node_temp
       