#-------------------- PREDICT SETS --------------------
PREDICT_SETS = {
    "imports_rec": ["import", "private", "class", "int", "long", "bool", "float", "double", "string", "const", "Identifier"],
    "imports_rec_values": ["Cmath", "Cstring", "Carray"]
}


DATATYPES = ["bool", "string", "int", "long", "double", "float"]

#-------------------- PARSER --------------------
class SyntaxAnalyzer:
    # Takes tokens, initializes current token and its index
    def __init__(self, tokens):
        self.errors = []
        self.tokens = [
            token.to_dict()
            for token in tokens
            if token.token_type not in ["single_comment", "multi-line comment"]
        ] # comments will be ignored by the parser
        
        if not self.tokens:
            message = "\n\tNo tokens to parse."
            self.errors.append(message)
            raise SyntaxError(message)

        self.currToken_index = 0
        self.currToken = self.tokens[self.currToken_index]

        self.lineContent = ''

    #-------------------- PARSER START --------------------
    def parse(self):
        #print(self.tokens)
        try:
            self.program()
            print("Parsing completed successfully.")
        except SyntaxError as e:
            print(f"Parsing incomplete with error/s: {e}")
        return self.errors

    #-------------------- HELPER FUNCTIONS --------------------
    # Advancer for the next token
    def nextToken(self):
        self.currToken_index += 1
        # Checks if there are still tokens
        if self.currToken_index < len(self.tokens):
            self.currToken = self.tokens[self.currToken_index]
        else:
            self.currToken = None

    # Checks if given token matches the expected token type, advances to the next token, else raises error
    def match(self, expected_token):
        if self.currToken is not None and self.currToken["tokenType"] == expected_token: ##TODO
            self.nextToken()
        else: 

            if self.currToken is None:  # EOF
                self.raiseError(expected_token, "Unexpected EOF")

            else: # Wrong token
                self.raiseError(expected_token, "Unexpected token")

    def matchPredictSet(self, non_terminal):
        if self.currToken is None:  # EOF
            self.raiseError("", "Unexpected EOF", PREDICT_SETS.get(non_terminal, []))
        expected_predict_set = PREDICT_SETS.get(non_terminal, [])
        if self.currToken["tokenType"] not in expected_predict_set:
            self.raiseError("", "Unexpected token", expected_predict_set)

            

    #-------------------- SYNTAX ERRORS --------------------
    # Current Syntax Errors:    
    #   - Unexpected EOF
    #   - Unexpected token
    #

    def raiseError(self, expected_token, error_type, expected_predict_set=[]):
        if not self.currToken:
            currToken = self.tokens[self.currToken_index - 1]
            currLine = currToken["tokenLine"]
            currCol = currToken["tokenCol"]
        else: 
            currToken = self.currToken["tokenName"]
            currLine = self.currToken["tokenLine"]
            currCol = self.currToken["tokenCol"]

        # Determine the expected message
        if expected_predict_set:
            # Format the list of expected tokens
            expected_tokens = ", ".join(f"'{token}'" for token in expected_predict_set)
            expected_message = f"{expected_tokens}"
        else:
            expected_message = f"'{expected_token}'"

        # Construct the error message
        message = (
            f"\n\tSyntax Error: {error_type}"
            + (f" '{currToken}'" if self.currToken else "")
            + f" at line {currLine}, column {currCol}"
            f"\n\tExpected: {expected_message}\n"
        )
        self.errors.append(message)
        raise SyntaxError(message)
        # lineContent = TBC LOL I'm thinking of extracting the line from the code using currCol and line[0] to line[currLine]
        # return generateError(errorType, currToken, currLine, currCol)


    #-------------------- CFG START --------------------
    def program(self):
        print("(parser) production: \"program\" detected")
        """<program> → <imports_list><program_constructs> int main(){ <main_body> return 0;}"""
        self.imports_list()
        print("(parser) production: ### after imports_list")
        self.matchPredictSet(PREDICT_imports_rec)
        self.program_constructs()
        print("(parser) production: ### after program_constructs")
        if self.currToken and self.currToken["tokenName"] == "main":
            self.match("Identifier")
            self.match("(")
            self.match(")")
            self.match("{")
            # self.main_body()
            self.match("return")
            self.match("whole_lit")
            self.match(";")
            self.match("}")
        else:
            if not self.currToken: self.raiseError("int main()", "Unexpected EOF")
       
    def imports_list(self):
        print("(parser) production: \"imports_list\" detected")
        """<imports_list> → import <iostar>;<imports_rec>"""
        self.match("import")
        self.match("<")
        if self.currToken and self.currToken["tokenName"] == "iostar":
            self.match("Identifier")  # iostar
        self.match(">")
        self.match(";")
        self.matchPredictSet("imports_rec")
        if self.currToken and self.currToken["tokenType"] == "import":
            self.imports_rec()

    def imports_rec(self):
        print("(parser) production: \"imports_rec\" detected")
        """<imports_rec> → import <<imports_rec_values>>;<imports_rec> | λ"""
        self.match("import")
        self.match("<")
        self.imports_rec_values()
        self.match(">")
        self.match(";")
        self.matchPredictSet("imports_rec")
        if self.currToken and self.currToken["tokenType"] == "import":
            self.imports_rec()

    def imports_rec_values(self):
        print("(parser) production: \"imports_rec_values\" detected")
        expected_predict_set = PREDICT_SETS["imports_rec_values"]
        if self.currToken["tokenName"] in expected_predict_set:
            self.std_lib()
        elif self.currToken and self.currToken["tokenType"] == "Identifier":
            self.match("Identifier")
            self.match(".")
            if self.currToken and self.currToken["tokenName"] == "cstr":
                self.match("Identifier")
            else:
                self.raiseError("cstr file", "Unexpected Token")
        else:
            self.raiseError("", "Unexpected Token", expected_predict_set + ["or cstr file"])


    def std_lib(self):
        print("(parser) production: \"std_lib\" detected")
        """<std_lib> → Cmath | Cstring | Carray"""
        if self.currToken["tokenName"] in {"Cmath", "Cstring", "Carray"}:
            self.nextToken()

    def program_constructs(self):
        print("(parser) production: \"program_constructs\" detected")
        while self.currToken:
            if self.currToken["tokenType"] == "private" or self.currToken["tokenType"] == "class":
                self.class_declaration()
            elif self.currToken["tokenType"] == "const":
                self.var_dec()
            elif self.currToken["tokenType"] == "void":
                self.function_dec()
            elif self.currToken["tokenType"] == "int":
                self.match("int")
                if self.currToken and self.currToken["tokenName"] == "main":
                    self.match("Identifier")
                    if self.currToken and self.currToken["tokenType"] == "(":
                        print("(parser) production: #### entering main function")
                        return
            else:
                self.matchPredictSet(DATATYPES)
                self.nextToken()
                self.match("Identifier")
                if self.currToken and self.currToken["tokenType"] == "(":
                    self.function_dec()
                elif self.currToken and self.currToken["tokenType"] == "=":
                    self.var_dec()
                else:
                    self.raiseError("", "Missing token", ["=", "("])

        
    def class_declaration(self):
        print("(parser) production: \"class_declaration\" detected")
        if self.currToken["tokenType"] == "private":
            self.match("private")
        self.match("class")
        self.match("Identifier")
        self.match("{")
        #self.class_body()
        self.match("}")
        self.match(";")

        self.program_constructs()

    def var_dec(self):
        print("(parser) production: \"var_dec\" detected")

        if self.currToken["tokenType"] != "=": # if not from second calling from program_construct
            if self.currToken["tokenType"] == "const":
                self.match("const")
            self.matchPredictSet(DATATYPES)
            self.nextToken()
            self.match("Identifier")
        
        ############# VAR ASSIGN RULES HERE
        self.match(";")
        self.program_constructs()

    def function_dec(self):
        print("(parser) production: \"function_dec\" detected")
        if self.currToken["tokenType"] == "void":
            self.match("void")
        else:
            self.matchPredictSet(DATATYPES)
            self.nextToken()
        self.match("Identifier")
        self.match("(")
        ############### PARAM RULES HERE
        self.match(")")
        self.match("{")
        ############### FUNCTION BODY RULES HERE
        self.match("}")
        self.program_constructs()