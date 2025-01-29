#-------------------- PREDICT SETS --------------------
PREDICT_SETS = {
    "imports_rec": ["import", "private", "class", "int", "long", "bool", "float", "double", "string", "const", "void", "Identifier"],
    "std_lib": ["Cmath", "Cstring", "Carray"],
    "program_constructs": ["private", "class", "int", "long", "bool", "float", "double", "string", "const", "void", "Identifier"],
    "data_types": ["bool", "string", "int", "long", "double", "float"],
    "class_body": [ "private" ,'static', "const", "int", "long", "bool", "float", "double", "string", "Identifier" , "private", "class", "}"],
    "literals": ["whole_lit", "frac_lit", "string_lit", "Identifier"], # need to add expressions here in the future
    "print_stmts" : ["print", "println"],
    "conditional_stmt" : ["if", "switch"],
    "loop_stmt" : ["for", "while", "do", "repeat"],
    "else_chain" : ["else"],
    "unary_operator" : ["++", "--", "Identifier"],
    "init_arg" : ["Identifier", "bool", "string", "int", "long", "double", "float"],
    "switch_value" : ["whole_lit", "string_lit", "Identifier"], # TO ADD other exps
    "ctrl_stmt_body" : ["break", "continue"], # +body
    "arith_operator" : ["+", "-", "*", "/", "%"],
    "inc_arg" : ["Identifier", "--", "++", "print", "println", "("],
    "func_arg" : ["!", "(", "++", "-", "--", "Identifier", "bool_lit", "frac_lit", "in", "string_lit", "whole_lit", ")"],
    "value":["!", "(", "++", "-", "--", "Identifier", "bool_lit", "frac_lit", "in", "string_lit", "whole_lit"],
    "rel_operator" : ["==", "!=", "<", "<=", ">", ">="],
    "logic_operator" : ["&&", "||"],
    "iden_mods" : ["(", "[", "."],  # TO ADD 
    "int_val" : ["whole_lit", "Identifier", "-", "("],
    "unary_operator" : ["++", "--"],
    "lit_type": ["whole_lit", "frac_lit", "string_lit", "whole_lit"],
    "assign_operator" : ["=", "+=", "-=", "*=", "/=", "%="],
    "var_init": ["=", "+=", "-=", "*=", "/=", "%=", ",", ";"],
    "string value": ["string_lit", "Identifier", "("],
}


# reminders for predict sets:
 
# two ways to use predict sets errors (u may add mroe)
#    - for general errors: use matchPredictSet( for general errors (like may unexpected token for a specific part of the grammar, this method will generate the general error na)
#    - for custom errors: just use " in PREDICT_SETS["<non_terminal>"]  "  this will return true/false then use a custom error nalang sa else

# note: not every prod have to use predict sets cos some of em just branch to 1 token

