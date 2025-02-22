import semantic_analyzer

#-------------------- PREDICT SETS --------------------
PREDICT_SETS = {
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
    
#------------------SEMANTIC ANALYZER-----------
sema = semantic_analyzer.SemanticAnalyzer()

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
        self.index_n = idx_n
        self.index2_n = idx2_n
    def __repr__(self):
        return f'{self.id_n}[{self.idx_n}]' + f'[{self.idx2_n}]' if self.idx2_n else '' 

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
        self.index_n = idx_n
        self.index2_n = idx2_n
    def __repr__(self):
        return f'{self.id_n}.{self.att_n}[{self.idx_n}]' + f'[{self.idx2_n}]' if self.idx2_n else '' 

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
        return f'({self.left_n} {self.op_t["tokenName"]} {self.right_n})'

class node_un_op:
    def __init__(self, left_t, right_n):
        self.left_t = left_t
        self.right_n = right_n
    def __repr__(self):
        return f'({self.left_t["tokenName"]} {self.right_n})'

class node_post_un_op:
    def __init__(self, left_n, right_t):
        self.left_n = left_n
        self.right_t = right_t
    def __repr__(self):
        return f'({self.left_n} {self.right_t["tokenName"]})'

class node_input:
    def __init__(self, type_t, prompt_n = None, count_n = None):
        self.type_t = type_t
        self.prompt_n = prompt_n
        self.count_n = count_n
    def __repr__(self):
        return f'in<{self.type_t["tokenName"]}>({self.prompt_n}, {self.count_n})'

class node_vardec:
    def __init__ (self, const_b, dtype_t, id_n, vardec_cont_n):
        self.const_b = const_b
        self.dtype_t = dtype_t
        self.id_n = id_n
        self.vardec_cont_n = vardec_cont_n
    def __repr__(self):
        return f'const: {self.const_b}, dtype: {self.dtype_t}, id: {self.id_n}, {self.vardec_cont_n}'

class node_vardec_cont:
    def __init__(self, value_n, idec_rec_n):
        self.value_n = value_n
        self.idec_rec_n = idec_rec_n
    
    def __repr__(self):
        return f"value: {self.value_n}, idec_rec_n: {self.idec_rec_n}"

class node_idec_rec:
    def __init__(self, id_n, value_n, idec_rec_n):
        self.id_n = id_n
        self.value_n = value_n
        self.idec_rec_n = idec_rec_n

class node_funcpar_var_defrec:
    def __init__(self, dtype_t, id_n, parvar_defrec_cont_n):
        self.dtype_t = dtype_t
        self.id_n = id_n
        self.parvar_defrec_cont_n = parvar_defrec_cont_n

class node_funcpar_var_defreccont:
    def __init__(self, value_n, parvar_defrec_n):
        self.value_n = value_n
        self.parvar_defrec_n = parvar_defrec_n

class node_output:
    def __init__(self, print_stmts_n, print_params_n):
        self.print_stmts_n = print_stmts_n
        self.print_params_n = print_params_n
    def __repr__(self):
        return f'{self.print_stmts_n}({self.print_params_n})'

class node_print_stmts:
    def __init__(self, type_t):
        self.type_t = type_t  
    def __repr__(self):
        return f'{self.type_t}'

class node_print_params:
    def __init__(self, value_n, output_rec_n=None):
        self.value_n = value_n  
        self.output_rec_n = output_rec_n  
    def __repr__(self):
        return f'{self.value_n} {self.output_rec_n if self.output_rec_n else ""}'

class node_output_rec:
    def __init__(self, value_n=None, output_rec_n=None):
        self.value_n = value_n  
        self.output_rec_n = output_rec_n  
    def __repr__(self):
        return f'{"," if self.value_n else ""} {self.value_n} {self.output_rec_n if self.output_rec_n else ""}'

class node_body:
    def __init__(self,statements_n, return_stmt_n=None):
        self.statements_n = statements_n
        self.return_stmt_n = return_stmt_n
    def __repr__(self):
        return f'body(statements_n={self.statements_n}, return_stmt_n={self.return_stmt_n})'

class node_return_block:
    def __init__(self, ret_value_n=None):
        self.ret_value_n = ret_value_n
    def __repr__(self):
        return f'return_block(ret_value_n={self.ret_value_n})'

class node_ret_value:
    def __init__(self, value_n=None):
        self.value_n = value_n
    def __repr__(self):
        return f'ret_value(value_n={self.value_n})'

class node_if_stmt:
    def __init__(self, condition_n, body_n, else_chain_n=None):
        self.condition_n = condition_n
        self.body_n = body_n
        self.else_chain_n = else_chain_n
    def __repr__(self):
        return f'if({self.condition_n}) {{ {self.body_n} }} {self.else_chain_n if self.else_chain_n else ""}'

class node_else_chain:
    def __init__(self, else_stmt_n):
        self.else_stmt_n = else_stmt_n
    def __repr__(self):
        return f'else {self.else_stmt_n}'

class node_else_stmt:
    def __init__(self, body_n):
        self.body_n = body_n
    def __repr__(self):
        return f'{{ {self.body_n} }}'

class node_ctrl_stmt_body:
    def __init__(self, statements_n):
        self.statements_n = statements_n
    def __repr__(self):
        return f'; ' .join(map(str, self.statements_n)) 

class node_break_stmt:
    def __repr__(self):
        return 'break;'

class node_continue_stmt:
    def __repr__(self):
        return 'continue;'

class node_class_inst:
    def __init__(self, class_id_n, obj_id_n, class_instcont_n):
        self.class_id_n = class_id_n
        self.obj_id_n = obj_id_n
        self.class_instcont_n = class_instcont_n

    def __repr__(self):
        return (f"node_class_inst(class_id_n={self.class_id_n}, "
                f"obj_id_n={self.obj_id_n}, "
                f"class_instcont_n={self.class_instcont_n})")

class node_classinst_cont:
    def __init__(self, class_id_n, func_arg_n):
        self.class_id_n = class_id_n
        self.func_arg_n = func_arg_n

    def __repr__(self):
        return f"node_classinst_cont(class_id_n={self.class_id_n}, func_arg_n={self.func_arg_n})"

class node_class_dec:
    def __init__(self, is_private_b, class_id_n, class_body_n, constructor_dec_n):
        self.is_private_b = is_private_b
        self.class_id_n = class_id_n
        self.class_body_n = class_body_n
        self.constructor_dec_n = constructor_dec_n

    def __repr__(self):
        return (f"node_class_dec(is_private_b={self.is_private_b}, "
                f"class_id_n={self.class_id_n}, "
                f"class_body_n={self.class_body_n}, "
                f"constructor_dec_n={self.constructor_dec_n})")

class node_class_body:
    def __init__(self, is_private_b, node_vardec, class_body_rec_n):
        self.is_private_b = is_private_b
        self.node_vardec = node_vardec
        self.class_body_rec_n = class_body_rec_n

    def __repr__(self):
        return (f"node_class_body(is_private_b={self.is_private_b}, "
                f"node_vardec={self.node_vardec}, "
                f"class_body_rec_n={self.class_body_rec_n})")

class node_constructor_dec:
    def __init__(self, class_id_n, params_dec_n, code_block_n):
        self.class_id_n = class_id_n
        self.params_dec_n = params_dec_n
        self.code_block_n = code_block_n

    def __repr__(self):
        return (f"node_constructor_dec(class_id_n={self.class_id_n}, "
                f"params_dec_n={self.params_dec_n}, "
                f"code_block_n={self.code_block_n})")


# alex here
class node_condition:
    def __init__(self, condition_n):
        self.condition_n = condition_n
    def __repr__(self):
        return f"condition: {self.condition_n}"

class node_switch_stmt:
    def __init__(self, value_n, case_n, default_n):
        self.value_n = value_n
        self.case_n = case_n
        self.default_n = default_n

    def __repr__(self):
        return f"switch ( switch_value: {self.value_n} ) {{ case -> {self.case_n} \n\t default -> {self.default_n} \n}}\n"

class node_case_stmt:
    def __init__(self, case_value_n, ctrl_stmt_body_n, case_stmt_rec_n):
        self.case_value_n = case_value_n
        self.ctrl_stmt_body_n = ctrl_stmt_body_n
        self.case_stmt_rec_n = case_stmt_rec_n

    def __repr__(self):
        return f"\n\t case {self.case_value_n}: ctrl_stmt_body -> {self.ctrl_stmt_body_n} \n\t case_stmt_rec -> {self.case_stmt_rec_n}"
        
class node_default_stmt:
    def __init__(self, ctrl_stmt_body_n):
        self.ctrl_stmt_body_n = ctrl_stmt_body_n

    def __repr__(self):
        return f"default: ctrl_stmt_body -> {self.ctrl_stmt_body_n}"

class node_loop_stmt:
    def __init__(self, loop_stmt_n):
        self.loop_stmt_n = loop_stmt_n
    def __repr__(self):
        return f"loop_stmt -> {self.loop_stmt_n}\n"

class node_forloop:
    def __init__(self, init_arg_n, condition_n, inc_arg_n, ctrl_stmt_body_n):
        self.init_arg_n = init_arg_n
        self.condition_n = condition_n
        self.inc_arg_n = inc_arg_n
        self.ctrl_stmt_body_n = ctrl_stmt_body_n

    def __repr__(self):
        return f"for ( \n\t init_arg -> {self.init_arg_n} \n\t {self.condition_n} \n\t inc_arg -> {self.inc_arg_n} \n) {{ \n\t ctrl_stmt_body -> {self.ctrl_stmt_body_n} \n}}\n"

class node_while:
    def __init__(self, condition_n, ctrl_stmt_body_n):
        self.condition_n = condition_n
        self.ctrl_stmt_body_n = ctrl_stmt_body_n

    def __repr__(self):
        return f"while ( {self.condition_n} ) {{ \n\t ctrl_stmt_body -> {self.ctrl_stmt_body_n} \n}}\n"

class node_do:
    def __init__(self, condition_n, ctrl_stmt_body_n):
        self.condition_n = condition_n
        self.ctrl_stmt_body_n = ctrl_stmt_body_n

    def __repr__(self):
        return f"do {{ \n\t ctrl_stmt_body -> {self.ctrl_stmt_body_n} \n}} \n while ( {self.condition_n} )\n"

class node_repeat:
    def __init__(self, repeat_value_n, ctrl_stmt_body_n):
        self.repeat_value_n = repeat_value_n
        self.ctrl_stmt_body_n = ctrl_stmt_body_n

    def __repr__(self):
        return f"repeat ( repeat_value: {self.repeat_value_n} ) {{ \n\t ctrl_stmt_body -> {self.ctrl_stmt_body_n} }}"


#-------------------- PARSER --------------------
class SyntaxAnalyzer:
    # Takes tokens, initializes current token and its index
    def __init__(self, tokens):
        self.classNames = []            #for checking if constructor name matches class name
        self.errors = []
        self.tokens = [token.to_dict() 
            for token in tokens 
            if token.token_type != ("single_comment" or "multi-line comment")] # comments will be ignored by the parser
        # print(self.tokens) #uncomment to check tokens that the parser accepted
        
        if not self.tokens:
            message = "\n\tNo tokens to parse."
            self.errors.append(message)
            raise SyntaxError(message)

        self.currToken_index = 0
        self.currToken = self.tokens[self.currToken_index]

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
            print(f"('match' function) token {expected_token} matched")
            retToken = self.currToken
            self.nextToken()
            return retToken
        elif hasSpecError:
            print("('match' function) deactivating default expected token error")
            return None
        else:
            print("('match' function) activating default expected token error")
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
            self.logError(f"Unexpected token: Expected {expected_token}, but reached EOF.")
        else:
            self.logError(
                f"Unexpected token: Expected {expected_token}, but found '{self.currToken['tokenName']}'."
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

    def ERROR_expected_stdlib_or_filename(self):
        self.logError(f"Expected a standard library (Cmath, Cstring, Carray) or a filename with '.cstr', found '{self.currToken["tokenName"] if self.currToken else "EOF"}' instead. ")

    def ERROR_expected_cstr_file(self):
        self.logError("Expected a filename with '.cstr' extension.")

    def ERROR_expected_stdlib(self):
        self.logError(f"Expected a standard library (Cmath, Cstring, Carray), found '{self.currToken["tokenName"] if self.currToken else "EOF"}' instead. ")

    def ERROR_expected_Identifier_classes(self):
        if not self.currToken:  # EOF case
            self.logError("Expected constructor call after '=', but reached EOF (End of File).")
        elif not self.match("Identifier"):  # Invalid token case
            current_value = self.currToken["tokenName"] if self.currToken else "EOF"
            self.logError(f"Expected constructor call after '=', but found '{current_value}' instead.")

    def ERROR_missing_initializer(self):
        if self.currToken:
            prev_token = self.tokens[self.currToken_index-1]
            error_message = f"Expected initializer before '{prev_token['tokenName']}'"
        else:
            error_message = "Expected initializer but reached EOF (End of File)"
        
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
        self.logError(f"Expected numerical value. Found '{self.currToken["tokenType"] if self.currToken else EOF}' instead.")
    
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
            self.program()
            #self.value()
            self.errors.append("Parsing completed successfully. No Syntax Errors found.")
            print("Parsing completed successfully. No Syntax Errors found.")
        except SyntaxError as e:
            #print(f"Parsing incomplete with error/s: {e}")
            print (e)
        return self.errors

    #-------------------- CFG START --------------------
    # for semantic stuff, instead of using "if not", just add else clause to add functionality in if match clause

    def program(self):
        print("(parser) production: \"program\" detected")
        """<program> → <imports_list><program_constructs> int main(){ <main_body> return 0;}"""
        
        self.imports_list()
        
        """<program> → <program_constructs> int main(){ <main_body> return 0;}"""
        # Parse constructs
        self.program_constructs()
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

                self.body(["}"], True) # isVoid = True here

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

    # CODE BLOCKS START HERE
    def code_block(self, isVoid = False):       
        print(f"(parser) Processing <code_block>: {self.currToken['tokenName'] if self.currToken else 'None'}")
        
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["code_block"]:
            currentTokenType = self.currToken["tokenType"]

            if currentTokenType == "Identifier":
                self.match("Identifier")
                self.class_as_func_post()
                if not self.match(";", True):
                    self.ERROR_terminating_token(";")

            elif currentTokenType in ["const"] + PREDICT_SETS["data_type"]:    
                if currentTokenType == "const":
                    self.match("const")
                self.data_type()
                self.match("Identifier")
                self.var_dec_cont()
                if not self.match(";"):
                    self.ERROR_terminating_token(";")

            elif currentTokenType == "++":
                self.match("++")
                self.match("Identifier", False)
                if not self.match(";"):
                    self.ERROR_terminating_token(";")

            elif currentTokenType == "--":
                self.match("--")
                self.match("Identifier", False)
                if not self.match(";"):
                    self.ERROR_terminating_token(";")
            
            elif currentTokenType in PREDICT_SETS["output"]:
                self.output()
                if not self.match(";"):
                    self.ERROR_terminating_token(";")

            elif currentTokenType in PREDICT_SETS["conditional_stmt"]:
                self.conditional_stmt(isVoid)
                
            elif currentTokenType in PREDICT_SETS["loop_stmt"]:
                self.loop_stmt(isVoid)
        
            else: self.logError("You're not supposed to see this.")
            self.code_block(isVoid)
        

    def class_as_func_post(self):       
        print("(parser) production: \"class_as_func_post\" detected")

        if self.currToken:
            currentTokenType = self.currToken["tokenType"]
            if currentTokenType in PREDICT_SETS["class_as_func_post"]:
                if currentTokenType == "Identifier":
                    self.match("Identifier")
                    # if not self.match("Identifier"):
                    #     self.ERROR_missing_initializer()
                    self.classinst_cont()
                    if self.currToken:
                        if self.currToken["tokenType"] == "[":
                            self.logError("Array of objects is not supported. Expected '=' or ';'")
                        if self.currToken["tokenType"] == "." or self.currToken["tokenType"] == "(":
                            self.logError(f"Unexpected Token '{self.currToken["tokenType"]}' for object declaration. Expected '=' or ';'")

                elif currentTokenType == "++":
                    self.match("++")
                elif currentTokenType == "--":
                    self.match("--")

                else: self.assign_func_method_mods()
            else: self.ERROR_expected_token(PREDICT_SETS["class_as_func_post"])
        else: self.ERROR_expected_token(PREDICT_SETS["class_as_func_post"])

    def assign_func_method_mods(self):
        print("(parser) production: \"assign_func_method_mods\" detected")

        if self.currToken:
            currentTokenType = self.currToken["tokenType"]
            if currentTokenType in PREDICT_SETS["assign_func_method_mods"]:
                if currentTokenType in (PREDICT_SETS["assign_operator"] + ["["]):
                    self.as_array()
                    self.assign_stmt_op()

                elif currentTokenType == "(":
                    self.match("(")
                    self.func_arg()
                    if not self.match(")"):
                        self.ERROR_unclosed_parentheses()

                elif currentTokenType == ".":
                    self.match(".")
                    self.match("Identifier")
                    self.assign_func_method_mods_cont()

            else: self.ERROR_expected_token(PREDICT_SETS["assign_func_method_mods"])
        else: self.ERROR_expected_token(PREDICT_SETS["assign_func_method_mods"])


    def assign_func_method_mods_cont(self):
        print("(parser) production: \"assign_func_method_mods_cont\" detected")

        if self.currToken:
            currentTokenType = self.currToken["tokenType"]
            if currentTokenType in (PREDICT_SETS["assign_func_method_mods_cont"] + PREDICT_SETS["assign_operator"]):
                if currentTokenType == "[" or currentTokenType in PREDICT_SETS["assign_operator"]:
                    self.as_array()
                    if not self.currToken or self.currToken["tokenType"] not in PREDICT_SETS["assign_operator"]:
                        self.ERROR_expected_token(PREDICT_SETS["assign_operator"])
                    self.assign_stmt_op()

                elif currentTokenType == "(":
                    self.match("(")
                    self.func_arg()
                    if not self.match(")"):
                        self.ERROR_unclosed_parentheses()

                elif self.currToken and self.currToken["tokenType"] == ".":
                    self.logError(f"Further accessing of object elements is not allowed. Expected '[' or '(', found '{self.currToken["tokenType"]}'.")    
            elif self.currToken and self.currToken["tokenType"] == ".":
                self.logError(f"Further accessing of object elements is not allowed. Expected '[' or '(', found '{self.currToken["tokenType"]}'.")  
            else: self.ERROR_expected_token(["[", "("] + PREDICT_SETS["assign_operator"])
        else: self.ERROR_expected_token(["[", "("] + PREDICT_SETS["assign_operator"])


    def body(self, stopChars, isVoid = False, inControlStruct = False):     # TODO: Check for return statements reachable only within if/code_blocks, thats one semantic error
        print(f"(parser) Processing <body>: {self.currToken['tokenName'] if self.currToken else 'None'}")
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["body"]:
            
            self.code_block(isVoid)
            statements_n = []
            return_stmt_n = None

            if self.currToken and self.currToken["tokenType"] == "return":
                  return_stmt_n = self.return_block(isVoid)
                  self.hasFunctionReturned = True     
                  if self.hasMainFunction:
                      self.hasMainReturn = True
            #     # TODO: DEAD CODE (CODE AFTER RETURN) ERROR IMPLEMENTATION\

                
            self.body(stopChars, isVoid, inControlStruct)

        if self.currToken and self.currToken["tokenType"] not in stopChars:
            self.logError(f"Unexpected Token '{self.currToken["tokenName"]}' found. Expected {PREDICT_SETS["body"]}.")

        if not self.hasFunctionReturned and not inControlStruct and not self.hasMainFunction:
                self.logError("A return statement outside of control structures is required in all functions.")
                #placeholder hehehehehhehehehehheyhueh
        
        print("(parser) production: \"body\" exited!!!!!!")
        #  return node_body(statements_n, return_stmt_n)

    def imports_list(self):
        print("(parser) production: \"imports_list\" detected")
        """<imports_list> → import <iostar>;<imports_rec>"""

        self.match("import", False)

        self.match("<", False)

        if not self.currToken or self.currToken["tokenName"] != "iostar":
            self.ERROR_expected_token("iostar")
        else:
            self.match("Identifier")  # Match 'iostar'

        if not self.match(">"):
            self.ERROR_unclosed_angled_bracket()

        if not self.match(";"):
            self.ERROR_terminating_token(";")

        # No need for predict set here bc the only path for imports_rec is if the next token is "import"
        if self.currToken and self.currToken["tokenType"] == "import":
            self.imports_rec()

        # If the next token (curr token in this case) is not import, it finishes imports_list, goes back to program prod


    def imports_rec(self):
        print("(parser) production: \"imports_rec\" detected")
        """<imports_rec> → import <<imports_rec_values>>;<imports_rec> | λ"""

        self.match("import", False)

        self.match("<", False)

        # Process content inside '<>'
        self.imports_rec_values()

        if not self.match(">"):
            self.ERROR_unclosed_angled_bracket()

        if not self.match(";"):
            self.ERROR_terminating_token(";")

        # Handle potential recursive imports_rec
        if self.currToken and self.currToken["tokenType"] == "import":
            self.imports_rec()


    def imports_rec_values(self):
        print("(parser) production: \"imports_rec_values\" detected")
        """<imports_rec_values> → standard library | standard library with .cstr | filename with .cstr"""

        if self.currToken:
            # Check for standard library or standard library with .cstr
            if self.currToken["tokenName"] in PREDICT_SETS["std_lib"]:   
                self.match("Identifier")  # Match the standard library -- put logic here per std lib for semantic
                if self.currToken and self.currToken["tokenType"] == ".":      # potentially stdlib and header file haev the same name 
                    self.match(".")
                    if self.currToken and self.currToken["tokenName"] == "cstr":
                        self.match("Identifier")  # Match 'cstr'
                    else:
                        self.ERROR_expected_cstr_file()

            # Check for filename (non-standard-library identifier followed by .cstr)
            elif self.currToken["tokenType"] == "Identifier":
                self.match("Identifier")  # Match the filename
                if self.currToken and self.currToken["tokenType"] == ".":
                    self.match(".")
                    if self.currToken and self.currToken["tokenName"] == "cstr":
                        self.match("Identifier")  # Match 'cstr'
                    else:
                        self.ERROR_expected_cstr_file()
                else:
                    self.ERROR_expected_stdlib_or_filename()
            else:
                self.ERROR_expected_stdlib_or_filename()
        else:
            self.ERROR_expected_stdlib_or_filename()



    # ----- TODO:REVISIT!! can't complete errors here yet bc errors would be found in each prod first, then check if there are external errors left 
    # ex of unimplemented error: if there's a sole variable (it can be considered a class inst, pero if not yet defined, it should throw another type of error)
    def program_constructs(self):
        
        print("(parser) production: \"program_constructs\" detected: currtoken is \""
      + str(self.currToken["tokenName"])+"\"" if self.currToken else "None" + "\"")
        
        if self.currToken:
            if self.matchPredictSet("program_constructs", False):  # Token is a valid start for program constructs
                currentTokenType = self.currToken["tokenType"]
                if currentTokenType in ["private", "class"]:
                    self.class_declaration()
                elif currentTokenType in PREDICT_SETS["iden_dec"]:
                    self.iden_dec()
                else:
                    print(f"identifier????????????????????? {self.currToken["tokenName"]}")
                    print(self.class_inst("program_constructs"))
            if not self.hasMainFunction:
                self.program_constructs()
        

    def iden_dec(self, inClassBody = False):
        print("(parser) production: \"iden_dec\" detected (current token: " + str(self.currToken["tokenName"]) + ")")
        

        if self.currToken:
            currentTokenType = self.currToken["tokenType"]
            if currentTokenType == "const":
                self.match("const")
                if self.currToken["tokenType"] == "void":
                    self.logError("Void function cannot be preceded by 'const'.")
                elif self.currToken["tokenType"] in PREDICT_SETS["data_type"]:
                    dtype_temp_t = self.data_type()
                    iden_temp_n = node_iden(self.match("Identifier",False))
                    vardec_cont_temp_n = self.var_dec_cont(dtype_temp_t, iden_temp_n)
                    if not self.match(";"):
                        self.ERROR_terminating_token(";")
                    
                    return node_vardec(True, dtype_temp_t, iden_temp_n, vardec_cont_temp_n)
                else: self.ERROR_expected_token(PREDICT_SETS["data_type"])

            elif currentTokenType not in PREDICT_SETS["data_type"] and currentTokenType != "void":
                self.logError(f"Expected data type or void, found '{currentTokenType}' instead.")

            elif currentTokenType == "void":
                self.match("void")
                isVoid = True
                if self.currToken:
                    if self.currToken["tokenName"] == "main" and not inClassBody:
                        self.hasMainFunction = True
                        print("MAIN FUNCTION FOUND!!!!")
                    self.match("Identifier", False)
                else:
                    self.logError("Expected Identifier for function declaration.")
                self.match("(", False)
                if not self.hasMainFunction:
                    self.params_dec_start(isVoid)
                else:
                    if self.currToken:
                        if self.currToken["tokenType"] != ")":
                            self.ERROR_unclosed_parentheses()
                    else: self.logError("Expected ')', but reached EOF.")

            elif currentTokenType in PREDICT_SETS["data_type"]:
                dtype_temp_t = self.data_type()
                id_temp_n = node_iden(self.match("Identifier", False))
                return self.iden_dec_cont(dtype_temp_t, id_temp_n)
            
            else:
                self.ERROR_expected_token(PREDICT_SETS["iden_dec"])

    def iden_dec_cont(self, dtype_temp_t, id_temp_n):
        print("(parser) production: \"iden_dec_cont\" detected")

        if self.currToken:

            if self.currToken["tokenType"] == "(":
                self.params_dec_start()
            elif self.currToken["tokenType"] in PREDICT_SETS["iden_dec_cont"]:
                node_temp = self.var_dec_cont(dtype_temp_t, id_temp_n)
                if not self.match(";"):
                    self.ERROR_terminating_token(";")
                
                return node_temp
            else: self.ERROR_expected_token(["("] + PREDICT_SETS["iden_dec_cont"])

        else: self.ERROR_expected_token(["("] + PREDICT_SETS["iden_dec_cont"])


    def var_dec_cont(self, dtype_temp_t, id_temp_n):
        print("(parser) production: \"var_dec_cont\" detected")
        value_temp_n = None
        idec_rec_temp_n = None
        vardec_cont_temp_n = None

        if self.currToken:
            if self.currToken["tokenType"] == "[":
                self.match("[", False)
                self.arith_exp(["]"])
                if not self.match("]"):
                    self.ERROR_unclosed_square_bracket()
                self.var_id_arr1D()

            else:
                value_temp_n = self.var_init()
                idec_rec_temp_n = self.var_iden_rec()
        
        # none arr var dec
        if value_temp_n or idec_rec_temp_n:
            vardec_cont_temp_n = node_vardec_cont(value_temp_n, idec_rec_temp_n)

        return node_vardec(False, dtype_temp_t, id_temp_n, vardec_cont_temp_n)


    def params_dec_start(self, isVoid = False):
        
        if not self.hasMainFunction:
            print(f"(parser) production: \"params_dec_start\" detected , isVoid = {isVoid}")
            self.match("(")
            self.params_dec()
            if not self.match(")", True):
                self.ERROR_unclosed_parentheses()
        
            self.match("{", False)
            self.body(["}"], isVoid)
            if not self.match("}"):
                self.ERROR_unclosed_curly_braces()
            self.hasFunctionReturned = False


    # TODO
    def class_declaration(self, inClassBody = False):
        print("(parser) production: \"class_declaration\" detected")
        if self.currToken["tokenType"] == "private":
            is_private_b = self.match("private")

        self.match("class", False)

        if self.currToken and self.currToken["tokenType"] == "Identifier":
            self.classNames.append(self.currToken["tokenName"])      # handles constructor name logic of recursive classes within classes
            self.match("Identifier")
        else:
            self.ERROR_expected_token("Identifier")
        
        self.match("{", False)

        self.class_body()
        self.constructor_dec()
        self.class_body()

        if self.currToken and self.currToken["tokenType"] == "Identifier":
            self.logError(f"Only one constructor per class allowed. Expected: {PREDICT_SETS['class_body']}")

        if not self.match("}"):
            self.ERROR_expected_token(PREDICT_SETS['class_body'] + ['}'])

        if not self.match(";", True):
            self.logError("Class Declaration is expected to be terminated by ';' after '}'.")

        if inClassBody:
            self.class_body()
        else:
            self.program_constructs()

    
    def class_body(self): # all of these are just 'if's because class_body can be null
        print("(parser) production: \"class_body\" detected")
        
        is_private_b = False
        inClassBody = True
        if self.matchPredictSet("class_body", True):   #throws no error if currToken not in here
            
            if self.currToken:
                if self.currToken["tokenType"] == "private":
                    is_private_b = self.match("private")
                    if self.currToken and self.currToken["tokenType"] == "class":
                        self.logError(f"Classes cannot be nested within classes. Expected {PREDICT_SETS['iden_dec']} or constructor declaration.")
                    if not self.currToken or self.currToken["tokenType"] not in PREDICT_SETS["iden_dec"]:
                        self.ERROR_expected_token(PREDICT_SETS["iden_dec"])
                
                node_vardec = self.iden_dec(inClassBody)
                class_body_rec_n = self.class_body()
                return node_class_body(is_private_b, node_vardec, class_body_rec_n)
            inClassBody = False 

        if self.currToken and self.currToken["tokenType"] == "class":
            self.logError(f"Classes cannot be nested within classes. Expected {PREDICT_SETS['class_body']} or constructor declaration.")
        return None

    def constructor_dec(self): 
        
        if self.currToken:
            if self.currToken["tokenType"] == "Identifier":
                print("(parser) production: \"constructor_dec\" detected")
                if self.currToken["tokenName"] != self.classNames[-1]: 
                    self.logError("Constructors must have the same name as its class.") 
                    #TODO: maybe fix error message here, just a placeholder

                class_id_n = node_iden(self.match("Identifier", False))
                self.classNames.pop()
                self.match("(", False)
                self.params_dec()
                if not self.match(")"):
                    self.ERROR_unclosed_parentheses()

                self.match("{", False)
                self.code_block()
                
                if self.currToken and self.currToken["tokenType"] == "return":
                    self.logError(f"Constructors cannot have return statements. Expected {PREDICT_SETS['code_block']} or }} ")


                if not self.match("}"):
                    self.ERROR_unclosed_curly_braces()

                print("(parser) production: \"constructor_dec\" exited!!!!!")


    def class_inst(self, location):
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
                return node_class_inst(class_id_n, obj_id_n, class_instcont_n)
            else:
                self.ERROR_terminating_token(";")

            # Continue parsing program constructs
            if self.currToken:
                if location == "program_constructs":
                    self.program_constructs()
                elif location == "code_block":
                    self.code_block()
            
    
    # Handle <classinst_cont>
    def classinst_cont(self):
        print("(parser) production: \"classinst_cont\" detected")
        has_Constructor_or_Array_Init = False
        # object instantiation
        if self.currToken and self.currToken["tokenType"] == "=":
            self.match("=")
            if self.currToken and self.currToken["tokenType"] != "Identifier": # should be the same name as the class name [SEMANTIC]
                self.ERROR_expected_Identifier_classes()

            class_id_n = node_iden(self.match("Identifier",False))

            if not self.currToken or self.currToken["tokenType"] != '(':
                self.logError(f"Expected '(' for constructor call after Identifier. Found '{self.currToken["tokenType"] if self.currToken else "EOF"}' instead.")
            self.match('(')
            func_arg_n = self.func_arg(True)
            has_Constructor_or_Array_Init = func_arg_n[1]
            if self.currToken and self.currToken["tokenType"] == ")":
                self.match(')')
            elif (self.currToken is None or self.currToken["tokenType"] not in PREDICT_SETS["func_arg"]) and not has_Constructor_or_Array_Init:
                self.ERROR_expected_constructor_param_closing()
            else:
                self.ERROR_expected_token([")", ","])

            return node_classinst_cont(class_id_n, func_arg_n)

        return None

    def func_arg(self, asConstructor = False):
        print("(parser) production: \"func_arg\" detected")
        retList = [None, None]
        hasConstructorValue = False
        isValidFuncArg = True
        # Check if there's a value to parse
        if self.currToken and self.currToken["tokenType"]in PREDICT_SETS["value"]:
            val_n = self.value([',',')'])
            if self.currToken and self.currToken["tokenType"] == ',':
                self.match(',')
                if self.value([',',')']):
                    retList[0] = node_func_args(val_n)
                    if self.currToken and self.currToken["tokenType"] == ',':
                        # Parse the recursive part of the arguments when , is detected
                        retList[0] = node_func_args(val_n, self.func_arg_rec())
                    hasConstructorValue = True
        else:
            if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["data_type"]:
                self.logError("Function call arguments cannot accept declarations.")
            else: 
                print("(parser) λ-production for <func_arg>")  # Handle λ (empty production)
        retList[1] = hasConstructorValue
        return retList if asConstructor else retList[0]
    

    def func_arg_rec(self):
        print("(parser) production: \"func_arg_rec\" detected")
        isValidFuncArg = True
        # Check for a comma indicating more arguments
        if self.currToken and self.currToken["tokenType"] == ",":
            # Peek ahead to check the token after the comma
            next_token = self.peek()
            if not next_token:
                # If there's no next token, it means EOF after the comma
                isValidFuncArg = False
                self.logError("Expected another value after ',' but reached EOF.")
            elif next_token["tokenType"] not in PREDICT_SETS["value"]:
                # If the next token is not a valid value
                isValidFuncArg = False
                self.logError(f"Expected another value after ',' but got '{next_token['tokenName']}'.")

            self.match(",")  # Match the comma
            print("(parser) Found ',' indicating more arguments.")

            # Parse the next <func_arg>
            return self.func_arg()
        else:
            print("(parser) λ-production for <func_arg_rec>")  # Handle λ (empty production)

        return isValidFuncArg

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
        print("(parser-value-chain): Entered \"value\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        return self.logic_exp(stopChars)

    def logic_exp(self, stopChars):
        print("(parser-value-chain): Entered \"logic_exp\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        left_n = self.rel_exp(stopChars)
        
        if self.currToken:
            if self.currToken["tokenType"] in PREDICT_SETS["logic_operator"]:
                left_n = self.logic_exp_cont(left_n, stopChars)
            self.stopCharOrOperatorCheck(stopChars)
                
        return left_n
    
    def logic_exp_cont(self, left_n, stopChars):
        print("(parser-value-chain): Entered \"logic_exp_cont\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
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
        print("(parser-value-chain): Entered \"rel_exp\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        left_n = self.arith_exp(stopChars)

        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["rel_operator"]:
            left_n = self.rel_exp_cont(left_n, stopChars)
        
        return left_n
    
    def rel_exp_cont(self, left_n, stopChars):
        print("(parser-value-chain): Entered \"rel_exp_cont\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
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
        print("(parser-value-chain): Entered \"arith_exp\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        left_n = self.term(stopChars)

        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["add_min_cont"]:
            left_n = self.add_min_cont(left_n, stopChars)

        return left_n

    def add_min_cont(self, left_n, stopChars):
        print("(parser-value-chain): Entered \"add_min_cont\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
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
        print("(parser-value-chain): Entered \"term\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        left_n = self.factor(stopChars)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["mult_div_modulo_cont"]:
            left_n = self.mult_div_modulo_cont(left_n, stopChars)

        return left_n

    def mult_div_modulo_cont(self, left_n, stopChars):
        print("(parser-value-chain): Entered \"mult_div_modulo_cont\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
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
        print("(parser-value-chain): Entered \"factor\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
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
        print("(parser-value-chain): Entered \"cast_val\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
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
        print("(parser-value-chain): Entered \"atom\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
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
            print("(parser-value-chain): Entered \"atom\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
            if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["mods_post_op"]:
                temp_node = self.mods_post_op(node_iden(temp_id))
            return temp_node

        return is_valid_value

    def mods_post_op(self, temp_id):
        print("(parser-value-chain): Entered \"mods_post_op\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["iden_mods"]:
            temp_node = self.iden_mods(temp_id)
        elif self.currToken and self.currToken["tokenType"] in ["++", "--"]:
            temp_node = self.mods_post_op_con(temp_id)
        return temp_node
    
    def mods_post_op_con(self, temp_id):
        print("(parser-value-chain): Entered \"mods_post_op_con\", current token: " + (self.currToken["tokenType"] if self.currToken else "EOF"))
        match self.currToken["tokenType"]:
            case "++":
                return node_post_un_op(temp_id, self.match("++"))
            case "--":
                return node_post_un_op(temp_id, self.match("--"))

    def data_type(self):
        match self.currToken["tokenType"]:
            case "int":
                return self.match("int", False)["tokenName"]
            case "long":
                return self.match("long", False)["tokenName"]
            case "float":
                return self.match("float", False)["tokenName"]
            case "double":
                return self.match("double", False)["tokenName"]
            case "bool":
                return self.match("bool", False)["tokenName"]
            case "string":
                return self.match("string", False)["tokenName"]

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

    
    def ret_type(self):
        print("(parser) production: \"ret_type\" detected")

        if self.currToken["tokenType"] in PREDICT_SETS["data_type"]:
            self.data_type()
        else:
            if not self.match("Identifier"):
                self.logError("Expected data type or Identifier (Class name).")

        print("(parser) production: \"ret_type\" exited!!!!!")


    def params_var(self):
        print("(parser) production: \"params_var\" detected")

        if self.currToken:
            if not self.match("Identifier"):
                self.logError("Expected Identifier (variable declaration or class name).")
            if self.currToken:
                if self.peek(-2)["tokenType"] == "Identifier" and self.currToken:
                    if self.currToken["tokenType"] == "=":
                        self.logError("Default values for object parameters are not supported. Expected ')' or ','. Found '=' instead.")
                    elif self.currToken["tokenType"] == "[":  # array
                        self.logError("Array of objects is not supported. Expected ')' or ','. Found '[' instead.")
            self.params_var_cont()
        else:
            self.ERROR_expected_token("Identifier")

        print("(parser) production: \"params_var\" exited!!!!!")

    #TODO: harley continue here
    def params_var_cont(self):
        print("(parser) production: \"params_var_cont\" detected")

        if self.currToken:
            if self.currToken["tokenType"] == "=":
                self.match("=")
                if not self.value([",", ")"]):
                    self.ERROR_expected_token("value")
                return self.params_def_rec()

            elif self.currToken["tokenType"] == "[":
                self.is_array()
            
            elif self.currToken["tokenType"] == ",":
                return self.params_var_rec()

        print("(parser) production: \"params_var_cont\" exited!!!!!")
        return None

    def params_var_rec(self):
        print("(parser) production: \"params_var_rec\" detected")

        if self.currToken:
            if self.currToken["tokenType"] == ",":
                self.match(",")
                if not self.currToken or self.currToken and self.currToken["tokenType"] not in PREDICT_SETS["data_type"] and self.currToken["tokenType"] != "Identifier":
                    self.logError("Expected data type or Identifier (Class name).")
                return self.params_dec()
    
        print("(parser) production: \"params_var_rec\" exited!!!!!")
        return None 

    def params_def_rec(self):
        # def rec means that there is already a default param before current params rec
        print("(parser) production: \"params_def_rec\" detected")
        ret_node_temp_n = None
        if self.currToken:
            if self.currToken["tokenType"] == ",":
                self.match(",")

                # def rec should be followed by only a data_type since objs dont have default params
                if not self.currToken or self.currToken and self.currToken["tokenType"] not in PREDICT_SETS["data_type"]:
                    if self.currToken:
                        self.logError(f"Expected data type for non-default variable declaration, instead got {self.currToken["tokenType"]}.\nCannot declare arrays, objects, or non-default variables at this point due to existing default parameters.")
                    else:
                        self.logError(f"Expected data type for non-default variable declaration.\nCannot declare arrays, objects, or non-default variables at this point due to existing default parameters.")
                
                # match datatype
                # if self.currToken["tokenType"] in PREDICT_SETS["data_type"]:
                #     self.nextToken()
                dtype_temp_t = self.data_type()
                
                id_temp_n = node_iden(self.match("Identifier", False))

                # if after default param the syntax is just <dtype> iden w/o initializing, throw error
                if not self.currToken or self.currToken and self.currToken["tokenType"] != "=":
                    # always look for '=' since default param before already exists
                    # EOF
                    if not self.currToken:
                        self.logError(f"Uninitialized variable. Expected '=' for initializing the variable parameter to a default value, instead reached EOF.")
                    # closed the func params with )
                    elif self.currToken["tokenType"] == ')':
                        self.logError(f"Uninitialized variable. Expected '=' for initializing the variable parameter to a default value.")
                    # Random token
                    elif self.currToken and self.currToken["tokenType"] != "=":
                        self.logError(f"Uninitialized variable. Expected '=' for initializing the variable parameter to a default value, instead got {self.currToken["tokenType"]}.")
                
                # if = is the next token, proceed to params_def_rec_cont
                elif self.currToken and self.currToken["tokenType"] == "=":
                    ret_node_temp_n = node_funcpar_var_defrec(dtype_temp_t, id_temp_n, self.params_def_rec_cont())

        print("(parser) production: \"params_def_rec\" exited!!!!!")
        return ret_node_temp_n
    def params_def_rec_cont(self,isDefault = False ):
        print("(parser) production: \"params_def_rec_cont\" detected")

        if self.currToken:
            if not self.currToken and isDefault or self.currToken["tokenType"] != "=":
                self.logError("No non-default parameter must follow a default parameter.")
            self.match("=", True)
            val_temp_n = self.value([",", ")"])
            if not val_temp_n:
                    self.ERROR_expected_token("value")
            par_defrec_temp_n = self.params_def_rec()

        print("(parser) production: \"params_def_rec_cont\" exited!!!!!")
        return node_funcpar_var_defreccont(val_temp_n, par_defrec_temp_n)

    def is_array(self):
        print("(parser) production: \"is_array\" detected")

        self.match("[")
        if not self.match("]"):
            self.ERROR_array_as_param_no_val()

        if self.currToken and self.currToken["tokenType"] == "[":
            self.match("[")
            if not self.match("]"):
                self.ERROR_array_as_param_no_val()

        if self.currToken and self.currToken["tokenType"] == "[":
            self.logError("Only up to 2-dimensions are allowed.")

        if self.currToken and self.currToken["tokenType"] == "=":
            self.logError("No default array values are allowed.")
        print("(parser) production: \"is_array\" exited!!!!!")


    def params_dec(self):
        print(f"(parser) production: \"params_dec\" detected, {self.currToken["tokenType"] if self.currToken else EOF}")

        if self.currToken and self.currToken["tokenType"] != ")":
            if self.currToken["tokenType"] in PREDICT_SETS["data_type"]:
                self.data_type()
                self.match("Identifier", False)
                self.params_var_cont()
            elif self.currToken["tokenType"] == "Identifier":
                self.match("Identifier", False)
                self.match("Identifier", False)
                self.params_var_rec()
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
        return node_condition(condition_temp_n)
        
    def output(self):
        '''<output> → <print_stmts>(<print_params>);'''
        print("(parser) entered production: \"output\"")
        
        '''<print_stmts> → print | println'''
        # <print_stmts> are already expected to be here before it entered func
        print_stmts_n = None
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
        print_params_n = []
        if self.currToken and self.currToken["tokenType"] != ")":
            self.print_params()
        
        if not self.match(")"): 
            self.ERROR_unclosed_parentheses()

        print("(parser) exited production: \"output\"")
        return node_output(print_stmts_n, print_params_n)

    def print_params(self):
        '''<print_params> → <value> <output_rec> | null'''
        print("(parser) entered production: \"print_params\"")
        
        print_params_n = []
        output_rec_n = None
        # if <print_params> are not null
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["value"]:
            if self.currToken and self.currToken["tokenType"] != ")":
                ############ DEBUG PRINTING AST
                # dbgVal = self.value([",", ")"])
                # print(f'---------------AST:-------------\n\n{dbgVal}\n\n')
                # if not dbgVal:
                ##### END DEBUG 
                value_n = self.value([",", ")"])
                if not value_n: #gets commented out for dbg
                    self.logError("Invalid 'print' statement parameter.")
                    print_params_n.append(value_n)
                if self.currToken and self.currToken["tokenType"] == ",":
                    print_params_n.extend(self.output_rec())
        else:
            print("entered else")
            self.ERROR_expected_valid_value()
        
        print("(parser) exited production: \"print_params\"")
        return node_print_params(value_n, output_rec_n)

    def output_rec(self):
        '''<output_rec> → ,<value> <output_rec> | null'''
        print("(parser) entered production: \"output_rec\"")
        
        self.match(",", False)
        
        output_rec_n = None
        print_params_n = []
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["value"]:
            value_n = self.value([",", ")"]) 
            if not value_n:
                message = f"Expected value after ',', got '{self.currToken['tokenType'] if self.currToken else 'EOF'}' instead."
                self.logError(message)
                print_params.append(value)
            if self.currToken and self.currToken["tokenType"] == ",":
                print_params_n.extend(self.output_rec())
                
        else:
            self.ERROR_expected_valid_value()

        print("(parser) exited production: \"output_rec\"")
        return node_print_params(value_n,output_rec_n)
    
    def conditional_stmt(self, isVoid = False):
        '''<conditional_stmt> → <if_stmt> | <swicth_stmt>'''
        print("(parser) entered production: \"conditional_stmt\"")

        if self.currToken and self.currToken["tokenType"] == "if":
            self.if_stmt(isVoid)
        elif self.currToken and self.currToken["tokenType"] == "switch":
            self.switch_stmt(isVoid)

        print("(parser) exited production: \"conditional_stmt\"")
    
    def if_stmt(self, isVoid = False): 
        '''<if_stmt> → if(<condition) {<ctrl_stmt_body>} <else_chain>'''
        print(f"(parser) entered production: \"if_stmt\" , isVoid = {isVoid}")

        # if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["init_arg"]:

        self.match("if", False)
        if not self.match("("):
            self.ERROR_missing_condition("if")
        condition_n = self.condition("if",[")"])
        if not self.match(")"): 
            self.ERROR_unclosed_parentheses()
        
        self.match("{", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"] + PREDICT_SETS["body"]:
            body_n = self.ctrl_stmt_body(isVoid)
        if not self.match("}"):
            self.ERROR_unclosed_curly_braces()
        self.hasFunctionReturned = False

        else_chain_n = None
        if self.currToken and self.currToken["tokenType"] == "else":
            else_chain_n = self.else_chain()

        print("(parser) entered production: \"if_stmt\"")
        return node_if_stmt(self, condition_n, body_n, else_chain_n)

    
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
                self.logError("Void functions cannot return a value and must be terminated by a ';' immediately.")
        
        if not isVoid:
            ret_value_n = self.value([";"])

        print("(parser) exited production: \"ret_value\"")
        return node_ret_value(ret_value_n)

    # bare-minimum tested
    def break_stmt(self):
        '''<break_stmt> → break;'''
        print("(parser) entered production: \"break_stmt\"")

        self.match("break", False)
        if not self.match(";"):
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"break_stmt\"")
        return node_break_stmt()

    # bare-minimum tested
    def continue_stmt(self):
        '''<continue_stmt> → continue;'''
        print("(parser) entered production: \"continue_stmt\"")

        self.match("continue", False)
        if not self.match(";"):
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"continue_stmt\"")
        return node_continue_stmt()

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

        print("(parser) exited production: \"init_arg\"")
        return f"{init_arg_n}" 

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
                    inc_arg_temp_n = self.assign_func_method_mods()

                else: self.logError("Expected: unary operation, assignment statement, function call, method call.")

            elif currentTokenType in PREDICT_SETS["print_stmts"]:
                inc_arg_temp_n = self.output()

        print("(parser) exited production: \"inc_arg\"")
        return f"{inc_arg_temp_n}"

    # bare-minimum tested
    def else_chain(self):
        '''<else_stmt> → <if_stmt> | { <ctrl_stmt_body> }'''
        print("(parser) entered production: \"else_chain\"")
        
        if self.currToken:
            self.match("else", False)
            else_stmt_n = self.else_stmt()
        
        print("(parser) exited production: \"else_chain\"")
        return node_else_stmt(else_stmt_n)

    def else_stmt(self, isVoid = False):
        print(f"(parser) entered production: \"else_stmt\", isVoid = {isVoid}")

        if self.currToken:
            if self.currToken and self.currToken["tokenType"] == "if":
                self.if_stmt()

            elif self.currToken and self.currToken["tokenType"] == "{":
                self.match("{")
                body_n = self.ctrl_stmt_body(isVoid)
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
            case_temp_n = self.case_stmt(isVoid)
            
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
            case_stmt_rec_temp_n = None

            self.match("case", False)
            case_value_temp_n = self.case_value()
            self.match(":", False)
            
            if self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
                ctrl_stmt_body_temp_n = self.ctrl_stmt_body(isVoid)
            
            if self.currToken["tokenType"] == "case":
                case_stmt_rec_temp_n = self.case_stmt()

        print("(parser) exited production: \"case_stmt\" !!!!!!!!!!!")
        return node_case_stmt(case_value_temp_n, ctrl_stmt_body_temp_n, case_stmt_rec_temp_n)
    

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
            ctrl_stmt_body_temp_n = self.ctrl_stmt_body(isVoid)

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
            condition_temp_n = None
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
                self.logError(f"Initialization argument is expected to be terminated by ';', but found '{self.currToken["tokenType"] if self.currToken else EOF}'.")
            
            ## CONDITION
            condition_temp_n = self.condition("for-loop",[";"])
            
            if not self.match(";"):
                self.logError(f"Condition argument is expected to be terminated by ';', but found '{self.currToken["tokenType"] if self.currToken else EOF}'.")

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
                ctrl_stmt_body_temp_n = self.ctrl_stmt_body(isVoid)
            
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
                ctrl_stmt_body_temp_n = self.ctrl_stmt_body(isVoid)
            
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
                ctrl_stmt_body_temp_n = self.ctrl_stmt_body(isVoid)

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
                ctrl_stmt_body_temp_n = self.ctrl_stmt_body(isVoid)

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
                statements_n.append(self.break_stmt_n())
            elif currentTokenType == "continue":
                statements_n.append(self.continue_stmt_n())
            elif currentTokenType in PREDICT_SETS["body"]:
                statements_n.append(self.body(["break", "continue", "case", "}"], isVoid, True))

            if self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"] and currentTokenType not in ["}", "case", "default"]:
                self.ctrl_stmt_body(isVoid)

        print("(parser) exited production: \"ctrl_stmt_body\"")
        return node_ctrl_stmt_body(statements_n)

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
                    self.logError("Expected a valid value of type \"string\".")
            
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

    
    def var_iden_rec(self):
        """<var_iden_rec> → , Identifier <var_init> <var_iden_rec> | λ"""
        print("(parser) entered production: \"var_iden_rec\"")
        
        if self.currToken:
            if self.currToken["tokenType"] == ",":
                self.match(",")
                id_temp_t = self.match("Identifier")
                if id_temp_t:
                    id_temp_n = node_iden(id_temp_t)
                    value_temp_n = self.var_init()
                    idec_rec_temp_n = None
                    if self.currToken["tokenType"] == ",":
                        idec_rec_temp_n = self.var_iden_rec()
                else:
                    self.ERROR_expected_token("Identifier")
                return node_idec_rec(id_temp_n, value_temp_n, idec_rec_temp_n)
            
        print("(parser) exited production: \"var_iden_rec\"")
        return None

    def var_id_arr1D(self):
        '''<var_id_arr1D> → <array1D_iden_rec> | <array1D_init>'''
        
        print("(parser) entered production: \"var_id_arr1D\"")
        
        if self.currToken:
            currentTokenType = self.currToken["tokenType"]

            if currentTokenType == ",":
                self.array1D_iden_rec()

            elif currentTokenType == "=":
                self.array1D_init()

            elif currentTokenType == "[":
                self.match("[", False)
                if not self.arith_exp(["]"]):
                    self.ERROR_expected_pos_integer_value()
                if not self.match("]", True):
                    self.ERROR_unclosed_square_bracket()
                if self.currToken["tokenType"] == "[":
                    self.logError("Only up to 2 dimensions of arrays are allowed.")
                self.var_id_arr2D()
        
        print("(parser) exited production: \"var_id_arr1D\"")


    def array1D_iden_rec(self):
        '''<array1D_iden_rec> → , Identifier [<int_val>] <array1D_iden_rec> | λ'''
        print("(parser) entered production: \"array1D_iden_rec\"")
        
        if self.currToken:
            self.match(",")
            self.match("Identifier", False)
            self.match("[", False)
            if not self.arith_exp(["]"]):
                self.ERROR_expected_pos_integer_value()
            if not self.match("]"):
                self.ERROR_unclosed_square_bracket()
            if self.currToken["tokenType"] == ",":
                self.array1D_iden_rec()

        print("(parser) exited production: \"array1D_iden_rec\"")


    def array1D_init(self):
            '''<array1D_init> → = {<arr_value_1D>}'''
            print("(parser) entered production: \"array1D_init\"")
            
            if self.currToken:
                self.match("=", False)
                self.match("{", False)
                self.arr_value_1D()
                if not self.match("}"):
                    self.ERROR_unclosed_curly_braces()
            
            print("(parser) exited production: \"array1D_init\"")


    def arr_value_1D(self):
            '''<arr_value_1D> → <value> <arr_value_1D_rec>'''
            print("(parser) entered production: \"arr_value_1D\"")
            
            if self.currToken:
                
                if self.currToken["tokenType"] in PREDICT_SETS["value"]:
                    self.value(["}", ","])
                    if self.currToken["tokenType"] == ",":
                        self.arr_value_1D_rec()
                else:
                    self.ERROR_expected_token("value")

            print("(parser) exited production: \"arr_value_1D\"")

    def arr_value_1D_rec(self):
            '''<arr_value_1D_rec> → , <value> <arr_value_1D_rec> | λ'''
            print("(parser) entered production: \"arr_value_1D_rec\"")

            if self.currToken:

                if self.currToken["tokenType"] == ",":
                    self.match(",")
                    if self.currToken["tokenType"] in PREDICT_SETS["value"]:
                        self.value(["}", ","])
                        self.arr_value_1D_rec()
                    else:
                        self.ERROR_expected_token("value")
           
            print("(parser) exited production: \"arr_value_1D_rec\"")

    def var_id_arr2D(self):
            '''<var_id_arr2D> → <array2D_iden_rec> | <array2D_init>'''
            print("(parser) entered production: \"var_id_arr2D\"")
            
            if self.currToken:
                currentTokenType = self.currToken["tokenType"]

                if currentTokenType == ",":
                    self.array2D_iden_rec()
                elif currentTokenType == "=":
                    self.array2D_init()
                #else:
                #    self.ERROR_expected_token([",", "="])

            print("(parser) exited production: \"var_id_arr2D\"")

    def array2D_iden_rec(self):
            '''<array2D_iden_rec> → , Identifier [<int_val>] [<int_val>] <array2D_iden_rec> | λ'''
            print("(parser) entered production: \"array2D_iden_rec\"")
            
            if self.currToken:

                self.match(",")
                self.match("Identifier", False)
                
                self.match("[", False)
                if not self.arith_exp(["]"]):
                    self.ERROR_expected_pos_integer_value()
                if not self.match("]"):
                    self.ERROR_unclosed_square_bracket()
                
                self.match("[", False)
                if not self.arith_exp(["]"]):
                    self.ERROR_expected_pos_integer_value()
                if not self.match("]"):
                    self.ERROR_unclosed_square_bracket()
                if self.currToken["tokenType"] == "[":
                    self.logError("Only up to 2 dimensions of arrays are allowed.")
                
                if self.currToken["tokenType"] == ",":
                    self.array2D_iden_rec()
                
                #else:
                #    self.ERROR_unclosed_square_bracket()

            print("(parser) exited production: \"array2D_iden_rec\"")

    def array2D_init(self):
            '''<array2D_init> → = {<arr_value_2D>}'''
            print("(parser) entered production: \"array2D_init\"")
            
            if self.currToken:
                self.match("=", False)
                self.match("{", False)
                self.arr_value_2D()
                if not self.match("}"):
                    self.ERROR_unclosed_curly_braces()
            
            print("(parser) exited production: \"array2D_init\"")
 
    def arr_value_2D(self):
            '''<arr_value_2D> → {<arr_value_1D>} <arr_value_2D_rec>'''
            print("(parser) entered production: \"arr_value_2D\"")
            
            if self.currToken:
                self.match("{", False)
                self.arr_value_1D()
                if not self.match("}"):
                    self.ERROR_unclosed_curly_braces()
                self.arr_value_2D_rec()

            print("(parser) exited production: \"arr_value_2D\"")
 

    def arr_value_2D_rec(self):
            '''<arr_value_2D_rec> → , {<arr_value_1D>} <arr_value_2D_rec> | λ'''
            print("(parser) entered production: \"arr_value_2D_rec\"")
            
            if self.currToken:
                self.match(",")
                self.match("{", False)
                self.arr_value_1D()
                if not self.match("}"):
                    self.ERROR_unclosed_curly_braces()
                if self.currToken["tokenType"] == ",":
                    self.arr_value_2D_rec()    
            
            print("(parser) exited production: \"arr_value_2D_rec\"")


    def assign_stmt(self):
        print("(parser) production: \"assign_stmt\" detected")
        """<assign_stmt> → Identifier <iden_as_var_mods> <assign_stmt_op>"""
        
        if self.match("Identifier", False):
            if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["iden_as_var_mods"]:
                self.iden_as_var_mods() # match iden mods if there are any
            self.assign_stmt_op() # match assign operator

        print("(parser) exited production: \"assign_stmt\"")
        return "(AST-TEMP) assign_stmt PASSED"

    def assign_stmt_op(self):
        print('(parser) production: "assign_stmt_op" detected')

        if self.matchPredictSet("assign_operator", False):
            match self.currToken["tokenName"]:
                case "=":
                    self.match("=") 
                case "+=":
                    self.match("+=") 
                case "-=":
                    self.match("-=") 
                case "*=":
                    self.match("*=")
                case "/=":
                    self.match("/=") 
                case "%=":
                    self.match("%=")
                case _:
                    self.logError(f"Expected an assignment operator, but found '{self.currToken['tokenName']}'.")

            if not self.value([';',')']):  # check valid value
                self.ERROR_expected_token("value") 

    def iden_as_var_mods(self):
        print("(parser) production: \"iden_as_var_mods\" detected")
        
        if self.currToken and self.currToken["tokenType"] == "[":
            print("(parser) production: INSIDE \"iden_as_var_mods\" going to as_array")
            # array element
            self.as_array()

        elif self.currToken and self.currToken["tokenType"] == ".":
            # object attribute (can be object attribute of an array element upon recursion)
            print("(parser) production: INSIDE \"iden_as_var_mods\" now checking identifier")
            self.match(".")
            self.match("Identifier", False)
            if self.currToken and self.currToken["tokenType"] == "[":
                print("(parser) production: INSIDE \"iden_as_var_mods\" going to as_array")
                # array element
                self.as_array() 

        else:
            print("(parser-debug): assign statement variable has no var mods")
            pass

        print("(parser) exited production: \"iden_as_var_mods\"")
       

    def assign_func_method_mods(self):
        print("(parser) production: \"assign_func_method_mods\" detected")

        if self.currToken:
            if self.currToken["tokenType"] == "(":
                self.match("(")
                self.func_arg()
                if not self.match(")"):
                    self.ERROR_unclosed_parentheses()

            elif self.currToken["tokenType"] == "[" or self.currToken["tokenType"] == "." or self.currToken["tokenType"] in PREDICT_SETS["assign_operator"]:
                if self.currToken["tokenType"] == "[" or self.currToken["tokenType"] in PREDICT_SETS["assign_operator"]:
                    self.as_array()
                    self.assign_stmt_op()
                elif self.currToken["tokenType"] == ".":
                    self.match(".")
                    self.match("Identifier", False)
                    self.assign_func_method_mods_cont()

            else: self.ERROR_expected_token(["[", "(", "."] + PREDICT_SETS["assign_operator"])
        else: self.ERROR_expected_token(["[", "(", "."] + PREDICT_SETS["assign_operator"])

        return f"(AST-TEMP) assign_func_method_mods PASSED"

