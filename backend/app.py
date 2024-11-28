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

#---GRAPH TRANSITIONS---
transitions = {
    's0':{
        'b':'s45',
        'c':'s55',
        'd':'s126',
        'f':'s155',
        'i':'s183',
        'l':'s200',
        's':'s297'
    },
    's45':{
        'o':'s46'
    },
    's46':{
        'o':'s47'
    },
    's47':{
        'l':'BOOL_CHECK'
    },
    's55':{
        'h':'s68'
    },
    's68':{
        'a':'s69'
    },
    's69':{
        'r':'CHAR_CHECK'  
    },
    's126':{
        'o':'s139'
    },
    's139':{
        'u':'s141'
    },
    's141':{
        'b':'s142'
    },
    's142':{
        'l':'s143'
    },
    's143':{
        'e':'DOUBLE_CHECK'  
    },
    's155':{
        'l':'s161'
    },
    's161':{
        'o':'s162'
    },
    's162':{
        'a':'s163'
    },
    's163':{
        't':'FLOAT_CHECK'
    },
    's183':{
        'n':'s192'
    },
    's192':{
        't':'INT_CHECK'
    },
    's200':{
        'o':'s201'
    },
    's201':{
        'n':'s202'
    },'s202':{
        'g':'LONG_CHECK'
    },
    's297':{
        't':'s305'
    },
    's305':{
        'r':'s311'
    },
    's311':{
        'i':'s372'
    },
    's372':{
        'n':'s373'
    },
    's373':{
        'g':'STRING_CHECK'
    },
    's420':{
        '_':'s420'
        # HELPER: alphanumeric:s420
    }
}

#---GRAPH HELPERS---
#s420 -alphanumeric> s420
for i in alphanumeric:
    transitions['s420'][i] = 's420'

#---TOKEN EXTRACTION AND CLASSIFICATION---
def extractTokens(code):
    code = code.replace('\r\n', '\n')
    for char in code:
        print(f'(debug) {char} : {ord(char)}')
    tokens = [] #tokens dict [token:tokenType]
    errors = [] #NOTE: CANNOT!! BE DICT, IT PREVENTS DUPLICATES (it slipped my mind :sob:)
    currToken = ''
    currState = 's0'

    for i in range(len(code)): #need index for fuckery later
        print('(dbg) state: ', currState)
        print('(dbg) ', code[i])
        print('(dbg) ascii: ', ord(code[i]))
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
                    currState ='s420'
                    print('(dbg) now in state 420')
                    continue
                else:
                    currToken += code[i]
                    errors.append((currToken, 'Incorrect delimiter'))
                    currToken = ''
                    currState = 's0'
                    continue

        #identifier state
        if (currState == 's420'):
            print('(dbg) in identifier check state now')
            if (code[i] in iden_delim):
                print('(dbg) correct delim')
                if (currToken[0] not in alphabetic_chars): #check first if first character is ok
                    errors.append((currToken, 'Identifier should start with alpha'))
                    currToken = ''
                    currState = 's0'
                    continue
                tokens.append((currToken, 'Identifier'))
                currToken = ''
                currState = 's0'
                continue
            elif (code[i] in alphanumeric or code[i] == '_'): #if not delim but still valid, keep looping
                    currToken += code[i]
                    currState ='s420'
                    continue
            else:
                currToken += code[i]
                errors.append((currToken, 'Incorrect delimiter')) #can be expanded with conditions to check what error
                currToken = ''
                currState = 's0'
                continue
    
        #iterating through chars
        if (code[i] == ' ' or code[i] == '\n'):
            continue
        if (code[i] in transitions[currState]):
            currToken += code[i]
            currState = transitions[currState][code[i]]
        else: #if not in s0 transitions assume identifier, go to state 420
            currToken += code[i]
            currState = 's420'
    
    lexerResults = [tokens, errors] 
    return lexerResults

#---FLASK ROUTES---
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'})

@app.route('/api/compile', methods=['POST'])
def compile_code():
    data = request.json
    code = data.get('code', '')
    lexres = extractTokens(code)
    # print(lexres)
    return jsonify(lexres)

if __name__ == '__main__':
    app.run(debug=True)