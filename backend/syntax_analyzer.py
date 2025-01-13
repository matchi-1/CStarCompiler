#---PARSER---
class SyntaxAnalyzer:
    # Takes tokens, initializes current token and its index
    def __init__(self, tokens):
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

    # Advancer for the next token
    def nextToken(self):
        self.currToken_index += 1
        # Checks if there are still tokens
        if self.currToken_index < len(self.tokens):
            self.currToken = self.tokens[self.currToken_index]
        else:
            self.currToken = None

    # If current token type matches the expected token type, advances to the next token
    def terminal(self, expected_type):
        if self.currToken is not None and self.currToken["tokenType"] == expected_type: ##TODO
            self.nextToken()
        else:
            # Incomplete Token Error
            if self.currToken is None: self.unexpectedEnd(expected_type)
            # Unexpected Token Error
            else: self.unexpectedToken(expected_type)

    # SYNTAX ERRORS
    # !!!! TODO: add pointers to errors 
    def unexpectedEnd(self, expected_type):
        errorType = "Unexpected end"
        currToken = self.tokens[self.currToken_index - 1]
        currLine = currToken["tokenLine"]
        currCol = currToken["tokenCol"]
        message = f"\n\tSyntax Error: {errorType} at line {currLine}, column {currCol}" + "\n\tExpected: '{}'\n".format(expected_type)
        self.errors.append(message)
        raise SyntaxError(message)

    def unexpectedToken(self, expected_type):
        errorType = "Unexpected token"
        currToken = self.currToken["tokenName"]
        currLine = self.currToken["tokenLine"]
        currCol = self.currToken["tokenCol"]
        message = f"\n\tSyntax Error: {errorType} '{currToken}' at line {currLine}, column {currCol}" + "\n\tExpected: '{}'\n".format(expected_type)
        self.errors.append(message) 
        raise SyntaxError(message)
        # lineContent = TBC LOL I'm thinking of extracting the line from the code using currCol and line[0] to line[currLine]
        # return generateError(errorType, currToken, currLine, currCol)

    # PARSER
    def parse(self):
        #print(self.tokens)
        try:
            self.program()
            print("Parsing completed successfully.")
        except SyntaxError as e:
            print(f"Parsing incomplete with error/s: {e}")

    # BARE-MINIMUM ONLY for testing, will be edited during finalization
    def program(self):
        """<program> → int main(){return 0;}"""
        self.terminal("int")
        self.terminal("Identifier")
        self.terminal("(")
        self.terminal(")")
        self.terminal("{")
        self.terminal("return")
        self.terminal("whole_lit")
        self.terminal(";")
        self.terminal("}")
        print("(parser) production: \"program\" detected")