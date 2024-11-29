from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # cross-origin requests

#---DEFINITIONS---
NULL = ''
whitespace = [' ']

 # alphabet characters
alpha_small = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
"n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
alpha_capital = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
"N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
alphabetic_chars = alpha_small+alpha_capital

# numbers
zero = ['0']
digit = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
numbers = zero + digit

# alphanum and special symbols
alphanumeric = alphabetic_chars + numbers
punc_symbols = ['@', '#', '$', '^', '"',',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '.', '|', '(', ')', '[', ']', '?', ':', ';']
escape_seq = ['\'', '\"', '\\', '\t', '\b', '\n']
format_spec = ['%c', '%s', '%d', '%ld', '%f', '%lf']
ascii = alphanumeric+punc_symbols

# data types
data_type = ['int', 'bool', 'string', 'float', 'double', 'char', 'long', 'void']

# operators
arithmetic_operator = ['+', '-', '*', '/', '%']
relational_operator = ['>', '<', '==', '<=', '>=', '!=']
logical_operator = ['!', '&&', '||']
unary_operator = ['++', '-']
assignment_operator = ['=', '+=', '-=', '*=', '/=']

# others
boolean = ['true', 'false']
comment = ['//', '/*', '*/']

#---DELIMETERS---
# escape sequence delim
newline = ['\n']

# reserved symbols delim
plaintext_delim = whitespace + alphanumeric
equal_delim = whitespace + ['=']
arithmetic_delim = plaintext_delim + ['(']
str_lit_delim = whitespace + ['+', ')', ',', ';']
newline_delim = [' ', '\n']
index_delim = [']'] + digit
default_delim = newline_delim + [':']
type_iden_delim = [')', ' ', '\n']
get_set_delim = newline_delim + ['{', ';']

# identifier delim
iden_delim = ['"',',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '.', '|', '(', ')', '[', ']', '?', ':', ';'] + newline_delim
closing_delim = arithmetic_operator + relational_operator + whitespace + ['&', '|']

# literals delim
num_delim = arithmetic_operator + whitespace + relational_operator + [',', ')', ']', '}', '=']
string_delim = newline_delim + ['+', ';']
bool_delim = whitespace + logical_operator + [';', ',', ')', '=', '!']

# control flow delim
loop_delim = newline_delim+['(']
block_delim = newline_delim+['{']

# methods delim
func_delim = newline_delim + ['(']

# other delim
single_delim = newline
comment_delim = ascii + whitespace


#---TOKEN STATES---
data_type = ['BOOL_CHECK', 'CHAR_CHECK', 'DOUBLE_CHECK', 'FLOAT_CHECK', 'INT_CHECK', 'LONG_CHECK', 'STRING_CHECK']
builtin_func = ['ABS_CHECK', 'ARR_FORITEMS_CHECK', 'ARR_LENGTH_CHECK']
#---GRAPH TRANSITIONS---
transitions = {
    's0':{
	  'a':'s1',
        'b':'s24',
        'c':'s34',
        'd':'s97',
        'f':'s117',
        'i':'s138',
        'l':'s155',
        's':'s233'
    },
    's1':{
        'b':'s2',
	  'r':'s5'
    },
    's2':{
        's':'ABS_CHECK'
    },
    's5':{
        'r':'s6'
    },
    's6':{
        '_':'s7'
    },
    's7':{
        'f':'s8',
        'l':'s17'
    },
    's8':{
        'o':'s9'
    },
    's9':{
        'r':'s10'
    },
    's10':{
        'I':'s11'
    },
    's11':{
        't':'s12'
    },
    's12':{
        'e':'s13'
    },
    's13':{
        'm':'s14'
    },
    's14':{
        's':'ARR_FORITEMS_CHECK'
    },
    's17':{
        'e':'s18'
    },
    's18':{
        'n':'s19'
    },
    's19':{
        'g':'s20'
    },
    's20':{
        't':'s21'
    },
    's21':{
        'h':'ARR_LENGTH_CHECK'
    },
    's24':{
        'o':'s25',
        'r':'s29'
    },
    's25':{
        'o':'s26'
    },
    's26':{
        'l':'BOOL_CHECK'
    },
    's29':{
        'e':'s30'
    },
    's30':{
        'a':'s31'
    },
    's31':{
        'k':'BREAK_CHECK'
    },
    's34':{
        'h':'s43'
    },
    's43':{
        'a':'s44'
    },
    's44':{
        'r':'CHAR_CHECK'  
    },
    's97':{
        'o':'s105'
    },
    's105':{
        'u':'s107'
    },
    's107':{
        'b':'s108'
    },
    's108':{
        'l':'s109'
    },
    's109':{
        'e':'DOUBLE_CHECK'  
    },
    's117':{
        'l':'s123'
    },
    's123':{
        'o':'s124'
    },
    's124':{
        'a':'s125'
    },
    's125':{
        't':'FLOAT_CHECK'
    },
    's138':{
        'n':'s147'
    },
    's147':{
        't':'INT_CHECK'
    },
    's155':{
        'o':'s156'
    },
    's156':{
        'n':'s157'
    },'s157':{
        'g':'LONG_CHECK'
    },
    's233':{
        't':'s241'
    },
    's241':{
        'r':'s247'
    },
    's247':{
        'i':'s308'
    },
    's308':{
        'n':'s309'
    },
    's309':{
        'g':'STRING_CHECK'
    },
    's421':{
        '_':'s421'
        # HELPER: alphanumeric:s421
    }
}

#---GRAPH HELPERS---
#s421 -alphanumeric> s421
for i in alphanumeric:
    transitions['s421'][i] = 's421'

#---TOKEN EXTRACTION AND CLASSIFICATION---\
def lexer(code):
    code = code.replace('\r\n', '\n')
    for char in code:
        print(f'(debug) {char} : {ord(char)}')
    tokens = [] #will hold token, tokentype tuple
    errors = [] #whill hold strings of error msges
    currToken = ''
    currState = 's0'
    lineContent = ''
    currLine = 1
    currCol = 1
    for i in range(len(code)): #need index for fuckery later
        print('(dbg) ---NEW CHAR---')
        print('(dbg) state: ', currState)
        print('(dbg) ', code[i])
        print('(dbg) ascii: ', ord(code[i]))
        #update line and col
        if (code[i] == '\n'): 
            currLine += 1
            currCol = 1
            lineContent = ''
        else:
            currCol += 1
            lineContent += code[i]
        #if no transitions, it means it's time for delim checking
        if (currState not in transitions):
            #data type keywords
            if (currState in data_type):
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, '<data_type>'))
                    currToken = ''
                    currState = 's0'
                    continue
                elif (code[i] in alphanumeric or code[i] == '_'):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 420')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
                    continue
            #built-in funcs spit out as identifiers 
            if (currState in builtin_func):
                if (code[i] in func_delim):
                    tokens.append((currToken, 'Identifier'))
                    currToken = ''
                    currState = 's0'
                    continue
                elif (code[i] in alphanumeric or code[i] == '_'):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 420')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
                    continue
            #break statement
            if (currState in 'BREAK_CHECK'):
                if (code[i] in func_delim):
                    tokens.append((currToken, 'break'))
                    currToken = ''
                    currState = 's0'
                    continue
                elif (code[i] in alphanumeric or code[i] == '_'):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 420')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
                    continue
        #identifier state
        if (currState == 's421'):
            print('(dbg) in identifier check state now')
            if (code[i] in iden_delim):
                print('(dbg) correct delim')
                tokens.append((currToken, 'Identifier'))
                currToken = ''
                currState = 's0'
                continue
            elif (code[i] in alphanumeric or code[i] == '_'): #if not delim but still valid, keep looping
                    currToken += code[i]
                    print('(dbg) accepted for iden')
                    currState ='s421'
                    continue
            else:
                currToken += code[i]
                # errors.append((currToken, f'Lexical Error: In line {currLine}, column {currCol-len(currToken)}; Unexpected \'{code[i]}\' for \'{currToken[:-1]}\'')) #can be expanded with conditions to check what error
                errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                currToken = ''
                currState = 's0'
                continue
    
        #iterating through chars
        #check whitespaces
        if (code[i] == ' '):
            tokens.append(('\' \' ', 'Space'))
            continue
        if (code[i] == '\n'):
            tokens.append(('\\n', 'New line'))
            continue
        #check states
        if (code[i] in transitions[currState]):
            currToken += code[i]
            currState = transitions[currState][code[i]]
            continue
        else: #if not in s0 transitions assume identifier, go to state 420
            print("(dbg) entering s421")
            if (currState == 's0'):
                if (code[i] in alphabetic_chars or code[i] == '_'):
                    currToken += code[i]
                    currState = 's421'
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
                    continue
            else:
                if (code[i] in alphanumeric or code[i] == '_'):
                    currToken += code[i]
                    currState = 's421'
                    continue
                elif (code[i] in iden_delim): #check delim
                    tokens.append((currToken, 'Identifier'))
                    currToken = ''
                    currState = 's0'
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
                    continue
    
    lexerResults = [tokens, errors] 
    return lexerResults

#---LEXER HELPER---
def delimError(currToken, currLine, currCol, incorrectDelim, lineContent):
    errorMsg = f'Lexical Error ({currLine}, {currCol-len(currToken)}): Unexpected \'{incorrectDelim}\' for \'{currToken}\'\n' 
    errorMsg += lineContent +'\n'
    errorMsg += '_'*(currCol-len(currToken)-1) + '^'
    print("(debug) ", errorMsg)
    return errorMsg
def idenFirstError(currToken, currLine, currCol, lineContent):
    errorMsg = f'Lexical Error ({currLine}, {currCol-len(currToken)}): Identifier {currToken} must start with an alpha character\n'
    errorMsg += lineContent + '\n'
    errorMsg += '_'*(currCol-len(currToken)-1) + '^'
    print("(debug) ", errorMsg)
    return errorMsg
#---FLASK ROUTES---
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'})

@app.route('/api/compile', methods=['POST'])
def compile_code():
    data = request.json
    code = data.get('code', '')
    lexres = lexer(code)
    # print(lexres)
    return jsonify(lexres)

if __name__ == '__main__':
    app.run(debug=True) 