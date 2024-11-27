from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # cross-origin requests

#---DEFINITIONS---
type_iden_delim = [')', ' ', '\n']
alphabetic_chars = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]
newline_delim = [' ', '\n']
iden_delim = ['"',',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '.', '|', '(', ')', '[', ']', '?', ':', ';'] + newline_delim
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphanumeric = alphabetic_chars + numbers
NULL = ''

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
    tokens = [] #tokens dict [token:tokenType]
    errors = [] #NOTE: CANNOT!! BE DICT, IT PREVENTS DUPLICATES (it slipped my mind :sob:)
    currToken = ''
    currState = 's0'

    for i in range(len(code)): #need index for fuckery later
        print('(dbg) state: ', currState)
        print('(dbg) ', code[i])
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