#-------------------- PARSER --------------------
class SyntaxAnalyzer:
    # Takes tokens, initializes current token and its index
    def __init__(self, tokens):
        self.dimensionCount = 0         #for 1d or 2d array inits | counts dimensions 
        self.isDefaultValRec = False    #for params_dec | checks if all of the default values are on the rightmost side
        self.classNames = []            #for checking if constructor name matches class name
        self.inClassBody = False        #for redirecting to <class_body> instead of <program_constructs>
        self.inConstructor = False      #for not requiring 'return' in function_dec()
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

    #-------------------- HELPER FUNCTIONS --------------------
    # Advancer for the next token
    def nextToken(self):
        #print("(parser)(dbg)currtoken: " + str(self.currToken))
        self.currToken_index += 1
        if self.currToken_index < len(self.tokens):
            self.currToken = self.tokens[self.currToken_index]
        else:
            self.currToken = None



    # Peeks at a token at the current index + offset.
    def peek(self, offset=1):
        peek_index = self.currToken_index + offset
        if 0 <= peek_index < len(self.tokens):
            return self.tokens[peek_index]
        return None

    # Matches the current token with the expected type. Returns True if matched, False otherwise.
    def match(self, expected_token, hasSpecError=True):
        if self.currToken is not None and self.currToken["tokenType"] == expected_token:
            print(f"(parser) token {expected_token} matched")
            self.nextToken()
            return True
        elif not self.currToken and hasSpecError:
            print("(parser) deactivating default expected token error")
            return False
        else:
            print("(parser) activating default expected token error")
            self.ERROR_expected_token(expected_token)
            return False

    def matchPredictSet(self, non_terminal):
        if self.currToken is None:  # EOF
            self.ERROR_unexpected("", "Unexpected EOF", PREDICT_SETS.get(non_terminal, []))
            return False
        expected_predict_set = PREDICT_SETS.get(non_terminal, [])
        if self.currToken["tokenType"] not in expected_predict_set:
            self.ERROR_unexpected("", "Unexpected token", expected_predict_set)
            return False
        return True
    def checkValProd(self, stopChars): # this is so fucking stupid hsohlskjhfouihouHJDF
        paren_stack = []
        bracket_stack = []
        inner = False
        outer_exists = True
        has_string = False
        prod = "single"
        peek_index = 0 #so that it counts currToken LOL THIS IS NOT HOW PEEK() IS SUPPOSED TO BE USED BUT IT WORKS
        while True:
            if (paren_stack or bracket_stack):
                inner = True
            else:
                inner = False
            t = self.peek(peek_index)
            if not t:
                return False
            print(f'(parser)(dbg) valCheck token: {t["tokenType"]}')
            if (t["tokenType"] in ["string", "string_lit"]):
                has_string = True
            if (t["tokenType"] in stopChars):
                if not inner:
                    return prod
            if (t["tokenType"] == "("):
                paren_stack.append(t["tokenType"])
                if (peek_index == 0):
                    outer_exists = False
            elif (t["tokenType"] == "["):
                bracket_stack.append(t["tokenType"])
            elif (t["tokenType"] == ")"):
                if (not paren_stack):
                    self.ERROR_unmatched_closing()
                else:
                    paren_stack.pop()
                if not outer_exists:
                    if (self.peek(peek_index+1) and self.peek(peek_index+1)["tokenType"] in stopChars):
                        return "paren_wrap"
                    else:
                        outer_exists = True
            elif (t["tokenType"] == "]"):
                if (not bracket_stack):
                    self.ERROR_unmatched_closing()
                else:
                    bracket_stack.pop()
            elif (t["tokenType"] == "?" and not inner):
                return "<ternary_exp>"
            elif (t["tokenType"] in PREDICT_SETS["logic_operator"]):
                prod = "<logic_exp>"
            elif (t["tokenType"] in PREDICT_SETS["rel_operator"]):
                if not inner:
                    if (t["tokenType"] == "<"):
                        if (self.peek(peek_index+1) and self.peek(peek_index+1)["tokenType"] in PREDICT_SETS["data_types"]):
                            peek_index += 1
                            continue
                    if (t["tokenType"] == ">"):
                        if (peek_index > 0):
                            if (self.peek(peek_index-1) in PREDICT_SETS["data_types"]):
                                peek_index += 1
                                continue
                    if (prod != "<logic_exp>"):
                        prod = "<rel_exp>"
            elif (t["tokenType"] in PREDICT_SETS["arith_operator"]):
                if not inner:
                    if (peek_index == 0): 
                        peek_index += 1
                        continue # so it doesnt count unary as operators
                    if (peek_index > 1):
                        if (self.peek(peek_index-1) == ")" and self.peek(peek_index-2) in PREDICT_SETS["data_types"]):
                            peek_index += 1
                            continue # to avoid looking at casting of negative exp
                    if prod not in ["<rel_exp>", "<logic_exp>"]:
                        if (t["tokenType"] == "+" and has_string):
                            prod = "<str_exp>"
                        else:
                            prod = "<arith_exp>"
            peek_index += 1
                        
    def checkArithParen(self):
        # this 'solution' is so fucking stupid but this shit is making me go schizo it works for now 
        # scan the outer paren to see if there are any arith_ops and if there are then read it as arith_exp otherwise its a num_val
        paren_stack = ['(']
        bracket_stack = []
        num_val_index = 1
        while (len(paren_stack) > 0):
            t = self.peek(num_val_index)
            if not t:
                print('(parser)(dbg) checkExp paren error')
                self.ERROR_unclosed_parentheses()
                return False
            if (t["tokenType"] in PREDICT_SETS["arith_operator"]):    
                if (num_val_index == 1): 
                    num_val_index += 1
                    continue # so it doesnt count unary as operators
                if (num_val_index > 2):
                    if (self.peek(num_val_index-1) == ")" and self.peek(num_val_index-2) in PREDICT_SETS["data_types"]):
                        num_val_index += 1
                        continue # to avoid looking at casting of negative exp
                if (len(paren_stack) == 1 and len(bracket_stack) == 0): #to make sure t doesnt look in indexing
                    return True
            elif (t["tokenType"] == "("):
                paren_stack.append(t["tokenType"])
            elif (t["tokenType"] == "["):
                bracket_stack.append(t["tokenType"])
            elif (t["tokenType"] == "]"):
                if (not bracket_stack):
                    self.ERROR_unmatched_closing()
                else:
                    bracket_stack.pop()
            elif (t["tokenType"] == ")"):
                if (not paren_stack):
                    self.ERROR_unmatched_closing()
                else:
                    paren_stack.pop()
            num_val_index += 1
        return False
    
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
                f"\n\tSyntax Error: Unexpected Token '{currToken}' at line {currLine}, column {currCol}"
                f"\n\tExpected: {expected_message}\n"
            )
        else:
            message = (
                f"\n\tSyntax Error: Unexpected EOF at line {currLine}, column {currCol}"
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
            message = f"Statement is expected to be terminated by '{expected_token}', but got '{actual_token}'."
        else:
            message = f"Statement is expected to be terminated by '{expected_token}', but reached EOF."
        self.logError(message)


    # Handles unexpected tokens when expecting a specific type.
    def ERROR_expected_token(self, expected_token):
        if self.currToken is None:
            self.logError(f"Expected {expected_token}, but reached EOF.")
        else:
            self.logError(
                f"Expected {expected_token}, but got '{self.currToken['tokenName']}'."
            )

    # If no main function was found throughout the whole program
    def ERROR_no_main_func(self):
        message = "Syntax Error: Missing 'main' function to execute the program.\nThe program must include a 'main' function as the entry point."
        self.errors.append(message)
        raise SyntaxError(message)

    def ERROR_unclosed_angled_bracket(self):
        self.logError("Unclosed angled bracket: Expected '>'.") ## should we add line no. + col. num sa mga error d2

    def ERROR_unclosed_parentheses(self):
        self.logError("Unclosed parentheses: Expected ')'.")
    
    def ERROR_unclosed_curly_braces(self):
        self.logError("Unclosed curly braces: Expected '}'.")

    def ERROR_unclosed_square_bracket(self):
        self.logError("Unclosed square bracket: Expected ']'.")

    def ERROR_expected_stdlib_or_filename(self):
        self.logError("Expected a standard library (Cmath, Cstring, Carray) or a filename with '.cstr'.")

    def ERROR_expected_cstr_file(self):
        self.logError("Expected a filename with '.cstr' extension.")

    def ERROR_expected_stdlib(self):
        self.logError("Expected a standard library (Cmath, Cstring, Carray).")

    def ERROR_expected_Identifier(self):
        self.logError("Expected Identifier.")

    def ERROR_expected_Identifier_classes(self):
        if not self.currToken:  # EOF case
            self.logError("Expected an identifier, but reached EOF (End of File).")
        elif not self.match("Identifier"):  # Invalid token case
            current_value = self.currToken["tokenName"] if self.currToken else "EOF"
            self.logError(f"Expected an identifier, but found '{current_value}' instead.")

    def ERROR_missing_initializer(self):
        if self.currToken:
            error_message = f"Expected initializer before '{self.currToken['tokenName']}'"
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
        self.logError("Expected numerical value.")
    
    def ERROR_unmatched_closing(self):
        self.logError(f"Found unmatched {self.currToken["tokenType"]}.")

    def ERROR_expected_integer_value(self, expected_tokens = PREDICT_SETS["int_val"]):
        current_value = self.currToken["tokenType"] if self.currToken else "EOF"
        self.logError(
            f"Expected an integer value. Allowed tokens: {', '.join(expected_tokens)}. "
            f"Encountered: '{current_value}'."
        )

    def ERROR_main_void_return(self):
        if not self.currToken:
            self.logError("Expected ';' to terminate the return statement, but reached end of file. Use 'return;' to exit the main function successfully.")
        elif self.currToken["tokenType"] != ";":
            self.logError(f"Expected ';' to terminate the return statement, but got '{self.currToken['tokenName']}' instead. Use 'return;' to exit the main function successfully.")

    def ERROR_main_missing_return(self):
        self.logError("Missing return statement in main function. Use 'return;' to exit the main function successfully.")


    #-------------------- PARSER START --------------------
    def parse(self):
        try:
            self.program()
            #self.expression([";"])
            #self.func_method_call()
            print("Parsing completed successfully.")
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

        print("(parser) production: ### after imports_list")
        
        """<program> → <program_constructs> int main(){ <main_body> return 0;}"""
        # Parse constructs
        self.program_constructs()

        # Check for main function presence
        if not self.hasMainFunction:
            self.ERROR_no_main_func()
        else:
            while self.currToken:
                self.match("(", False)
                self.match(")", False)

                if self.match("{", False):
                    print("(parser) production: ### inside main -- START OF MAIN BODY")

                    #self.expression([";", "}"])
                    #self.match(";", False)

                    #### TEMPORARY code block
                    if self.currToken:  # Ensure self.currToken is not None
                        if self.currToken["tokenName"] in PREDICT_SETS["print_stmts"]:
                            self.output()

                    #     #if self.currToken["tokenName"] in PREDICT_SETS["conditional_stmt"]:
                    #     #    self.conditional_stmt()

                    #     #if self.currToken["tokenName"] in PREDICT_SETS["else_chain"]:
                    #     #    current_value = self.currToken["tokenName"]
                    #     #    error_message = f"'else' statements may only be used after an 'if' statement."
                    #     #    self.logError(error_message)

                        if self.currToken["tokenName"] in PREDICT_SETS["loop_stmt"]:
                            self.loop_stmt()
            
                        #else:
                        #    print("(parser) broke out of loop")
                        #    break
                    else:
                        # Handle EOF case
                        self.logError("Unexpected end of file while parsing.")

                    #print("(parser) exited temp code block")

                if not self.match("return"):
                    self.ERROR_main_missing_return()

                if not self.currToken or self.currToken["tokenType"] != ";":
                    self.ERROR_main_void_return()
                
                if not self.match(";"):
                    self.ERROR_terminating_token(";")



                if not self.match("}"):
                    self.ERROR_unclosed_curly_braces()

                # might have to be revisited, for some reason it's off by one line
                if self.currToken: 
                    currLine = self.currToken["tokenLine"]
                    currCol = self.currToken["tokenCol"]

                    print(f"warning: ({currLine}, {currCol}): Unreachable code detected")
                    break


    #def code_blocks(self):




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



    # ----- REVISIT!! can't complete errors here yet bc errors would be found in each prod first, then check if there are external errors left 
    # ex of unimplemented error: if there's a sole variable (it can be considered a class inst, pero if not yet defined, it should throw another type of error)
    def program_constructs(self):
        
        print("(parser) production: \"program_constructs\" detected: currtoken is \""
      + str(self.currToken["tokenName"])+"\"" if self.currToken else "None" + "\"")
        
        if self.currToken and self.matchPredictSet("program_constructs"):  # Top checking for predict sets, will automatically throw error if there are unexpected tokens (di na kailangan ng else statement for unexpected tokens)
            print("(parser-dbg) inside program_constructs: " + str(self.currToken["tokenName"]))
            
            # CLASS DEC
            if self.currToken["tokenType"] == "private" or self.currToken["tokenType"] == "class":
                self.class_declaration()

            # VAR DEC
            elif self.currToken["tokenType"] == "const":
                self.var_dec()

            # VOID MAIN FUNCTION OR VOID FUNCTION
            elif self.currToken["tokenType"] == "void":
                self.match("void")
                if self.currToken and self.currToken["tokenName"] == "main":
                    self.match("Identifier")
                    if self.currToken and self.currToken["tokenType"] == "(":
                        self.hasMainFunction = True  # Found main function
                    else:
                        print("( expected in main")
                        self.ERROR_expected_token('(')
                else:
                    if self.currToken:
                        if not self.match("Identifier"):
                            self.ERROR_expected_Identifier()
        
                        if self.currToken and self.currToken["tokenType"] == "(": # void Identifier(
                            self.function_dec()

                        else:
                            print("( expected in iden and not main")
                            self.ERROR_expected_token('(')
                    else:
                        self.logError("Expected a function declaration or main function.")
                

            # OBJECT INSTANTIATION -- GLOBAL OBJECTS
            elif self.currToken["tokenType"] == "Identifier":
                print("(parser): ENTERING CLASS INST")
                self.class_inst()
                print("(parser): DONE CLASS INST")
                
            # VAR OR FUNC DEC
            elif self.currToken["tokenType"] in PREDICT_SETS["data_types"]:  # sample of custom error not using matchPredictSet
                self.nextToken()
                if self.match("Identifier"): 
                    if self.currToken and self.currToken["tokenType"] == "(":  # FUNC DEC
                        self.function_dec()
                    elif self.currToken and self.currToken["tokenType"] == "=":  # VAR DEC
                        self.var_dec()
                    else:
                        self.ERROR_expected_token(["(","="])
                else:
                    self.logError("Expected a variable declaration or function declaration.")
    
        ############ FOR TESTING ONLY, WILL BE MOVED --------------------------------------------------------------------------------------
        #if self.currToken and self.matchPredictSet("print_stmts"):
        #    self.output()



    # TODO
    def class_declaration(self):
        print("(parser) production: \"class_declaration\" detected")
        if self.currToken["tokenType"] == "private":
            self.match("private")

        self.match("class", False)

        if self.currToken and self.currToken["tokenType"] == "Identifier":
            self.classNames.append(self.currToken["tokenName"])      # handles constructor name logic of recursive classes within classes
            self.match("Identifier")
        else:
            self.ERROR_expected_Identifier()
        
        self.match("{", False)

        self.class_body()

        if not self.match("}"):
            self.ERROR_unclosed_curly_braces()

        if not self.match(";"):
            self.ERROR_terminating_token(";")

        self.inClassBody = False
        self.program_constructs()

    # TODO
    def var_dec(self):      #starts at token '=' or 'const' or 'data_types'
        print("(parser) production: \"var_dec\" detected")

        if not self.currToken:
            self.matchPredictSet("data_types")
        
        if self.currToken and self.currToken["tokenType"] != "=": # if not from second calling from program_construct
            if self.currToken["tokenType"] == "const":
                self.match("const")

            self.matchPredictSet("data_types")
            self.nextToken()
            
            if not self.match("Identifier"):
                self.ERROR_expected_Identifier()

            self.iden_mods()

        
        if self.currToken and self.currToken["tokenType"] == "=":
            self.match("=")
            ############# VAR ASSIGN RULES HERE


        if not self.match(";"): 
            self.ERROR_terminating_token(";")
        
        if not self.inClassBody:
            self.program_constructs()

        else:
            self.class_body()

    # TODO
    def function_dec(self):
        print("(parser) production: \"function_dec\" detected")
        isNotVoid = True
        if self.currToken["tokenType"] != "(": # if not from second calling from program_construct
            if self.currToken["tokenType"] == "void":
                self.match("void")
                isNotVoid = False
            else:
                self.matchPredictSet("data_types")
                self.nextToken()
            if not self.match("Identifier"):
                self.ERROR_expected_Identifier()

        self.match("(", False)
            
        self.params_dec() ############### PARAM RULES HERE
        
        if not self.match(")"):
            self.ERROR_unclosed_parentheses()

        self.match("{", False)

        ############### FUNCTION BODY RULES HERE
        if isNotVoid and not self.inConstructor:
            if not self.match("return"):
                self.logError("Non-void functions must have return statement.")
            ### TODO: how to check return type and if it matches return statement?

            ################## <return_block> or <ret_value> HERE

            if not self.match(";"):
                self.logError("just add ';' for now, no logic for return vals yet")
                self.ERROR_terminating_token(";")
        
        if not isNotVoid and self.match("return"):
            self.logError("Void functions cannot have return statement.")

        if self.inConstructor and self.match("return"):
            self.logError("Constructors cannot have return statement.")
        
        if not self.match("}"):
            self.ERROR_unclosed_curly_braces()

        self.inConstructor = False

        if not self.inClassBody:
            self.program_constructs()

        else:
            self.class_body()



    # MICH START HERE
    def class_inst(self):
        print("(parser) !!!!!!!!!!!!production: \"class_inst\" detected")

        # Parse the first Identifier (class name or type)
        if not self.match("Identifier"):
            self.logError("Expected an identifier for class instantiation.")  # MICH CURRENTLY DOING
            # This error is just a placeholder habang wala pang semantic, cos normally it should identify if existing na ung class

        # Parse the second Identifier (variable name)
        if self.currToken and self.currToken["tokenType"] == "Identifier":
            self.match("Identifier")
        else:
            self.ERROR_missing_initializer()
        

        # check continuation (if single class instantiation or w/ constructor)
        has_Constructor_or_Array_Init = self.classinst_cont()

        print("(parser-dbg): done after classinst_cont -- should match semicolon")

        # Match terminating symbol
        if self.currToken:
            if self.currToken["tokenType"] not in [";", "}"] and not has_Constructor_or_Array_Init:
                self.ERROR_expected_token(['=', '[', ';'])
            elif self.currToken["tokenType"] == ";":
                self.match(";")  # valid termination
            else:
                self.ERROR_terminating_token(";")
        else:
            # If currToken is None, we're at EOF (End of File)
            if not has_Constructor_or_Array_Init:
                self.ERROR_expected_token(['=', '[', ';'])
            else:
                self.ERROR_terminating_token(";")


        # Continue parsing program constructs
        self.program_constructs()
    
    # Handle <classinst_cont>
    def classinst_cont(self):
        has_Constructor_or_Array_Init = False
        # object instantiation
        if self.currToken and self.currToken["tokenType"] == "=":
            self.match("=")
            if not self.match("Identifier"):  # should be the same name as the class name [SEMANTIC]
                self.ERROR_expected_Identifier_classes()

            self.match('(', False)

            has_Constructor_or_Array_Init = self.func_arg()

            if self.currToken and self.currToken["tokenType"] == ")":
                self.match(')')
            elif (self.currToken is None or self.currToken["tokenType"] not in PREDICT_SETS["func_arg"]) and not has_Constructor_or_Array_Init:
                self.ERROR_expected_constructor_param_closing()
            else:
                self.ERROR_expected_token([")", ","])
            return True

        # array of objects
        elif self.currToken and self.currToken["tokenType"] == "[":
            has_Constructor_or_Array_Init = True
            self.match("[")
            
            # Check if there's an integer value or EOF
            if self.currToken is None or self.currToken["tokenType"] not in PREDICT_SETS["int_val"]:
                self.ERROR_expected_integer_value(['whole_lit', 'Identifier','('])
            else:
                self.int_val([']'])    # parse <int_val>

            # Check if the next token is a closing square bracket
            if not self.currToken or not self.match("]"):
                self.ERROR_unclosed_square_bracket()


            self.classinst_def_1Drec_arr()   # parse <classinst_def_1Drec_arr>

        else:
            # λ-production (null value) = no additional tokens after the second identifier
            # Simple object instantiation
            pass

        return has_Constructor_or_Array_Init

    # Handle <classinst_def_1Drec_arr>
    def classinst_def_1Drec_arr(self):
        if self.currToken and self.currToken["tokenType"] == "[":
            self.match("[")
            
            # Check if there's an integer value or EOF
            if self.currToken is None or self.currToken["tokenType"] not in PREDICT_SETS["int_val"]:
                self.ERROR_expected_integer_value()
            else:
                self.int_val([']'])  

            if not self.match("]"):
                self.ERROR_unclosed_square_bracket()

            self.classinst_def_2Drec_arr()  # parse <classinst_def_2Drec_arr>

        elif self.currToken and self.currToken["tokenType"] == "=":
            self.match("=", False)
            self.match("{", False)

            self.object_arr1D_value()  # Parse <object_arr1D_value>

            if not self.match("}"):
                print("matching closing } for 1D parent prod")
                self.ERROR_unclosed_curly_braces()
        else:
            # λ-production
            print("(parser) λ-production for <classinst_def_1Drec_arr>")

    # Handle <classinst_def_2Drec_arr>
    def classinst_def_2Drec_arr(self):
        if self.currToken and self.currToken["tokenType"] == "=":
            self.match("=", False)
            self.match("{", False)

            self.object_arr2D_value()  # Parse <object_arr2D_value>

            if not self.match("}"):
                self.ERROR_unclosed_curly_braces()
        else:
            # λ-production
            print("(parser) λ-production for <classinst_def_2Drec_arr>")

    # Handle <object_arr1D_value>
    def object_arr1D_value(self):
        if self.currToken and self.currToken["tokenType"] == "Identifier":
            self.match("Identifier")
            self.match("(", False)

            hasNewVal = self.func_arg()

            if self.currToken and self.currToken["tokenType"] == ")":
                self.match(')')
            elif (self.currToken is None or self.currToken["tokenType"] not in PREDICT_SETS["func_arg"]) and not hasNewVal:
                self.ERROR_expected_constructor_param_closing()
            else:
                self.ERROR_expected_token([")", ","])
                

            self.object_arr_value_1D_rec()  # Parse <object_arr_value_1D_rec>
        else:
            self.ERROR_expected_Identifier_classes()

    # Handle <object_arr_value_1D_rec>
    def object_arr_value_1D_rec(self):
        if self.currToken and self.currToken["tokenType"] == ",":
            self.match(",")
            if not self.match("Identifier"):
                self.ERROR_expected_Identifier_classes()

            self.match("(", False)

            hasNewVal = self.func_arg()

            if self.currToken and self.currToken["tokenType"] == ")":
                self.match(')')
            elif (self.currToken is None or self.currToken["tokenType"] not in PREDICT_SETS["func_arg"]) and not hasNewVal:
                self.ERROR_expected_constructor_param_closing()
            else:
                self.ERROR_expected_token([")", ","])

            self.object_arr_value_1D_rec()  # Recursive call for more values
        else:
            # λ-production
            print("(parser) λ-production for <object_arr_value_1D_rec>")

    # Handle <object_arr2D_value>
    def object_arr2D_value(self):
        if self.currToken and self.currToken["tokenType"] == "{":
            self.match("{", False)

            self.object_arr1D_value()

            if not self.match("}"):
                self.ERROR_unclosed_curly_braces()

            self.object_arr2D_value_rec()  # Parse <object_arr2D_value_rec>
        else:
            self.ERROR_expected_token("{")

    # Handle <object_arr2D_value_rec>
    def object_arr2D_value_rec(self):
        if self.currToken and self.currToken["tokenType"] == ",":
            self.match(",")

            self.match("{", False)
    
            self.object_arr1D_value()

            if not self.match("}"):
                self.ERROR_unclosed_curly_braces()

            self.object_arr2D_value_rec()  # Recursive call for more values
        else:
            # λ-production
            print("(parser) λ-production for <object_arr2D_value_rec>")


    def func_arg(self):
        hasConstructorValue = False
        # Check if there's a value to parse
        if self.currToken and self.value([')',',']):
            # Parse the recursive part of the arguments
            self.func_arg_rec()
            hasConstructorValue = True
        else:
            print("(parser) λ-production for <func_arg>")  # Handle λ (empty production)
        return hasConstructorValue
    

    def func_arg_rec(self):
        # Check for a comma indicating more arguments
        if self.currToken and self.currToken["tokenType"] == ",":
            # Peek ahead to check the token after the comma
            next_token = self.peek()
            if not next_token:
                # If there's no next token, it means EOF after the comma
                self.logError("Expected another value after ',' but reached EOF.")
            elif next_token["tokenType"] not in PREDICT_SETS["value"]:
                # If the next token is not a valid value
                self.logError(f"Expected another value after ',' but got '{next_token['tokenName']}'.")

            self.match(",")  # Match the comma
            print("(parser) Found ',' indicating more arguments.")

            # Parse the next <func_arg>
            self.func_arg()
        else:
            print("(parser) λ-production for <func_arg_rec>")  # Handle λ (empty production)

    def func_method_call(self):
        self.match("Identifier")
        self.func_method_call_mods()
        if not self.match(";"):
            self.ERROR_terminating_token(";")


    def func_method_call_mods(self):
        if self.currToken and self.currToken["tokenType"] == "(":
            # Handle (<func_arg>) -- direct func call
            self.match("(", False)
            self.func_arg()
            if not self.match(")"):
                self.ERROR_unclosed_parentheses()
        elif self.currToken and self.currToken["tokenType"] == ".":
            # .Identifier(<func_arg>) -- method call
            self.match(".", False)
            self.match("Identifier", False)
            self.match("(", False)
            self.func_arg()
            if not self.match(")", False):
                self.ERROR_unclosed_parentheses()
        else:
            # Handle λ-production (no further modifications)
            self.ERROR_expected_token([".","("])
            print("(parser) λ-production for <func_method_call_mods>")



        # CODE BLOCKS!!!





        
#TODO: harley todos: errors, prod integration

    def int_val(self, stopChars):
        print('(parser) production: "int_val" detected')
        if (self.currToken and self.matchPredictSet("int_val")):
            prod = self.checkValProd(stopChars)
            if (prod == "paren_wrap"):
                self.match("(")
                self.int_val([")"])
                if not self.match(")"):
                    self.ERROR_unclosed_parentheses()
                return True
            elif (prod == "<arith_exp>"):
                self.arith_exp()
                return True
            elif (self.currToken and self.currToken["tokenType"] == "("):
                if (self.peek() in PREDICT_SETS["data_types"]):
                    self.typecast_exp()
                    return True
            elif (self.currToken and self.currToken["tokenType"] == "whole_lit"):
                self.match("whole_lit")
                return True
            elif (self.currToken and self.currToken["tokenType"] == "Identifier"):
                self.match("Identifier")
                self.iden_mods()
                return True
        else:
            return False

    def value(self, stopChars):
        print('(parser) production "value" detected')
        if (self.currToken):
            prod = self.checkValProd(stopChars)
            print(f'(parser)(dbg) value prod: {prod}')
            if (prod == "paren_wrap"):
                self.match("(")
                self.value([")"])
                if not self.match(")"):
                    self.ERROR_unclosed_parentheses()
                return True
            elif (prod == "<ternary_exp>"):
                self.ternary_exp(stopChars)
                return True
            elif (prod == "<logic_exp>"):
                print('(parser)(dbg) logic_exp')
                self.logic_exp(stopChars)     #########<logic_exp> HERE
                return True
            elif (prod == "<rel_exp>"):
                self.rel_exp(stopChars)
                return True
            elif (prod == "<arith_exp>"):
                self.arith_exp()
                return True
            elif (prod == "<str_exp>"):
                print('(parser)(dbg)<str_exp>')
                self.str_exp()##### <str_exp> HERE
                return True
            elif (self.currToken and self.currToken["tokenType"] == "in"):
                self.match("in")
                self.match("<")
                if (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["data_types"]):
                    self.nextToken()
                    self.match(">")
                    self.match("(")
                    self.input_params()#######<input_params> HERE
                    self.match(")")
                    return True
            elif (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["unary_operator"]):
                self.unary_exp()
                return True
            elif (self.currToken and self.currToken["tokenType"] == "("):
                if (self.peek() in PREDICT_SETS["data_types"]):
                    self.typecast_exp()
                    return True
            elif (self.currToken and self.currToken["tokenType"] == "!"):
                print('(parser)(dbg) logic_exp')
                self.logic_exp(stopChars)   #########<logic_exp> HERE
                return True
            elif (self.currToken and self.currToken["tokenType"] == "-"):
                self.negative_exp()
                return True
            elif (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["lit_type"]):
                self.lit_type() 
                return True
            elif (self.currToken and self.currToken["tokenType"] == "Identifier"):
                self.match("Identifier")
                self.iden_mods()
                if (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["unary_operator"]):
                    self.unary_exp(True)
                    return True
                return True
            else:
                self.ERROR_expected_token("value")
                return False
        else: 
            self.ERROR_expected_token("value")
            return False

    def lit_type(self):
        print('(parser) production: "lit_type" deteted')
        if (self.currToken and self.currToken["tokenType"] == "whole_lit"):
            self.match("whole_lit")
        elif (self.currToken and self.currToken["tokenType"] == "frac_lit"):
            self.match("frac_lit")
        elif (self.currToken and self.currToken["tokenType"] == "string_lit"):
            self.match("string_lit")
        elif (self.currToken and self.currToken["tokenType"] == "bool_lit"):
            self.match("bool_lit")

    #TODO: func_args
    def iden_mods(self):
        print('(parser) production: "iden_mods" detected')
        if (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["iden_mods"]):
            if (self.currToken and self.currToken["tokenType"] == "("):
                self.match("(")
                self.func_arg()
                if not self.match(")"):
                    print('(parser)(dbg) iden_mods paren error')
                    self.ERROR_unclosed_parentheses()
            elif (self.currToken and self.currToken["tokenType"] == "["):
                self.as_array()
                if (self.currToken and self.currToken["tokenType"] == "."):
                    self.object_rec()
            elif (self.currToken and self.currToken["tokenType"] == "."):
                self.object_rec()

    def as_array(self):
        print('(parser) production: "as_array" detected')
        if (self.currToken and self.currToken["tokenType"] == "["):
            self.match("[")
            if not self.int_val(["]"]):
                self.ERROR_expected_integer_value()
            if not self.match("]"):
                self.ERROR_unclosed_square_bracket()
            if (self.currToken and self.currToken["tokenType"] == "["):
                self.is_2d_arr()

    def is_2d_arr(self):
        print('(parser) production: "is_2d_arr" detected')
        if (self.currToken and self.currToken["tokenType"] == "["):
            self.match("[")
            if not self.int_val(["]"]):
                self.ERROR_expected_integer_value()
            if not self.match("]"):
                self.ERROR_unclosed_square_bracket()
                
    def object_rec(self):
        print('(parser) production: "object_rec" detected')
        if (self.currToken and self.currToken["tokenType"] == "."):
            self.match(".")
            self.match("Identifier")
        if (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["iden_mods"]):
            self.iden_mods()

    def expression(self, stopChars):
        print('(parser) production "expression" detected')
        if (self.currToken):
            prod = self.checkValProd(stopChars)
            print(f'(parser)(dbg) expression prod: {prod}')
            if (prod == "paren_wrap"):
                self.match("(")
                self.expression([")"])
                if not self.match(")"):
                    self.ERROR_unclosed_parentheses()
            elif (prod == "<ternary_exp>"):
                self.ternary_exp(stopChars)
            elif (prod == "<logic_exp>"):
                print('(parser)(dbg) logic_exp')
                self.logic_exp(stopChars)       #########<logic_exp> HERE
            elif (prod == "<rel_exp>"):
                self.rel_exp(stopChars)
            elif (prod == "<arith_exp>"):
                self.arith_exp()
            elif (prod == "<str_exp>"):
                print('(parser)(dbg)<str_exp>')
                self.str_exp()          ######### <str_exp> HERE
            elif (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["unary_operator"]):
                self.unary_exp()
            elif (self.currToken and self.currToken["tokenType"] == "("):
                if (self.peek() in PREDICT_SETS["data_types"]):
                    self.typecast_exp()
            elif (self.currToken and self.currToken["tokenType"] == "!"):
                print('(parser)(dbg) logic_exp')
                self.logic_exp(stopChars) #########<logic_exp> HERE
            elif (self.currToken and self.currToken["tokenType"] == "-"):
                self.negative_exp()
            elif (self.currToken and self.currToken["tokenType"] == "Identifier"):
                self.match("Identifier")
                self.iden_mods()
                if (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["unary_operator"]):
                    self.unary_exp(True)
                else:
                    self.ERROR_expected_token("{++, --}")
        else:
            self.ERROR_expected_token("expression")


    def negative_exp(self):
        print('(parser) production: "negative_exp" detected')
        if (self.currToken and self.currToken["tokenType"] == "("):
            self.match("(")
            self.negative_exp()
            if not self.match(")"):
                self.ERROR_unclosed_parentheses()
        elif (self.currToken and self.currToken["tokenType"] == "-"):
            self.match("-")
            if self.num_value() == False:
                print('(parser)(dbg) negexp num_val false ret')
                self.ERROR_expected_num_value()
        else:
            self.ERROR_expected_num_value()

    def num_value(self):
        print('(parser) production: "num_value" detected')
        if (self.currToken and self.currToken["tokenType"] == "whole_lit"):
            self.match("whole_lit")
        elif (self.currToken and self.currToken["tokenType"] == "frac_lit"):
            self.match("frac_lit")
        elif (self.currToken and self.currToken["tokenType"] == "Identifier"):
            self.match("Identifier")
            self.iden_mods()
            if (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["unary_operator"]):
                self.unary_exp(True) #no idea how to do this except for call the func to go to semantic ig???? bc if we reach this point its already a correct postfix unary exp
        elif (self.currToken and self.currToken["tokenType"] == "-"):
            self.negative_exp()
        elif (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["unary_operator"]):
            self.unary_exp()
        elif (self.currToken and self.currToken["tokenType"] == "("):
            if (self.checkArithParen()):
                self.match("(")
                self.arith_exp()
                if not self.match(")"):
                    self.ERROR_unclosed_parentheses()
            else:
                if (self.peek()["tokenType"] in PREDICT_SETS["data_types"]):
                    self.typecast_exp()
                else:
                    self.match("(")
                    if self.num_value() == False:
                        self.ERROR_expected_num_value()
                    if not self.match(")"):
                        self.ERROR_unclosed_parentheses()
        else:
            return False #for error later
    
    def arith_operator(self):
        print('(parser) producton: "arith_operator" detected')
        if (self.currToken and self.currToken["tokenType"] == "+"):
            self.match("+")
        elif (self.currToken and self.currToken["tokenType"] == "-"):
            self.match("-")
        elif (self.currToken and self.currToken["tokenType"] == "/"):
            self.match("/")
        elif (self.currToken and self.currToken["tokenType"] == "*"):
            self.match("*")
        elif (self.currToken and self.currToken["tokenType"] == "%"):
            self.match("%")
        else:
            self.ERROR_expected_token("{+, -, *, /, %}") #this will probably literally never be called because we check before calling arith_op but eh ¯\_(ツ)_/¯

    def arith_exp(self): #doesnt take precedence into account, only checks form (hopefully LMAO)
        print('(parser) production: "arith_exp" detected')
        self.num_value()
        if (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["arith_operator"]):
            while (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["arith_operator"]):
                self.arith_operator()
                if self.num_value() == False: #not using 'not' since num_value doesnt return a True
                    self.ERROR_expected_num_value()
        else:
            self.ERROR_expected_token("{+, -, *, /, %}")

    def ternary_exp(self, stopChars):
        print('(parser) production: "ternary_exp" detected')
        if (self.currToken and self.currToken["tokenType"] == "("):
            self.match("(")
            ####<condition> HERE
            print('(parser)(dbg)<condition>')
            if not self.match(")"):
                self.ERROR_unclosed_parentheses()
            if not self.match("?"):
                self.ERROR_expected_token("?")
            if not self.value([":"]):
                self.ERROR_expected_token("value")
            if not self.match(":"):
                self.ERROR_expeted_token(":")
            if not self.value(stopChars):
                self.ERROR_expected_token("value")

    def logic_exp(self, stopChars):
        print("(parser) production: \"logic_exp\" detected")
        if self.currToken and self.currToken["tokenType"] != "!":
            self.bool_value(PREDICT_SETS["logic_operator"] + stopChars)
            if (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["logic_operator"]):
                while (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["logic_operator"]):
                    self.logic_operator()
                    if not self.bool_value(PREDICT_SETS["logic_operator"] + stopChars): 
                        print('(parser)(dbg) ERROR: expected value')
                        self.ERROR_expected_token("bool value") #should i expound errors like this, bool value can be iden, bool_lit, rel_exp, logic_exp, etc.
            # else:
            #     self.ERROR_expected_token("{||, &&}")
        else:   
            self.match("!", False)
            self.logic_exp(stopChars)

        print("(parser) production: \"logic_exp\" EXITED!!")

    def logic_operator(self):
        print("(parser) production: \"logic_operator\" detected")
        if (self.currToken and self.currToken["tokenType"] == "&&"):
            self.match("&&")
        elif (self.currToken and self.currToken["tokenType"] == "||"):
            self.match("||")
        else:
            self.ERROR_expected_token("{||, &&}")


    #####CONDITION

    def bool_value(self, stopChars):
        print('(parser) production: "bool_value" detected')
        if self.currToken:
            prod = self.checkValProd(stopChars)
            if (prod == "<logic_exp>"):
                self.logic_exp(stopChars)   #######<logic_exp> HERE
                print('(parser)(dbg)<logic_exp>')
                return True
            elif (prod == "<rel_exp>"):
                self.rel_exp(stopChars)
                return True
            elif (prod == "paren_wrap"):
                self.match("(")
                if self.currToken and self.bool_value([")"]):
                    if not self.match(")"):
                        self.ERROR_unclosed_parentheses()
                        return True
                else:
                    return False
            else:
                if (self.currToken["tokenType"] == "("):
                    if (self.peek() in PREDICT_SETS["data_types"]):
                        self.typecast_exp()
                        return True
                elif (self.currToken["tokenType"] == "!"):
                    self.logic_exp(stopChars) #########<logic_exp> HERE
                    print('(parser)(dbg)<logic_exp>')
                    return True
                elif (self.currToken["tokenType"] == "Identifier"):
                    self.match("Identifier")
                    self.iden_mods()
                    return True
                elif (self.currToken["tokenType"] == "bool_lit"):
                    self.match("bool_lit")
                    return True
                else:
                    self.ERROR_expected_token("bool_value")
                    return False
        else:
            self.ERROR_expected_token("bool_value")
            return False
                
    def rel_exp(self, stopChars):
        print('(parser) production: "rel_exp" detected')
        self.value(PREDICT_SETS["rel_operator"])
        if (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["rel_operator"]):
            while (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["rel_operator"]):
                self.rel_operator()
                if not self.value(PREDICT_SETS["rel_operator"] + stopChars): 
                    print('(parser)(dbg) ERROR: expectced value')
                    self.ERROR_expected_token("value")
        else:
            self.ERROR_expected_token("{==, !=, >, <, >=, <=}")
            
    def rel_operator(self):
        print('(parser) producton: "rel_operator" detected')
        if (self.currToken and self.currToken["tokenType"] == "=="):
            self.match("==")
        elif (self.currToken and self.currToken["tokenType"] == "!="):
            self.match("!=")
        elif (self.currToken and self.currToken["tokenType"] == ">"):
            self.match(">")
        elif (self.currToken and self.currToken["tokenType"] == "<"):
            self.match("<")
        elif (self.currToken and self.currToken["tokenType"] == ">="):
            self.match(">=")
        elif (self.currToken and self.currToken["tokenType"] == "<="):
            self.match("<=")
        else:
            self.ERROR_expected_token("{==, !=, >, <, >=, <=}")

    def typecast_exp(self):
        print('(parser) production: "typecast_exp" detected')
        if (self.currToken and self.currToken["tokenType"] == "("):
            self.match("(")
            if (self.currToken and self.matchPredictSet("data_types")):
                self.nextToken()
                if not self.match(")"):
                    self.ERROR_unclosed_parentheses()
                if (self.currToken and self.currToken["tokenType"] == "("):
                    if self.peek()["tokenType"] in PREDICT_SETS["data_types"]:
                        self.typecast_exp_rec()
                    else:
                        self.match("(")
                        self.value([")"])
                        if not self.match(")"):
                            self.ERROR_unclosed_parentheses()
                else:
                    if (self.currToken and self.currToken["tokenType"] in PREDICT_SETS["lit_type"]):
                        self.lit_type()
                    elif (self.currToken and self.currToken["tokenType"] == "Identifier"):
                        self.match("Identifier")
                        self.iden_mods()
            else:
                self.ERROR_expected_token(PREDICT_SETS["data_types"])
        else:
            print(f'(parser)(dbg){self.currToken}')
            print('(parser)(dbg) wtf')

    def typecast_exp_rec(self):
        print('(parser) production: "typecast_exp_rec" detected')
        if (self.currToken and self.currToken["tokenType"] == "("):
            self.match("(")
            if (self.currToken and self.matchPredictSet("data_types")):
                self.nextToken()
                if not self.match(")"):
                    self.ERROR_unclosed_parentheses()
                if (self.currToken and self.currToken["tokenType"] == "("):
                    if self.peek()["tokenType"] in PREDICT_SETS["data_types"]:
                        self.typecast_exp_rec()
            else:
                self.ERROR_expected_token(PREDICT_SETS["data_types"])

    def unary_exp(self, post=False):
        print('(parser) production: "unary_exp" detected')
        if (post):
            self.match("Identifier", False)
            if (self.currToken and self.currToken["tokenType"] == "++"):
                self.match("++")
                # idfk man semantic ig
            elif (self.currToken and self.currToken["tokenType"] == "--"):
                self.match("--")
                # move onto semantic ig
        else:
            if (self.currToken and self.currToken["tokenType"] == "++"):
                self.match("++")
                if not self.match("Identifier"):
                    self.ERROR_expected_token("Identifier")
                self.iden_mods()
            elif (self.currToken and self.currToken["tokenType"] == "--"):
                self.match("--")
                if not self.match("Identifier"):
                    self.ERROR_expected_token("Identifier")
                self.iden_mods()



    def class_body(self): # all of these are just 'if's because class_body can be null
        print("(parser) production: \"class_body\" detected")
        self.inClassBody = True
        self.matchPredictSet("class_body")

        if self.currToken and self.currToken["tokenType"] == "private": # 17. <is_private> 
            self.match("private")
            if not self.currToken:
                self.logError("Expected Identifier, token 'class', or token 'static'.")
            elif self.currToken["tokenType"] != "static" and self.currToken["tokenType"] != "Identifier" and self.currToken["tokenType"] != "class":
                self.logError("Expected Identifier, token 'class', or token 'static'.")
        
        if self.currToken and self.currToken["tokenType"] == "class": # 22. <class_declaration>
            self.class_declaration()       #subclass declaration

        if self.currToken and self.currToken["tokenType"] == "static": # 26. <is_static> 
            self.match("static")
            self.var_dec()      #attribute dec equivaelnt

        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["data_types"]: #attribute_dec or method_dec path
            self.nextToken()
            if self.match("Identifier"): 
                    if self.currToken and self.currToken["tokenType"] == "(":
                        self.function_dec()     # method
                    elif self.currToken and self.currToken["tokenType"] == "=":
                        self.var_dec()          # attribute
                    elif self.currToken and self.currToken["tokenType"] != ";":
                        self.ERROR_expected_token(["(","=", ";"])
            else:
                self.logError("Expected a variable declaration or function declaration.")

        if self.currToken and self.currToken["tokenType"] == "Identifier": #for constructor path
            if self.currToken["tokenName"] == self.classNames[-1]:
                self.match("Identifier")
                self.classNames.pop()
                if self.currToken and self.currToken["tokenType"] == "(":
                    self.inConstructor = True
                    self.function_dec() #TODO: maybe revisit in da future
                                        
                else:
                    self.ERROR_expected_token("(")
            else:
                self.logError("Expected data type or access modifier ('private' or 'static'). Constructors must have the same name as its class.") 
                #TODO: fix error message here, just a placeholder
        
        if self.currToken and self.currToken["tokenType"] != "}":
            self.class_body()

        if not self.currToken:
            self.ERROR_unclosed_curly_braces()

    def params_dec(self):
        print("(parser) production: \"params_dec\" detected")

        if self.currToken and self.currToken["tokenType"] != ")":
            if self.currToken and self.currToken["tokenType"] not in PREDICT_SETS["data_types"] and self.currToken["tokenType"] != "Identifier":
                self.logError("Expected data type or Identifier.")
            self.nextToken()

            if self.match("Identifier"):
                if self.match("[") and self.currToken:
                    if not self.match("]"):
                        self.ERROR_unclosed_square_bracket()
                    self.dimensionCount+=1

                if self.match("[") and self.currToken:
                    if not self.match("]"):
                        self.ERROR_unclosed_square_bracket()
                    self.dimensionCount+=1

                if self.currToken and self.currToken["tokenType"] == "[":
                    self.logError("Only up to two dimensional arrays are allowed.")
            else: self.ERROR_expected_Identifier()
            
            if self.currToken and self.currToken["tokenType"] == "=":
                self.isDefaultValRec = self.match("=")  # when '=' is matched in params, isDefaultValRec becomes true
                if self.dimensionCount <= 0:        #handle when param init not array
                    self.matchPredictSet("literals")
                    self.nextToken()
                else:
                    if self.currToken and not self.match("{"):
                        self.logError("Expected array initialization. E.g. {value, value, value, ...}")
                        # placeholder error for now
                    self.array_init()
                    print("Outside array_init")
                    self.dimensionCount = 0
                    if self.currToken and not self.match("}"):
                        self.ERROR_unclosed_curly_braces()
            
            if self.currToken and self.isDefaultValRec and self.currToken["tokenType"] != "=" and self.currToken["tokenType"] != ",":
                self.logError("No non-default argument must follow default argument.")
                
            if self.currToken and self.currToken["tokenType"] == ",":
                self.match(",")
                if not self.currToken or self.currToken["tokenType"] not in PREDICT_SETS["data_types"] and self.currToken["tokenType"] != "Identifier":
                    self.logError("Expected data type or Identifier.")
                self.params_dec()   #recurse when ',' is found

        
        
    def array_init(self):   
        print(f"(parser) production: \"array_init #{self.dimensionCount}\" detected")
        
        # data_type Identifier[int_val][int_val] = {
        #                                            ^ starts AFTER token "{" 
        # uses self.dimensionCount

        if self.dimensionCount == 2:        # for 2d arrays
            self.match("{", False)

            self.dimensionCount-=1
            self.array_init()       #go into array_init as 1d array
            # print("back as 2d array")
            self.dimensionCount+=1

            if self.currToken and self.currToken["tokenType"] == ",":
                self.match(",")
                self.array_init()   #go into array_init as 2d array

            elif not self.currToken or not self.match("}"):     #outer 2d array closing bracket
                # print("from 2d na error")
                self.ERROR_unclosed_curly_braces()

        else:               #for 1d array and inner 2darray {}'s
            self.matchPredictSet("literals")    #TODO: maybe add different error here? pwede expressions d2 but not yet implemented
            self.nextToken()

            if self.currToken and self.currToken["tokenType"] == ",":
                    self.match(",")
                    if not self.currToken or self.currToken["tokenType"] not in PREDICT_SETS["literals"] and self.currToken["tokenType"] != "Identifier":
                        self.logError("Expected literal or Identifier.")
                    self.array_init()       #recurse if found a ',' token

            elif self.currToken and self.currToken["tokenType"] == "}":      #inner 1d array closing bracket
                self.match("}")
            
            else:
                #print("from 1d na error")
                self.ERROR_unclosed_curly_braces()
    
  
  # ALEX start here
    def condition(self, condType):
        '''<condition> → <bool_value>'''
        print("(parser) entered production: \"condition\"")
        
        ## <bool_value> here (only bool_lit for now)
        if not self.match("bool_lit"):
            if self.currToken and self.currToken["tokenType"] == ")":
                self.ERROR_missing_condition(condType)
            else: 
                self.ERROR_invalid_condition(condType)

        print("(parser) exited production: \"condition\"")
    
    # bare-minimum tested
    def output(self):
        '''<output> → <print_stmts>(<print_params>);'''
        print("(parser) entered production: \"output\"")
        
        '''<print_stmts> → print | println'''
        # <print_stmts> are already expected to be here before it entered func
        if self.matchPredictSet("print_stmts"):
            self.nextToken()
        self.match("(", False)
        
        # won't enter print_params if null
        if self.currToken and self.currToken["tokenType"] != ")":
            self.print_params()
        
        if not self.match(")"): 
            self.ERROR_unclosed_parentheses()
        if not self.match(";"): 
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"output\"")

    # bare-minimum tested
    def print_params(self):
        '''<print_params> → <value> <output_rec> | null'''
        print("(parser) entered production: \"print_params\"")
        
        # if <print_params> are not null
        if self.currToken and self.currToken["tokenType"] != ")":
            ## <value> here (string_lit for now)
            self.match("string_lit", False)
            # self.value([",", ")"])
            if self.currToken and self.currToken["tokenType"] == ",":
                self.output_rec()
        
        print("(parser) exited production: \"print_params\"")

    # bare-minimum tested
    def output_rec(self):
        '''<output_rec> → ,<value> <output_rec> | null'''
        print("(parser) entered production: \"output_rec\"")
        
        self.match(",", False)
        ## <value> cannot be empty
        ## <value> here (string_lit for now)
        self.match("Identifier", False)

        #if not self.value([",", ")"]):
        #    self
        if self.currToken and self.currToken["tokenType"] == ",":
            self.output_rec()

        print("(parser) exited production: \"output_rec\"")
    
    # bare-minimum tested
    def conditional_stmt(self):
        '''<conditional_stmt> → <if_stmt> | <swicth_stmt>'''
        print("(parser) entered production: \"conditional_stmt\"")

        if self.currToken and self.currToken["tokenType"] == "if":
            self.if_stmt()
        elif self.currToken and self.currToken["tokenType"] == "switch":
            self.switch_stmt()

        print("(parser) exited production: \"conditional_stmt\"")
    
    # bare-minimum tested
    def if_stmt(self):
        '''<if_stmt> → if(<condition){<ctrl_stmt_body>} <else_chain>'''
        print("(parser) entered production: \"if_stmt\"")

        self.match("if", False)
        if self.currToken and self.currToken["tokenType"] == "{":
            self.ERROR_missing_condition("if")
        self.match("(", False)
        self.condition("if")
        if not self.match(")"): 
            self.ERROR_unclosed_parentheses()
        
        self.match("{", False)

        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
            self.ctrl_stmt_body()

        if not self.match("}"):
            self.ERROR_unclosed_curly_braces()

        if self.currToken["tokenName"] in PREDICT_SETS["else_chain"]:
            self.else_chain()

        print("(parser) entered production: \"if_stmt\"")

    
    def ret_value(self):
        '''<ret_value> → <value> | null'''
        print("(parser) entered production: \"ret_value\"")

        if self.peek() != ";":
            # <value> here (literals for now)
            self.value([";"])
            # self.matchPredictSet("literals")
            # self.nextToken() 

        print("(parser) exited production: \"ret_value\"")

    # bare-minimum tested
    def break_stmt(self):
        '''<break_stmt> → break;'''
        print("(parser) entered production: \"break_stmt\"")

        self.match("break", False)
        if not self.match(";"):
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"break_stmt\"")

    # bare-minimum tested
    def continue_stmt(self):
        '''<continue_stmt> → continue;'''
        print("(parser) entered production: \"continue_stmt\"")

        self.match("continue", False)
        if not self.match(";"):
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"continue_stmt\"")

    # bare-minimum tested
    def init_arg(self):
        '''<init_arg> → <for_init_data_type> Identifier = <value> <assign_stmt_rec> <var_iden_rec> | null'''
        '''<for_init_data_type> → <data_type> | null'''
        print("(parser) entered production: \"init_arg\"")

        if self.currToken["tokenName"] in PREDICT_SETS["data_types"]:
            self.nextToken()
        self.match("Identifier", False)
        self.match("=", False)
        # <value> here (literals for now)
        # if self.currToken["tokenName"] in PREDICT_SETS["literals"]:
            # self.nextToken()
        self.value(PREDICT_SETS["assign_operator"] + [",", ";"])
        #self.assign_stmt_rec()
        #self.var_iden_rec()

        print("(parser) exited production: \"init_arg\"")

    # to continue testing
    def inc_arg(self):
        '''<inc_arg> → <unary_exp> | Identifier = <value> <assign_stmt_rec> <var_iden_rec> 
        | <output> | <func_method_call>'''
        print("(parser) entered production: \"inc_arg\"")
        
        if self.currToken["tokenName"] in PREDICT_SETS["unary_operator"]:
            print("(parser) entered production: \"unary_exp\"")
            self.unary_exp()
            print("(parser) exited production: \"unary_exp\"")
        
        elif self.currToken and self.currToken["tokenType"] == "Identifier":
            if self.peek() in PREDICT_SETS["unary_operator"]:
                print("(parser) entered production: \"unary_exp\"")
                self.unary_exp(True)
                print("(parser) exited production: \"unary_exp\"")
                
            elif self.peek() == "(":
                print("(parser) entered production: \"func_method_call\"")
                #self.func_method_call()
                print("(parser) exited production: \"func_method_call\"")
                
            elif self.peek() == "=":
                self.match("Identifier", False)
                self.match("=", False)
                # <value> here (literals for now)
                self.value(PREDICT_SETS["assign_operator"] + [",", ")"])
                # if self.matchPredictSet("literals"):
                #     self.nextToken()
                #self.assign_stmt_rec()
                #self.var_iden_rec()
        
        elif self.currToken and self.currToken["tokenType"] in PREDICT_SETS["print_stmts"]:
            self.output()

        elif self.currToken and self.currToken["tokenType"] == "(":
            self.match("(", False)
            self.inc_arg()
            if not self.match(")"):
                self.ERROR_unclosed_parentheses()

        print("(parser) exited production: \"inc_arg\"")

    # bare-minimum tested
    def else_chain(self):
        '''<else_stmt> → <if_stmt> | { <ctrl_stmt_body> }'''
        print("(parser) entered production: \"else_chain\"")

        self.match("else", False)
        if self.currToken and self.currToken["tokenType"] == "if":
            self.if_stmt()
        else:
            self.match("{", False)
            if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
                self.ctrl_stmt_body()
            if not self.match("}"):
                self.ERROR_unclosed_curly_braces()
        
        print("(parser) exited production: \"else_chain\"")
        
    # bare-minimum tested
    def switch_stmt(self):
        '''<switch_stmt> → switch (<switch_value>) {<case_stmt> <default_stmt>}'''
        print("(parser) entered production: \"switch_stmt\"")

        self.match("switch", False)
        if self.currToken and self.currToken["tokenType"] == "{":
            self.ERROR_missing_condition("switch")
        self.match("(", False)
        
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["switch_value"]:
            self.switch_value()
        else: #cannot be empty
            self.logError("'switch' condition cannot be empty.")
        
        if not self.match(")"): 
            self.ERROR_unclosed_parentheses()
        
        self.match("{", False)
        self.case_stmt()
        if self.currToken and self.currToken["tokenType"] == "default":
            self.default_stmt()
        if not self.match("}"):
            self.ERROR_unclosed_curly_braces()
        
        print("(parser) exited production: \"switch_stmt\"")

    # bare-minimum tested
    def switch_value(self):
        '''<switch_value> → string_lit | whole_lit | Identifier<iden_mods> 
        | <arith_exp> | <negative_exp> | <typecast_exp>'''
        print("(parser) entered production: \"switch_value\"")

        if self.currToken and self.currToken["tokenType"] == "string_lit": 
            self.match("string_lit", False)

        elif self.currToken and self.currToken["tokenType"] == "whole_lit": 
            self.match("whole_lit", False)
        
        elif self.currToken and self.currToken["tokenType"] == "Identifier":
            
            if self.peek() in PREDICT_SETS["iden_mods"]:
                print("(parser) entered production: \"iden_mods\"")
                #self.iden_mods()
                print("(parser) exited production: \"iden_mods\"")
           
            elif self.peek() in PREDICT_SETS["arith_operator"]:
                print("(parser) entered production: \"arith_exp\"")
                #self.arith_exp()
                print("(parser) exited production: \"arith_exp\"")

            else:
                self.match("Identifier", False)
                
        elif self.currToken and self.currToken["tokenType"] == "(":
            
            if self.peek() in PREDICT_SETS["data_types"]:
                print("(parser) entered production: \"typecast_exp\"")
                #self.typecast_exp()
                print("(parser) exited production: \"typecast_exp\"")
            
            else: # for when a madman decides to do this ((((((((()))))))))
                for x in self.peek(x):
                    if x == "(":
                        continue
                    elif x == "-":
                        print("(parser) entered production: \"negative_exp\"")
                        #self.negative_exp()
                        print("(parser) exited production: \"negative_exp\"")
                        break;
                    elif x == ("whole_lit" or "Identifier"):
                        print("(parser) entered production: \"arith_exp\"")
                        #self.arith_exp()
                        print("(parser) exited production: \"arith_exp\"")
                        break;
                    else:
                        self.logError("Invalid value for 'switch' statement.")
       
        else:
            self.logError("'switch' condition cannot be empty.")
    
        print("(parser) exited production: \"switch_value\"")

    # bare-minimum tested
    def case_stmt(self):
        '''<case_stmt> → case <case_value>: <ctrl_stmt_body> <case_stmt_rec>'''
        print("(parser) entered production: \"case_stmt\"")

        self.match("case", False)
        self.case_value()
        self.match(":")
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
            self.ctrl_stmt_body()
        if self.currToken and self.currToken["tokenType"] == "case":
            self.case_stmt()

        print("(parser) exited production: \"case_stmt\"")
    
    # bare-minimum tested
    def case_value(self):
        '''<switch_value> → string_lit | whole_lit | <arith_exp> | <negative_exp> | <typecast_exp>'''
        print("(parser) entered production: \"case_value\"")   

        if self.currToken and self.currToken["tokenType"] == "string_lit": 
            if self.peek() == "+":
                print("(parser) entered production: \"str_exp\"")
                #self.str_exp()
                print("(parser) exited production: \"str_exp\"")
            else:
                self.match("string_lit", False)
            
        elif self.currToken and self.currToken["tokenType"] == "whole_lit": 
            if self.peek() in PREDICT_SETS["arith_operator"]:
                print("(parser) entered production: \"arith_exp\"")
                #self.arith_exp()
                print("(parser) exited production: \"arith_exp\"")
            else:
                self.match("whole_lit", False)
        
        elif self.currToken and self.currToken["tokenType"] == "-":
            print("(parser) entered production: \"negative_exp\"")
            #self.negative_exp()
            print("(parser) exited production: \"negative_exp\"") 
        
        elif self.currToken and self.currToken["tokenType"] == "(":
            if self.peek() in PREDICT_SETS["data_types"]:
                print("(parser) entered production: \"typecast_exp\"")
                #self.typecast_exp()
                print("(parser) exited production: \"typecast_exp\"")
            
            else: 
                self.match("(", False)
                self.case_value()
                if not self.match(")"):
                    self.ERROR_unclosed_parentheses()

        else:
            self.logError("Invalid value for 'switch' statement.")

        print("(parser) exited production: \"case_value\"")

    # bare-minimum tested
    def default_stmt(self):
        self.match("default", False)
        self.match(":", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
            self.ctrl_stmt_body()
    
    # bare-minimum tested
    def loop_stmt(self):
        print("(parser) entered production: \"loop_stmt\"")

        if self.currToken and self.currToken["tokenType"] == "while":
            self.while_stmt()
        elif self.currToken and self.currToken["tokenType"] == "do": 
            self.do_stmt()
        elif self.currToken and self.currToken["tokenType"] == "for":
            self.forloop_stmt()
        elif self.currToken and self.currToken["tokenType"] == "repeat":
            self.repeat_stmt()

        print("(parser) exited production: \"loop_stmt\"")
    
    # bare-minimum tested
    def forloop_stmt(self):
        print("(parser) entered production: \"forloop_stmt\"")

        self.match("for", False)
        self.match("(", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["init_arg"]:
            self.init_arg()
        if not self.match(";"):
            self.ERROR_terminating_token(";")
        
        self.condition("for-loop")
        
        if not self.match(";"):
            self.ERROR_terminating_token(";")
        
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["inc_arg"]:
            self.inc_arg()
        
        if not self.match(")"):
            self.ERROR_unclosed_parentheses()

        self.match("{", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
            self.ctrl_stmt_body()
        if not self.match("}"):
            self.ERROR_unclosed_curly_braces()
        
        print("(parser) exited production: \"forloop_stmt\"")
    
    # bare-minimum tested
    def while_stmt(self):
        print("(parser) entered production: \"while_stmt\"")

        self.match("while", False)
        
        self.match("(", False)
        self.condition("while")
        if not self.match(")"):
            self.ERROR_unclosed_parentheses()
        
        self.match("{", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
            self.ctrl_stmt_body()
        if not self.match("}"):
            self.ERROR_unclosed_curly_braces()
        
        print("(parser) exited production: \"while_stmt\"")

    # bare-minimum tested
    def do_stmt(self):
        print("(parser) entered production: \"do_stmt\"")
        
        self.match("do", False)
        
        self.match("{", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
            self.ctrl_stmt_body()
        if not self.match("}"):
            self.ERROR_unclosed_curly_braces()
        
        if not self.match("while"):
            self.logError("'do' statement must include 'while' condition.")
        self.match("(", False)
        self.condition("while")
        if not self.match(")"):
            self.ERROR_unclosed_parentheses()
        if not self.match(";"):
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"do_stmt\"")

    # bare-minimum tested
    def repeat_stmt(self):
        print("(parser) entered production: \"repeat_stmt\"")

        self.match("repeat", False)
        self.match("(", False)
        # <int_value> here (whole_lit for now)
        self.int_val([")"])
        # self.match("whole_lit", False)
        if not self.match(")"):
            self.ERROR_unclosed_parentheses()
        
        self.match("{", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
            self.ctrl_stmt_body()
        if not self.match("}"):
            self.ERROR_unclosed_curly_braces()
        
        print("(parser) exited production: \"repeat_stmt\"")
    
    
    def return_block(self):
        print("(parser) entered production: \"return_block\"")
        
        self.match("return", False)
        # <ret_value> here, (literals for now)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["literals"]:
            self.ret_value()
        if not self.match(";"):
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"return_block\"")
    
    # bare-minimum tested
    def ctrl_stmt_body(self):
        print("(parser) entered production: \"ctrl_stmt_body\"")

        if self.currToken and self.currToken["tokenType"] == "break":
            self.break_stmt()
        elif self.currToken and self.currToken["tokenType"] == "continue":
            self.continue_stmt()
        #elif self.currToken and self.currToken["tokenType"] in PREDICT_SETS["body"]:
        #self.body()

        print("(parser) exited production: \"ctrl_stmt_body\"")



#jeh
    def input(self):
        print("(parser) entered production: \"input\"")
        '''<input> → in<data_type>(<input_params>)'''
        self.match("in", False)
        self.match("<", False)
        
        ## For literals, data types, operators, or any prods that ONLY contain terminals
        ## use matchPredictSet and specify the name of the predict set to be used
        ## ADD to predict set if it doesn't exist yet
        if self.matchPredictSet("data_types"):
            self.nextToken()
        
        if not self.match(">"):
            self.ERROR_unclosed_angled_bracket()
        
        self.match("(", False)
        
        ## Before it even enters input_params you have to catch whether it exists or not
        ## self.peek() allows you to check the next token w/o having to move to it
        if self.peek() != ")":
            self.input_params()
        
        if not self.match(")"):
            self.ERROR_unclosed_parentheses()
        
        if not self.match(";"):
            self.ERROR_terminating_token(";")
        
        print("(parser) exited production: \"input\"")


    def input_params(self):
        print("(parser) entered production: \"input_params\"")
        """<input_params> → <int_val> | <string_value> | <string_value>,<int_val> | λ"""
        
        ## You can use literals muna for testing values, use int_val, string_val, etc.
        ## later on when all prods are complete

        if self.currToken and self.currToken["tokenType"] == "whole_lit": #int_val:
            self.int_val()
            self.match("whole_lit", False)
        
        elif self.currToken and self.currToken["tokenType"] == "string_lit":
            self.string_value()
            self.match("string_lit", False)
            
            if self.match(","):
                if not self.match("whole_lit"):
                    ## Special error
                    self.logError("Invalid value for 'in' statement character limit")

                ## We'll use this later on when prods are complete, might have to be revised
                
                if self.currToken and self.currToken["tokenType"] == "int_val":
                    self.int_val()
        
        
        print("(parser) exited production: \"input_params\"")



    def var_iden(self):
        print("(parser) entered production: \"var_iden\"")
        """<var_iden> → Identifier <var_id_mods>"""

        if self.match("Identifier", False):
            if self.peek() != [",", "=", "["]:
                self.var_id_mods()
      
        print("(parser) exited production: \"var_iden\"")


    def var_id_mods(self):
        print("(parser) entered production: \"var_id_mods\"")
        """<var_id_mods> → <var_init> <var_iden_rec> | [<int_val>] <var_id_arr1D> | λ"""
    
        if self.match("="):
            self.var_init()
            self.var_iden_rec()
        
        elif self.match("["):
            if self.peek() == "whole_lit":
                self.int_val()
                self.var_id_arr1D()
        
        print("(parser) exited production: \"var_id_mods\"")


    def var_init(self):
        """<var_init> → = <value> <assign_stmt_con> <var_iden_rec> | λ"""
        print("(parser) entered production: \"var_init\"")
        
        if self.match("="):
            if self.matchPredictSet("value", False):
                self.value(PREDICT_SETS["var_init"])
            self.assign_stmt_con()
            self.var_iden_rec()
       
        
        print("(parser) exited production: \"var_init\"")


    def var_iden_rec(self):
        """<var_iden_rec> → , Identifier <var_init> <var_iden_rec> | λ"""
        print("(parser) entered production: \"var_iden_rec\"")
        
        if self.match(","):
            if self.match("Identifier"):
                self.var_init()
                self.var_iden_rec()
            else:
                self.ERROR_expected_token("Identifier")
        print("(parser) exited production: \"var_iden_rec\"")


    def var_id_arr1D(self):
        '''<var_id_arr1D> → <array1D_iden_rec> | <array1D_init>'''
        print("(parser) entered production: \"var_id_arr1D\"")
        if self.currToken["tokenType"] == ",":
           self.array1D_iden_rec()
        elif self.currToken["tokenType"] == "=":
            self.array1D_init()
        else:
            self.ERROR_expected_token([",", "="])
        print("(parser) exited production: \"var_id_arr1D\"")

    def array1D_iden_rec(self):
        '''<array1D_iden_rec> → , Identifier [<int_val>] <array1D_iden_rec> | λ'''
        print("(parser) entered production: \"array1D_iden_rec\"")
        if self.match(","):
            if self.match("Identifier", False):
                if self.match("[", False):
                    self.int_val(["]"])
                    if not self.match("]"):
                        self.ERROR_unclosed_square_bracket()
                    self.array1D_iden_rec()
        print("(parser) exited production: \"array1D_iden_rec\"")

    def array1D_init(self):
            '''<array1D_init> → = {<arr_value_1D>}'''
            print("(parser) entered production: \"array1D_init\"")
            if self.match("=", False):
                if self.match("{", False):
                    self.arr_value_1D()
                    if not self.match("}"):
                        self.ERROR_unclosed_curly_braces()
                print("(parser) exited production: \"array1D_init\"")

    def arr_value_1D(self):
            '''<arr_value_1D> → <value> <arr_value_1D_rec>'''
            print("(parser) entered production: \"arr_value_1D\"")
            if self.currToken["tokenType"] in PREDICT_SETS["value"]:
                self.value(["}", ","])
                self.arr_value_1D_rec()
            else:
                self.ERROR_expected_token("value")

            print("(parser) exited production: \"arr_value_1D\"")

    def arr_value_1D_rec(self):
            '''<arr_value_1D_rec> → , <value> <arr_value_1D_rec> | λ'''
            print("(parser) entered production: \"arr_value_1D_rec\"")
            if self.match(","):
                if self.currToken["tokenType"] in PREDICT_SETS["value"]:
                    self.value(["}", ","])
                    self.arr_value_1D_rec()
                else:
                    self.ERROR_expected_token("value")
           
            print("(parser) exited production: \"arr_value_1D_rec\"")

    def var_id_arr2D(self):
            '''<var_id_arr2D> → <array2D_iden_rec> | <array2D_init>'''
            print("(parser) entered production: \"var_id_arr2D\"")
            if self.currToken["tokenType"] == ",":
                self.array2D_iden_rec()
            elif self.currToken["tokenType"] == "=":
                self.array2D_init()
            else:
                self.ERROR_expected_token([",", "="])

            print("(parser) exited production: \"var_id_arr2D\"")

    def array2D_iden_rec(self):
            '''<array2D_iden_rec> → , Identifier [<int_val>] [<int_val>] <array2D_iden_rec> | λ'''
            print("(parser) entered production: \"array2D_iden_rec\"")
            if self.match(","):
                if self.match("Identifier", False):
                    if self.match("[", False):
                        self.int_val(["]"])
                        if self.match("]") and self.match("["):
                            self.int_val(["]"])
                            if not self.match("]"):
                                self.ERROR_unclosed_square_bracket()
                            self.array2D_iden_rec()
                        else:
                            self.ERROR_unclosed_square_bracket()

            print("(parser) exited production: \"array2D_iden_rec\"")

    def array2D_init(self):
            '''<array2D_init> → = {<arr_value_2D>}'''
            print("(parser) entered production: \"array2D_init\"")
            if self.match("=", False):
                if self.match("{", False):
                    self.arr_value_2D()
                    if not self.match("}"):
                        self.ERROR_unclosed_curly_braces()
            print("(parser) exited production: \"array2D_init\"")
 
    def arr_value_2D(self):
            '''<arr_value_2D> → {<arr_value_1D>} <arr_value_2D_rec>'''
            print("(parser) entered production: \"arr_value_2D\"")
            if self.match("{", False):
                self.arr_value_1D()
                if not self.match("}"):
                    self.ERROR_unclosed_curly_braces()
                self.arr_value_2D_rec()

            print("(parser) exited production: \"arr_value_2D\"")
 

    def arr_value_2D_rec(self):
            '''<arr_value_2D_rec> → , {<arr_value_1D>} <arr_value_2D_rec> | λ'''
            print("(parser) entered production: \"arr_value_2D_rec\"")
            if self.match(","):
                if self.match("{", False):
                    self.arr_value_1D()
                    if not self.match("}"):
                        self.ERROR_unclosed_curly_braces()
                    self.arr_value_2D_rec()
            print("(parser) exited production: \"arr_value_2D_rec\"")

    def str_exp(self):
        print("(parser) production: \"str_exp\" detected")
        """<str_exp> → <string_value> + <string_value>"""

        if self.matchPredictSet("string_value", False):
            self.string_value()  
            
            if self.match("+", False):  
                self.matchPredictSet("string_value", False)
                self.string_value()
   
        print("(parser) exited production: \"str_exp\"")


    def string_value(self):
        print("(parser) production: \"string_value\" detected")
        """<string_value> → string_lit | Identifier <iden_mods> | <str_exp> | (<string_value>) | <typecast_exp>"""
        if not self.match("string-lit", False):
           return 
        elif self.peek() == "+":
                self.match("+", False)  
                self.str_exp()

        elif self.peek() == "(":
                self.match("(", False)
                self.string_value()  
                if not self.match(")"):
                    self.ERROR_unclosed_parentheses()
        elif self.match("Identifier", False):
                self.iden_mods()
        elif self.peek() in PREDICT_SETS["typecast_exp", False]:
                self.typecast_exp()

        print("(parser) exited production: \"string_value\"")


    def assign_stmt(self):
        print("(parser) production: \"assign_stmt\" detected")
        """<assign_stmt> → Identifier <iden_as_var_mods> <assign_stmt_con> ;"""

        if not self.match("Identifier", False):
            self.iden_as_var_mods()
            self.assign_stmt_con()

        if not self.match(";"):
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"assign_stmt\"")

    def assign_stmt_con(self):
        print("(parser) production: \"assign_stmt_con\" detected")
        """<assign_stmt_con> → <assign_operator> <value> | <assign_stmt_rec> <assign_const>"""

        if self.matchPredictSet("assign_operator"):
            next_token = self.peek()
            if next_token and next_token["tokenType"] == "Identifier":
                print("(parser) entered production: \"assign_stmt_rec\"")
                self.assign_stmt_rec()  
                self.assign_const()  
                print("(parser) exited production: \"assign_stmt_rec\"")
            else:
                self.assign_operator()
                self.value([])

        print("(parser) exited production: \"assign_stmt_con\"")

    def assign_operator(self):
            print("(parser) production: \"assign_operator\" detected")
            """<assign_operator> → = | += | -= | *= | /= | %="""

            if self.matchPredictSet("assign_operator", False):
                self.match(self.currToken["tokenName"])

            print("(parser) exited production: \"assign_operator\"")


    def assign_stmt_rec(self):
        print("(parser) production: \"assign_stmt_rec\" detected")
        """<assign_stmt_rec> → <assign_operator> Identifier <iden_as_var_mods> <assign_stmt_rec> | λ"""
        if self.matchPredictSet("assign_operator"):
            self.assign_operator()  
            if self.match("Identifier", False):
                self.iden_as_var_mods() 

            self.assign_stmt_rec()

        print("(parser) exited production: \"assign_stmt_rec\"")
            
    def assign_const(self):
        print("(parser) production: \"assign_const\" detected")
        """<assign_const> → <assign_operator> <value> | λ"""

        if self.matchPredictSet("assign_operator"):
            self.assign_operator()
        if not self.value([]):
            self.ERROR_expected_token(["value"])

        print("(parser) exited production: \"assign_const\"")

    def iden_as_var_mods(self):
        print("(parser) production: \"iden_as_var_mods\" detected")
        """<iden_as_var_mods> → <as_array> <iden_as_var_mods_cont>"""

        self.as_array()         
        self.iden_as_var_mods_cont()  

        print("(parser) exited production: \"iden_as_var_mods\"")

    def iden_as_var_mods_cont(self):
        print("(parser) production: \"iden_as_var_mods_cont\" detected")
        """<iden_as_var_mods_cont> → . Identifier <as_array> | λ"""

        if self.match("."):
            self.match("Identifier", False)
            self.as_array()  

        print("(parser) exited production: \"iden_as_var_mods_cont\"")

