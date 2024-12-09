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
escape_seq = ['\\\'', '\\\"', '\\\\', '\\t', '\\b', '\\n']
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
arithmetic_delim = plaintext_delim + ['(', '+', '-']
str_lit_delim = whitespace + ['+', ')', ',', ';']
newline_delim = [' ', '\n']
index_delim = [']'] + digit
default_delim = whitespace + newline_delim + [':']
type_iden_delim = [')', ' ', '\n', '>', '[']
get_set_delim = newline_delim + ['{', ';']

# identifier delim
iden_delim = ['"',',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '.', '|', '(', ')', '[', ']', '?', ':', ';'] + newline_delim
closing_delim = arithmetic_operator + relational_operator + whitespace + logical_operator + assignment_operator + ['&', '|', '{', '(', ')', ';', '\n', ',']

# literals delim
num_delim = arithmetic_operator + whitespace + relational_operator + [',', ')', ']', '}', '=', ';'] + newline
string_delim = newline_delim + ['+', ';']
bool_delim = whitespace + logical_operator + [';', ',', ')', '=', '!']

# control flow delim
loop_delim = newline_delim+ whitespace + ['(']
block_delim = newline_delim+whitespace+['{']

# methods delim
func_delim = newline_delim + ['(']

# other delim
single_delim = newline
comment_delim = ascii + whitespace


#---TOKEN STATES---
builtin_func = ['ABS_CHECK', 'ARR_FORITEMS_CHECK', 'ARR_LENGTH_CHECK', 'CEIL_CHECK', 'CHR_TOLOWER_CHECK', 'CHR_TOUPPER_CHECK', 'CHR_ISALPHA_CHECK', 'CHR_ISALPHANUM_CHECK', 'CHR_ISDIGIT_CHECK', 'FLOOR_CHECK', 'MAX_CHECK', 'MEAN_CHECK', 'MEDIAN_CHECK', 'MIN_CHECK', 'MODE_CHECK', 'RANDDOUBLE_CHECK', 'RANDFLOAT_CHECK', 'RANDINT_CHECK', 'SQRT_CHECK', 'STR_ISEMPTY_CHECK', 'STR_LENGTH_CHECK', 'STR_POPALPHA_CHECK', 'STR_POPDIGITS_CHECK', 'STR_POPSPECIAL_CHECK', 'STR_SLICE_CHECK', 'STR_TOLOWER_CHECK', 'STR_TOUPPER_CHECK', 'TRUNC_CHECK']
#---GRAPH TRANSITIONS---
transitions = {
    's0':{
        'b':'s1',
        'c':'s11',
        'd':'s36',
        'e':'s51',
        'f':'s56',
        'g':'s70',
        'i':'s74',
        'l':'s91',
        'p':'s96',
	    'r':'s117',
        's':'s129',
        't':'s150', 
        'v':'s159',
        'w':'s164', 
	    '-':'DASH_CHECK', #s170
        '!':'NEGATION_CHECK', #s176
        '%':'MODULO_CHECK', #180
        '&':'s184',
        '(':'OPEN_PAREN_CHECK',
        ')':'CLOSING_PAREN_CHECK',
        '*':'ASTERISK_CHECK', #s191
        ',':'COMMA_CHECK',
        '.':'DOT_CHECK', #s264
        '/':'SLASH_CHECK', #s201
        ';':'SEMICOLON_CHECK',
        '?':'QUESTION_CHECK',
        ':':'COLON_CHECK',
        '[':'OPEN_BRACKET_CHECK',
        ']':'CLOSING_BRACKET_CHECK',
        '{':'OPEN_CURLY_CHECK',
        '}':'CLOSING_CURLY_CHECK',
        '|':'s223',
        '\"':'s258', #start string loop
        '+':'PLUS_CHECK', #s230
        '<':'OPEN_ANGLE_CHECK', #s236
        '>':'CLOSING_ANGLE_CHECK', #s240
        '=':'ASSIGN_CHECK', #s244
        '\'':'s261' #char checking
    },
    's1':{
        'o':'s2',
	    'r':'s6'
    },
    's2':{
        'o':'s3'
    },
    's3':{
        'l':'BOOL_CHECK'
    },
    's5':{
        'r':'s6'
    },
    's6':{
        'e':'s7'
    },
    's7':{
        'a':'s8',
    },
    's8':{
        'k':'BREAK_CHECK'
    },
    's9':{
        'r':'s10'
    },
    's10':{
        'I':'s11'
    },
    's11':{
        'a':'s12',
        'h':'s16',
        'l':'s20',
        'o':'s25'
    },
    's12':{
        's':'s13'
    },
    's13':{
        'e':'CASE_CHECK'
    },
    's16':{
        'a':'s17'
    },
    's17':{
        'r':'CHAR_CHECK'
    },
    's20':{
        'a':'s21'
    },
    's21':{
        's':'s22'
    },
    's22':{
        's':'CLASS_CHECK'
    },
    's25':{
        'n':'s26'
    },
    's26':{
        't':'s27',
        's':'s33'
    },
    's27':{
        'i':'s28'
    },
    's28':{
        'n':'s29'
    },
    's29':{
        'u':'s30'
    },
    's30':{
        'e':'CONTINUE_CHECK'
    },
    's33':{
        't':'CONST_CHECK'
    },
    's36':{
	  'e':'s37', #s37
      'o':'DO_CHECK' #s44
    },
    's37':{
        'f':'s38'
    },
    's38':{
        'a':'s39'
    },
    's39':{
        'u':'s40'
    },
    's40':{
        'l':'s41'
    },
    's41':{
        't':'DEFAULT_CHECK'
    },
    's44':{
        'u':'s46' 
    },
    's46':{
        'b':'s47'
    },
    's47':{
        'l':'s48'
    },
    's48':{
        'e':'DOUBLE_CHECK'
    },
    's51':{
        'l':'s52'
    },
    's52':{
        's':'s53'
    },
    's53':{
        'e':'ELSE_CHECK'
    },
    's56':{
        'a':'s57',
        'l':'s62',
        'o':'s67'
    },
    's57':{
        'l':'s58'
    },
    's58':{
        's':'s58'
    },
    's59':{
        'e':'FALSE_CHECK'
    },
    's62':{
        'o':'s63'
    },
    's63':{
        'a':'s64',
    },
    's64':{
        't':'FLOAT_CHECK' 
    },
    's67':{
        'r':'FOR_CHECK'
    },
    's70':{
        'e':'s71' 
    },
    's71':{
        't':'GET_CHECK' 
    },
    's74':{
        'f':'IF_CHECK', 
        'm':'s77',
        'n':'IN_CHECK', #s83
        't':'s87' 
    },
    's77':{
        'p':'s78' 
    },
    's78':{
        'o':'s79' 
    },
    's79':{
        'r':'s80' 
    },
    's80':{
        't':'IMPORT_CHECK'  
    },
    's83':{
        't':'INT_CHECK'
    },
    's87':{
        'e':'s88'
    },
    's88':{
        'm':'ITEM_CHECK' 
    },
    's91':{
        'o':'s92'
    },
    's92':{
        'n':'s93'
    },
    's93':{
        'g':'LONG_CHECK' 
    },
    's96':{
        'r':'s97'
    },
    's97':{
        'i':'s98',
        'o':'s110'
    },
    's98':{
        'n':'s99',
	    'v':'s105'
    },
    's99':{
        't':'PRINT_CHECK', #100
    },
    's100':{
        'l':'s102'
    },
    's102':{
        'n':'PRINTLN_CHECK'
    },
    's105':{
        'a':'s106'
    },
    's106':{
        't':'s107'
    },
    's107':{
        'e':'PRIVATE_CHECK'
    },
    's110':{
        'p':'s111'
    },
    's111':{
        'e':'s112'
    },
    's112':{
        'r':'s113'
    },
    's113':{
        't':'s114'
    },
    's114':{
        'y':'PROPERTY_CHECK'
    },
    's117':{
        'e':'s118'
    },
    's118':{
        'p':'s119',
        't':'s124'
    },
    's119':{
        'e':'s120'
    },
    's120':{
        'a':'s121'
    },
    's121':{
        't':'REPEAT_CHECK'
    },
    's124':{
        'u':'s125'
    },
    's125':{
        'r':'s126'
    },
    's126':{
        'n':'RETURN_CHECK'
    },
    's129':{
        'e':'s130',
        't':'s133',
        'w':'s144'
    },
    's130':{
        't':'SET_CHECK'
    },
    's133':{
        'a':'s134',
        'r':'s139'
    },
    's134':{
	  't':'s135'
    },
    's135':{
	  'i':'s136'
    },
    's136':{
	  'c':'STATIC_CHECK'
    },
    's139':{
        'i':'s140'
    },
    's140':{
        'n':'s141'
    },
    's141':{
        'g':'STRING_CHECK'
    },
    's144':{
        'i':'s145'
    },
    's145':{
        't':'s146'
    },
    's146':{
        'c':'s147'
    },
    's147':{
        'h':'SWITCH_CHECK'
    },
    's150':{
        'h':'s151',
        'r':'s155'
    },
    's151':{
        'i':'s152'
    },
    's152':{
        's':'THIS_CHECK'
    },
    's155':{
        'u':'s156'
    },
    's156':{
        'e':'TRUE_CHECK',
    },
    's159':{
        'o':'s160'
    },
    's160':{
        'i':'s161'
    },
    's161':{
        'd':'VOID_CHECK'
    },
    's164':{
        'h':'s165'
    },
    's165':{
        'i':'s166'
    },
    's166':{
        'l':'s167'
    },
    's167':{
        'e':'WHILE_CHECK'
    },
    's170':{
        '-':'DECREMENT_CHECK',
        '=':'MINUS_ASS_CHECK'
    },
    's178':{
        '=':'NOT_EQUAL_CHECK'
    },
    's180':{
        '=':'MODULO_ASS_CHECK'
    },
    's184':{
        '&':'LOGICAND_CHECK'
    },
    's191':{
        '=':'MULT_ASS_CHECK'
    },
    's201':{
        '*':'s254', #start mult comment loop
        '/':'s251', #start single comment loop
        '=':'DIV_ASS_CHECK'
    },
    's223':{
        '|':'LOGICOR_CHECK'
    },
    's230': {
        '+':'INCREMENT_CHECK',
        '=':'ADD_ASS_CHECK'
    },
    's236':{
        '=':'LESS_OR_EQUAL_CHECK'
    },
    's240':{
        '=':'GREATER_OR_EQUAL_CHECK'
    },
    's244':{
        '=':'EQUAL_CHECK'
    },
    
    's248':{
        '_':'s248'
        # HELPER: alphanumeric:'s248'
    },
    's251':{
        # HELPER: ascii:'s251'
    },
    's254':{
        '\n':'s254',
        '*':'s255'
        # HELPER: ascii:'s254'
    },
    's255':{
        '/':'MULTI_COMMENT_CHECK'
    },
    's258':{
        '"':'STRING_LIT_CHECK'
        # HELPER: ascii:'s258'
    },
    's261':{
        '\'':'CHAR_LIT_CHECK'
    },
    's264':{
        # HELPER: numbers:'s264'
    },
    's297':{
        '.':'s264'
        # HELPER: numbers: '470'
    }
}
#---GRAPH HELPERS---
#s248 -alphanumeric> s248
for i in alphanumeric:
    transitions['s248'][i] = 's248'
for i in ascii:
    transitions['s251'][i] = 's251'
    transitions['s254'][i] = 's254'
    #override for multiline comment
    transitions['s254']['*'] = 's255'
    transitions['s258'][i] = 's258'
    #overrde for string
    transitions['s258']['\"'] = 'STRING_LIT_CHECK'
for i in numbers:
    transitions['s264'][i] = 's264'
    transitions['s297'][i] = 's297'

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
    currWholeCount = 0
    currFracCount = 0
    print("(dbgl ----------SCAN START--------")
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
            print('(dbg) delim checking')
            #data type keywords
            if (currState == 'BOOL_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'bool'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            if (currState == 'CHAR_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'char'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            if (currState == 'DOUBLE_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'double'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            if (currState == 'FLOAT_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'float'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            if (currState == 'INT_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'int'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            if (currState == 'LONG_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'long'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            if (currState == 'STRING_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'string'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            #break statement
            if (currState == 'BREAK_CHECK'):
                expected = newline_delim + [';']
                if (code[i] in newline_delim + [';']):
                    tokens.append((currToken, 'break'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # ( symbol
            if (currState == 'OPEN_PAREN_CHECK'):
                expected = ['alphanumeric', ' ', '\"', '!', ')', '+', '-']
                if (code[i] in arithmetic_delim + ['\"', '!', ')']):
                    tokens.append((currToken, '('))
                    currToken = ''
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # ) symbol
            if (currState == 'CLOSING_PAREN_CHECK'):
                expected = closing_delim + [';']
                if (code[i] in closing_delim + [';']):
                    tokens.append((currToken, ')'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # ; symbol
            if (currState == 'SEMICOLON_CHECK'):
                expected = ['alphanumeric', ' ', '}'] + newline
                if (code[i] in plaintext_delim + newline + ['}']):
                    tokens.append((currToken, ';'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # - symbol
            if (currState == 'DASH_CHECK'):
                expected = ['alphanumeric', ' ', '(', '+', '-']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '-'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's170'
            # ! symbol
            if (currState == 'NEGATION_CHECK'):
                expected = ['alphabetic', '('] + whitespace 
                if (code[i] in whitespace + alphabetic_chars + ['(']):
                    tokens.append((currToken, '!'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's178'
            # % symbol
            if (currState == 'MODULO_CHECK'):
                expected = ['alphanumeric', ' ', '(', '+', '-']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '%'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's180'
            # ( symbol
            if (currState == 'OPEN_PAREN_CHECK'):
                expected = ['alphanumeric', ' ', '(', '\"', '!', ')', '+', '-']
                if (code[i] in arithmetic_delim + ['\"', '!', ')']):
                    tokens.append((currToken, '('))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # ) symbol
            if (currState == 'CLOSING_PAREN_CHECK'):
                expected = closing_delim
                if (code[i] in closing_delim + [';']):
                    tokens.append((currToken, ')'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # * symbol
            if (currState == 'ASTERISK_CHECK'):
                expected = ['alphanumeric', ' ', '(', '+', '-']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '%'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's191'
            # , symbol
            if (currState == 'COMMA_CHECK'):
                expected = ['alphanumeric', ' ']
                if (code[i] in plaintext_delim):
                    tokens.append((currToken, ','))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # . symbol
            if (currState == 'DOT_CHECK'):
                expected = ['alphabetic'] + whitespace
                if (code[i] in alphabetic_chars+whitespace):
                    tokens.append((currToken, '.'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's264'
            # / symbol
            if (currState == 'SLASH_CHECK'):
                expected = ['alphanumeric', ' ', '(', '+', '-']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '/'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's201'
            # ? symbol
            if (currState == 'QUESTION_CHECK'):
                expected = ['alphanumeric', '('] + newline
                if (code[i] in plaintext_delim + newline + ['(']):
                    tokens.append((currToken, '?'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # : symbol
            if (currState == 'COLON_CHECK'):
                expected = ['alphanumeric', '(', ' '] + newline
                if (code[i] in plaintext_delim + newline + ['(']):
                    tokens.append((currToken, ':'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's386'
            # [ symbol
            if (currState == 'OPEN_BRACKET_CHECK'):
                expected = ['alphanumeric', ']'] + whitespace
                if (code[i] in alphanumeric + whitespace + [']']):
                    tokens.append((currToken, '['))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # ] symbol
            if (currState == 'CLOSING_BRACKET_CHECK'):
                expected = iden_delim
                if (code[i] in iden_delim):
                    tokens.append((currToken, ']'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # { symbol
            if (currState == 'OPEN_CURLY_CHECK'):
                expected = ['alphanumeric', ' ', '{', '}'] + newline_delim
                if (code[i] in plaintext_delim + newline_delim + ['{', '}']):
                    tokens.append((currToken, '{'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # } symbol
            if (currState == 'CLOSING_CURLY_CHECK'):
                expected = ['alphanumeric', ' ', ';'] + newline_delim
                if (code[i] in plaintext_delim + newline_delim + [';']):
                    tokens.append((currToken, '}'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # + symbol
            if (currState == 'PLUS_CHECK'):
                expected = ['alphanumeric', ' ', '(', '\"', '+', '-']
                if (code[i] in arithmetic_delim + ['\"']):
                    tokens.append((currToken, '+'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's230'
            # < symbol
            if (currState == 'OPEN_ANGLE_CHECK'):
                expected = ['alphanumeric', ' ', '(', '+', '-'] + newline
                print("(dbg) open angle check curr char ", code[i])
                if (code[i] in arithmetic_delim + newline):
                    print("(dbg) arithmetic spotted for <")
                    tokens.append((currToken, '<'))
                    currToken = ''  
                    currState = 's0'
                else:
                    print("(dbg) going from open angle check to s409")
                    currState = 's236'
            # > symbol
            if (currState == 'CLOSING_ANGLE_CHECK'):
                expected = ['alphanumeric', ' ', '(', ';', '+', '-'] + newline
                if (code[i] in arithmetic_delim + [';'] + newline):
                    tokens.append((currToken, '>'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's240'
            # = symbol
            if (currState == 'ASSIGN_CHECK'):
                expected = ['alphanumeric', ' ', '\"', '+', '-']
                if (code[i] in arithmetic_delim + ['\"']):
                    tokens.append((currToken, '='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's244'
            # in statement
            if (currState == 'IN_CHECK'):
                expected = ['<']
                if (code[i] == '<'):
                    tokens.append((currToken, 'in'))
                    currToken = ''
                    currState = 's0'
                else:
                    currState = 's83'
            # print statement
            if (currState == 'PRINT_CHECK'):
                expected = func_delim
                if (code[i] in func_delim):
                    tokens.append((currToken, 'print'))
                    currToken = ''
                    currState = 's0'
                else:
                    currState = 's100'
            # println statement
            if (currState == 'PRINTLN_CHECK'):
                expected = func_delim
                if (code[i] in func_delim):
                    tokens.append((currToken, 'println'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # private statement
            if (currState == 'PRIVATE_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'private'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # property statement
            if (currState == 'PROPERTY_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'property'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # repeat statement
            if (currState == 'REPEAT_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'repeat'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # return statement
            if (currState == 'RETURN_CHECK'):
                expected = newline_delim + [';']
                if (code[i] in newline_delim + [';']):
                    tokens.append((currToken, 'return'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # set statement
            if (currState == 'SET_CHECK'):
                expected = get_set_delim
                if (code[i] in get_set_delim):
                    tokens.append((currToken, 'get'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # static statement
            if (currState == 'STATIC_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'static'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # switch statement
            if (currState == 'SWITCH_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'switch'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # this statement
            if (currState == 'THIS_CHECK'):
                expected = ['.']
                if (code[i] == '.'):
                    tokens.append((currToken, 'this'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # this statement
            if (currState == 'TRUE_CHECK'):
                expected = bool_delim
                if (code[i] in bool_delim):
                    tokens.append((currToken, 'bool_lit'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # void statement
            if (currState == 'VOID_CHECK'):
                expected = whitespace + newline
                if (code[i] in whitespace + newline):
                    tokens.append((currToken, 'void'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # while statement
            if (currState == 'WHILE_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'while'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # -- symbol
            if (currState == 'DECREMENT_CHECK'):
                expected = whitespace + ['alphanumeric'] + [';', ')']
                if (code[i] in whitespace + alphanumeric + [';', ')']):
                    tokens.append((currToken, '--'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # -= symbol
            if (currState == 'MINUS_ASS_CHECK'):
                expected = ['alphanumeric', ' ', '(', '+', '-']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '-='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # != symbol
            if (currState == 'NOT_EQUAL_CHECK'):
                expected = whitespace + ['alphabetic', '(']
                if (code[i] in whitespace + alphabetic_chars + ['(']):
                    tokens.append((currToken, '!='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # %= symbol
            if (currState == 'MODULO_ASS_CHECK'):
                expected = ['alphanumeric', ' ', '(', '+', '-']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '%='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # && symbol
            if (currState == 'LOGICAND_CHECK'):
                expected = ['alphanumeric', ' ', '(', '\"']
                if (code[i] in plaintext_delim + ['(', '\"']):
                    tokens.append((currToken, '%='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # *= symbol
            if (currState == 'MULT_ASS_CHECK'):
                expected = ['alphanumeric', ' ', '(', '+', '-']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '*='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # /= symbol
            if (currState == 'DIV_ASS_CHECK'):
                expected = ['alphanumeric', ' ', '(', '+', '-']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '/='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # :: symbol
            if (currState == 'SCOPE_ACC_CHECK'):
                expected = ['alphanumeric', ' '] + newline
                if (code[i] in plaintext_delim + newline):
                    tokens.append((currToken, '::'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # || symbol
            if (currState == 'LOGICOR_CHECK'):
                expected = ['alphanumeric', ' ', '(', '\"']
                if (code[i] in plaintext_delim + ['(', '\"']):
                    tokens.append((currToken, '||'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # ++ symbol
            if (currState == 'INCREMENT_CHECK'):
                expected = whitespace + ['alphanumeric', ')', ';']
                if (code[i] in whitespace + alphanumeric + [')', ';']):
                    tokens.append((currToken, '++'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # += symbol
            if (currState == 'ADD_ASS_CHECK'):
                expected = ['alphanumeric', ' ', '(', '\"', '+', '-']
                if (code[i] in arithmetic_delim + ['\"']):
                    tokens.append((currToken, '+='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # <= symbol
            if (currState == 'LESS_OR_EQUAL_CHECK'):
                expected = ['alphanumeric', ' ', '(', '+', '-']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '<='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # >= symbol
            if (currState == 'GREATER_OR_EQUAL_CHECK'):
                expected = ['alphanumeric', ' ', '(', '+', '-']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '>='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # == symbol
            if (currState == 'EQUAL_CHECK'):
                expected = ['alphanumeric', ' ', '(', '\"', '+', '-']
                if (code[i] in arithmetic_delim + ['\"']):
                    tokens.append((currToken, '=='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # string literal
            if (currState == 'STRING_LIT_CHECK'):
                expected = str_lit_delim
                if (code[i] in str_lit_delim):
                    tokens.append((currToken, 'string_lit'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # character literal
            if (currState == 'CHAR_LIT_CHECK'):
                expected = num_delim + newline_delim
                if (code[i] in num_delim + newline_delim):
                    tokens.append((currToken, 'char_lit'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # multicomments 
            if (currState == 'MULTI_COMMENT_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'multi-line comment'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # case statement 
            if (currState == 'CASE_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'case'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # class statement 
            if (currState == 'CLASS_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'class'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # continue statement 
            if (currState == 'CONTINUE_CHECK'):
                expected = newline_delim + [';']
                if (code[i] in newline_delim + [';']):
                    tokens.append((currToken, 'continue'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # const statement 
            if (currState == 'CONST_CHECK'):
                expected = newline_delim + [';']
                if (code[i] in newline_delim + [';']):
                    tokens.append((currToken, 'continue'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # default statement 
            if (currState == 'DEFAULT_CHECK'):
                expected = default_delim
                if (code[i] in default_delim):
                    tokens.append((currToken, 'default'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # do statement 
            if (currState == 'DO_CHECK'):
                expected = block_delim
                if (code[i] in block_delim):
                    tokens.append((currToken, 'do'))
                    currToken = ''
                    currState = 's0'
                else:
                    currState = 's44'
            # else statement 
            if (currState == 'ELSE_CHECK'):
                expected = block_delim
                if (code[i] in block_delim):
                    tokens.append((currToken, 'else'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # false statement
            if (currState == 'FALSE_CHECK'):
                expected = bool_delim
                if (code[i] in bool_delim):
                    tokens.append((currToken, 'bool_lit'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # for statement
            if (currState == 'FOR_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'for'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # get statement
            if (currState == 'GET_CHECK'):
                expected = get_set_delim
                if (code[i] in get_set_delim):
                    tokens.append((currToken, 'get'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # if statement
            if (currState == 'IF_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'if'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # import statement
            if (currState == 'IMPORT_CHECK'):
                expected = whitespace + ['<'] + newline
                if (code[i] in whitespace + ['<'] + newline):
                    tokens.append((currToken, 'import'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
            # item statement
            if (currState == 'ITEM_CHECK'):
                expected = iden_delim
                if (code[i] in iden_delim):
                    tokens.append((currToken, 'item'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s248'
                    print('(dbg) now in state 248')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
        # end of delim checking if statement
#---SPECIAL STATES---
        #identifier state
        if (currState == 's248'):
            print('(dbg) in identifier check state now')
            if (code[i] in iden_delim):
                print('(dbg) correct delim')    
                if (currToken[0] not in alphabetic_chars + ['_']):
                        errors.append(idenFirstError(currToken, currLine, currCol,lineContent))
                        currToken = ''  
                        currState = 's0'
                else:
                    tokens.append((currToken, 'Identifier'))
                currToken = ''
                currState = 's0'
            elif (code[i] in alphanumeric + ['_']): #if not delim but still valid, keep looping
                    currToken += code[i]
                    print('(dbg) accepted for iden')
                    currState ='s248'
                    continue
            else:
                currToken += code[i]
                expected = iden_delim
                # errors.append((currToken, f'Lexical Error: In line {currLine}, column {currCol-len(currToken)}; Unexpected \'{code[i]}\' for \'{currToken[:-1]}\'')) #can be expanded with conditions to check what error
                errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                currToken = ''  
                currState = 's0'
        #end of identifier looping
        #character lit check
        if (currState == 's261'):
            if (code[i] != '\''):
                if (code[i-1] == '\\'):
                    if (code[i] not in ['\'', '\"', '\\', 't', 'n', 'b']):
                        errors.append(charEscSeqError(currToken, currLine, currCol, lineContent))
                        currToken = ''  
                        currState = 's0'
                elif (code[i-1] != '\''):
                    errors.append(charLengthError(currToken, currLine, currCol, lineContent))
                    currToken = ''  
                    currState = 's0'
                currToken += code[i]
                continue
        #end of charcter lit checking
        #single line comment
        if (currState == 's251'):
            if (code[i] == '\n'):
                tokens.append((currToken, 'single_comment'))
                currToken = ''
                currState = 's0'
                continue
            else:
                currToken += code[i]
                continue
        #end of single line comment
        #multi-line comment
        if (currState == 's255'):
            if (code[i] != '/'):
                currState = 's254'
        #end of multi-line comment
        #whole number
        if (currState == 's297'):
            if (code[i] in numbers):
                print("(dbg) got another number")
                currWholeCount += 1
                currToken += code[i]
                if (currWholeCount > 19):
                    errors.append(wholeRangeError(currToken, currLine, currCol, lineContent))
                    currWholeCount = 0
                    currFracCount = 0
                    currToken = ''  
                    currState = 's0'
                else:
                    continue
            if (code[i] in num_delim):
                tokens.append((currToken, 'whole_lit'))
                currWholeCount = 0
                currFracCount = 0
                currToken = ''
                currState = 's0'
            elif (code[i] != '.'):
                currToken += code[i]
                expected = num_delim
                errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                currWholeCount = 0
                currFracCount = 0
                currToken = ''  
                currState = 's0'
        #end of whole number
        #fractional part of number
        if (currState == 's264'):
            if (code[i] in numbers):
                currFracCount += 1
                currToken += code[i]
                if (currFracCount > 16): 
                    errors.append(fracPrecError(currToken, currLine, currCol, lineContent))
                    currWholeCount = 0
                    currFracCount = 0
                    currToken = ''  
                    currState = 's0'
                else:
                    continue
            if (code[i] in num_delim):
                    tokens.append((currToken, 'frac_lit'))
                    currWholeCount = 0
                    currFracCount = 0
                    currToken = ''  
                    currState = 's0'
            else:
                currToken += code[i]
                expected = num_delim
                errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                currWholeCount = 0
                currFracCount = 0
                currToken = ''  
                currState = 's0'
        #end of fractional number

        #iterating through chars
        #check whitespaces
        if (currState not in ['s258', 's251', 's254']):
            if (code[i] == ' '):
                tokens.append(('\' \' ', 'Space'))
                continue
            if (code[i] == '\n'):
                if (i != len(code)-1):
                    tokens.append(('\\n', 'New line'))
                continue
        #check states
        if (code[i] in transitions[currState]):
            print(f'(dbg) in {currState} transitions')  
            currToken += code[i]
            print(f'(dbg) transitioning: {currState} - {code[i]} -> {transitions[currState][code[i]]}')
            currState = transitions[currState][code[i]]
            continue
        else: #if not in s0 transitions assume identifier, go to state 420
            print(f"(dbg) not in {currState} transitions")
            if (currState == 's0'):
                # if (code[i] in alphabetic_chars + ['_']):
                    #check if valid first char
                if (code[i] in numbers):
                    currToken += code[i]
                    print("(dbg)s0 is num")
                    #go to whole num loop state
                    currWholeCount += 1
                    currState = 's297'  
                    continue
                currToken += code[i]
                currState = 's248'
                continue
                # else:
                #     currToken += code[i]
                #     errors.append(idenFirstError(currToken, currLine, currCol,lineContent))
                #     currToken = ''
                #     currState = 's0'  
            else:
                if (currState == 's254'):
                    currToken += code[i]
                    continue
                if (currState == 's258'):
                    if (code[i] == '\n'):
                        errors.append(stringNewLineError(currToken, currLine, currCol, lineContent))
                        currToken = ''  
                        currState = 's0'
                    else:
                        currToken += code[i]
                        continue
                if (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState = 's248'
                    continue
                elif (code[i] in iden_delim): #check delim
                    if (currToken[0] not in alphabetic_chars + ['_']):
                        errors.append(idenFirstError(currToken, currLine, currCol,lineContent))
                        currToken = ''  
                        currState = 's0'
                    else:
                        print("(dbg) other iden append")
                        tokens.append((currToken, 'Identifier'))
                        currToken = code[i]
                        currState = transitions['s0'][code[i]]
                else:
                    currToken += code[i]
                    expected = iden_delim
                    if (code[i-1] in arithmetic_operator):
                        expected = ['alphanumeric', ' ', '(']
                    if (code[i-1] == '+'):
                        expected.append('\"')
                    print('(dbg) currState: ', currState)
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''  
                    currState = 's0'
    
    lexerResults = [tokens, errors] 
    return lexerResults

#---LEXER ERRORS---
def delimError(currToken, currLine, currCol, incorrectDelim, lineContent, expected):
    errorMsg = f'Lexical Error ({currLine}, {currCol-len(currToken)}): Unexpected \'{'newline' if incorrectDelim == '\n' else incorrectDelim}\' for \'{currToken}\'\n' 
    errorMsg += lineContent +'\n'
    errorMsg += '_'*(currCol-len(currToken)-1) + '^\n'
    errorMsg += f'Expected delimiters: {expected}'
    print("(debug) ", errorMsg)
    return errorMsg
def idenFirstError(currToken, currLine, currCol, lineContent):
    errorMsg = f'Lexical Error ({currLine}, {currCol-len(currToken)}): Identifier {currToken} must start with an alpha character\n'
    errorMsg += lineContent + '\n'
    errorMsg += '_'*(currCol-len(currToken)-1) + '^'
    print("(debug) ", errorMsg)
    return errorMsg
def stringNewLineError(currToken, currLine, currCol, lineContent):
    errorMsg = f'Lexical Error ({currLine}, {currCol-len(currToken)}): String literal {currToken} cannot have newline\n'
    errorMsg += lineContent + '\n'
    errorMsg += '_'*(currCol-len(currToken)-1) + '^'
    print("(debug) ", errorMsg)
    return errorMsg
def charEscSeqError(currToken, currLine, currCol, lineContent):
    errorMsg = f'Lexical Error ({currLine}, {currCol-len(currToken)}): Invalid escape sequence for character literal {currToken}\n'
    errorMsg += lineContent + '\n'
    errorMsg += '_'*(currCol-len(currToken)-1) + '^'
    print("(debug) ", errorMsg)
    return errorMsg
def charLengthError(currToken, currLine, currCol, lineContent):
    errorMsg = f'Lexical Error ({currLine}, {currCol-len(currToken)}): Invalid character length for character literal {currToken}\n'
    errorMsg += lineContent + '\n'
    errorMsg += '_'*(currCol-len(currToken)-1) + '^'
    print("(debug) ", errorMsg)
    return errorMsg
def wholeRangeError(currToken, currLine, currCol, lineContent):
    errorMsg = f'Lexical Error ({currLine}, {currCol-len(currToken)}): Numeric {currToken} exceeding max range\n'
    errorMsg += lineContent + '\n'
    errorMsg += '_'*(currCol-len(currToken)-1) + '^'
    print("(debug) ", errorMsg)
    return errorMsg
def fracPrecError(currToken, currLine, currCol, lineContent):
    errorMsg = f'Lexical Error ({currLine}, {currCol-len(currToken)}): Numeric {currToken} exceeding max precision\n'
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
    code += '\n'
    lexres = lexer(code)
    # print(lexres)
    return jsonify(lexres)

if __name__ == '__main__':
    app.run(debug=True) 
