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
    "else_chain" : ["else"],
    "unary_operator" : ["++", "--", "Identifier"],
    "init_arg" : ["Identifier", "bool", "string", "int", "long", "double", "float"],
    "switch_value" : ["whole_lit", "string_lit", "Identifier"], # TO ADD other exps
    "ctrl_stmt_body" : ["break", "continue"], # +body
    "iden_mods" : ["("], # TO ADD 
    "arith_operator" : ["+", "-", "*", "/", "%"],
    "inc_arg" : ["Identifier", "--", "++", "print", "println", "("]
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

    #-------------------- PARSER START --------------------
    def parse(self):
        try:
            self.program()
            print("Parsing completed successfully.")
        except SyntaxError as e:
            #print(f"Parsing incomplete with error/s: {e}")
            print (e)
        return self.errors

    #-------------------- HELPER FUNCTIONS --------------------
    # Advancer for the next token
    def nextToken(self):
        #print("currtoken: " + str(self.currToken))
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
            self.nextToken()
            return True
        elif self.currToken is not None and hasSpecError:
            return False
        else:
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
            message = f"Statement is expected to be terminated by '{expected_token}', before '{actual_token}'."
        else:
            message = f"Statement is expected to be terminated by '{expected_token}', but reached EOF."
        self.logError(message)


    # Handles unexpected tokens when expecting a specific type.
    def ERROR_expected_token(self, expected_token):
        if self.currToken is None:
            self.logError(f"Expected '{expected_token}', but reached EOF.")
        else:
            self.logError(
                f"Expected '{expected_token}', but got '{self.currToken['tokenName']}'."
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

    def ERROR_missing_initializer(self):
        self.logError("Expected initializer before " + self.currToken["tokenName"])

    def ERROR_missing_condition(self):
        self.logError(f"Expected condition after '{self.tokens[self.currToken_index - 1]}'")

    def ERROR_invalid_condition(self, condType):
        self.logError(f"Invalid condition for '{condType}' statement")

    def ERROR_empty_condition(self, condType):
        self.logError(f"Condition cannot be empty for '{condType}' statement")
    

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
                if self.currToken["tokenName"] == "(":
                    self.match("(", False)
                    self.match(")", False)
                    self.match("{", False)
                    print("(parser) production: ### inside main")

                    #### TEMPORARY code block
                    if self.currToken["tokenName"] in PREDICT_SETS["print_stmts"]:
                        self.output()

                    if self.currToken["tokenName"] in PREDICT_SETS["conditional_stmt"]:
                        self.conditional_stmt()

                    if self.currToken["tokenName"] in PREDICT_SETS["else_chain"]:
                        current_value = self.currToken["tokenName"]
                        error_message = f"'else' statements may only be used after an 'if' statement."
                        self.logError(error_message)

                    self.match("return", False)

                    # if not whole lit or 0: error should state that the final return statement of the main function is 0, instead it got currtoken
                    if not self.match("whole_lit"):
                        current_value = self.currToken["tokenName"] if self.currToken else "EOF"
                        error_message = (
                            f"The main function must end with a return statement returning '0'.\n"
                            f"Instead, encountered '{current_value}'. Ensure the main function has a final return statement as 'return 0;'."
                        )
                        self.logError(error_message)


                    if not self.match(";"):
                        self.ERROR_terminating_token(";")

                    if not self.match("}"):
                        self.ERROR_unclosed_curly_braces()

                elif self.currToken["tokenName"] == ";":
                    if not self.match(";"):
                        self.ERROR_terminating_token(";")

        
    def imports_list(self):
        print("(parser) production: \"imports_list\" detected")
        """<imports_list> → import <iostar>;<imports_rec>"""

        if not self.match("import"):
            self.ERROR_expected_token("import")

        if not self.match("<"):
            self.ERROR_expected_token("<")

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

        if not self.match("import"):
            self.ERROR_expected_token("import")

        if not self.match("<"):
            self.ERROR_expected_token("<")

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
            if self.currToken["tokenType"] == "private" or self.currToken["tokenType"] == "class":
                self.class_declaration()

            elif self.currToken["tokenType"] == "const":
                self.var_dec()

            elif self.currToken["tokenType"] == "void":
                self.function_dec()

            elif self.currToken["tokenType"] == "int": #check for int main()
                self.match("int")
                if self.currToken and self.currToken["tokenName"] == "main":
                    self.match("Identifier")
                    if self.currToken and self.currToken["tokenType"] == "(":
                        self.hasMainFunction = True  # Found main function
                        print("(parser) production: #### entering main function")
                    elif self.currToken and self.currToken["tokenType"] == "=":
                        self.var_dec()
                    else:
                        self.ERROR_expected_token(["(","="])
                else:
                    if self.currToken:
                        if not self.match("Identifier"):
                            self.ERROR_expected_Identifier()
        
                        if self.currToken and self.currToken["tokenType"] == "(": # int Identifier(
                            self.function_dec()

                        elif self.currToken and self.currToken["tokenType"] == "=": # int Identifier =
                            self.var_dec()

                        else:
                            self.ERROR_expected_token(["(","="])
                    else:
                        self.logError("Expected a variable declaration, function declaration, or main function.")


            elif self.currToken["tokenType"] == "Identifier":
                self.class_inst()

            elif self.currToken["tokenType"] in PREDICT_SETS["data_types"]:  # sample of custom error not using matchPredictSet
                self.nextToken()
                if self.match("Identifier"): 
                    if self.currToken and self.currToken["tokenType"] == "(":
                        self.function_dec()
                    elif self.currToken and self.currToken["tokenType"] == "=":
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

        if not self.match("class"):
            self.ERROR_expected_token("class")

        if self.currToken and self.currToken["tokenType"] == "Identifier":
            self.classNames.append(self.currToken["tokenName"])      # handles constructor name logic of recursive classes within classes
            self.match("Identifier")
        else:
            self.ERROR_expected_Identifier()
        
        if not self.match("{"):
            self.ERROR_expected_token("{")

        self.class_body()
        self.match("}")

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

            ############# ID MODS HERE

        
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

        if not self.match("("):
            self.ERROR_expected_token("(")
            
        self.params_dec() ############### PARAM RULES HERE
        
        if not self.match(")"):
            self.ERROR_unclosed_parentheses()

        if not self.match("{"):
            self.ERROR_expected_token("{")

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
        print("(parser) production: \"class_inst\" detected")

        # Parse the first Identifier (class name or type)
        if not self.match("Identifier"):
            self.logError("Expected an identifier for class instantiation.")  # MICH CURRENTLY DOING
            # This error is just a placeholder habang wala pang semantic, cos normally it should identify if existing na ung class

        
        # Parse the second Identifier (variable name)
        if self.currToken and not self.match("Identifier"):
            self.ERROR_missing_initializer() 
            

        # # Handle <classinst_cont>
        # if self.currToken and self.currToken["tokenType"] == "=":
        #     self.match("=")
        #     if not self.match("Identifier"):
        #         self.logError(" ") ################################################
            
        #     # (  )   self.func_arg()  # Handle (<func_arg>)

        # elif self.currToken and self.currToken["tokenType"] == "[":################################################
        #     self.match("[")
        #     self.int_val()  # Parse <int_val> ################################################

        #     if not self.match("]"):
        #         self.ERROR_unclosed_square_bracket()

        #     self.classinst_def_1Drec_arr()  # Handle <classinst_def_1Drec_arr> ################################################

        # else:
        #     # Handle λ (no additional tokens after the second identifier) ################################################
        #     pass


        # Match the semicolon at the end
        if not self.match(";"):
            self.ERROR_terminating_token(";")

        # Continue parsing program constructs
        self.program_constructs()


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
            if not self.match("{"):
                self.ERROR_expected_token("{")

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
    
    
    def output(self):
        '''<output> → <print_stmts>(<print_params>);'''
        print("(parser) entered production: \"output\"")
        
        '''<print_stmts> → print | println'''
        # <print_stmts> are already expected to be here before it entered func
        self.nextToken()
        self.match("(", False)
        self.print_params()
        if not self.match(")"): 
            self.ERROR_unclosed_parentheses()
        if not self.match(";"): 
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"output\"")


    def print_params(self):
        '''<print_params> → <value> <output_rec> | null'''
        print("(parser) entered production: \"print_params\"")
        
        # if <print_params> are not null
        if self.currToken and self.currToken["tokenType"] != ")":
            ## <value> here (string_lit for now)
            self.match("string_lit", False)
            if self.currToken and self.currToken["tokenType"] == ",":
                self.output_rec()
        
        print("(parser) exited production: \"print_params\"")

    
    def output_rec(self):
        '''<output_rec> → ,<value> <output_rec> | null'''
        print("(parser) entered production: \"output_rec\"")
        
        self.match(",", False)
        ## <value> cannot be empty
        ## <value> here (string_lit for now)
        if not self.match("string_lit", False):
            self
        if self.currToken and self.currToken["tokenType"] == ",":
            self.output_rec()

        print("(parser) entered production: \"output_rec\"")
    
    
    def conditional_stmt(self):
        '''<conditional_stmt> → <if_stmt> | <swicth_stmt>'''
        print("(parser) entered production: \"conditional_stmt\"")

        if self.currToken and self.currToken["tokenType"] == "if":
            self.if_stmt()
        elif self.currToken and self.currToken["tokenType"] == "switch":
            self.switch_stmt()

        print("(parser) exited production: \"conditional_stmt\"")
    
    
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
            self.matchPredictSet("literals")
            self.nextToken() 

        print("(parser) exited production: \"ret_value\"")


    def break_stmt(self):
        '''<break_stmt> → break;'''
        print("(parser) entered production: \"break_stmt\"")

        self.match("break", False)
        if not self.match(";"):
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"break_stmt\"")

    def continue_stmt(self):
        '''<continue_stmt> → continue;'''
        print("(parser) entered production: \"continue_stmt\"")

        self.match("continue", False)
        if not self.match(";"):
            self.ERROR_terminating_token(";")

        print("(parser) exited production: \"continue_stmt\"")


    def init_arg(self):
        '''<init_arg> → <for_init_data_type> Identifier = <value> <assign_stmt_rec> <var_iden_rec> | null'''
        '''<for_init_data_type> → <data_type> | null'''
        print("(parser) entered production: \"init_arg\"")

        if self.currToken["tokenName"] in PREDICT_SETS["data_types"]:
            self.nextToken()
        self.match("Identifier", False)
        self.match("=", False)
        # <value> here (literals for now)
        if self.currToken["tokenName"] in PREDICT_SETS["literals"]:
            self.nextToken()
        #self.assign_stmt_rec()
        #self.var_iden_rec()

        print("(parser) exited production: \"init_arg\"")


    def inc_arg(self):
        '''<inc_arg> → <unary_exp> | Identifier = <value> <assign_stmt_rec> <var_iden_rec> 
        | <output> | <func_method_call>'''
        print("(parser) entered production: \"inc_arg\"")
        
        if self.currToken["tokenName"] in PREDICT_SETS["unary_operator"]:
            print("(parser) entered production: \"unary_exp\"")
            #self.unary_exp()
            print("(parser) exited production: \"unary_exp\"")
        
        elif self.currToken and self.currToken["tokenType"] == "Identifier":
            if self.peek() in PREDICT_SETS["unary_operator"]:
                print("(parser) entered production: \"unary_exp\"")
                #self.unary_exp()
                print("(parser) exited production: \"unary_exp\"")
                
            elif self.peek() == "(":
                print("(parser) entered production: \"func_method_call\"")
                #self.func_method_call()
                print("(parser) exited production: \"func_method_call\"")
                
            elif self.peek() == "=":
                self.match("Identifier", False)
                self.match("=", False)
                # <value> here (literals for now)
                if self.matchPredictSet("literals"):
                    self.nextToken()
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
        
    
    def switch_stmt(self):
        '''<switch_stmt> → switch (<switch_value>) {<case_stmt> <default_stmt>}'''
        print("(parser) entered production: \"switch_stmt\"")

        self.match("switch", False)
        if self.currToken and self.currToken["tokenType"] == "{":
            self.ERROR_missing_condition("switch")
        self.match("(", False)
        
        if self.matchPredictSet("switch_value"):
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
                    elif x == ("whole_lit" or "Identifier"):
                        print("(parser) entered production: \"arith_exp\"")
                        #self.arith_exp()
                        print("(parser) exited production: \"arith_exp\"")
                    else:
                        self.logError("Invalid value for 'switch' statement.")
       
        else:
            self.logError("'switch' condition cannot be empty.")
    
        print("(parser) exited production: \"switch_value\"")

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

    
    def default_stmt(self):
        self.match("default", False)
        self.match(":", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
            self.ctrl_stmt_body()
    
    def loop_stmt(self):
        if self.currToken and self.currToken["tokenType"] == "while":
            self.while_stmt()
        elif self.currToken and self.currToken["tokenType"] == "do": 
            self.do_stmt()
        elif self.currToken and self.currToken["tokenType"] == "for":
            self.forloop_stmt()
        elif self.currToken and self.currToken["tokenType"] == "repeat":
            self.repeat_stmt()
    
    def forloop_stmt(self):
        self.match("for", False)
        self.match("(", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["init_arg"]:
            self.init_arg()
        if not self.match(";"):
            self.ERROR_terminating_token(";")
        
        self.condition()
        if not self.match(";"):
            self.ERROR_terminating_token(";")
        
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["inc_arg"]:
            self.inc_arg()
        
        if not self.match(")"):
            self.ERROR_unclosed_parentheses()
    
    def while_stmt(self):
        self.match("while", False)
        
        self.match("(", False)
        self.condition()
        if not self.match(")"):
            self.ERROR_unclosed_parentheses()
        
        self.match("{", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
            self.ctrl_stmt_body()
        if not self.match("}"):
            self.ERROR_unclosed_curly_braces()

    def do_stmt(self):
        self.match("do", False)
        
        self.match("{", False)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["ctrl_stmt_body"]:
            self.ctrl_stmt_body()
        if not self.match("}"):
            self.ERROR_unclosed_curly_braces()
        
        if not self.match("while"):
            self.logError("'do' statement must include 'while' condition.")
        self.match("(", False)
        self.condition()
        if not self.match(")"):
            self.ERROR_unclosed_parentheses()
        if not self.match(";"):
            self.ERROR_terminating_token(";")

    def repeat_stmt(self):
        self.match("repeat", False)
        self.match("(", False)
        # <int_value> here (whole_lit for now)
        #self.int_val()
        self.match("whole_lit", False)
        if not self.match(")"):
            self.ERROR_unclosed_parentheses()
    
    def return_block(self):
        self.match("return", False)
        # <ret_value> here, (literals for now)
        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["literals"]:
            self.ret_value()
        if not self.match(";"):
            self.ERROR_terminating_token(";")
    
    def ctrl_stmt_body(self):
        if self.currToken and self.currToken["tokenType"] == "break":
            self.break_stmt()
        elif self.currToken and self.currToken["tokenType"] == "continue":
            self.continue_stmt()
        #elif self.currToken and self.currToken["tokenType"] in PREDICT_SETS["body"]:
        #self.body()