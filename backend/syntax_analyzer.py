import app

#---PARSER---
class SyntaxAnalyzer:
    # Takes tokens, initializes current token and its index
    def __init__(self, tokens):
        self.tokens = [token.to_dict() 
            for token in tokens 
            if token.token_type != "single_comment" or "multiline_comment"] # comments will be ignored by the parser
        self.currToken_index = 0
        self.currToken = self.tokens[self.currToken_index]
        self.synterror = False

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
        if self.currToken and self.currToken["tokenType"] == expected_type: ##TODO
            self.nextToken()
        else:
            # Unexpected Token Error
            self.unexpectedToken()

    # TODO: finalize error list
    def unexpectedToken(self):
        self.synterror = True 
        errorType = "Unexpected token"
        currToken = self.currToken["tokenName"]
        currLine = self.currToken["tokenLine"]
        currCol = self.currToken["tokenCol"]
        print("Syntax Error: ", errorType, currToken, currLine, currCol)
        # lineContent = TBC LOL I'm thinking of extracting the line from the code using currCol and line[0] to line[currLine]
        # return generateError(errorType, currToken, currLine, currCol)

    def parse(self):
        #print(self.tokens)
        self.program()

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