#-------------------- PREDICT SETS --------------------
PREDICT_SETS = {
    "imports_rec": ["import", "private", "class", "int", "long", "bool", "float", "double", "string", "const", "void", "Identifier"],
    "std_lib": ["Cmath", "Cstring", "Carray"],
    "program_constructs": ["private", "class", "int", "long", "bool", "float", "double", "string", "const", "void", "Identifier"],
    "data_types": ["bool", "string", "int", "long", "double", "float"],
    "class_body": [ "private" ,'static', "const", "int", "long", "bool", "float", "double", "string", "Identifier" , "private", "class", "}"]
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
        self.classNames = []
        self.inClassBody = False
        self.inConstructor = False
        self.errors = []
        self.tokens = [token.to_dict() 
            for token in tokens 
            if token.token_type != "single_comment" or "multi-line comment"] # comments will be ignored by the parser
        
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
        #print(self.tokens)
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
    def match(self, expected_token):
        if self.currToken is not None and self.currToken["tokenType"] == expected_token:
            self.nextToken()
            return True
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
                    self.match("(")
                    if not self.match(")"):
                        self.ERROR_expected_token(")")

                    if self.match("{"):
                        print("(parser) production: ### inside main")
                    else:
                        self.ERROR_expected_token("{")

                    if not self.match("return"):
                        self.ERROR_expected_token("return")

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
    def var_dec(self):
        print("(parser) production: \"var_dec\" detected")

        if self.currToken and self.currToken["tokenType"] != "=": # if not from second calling from program_construct
            if self.currToken["tokenType"] == "const":
                self.match("const")
            self.matchPredictSet("data_types")
            self.nextToken()
            if not self.match("Identifier"):
                self.ERROR_expected_Identifier()

        
        if not self.match("="):
            self.ERROR_expected_token("=")
        ############# VAR ASSIGN RULES HERE
        if not self.match(";"): 
            self.logError("error expected ';', this error only placeholder because no logic pa")
            self.ERROR_expected_token(";")
        
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
            
        ############### PARAM RULES HERE
        if not self.match(")"):
            self.ERROR_unclosed_parentheses()

        if not self.match("{"):
            self.ERROR_expected_token("{")

        ############### FUNCTION BODY RULES HERE
        if isNotVoid and not self.inConstructor:
            if not self.match("return"):
                self.logError("Non-void functions must have return statement.")
            ### uhmmm how to check return type and if it matches return statement?

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
        if self.currToken and self.currToken["tokenType"] == "private":
            self.match("private")
            if self.currToken["tokenType"] != "static" and self.currToken["tokenType"] != "Identifier" or not self.currToken and self.currToken["tokenType"] != "class":
                self.logError("Expected Identifier, token 'class', or token 'static'.")
        
        if self.currToken and self.currToken["tokenType"] == "class":
            self.class_declaration()
            #also goes back to program_constructs, it really shouldnt

    
        if self.currToken and self.currToken["tokenType"] == "static":
            self.match("static")
            self.var_dec()      #attribute dec equivaelnt

        if self.currToken and self.currToken["tokenType"] in PREDICT_SETS["data_types"]: #attribute or method path
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

        if self.currToken and self.currToken["tokenType"] == "Identifier": #for constructor path
            if self.currToken["tokenName"] == self.classNames[-1]:
                self.match("Identifier")
                self.classNames.pop()
                if self.currToken and self.currToken["tokenType"] == "(":
                    self.inConstructor = True
                    self.function_dec() #maybe revisit in da future
                                        
                else:
                    self.ERROR_expected_token("(")
            else:
                self.logError("Expected data type or access modifier ('private' or 'static'). Constructors must have the same name as its class.") 
                #???? placeholder
        
        if self.currToken and self.currToken["tokenType"] != "}":
            self.class_body()

        if not self.currToken:
            self.ERROR_unclosed_curly_braces()
