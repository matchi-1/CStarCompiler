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
arithmetic_delim = plaintext_delim + ['(']
str_lit_delim = whitespace + ['+', ')', ',', ';']
newline_delim = [' ', '\n']
index_delim = [']'] + digit
default_delim = newline_delim + [':']
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
loop_delim = newline_delim+['(']
block_delim = newline_delim+['{']

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
	  'a':'s1',
        'b':'s24',
        'c':'s34',
        'd':'s97',
        'e':'s112',
        'f':'s117',
        'g':'s134',
        'i':'s138',
        'l':'s155',
        'm':'s160',
        'p':'s180',
	    'r':'s201',
        's':'s233',
        't':'s318', 
        'v':'s330',
        'w':'s335', 
	    '-':'DASH_CHECK', #s341
        '!':'NEGATION_CHECK', #s347
        '%':'MODULO_CHECK', #s351
        '&':'s355',
        '(':'OPEN_PAREN_CHECK',
        ')':'CLOSING_PAREN_CHECK',
        '*':'ASTERISK_CHECK', #s362
        ',':'COMMA_CHECK',
        '.':'DOT_CHECK', #s437
        '/':'SLASH_CHECK', #s372
        ';':'SEMICOLON_CHECK',
        '?':'QUESTION_CHECK',
        ':':'COLON_CHECK', #s386
        '[':'OPEN_BRACKET_CHECK',
        ']':'CLOSING_BRACKET_CHECK',
        '{':'OPEN_CURLY_CHECK',
        '}':'CLOSING_CURLY_CHECK',
        '|':'s396',
        '\"':'s431', #start string loop
        '+':'PLUS_CHECK', #s403
        '<':'OPEN_ANGLE_CHECK', #s409
        '>':'CLOSING_ANGLE_CHECK', #s413
        '=':'ASSIGN_CHECK', #s417
        '\'':'s434' #char checking
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
        'a':'s35',
        'e':'s39',
        'h':'s43',
        'l':'s81',
        'o':'s86'
    },
    's35':{
	  's':'s36'
    },
    's36':{
	  'e':'CASE_CHECK' #s37
    },
    's39':{
	  'i':'s40'
    },
    's40':{
	  'l':'CEIL_CHECK' #s41
    },
    's43':{
        'a':'s44',
	  'r':'s47'
    },
    's44':{
        'r':'CHAR_CHECK' #s45
    },
    's47':{
        '_':'s48'
    },
    's48':{
        't':'s49',
        'i':'s63'
    },
    's49':{
        'o':'s50'
    },
    's50':{
        'L':'s51',
        'U':'s57'
    },
    's51':{
        'o':'s52'
    },
    's52':{
        'w':'s53'
    },
    's53':{
        'e':'s54'
    },
    's54':{
        'r':'CHR_TOLOWER_CHECK' #s55
    },
    's57':{
        'p':'s58'
    },
    's58':{
        'p':'s59'
    },
    's59':{
        'e':'s60'
    },
    's60':{
        'r':'CHR_TOUPPER_CHECK' #s61
    },
    's63':{
        's':'s64'
    },
    's64':{
        'A':'s65',
        'D':'s75'
    },
    's65':{
        'l':'s66'
    },
    's66':{
        'p':'s67'
    },
    's67':{
        'h':'s68'
    },
    's68':{
        'a':'CHR_ISALPHA_CHECK' #s69
    },
    's69':{
        'N':'s70'
    },
    's71':{
        'u':'s72'
    },
    's72':{
        'm':'CHR_ISALPHANUM_CHECK' #s73
    },
    's75':{
        'i':'s76'
    },
    's76':{
        'g':'s77'
    },
    's77':{
        'i':'s78'
    },
    's78':{
        't':'CHR_ISDIGIT_CHECK' #s79
    },
    's81':{
        'a':'s82'
    },
    's82':{
        's':'s83'
    },
    's83':{
        's':'CLASS_CHECK' #s84
    },
    's86':{
        'n':'s87'
    },
    's87':{
        't':'s88',
        's':'s94'
    },
    's88':{
        'i':'s89'
    },
    's89':{
        'n':'s90'
    },
    's90':{
        'u':'s91'
    },
    's91':{
        'e':'CONTINUE_CHECK' #s92
    },
    's94':{
        't':'CONST_CHECK' #s95
    },
    's97':{
        'e':'s98',
        'o':'DO_CHECK' #s105
    },
    's98':{
        'f':'s99'
    },
    's99':{
        'a':'s100'
    },
    's100':{
        'u':'s101'
    },
    's101':{
        'l':'s102'
    },
    's102':{
        't':'DEFAULT_CHECK' #s103
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
        'e':'DOUBLE_CHECK' #s110
    },
    's112':{
        'l':'s113'
    },
    's113':{
        's':'s114'
    },
    's114':{
        'e':'ELSE_CHECK' #s115
    },
    's117':{
        'a':'s118',
        'o':'s131',
        'l':'s123'
    },
    's118':{
        'l':'s119'
    },
    's119':{
        's':'s120'
    },
    's120':{
        'e':'FALSE_CHECK' #s121
    },
    's123':{
        'o':'s124'
    },
    's124':{
        'a':'s125',
        'o':'s128'
    },
    's125':{
        't':'FLOAT_CHECK' #s126
    },
    's128':{
        'r':'FLOOR_CHECK' #s129
    },
    's131':{
        'r':'FOR_CHECK' #s129
    },
    's134':{
        'e':'s135' 
    },
    's135':{
        't':'GET_CHECK' #s136
    },
    's138':{
        'f':'IF_CHECK', #s139
        'm':'s141',
        'n':'IN_CHECK', #s147
        't':'s151' 
    },
    's141':{
        'p':'s142' 
    },
    's142':{
        'o':'s143' 
    },
    's143':{
        'r':'s144' 
    },
    's144':{
        't':'IMPORT_CHECK' #s145 
    },
    's147':{
        't':'INT_CHECK'
    },
    's151':{
        'e':'s152'
    },
    's152':{
        'm':'ITEM_CHECK' #s153
    },
    's155':{
        'o':'s156'
    },
    's156':{
        'n':'s157'
    },
    's157':{
        'g':'LONG_CHECK' #s158
    },
    's160':{
        'a':'s161',
        'e':'s164',
        'i':'s173',
        'o':'s176'
    },
    's161':{
        'x':'MAX_CHECK' #s162
    },
    's164':{
        'a':'s165',
        'd':'s168' 
    },
    's165':{
        'n':'MEAN_CHECK'  #s166
    },
    's168':{
        'i':'s169' 
    },
    's169':{
        'a':'s170'  
    },
    's170':{
        'n':'MEDIAN_CHECK' #s171  
    },
    's173':{
        'n':'MIN_CHECK' #s174  
    },
    's176':{
        'd':'s177' 
    },
    's177':{
        'e':'MODE_CHECK'  #s178
    },
    's180':{
        'r':'s181'
    },
    's181':{
        'i':'s182',
        'o':'s194'
    },
    's182':{
        'n':'s183',
	  'v':'s189'
    },
    's183':{
        't':'PRINT_CHECK', #s184
    },
    's184':{
        'l':'s186'
    },
    's186':{
        'n':'PRINTLN_CHECK'
    },
    's189':{
        'a':'s190'
    },
    's190':{
        't':'s191'
    },
    's191':{
        'e':'PRIVATE_CHECK'
    },
    's194':{
        'p':'s195'
    },
    's195':{
        'e':'s196'
    },
    's196':{
        'r':'s197'
    },
    's197':{
        't':'s198'
    },
    's198':{
        'y':'PROPERTY_CHECK'
    },
    's201':{
        'a':'s202',
        'e':'s222'
     },
    's202':{
        'n':'s203'
    },
    's203':{
        'd':'s204'
    },
    's204':{
        'D':'s205',
	  'F':'s212',
        'I':'s218'
    },
    's205':{
        'o':'s206'
    },
    's206':{
        'u':'s207'
    },
    's207':{
        'b':'s208'
    },
    's208':{
        'l':'s209'
    },
    's209':{
        'e':'RANDDOUBLE_CHECK'
    },
    's212':{
        'l':'s213'
    },
    's213':{
        'o':'s214'
    },
    's214':{
        'a':'s215'
    },
    's215':{
        't':'RANDFLOAT_CHECK'
    },
    's218':{
        'n':'s219'
    },
    's219':{
        't':'RANDINT_CHECK'
    },
    's222':{
        'p':'s223',
        't':'s228'
    },
    's223':{
        'e':'s224'
    },
    's224':{
        'a':'s225'
    },
    's225':{
        't':'REPEAT_CHECK'
    },
    's228':{
        'u':'s229'
    },
    's229':{
        'r':'s230'
    },
    's230':{
        'n':'RETURN_CHECK'
    },
    's233':{
        'e':'s234',
        'q':'s237',
        't':'s241',
        'w':'s312'
    },
    's234':{
        't':'SET_CHECK'
    },
    's237':{
        'r':'s238'
    },
    's238':{
        't':'SQRT_CHECK'
    },
    's241':{
	  'a':'s242',
        'r':'s247'
    },
    's242':{
	  't':'s243'
    },
    's243':{
	  'i':'s244'
    },
    's244':{
	  'c':'STATIC_CHECK'
    },
    's247':{
        '_':'s248',
        'i':'s308' 
    },
    's248':{
        'i':'s249',
        'l':'s257',
        'p':'s264',
	  's':'s288',
        't':'s294'
    },

    's249':{
        's':'s250' 
    },
    's250':{
        'E':'s251' 
    },
    's251':{
        'm':'s252'
    }, 
    's252':{
        'p':'s253' 
    },
    's253':{
        't':'s254' 
    },
    's254':{
        'y':'STR_ISEMPTY_CHECK' 
    },
    's257':{
        'e':'s258' 
    },
    's258':{
        'n':'s259' 
    },
    's259':{
        'g':'s260' 
    },
    's260':{
        't':'s261' 
    },
    's261':{
        'h':'STR_LENGTH_CHECK' 
    },
    's264':{
        'o':'s265' 
    },
    's265':{
        'p':'s266' 
    },
    's266':{
        'A':'s267',
	  'D':'s273',
        'S':'s280'
    },
    's267':{
        'l':'s268'
    },
    's268':{
        'p':'s269'
    },
    's269':{
        'h':'s270'
    },
    's270':{
        'a':'STR_POPALPHA_CHECK'
    },
    's273':{
        'i':'s274'
    },
    's274':{
        'g':'s275'
    },
    's275':{
        'i':'s276'
    },
    's276':{
        't':'s277'
    },
    's277':{
        's':'STR_POPDIGITS_CHECK'
    },
    's280':{
        'p':'s281'
    },
    's281':{
        'e':'s282'
    },
    's282':{
        'c':'s283'
    },
    's283':{
        'i':'s284'
    },
    's284':{
        'a':'s285'
    },
    's285':{
        'l':'STR_POPSPECIAL_CHECK'
    },
    's288':{
        'l':'s289'
    },
    's289':{
        'i':'s290'
    },
    's290':{
        'c':'s291'
    },
    's291':{
        'e':'STR_SLICE_CHECK'
    },
    's294':{
        'o':'s295'
    },
   's295':{
        'L':'s296',
        'U':'s302'
    },
    's296':{
        'o':'s297'
    },
    's297':{
        'w':'s298'
    },
    's298':{
        'e':'s299'
    },
    's299':{
        'r':'STR_TOLOWER_CHECK'
    },
    's302':{
        'p':'s303'
    },
    's303':{
        'p':'s304'
    },
    's304':{
        'e':'s305'
    },
    's305':{
        'r':'STR_TOUPPER_CHECK'
    },
    's308':{
        'n':'s309'
    },
    's309':{
        'g':'STRING_CHECK'
    },
    's312':{
        'i':'s313'
    },
    's313':{
        't':'s314'
    },
    's314':{
        'c':'s315'
    },
    's315':{
        'h':'SWITCH_CHECK'
    },
    's318':{
        'h':'s319',
        'r':'s323'
    },
    's319':{
        'i':'s320'
    },
    's320':{
        's':'THIS_CHECK'
    },
    's323':{
        'u':'s324'
    },
    's324':{
        'e':'TRUE_CHECK',
        'n':'s327'
    },
    's327':{
        'c':'TRUNC_CHECK'
    },
    's330':{
        'o':'s331'
    },
    's331':{
        'i':'s332'
    },
    's332':{
        'd':'VOID_CHECK'
    },
    's335':{
        'h':'s336'
    },
    's336':{
        'i':'s337'
    },
    's337':{
        'l':'s338'
    },
    's338':{
        'e':'WHILE_CHECK'
    },
    's341':{
        '-':'DECREMENT_CHECK',
	  '=':'MINUS_ASS_CHECK'
    },
    's347':{
        '=':'NOT_EQUAL_CHECK'
    },
    's351':{
        '=':'MODULO_ASS_CHECK'
    },
    's355':{
        '&':'LOGICAND_CHECK'
    },
    's362':{
        '=':'MULT_ASS_CHECK'
    },
    's372':{
        '*':'s427', #start mult comment loop
        '/':'s424', #start single comment loop
        '=':'DIV_ASS_CHECK'
    },
    's386':{
        ':':'SCOPE_ACC_CHECK'
    },
    's396':{
        '|':'LOGICOR_CHECK'
    },
    's403':{
        '+':'INCREMENT_CHECK',
        '=':'ADD_ASS_CHECK'
    },
    's409':{
        '=':'LESS_OR_EQUAL_CHECK'
    },	
    's413':{
        '=':'GREATER_OR_EQUAL_CHECK'
    },
    's417':{
        '=':'EQUAL_CHECK'
    },
    's421':{
        '_':'s421'
        # HELPER: alphanumeric:'s421'
    },
    's424':{
        # HELPER: ascii:'s424'
    },
    's427':{
        '\n':'s427',
        '*':'s428'
        # HELPER: ascii:'s427'
    },
    's428':{
        '/':'MULTI_COMMENT_CHECK'
    },
    's431':{
        '"':'STRING_LIT_CHECK'
        # HELPER: ascii:'s431'
    },
    's434':{
        '\'':'CHAR_LIT_CHECK'
    },
    's437':{
        # HELPER: numbers:'s437'
    },
    's470':{
        '.':'s437'
        # HELPER: numbers: '470'
    }
}
#---GRAPH HELPERS---
#s421 -alphanumeric> s421
for i in alphanumeric:
    transitions['s421'][i] = 's421'
for i in ascii:
    transitions['s424'][i] = 's424'
    transitions['s427'][i] = 's427'
    #override for multiline comment
    transitions['s427']['*'] = 's428'
    transitions['s431'][i] = 's431'
    #overrde for string
    transitions['s431']['\"'] = 'STRING_LIT_CHECK'
for i in numbers:
    transitions['s437'][i] = 's437'
    transitions['s470'][i] = 's470'

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
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            if (currState == 'CHAR_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'char'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            if (currState == 'DOUBLE_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'double'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            if (currState == 'FLOAT_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'float'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            if (currState == 'INT_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'int'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            if (currState == 'LONG_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'long'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            if (currState == 'STRING_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'string'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            #built-in funcs spit out as identifiers 
            if (currState in builtin_func):
                expected = func_delim
                if (code[i] in func_delim):
                    tokens.append((currToken, 'Identifier'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            #break statement
            if (currState == 'BREAK_CHECK'):
                expected = newline_delim + [';']
                if (code[i] in newline_delim + [';']):
                    tokens.append((currToken, 'break'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # ( symbol
            if (currState == 'OPEN_PAREN_CHECK'):
                expected = ['alphanumeric', ' ', '\"', '!', ')']
                if (code[i] in arithmetic_delim + ['\"', '!', ')']):
                    tokens.append((currToken, '('))
                    currToken = ''
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
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
                    break
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
                    break
            # - symbol
            if (currState == 'DASH_CHECK'):
                expected = ['alphanumeric', ' ', '(']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '-'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's341'
            # ! symbol
            if (currState == 'NEGATION_CHECK'):
                expected = ['alphabetic', '('] + whitespace 
                if (code[i] in whitespace + alphabetic_chars + ['(']):
                    tokens.append((currToken, '!'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's347'
            # % symbol
            if (currState == 'MODULO_CHECK'):
                expected = ['alphanumeric', ' ', '(']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '%'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's351'
            # ( symbol
            if (currState == 'OPEN_PAREN_CHECK'):
                expected = ['alphanumeric', ' ', '(', '\"', '!', ')']
                if (code[i] in arithmetic_delim + ['\"', '!', ')']):
                    tokens.append((currToken, '('))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
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
                    break
            # * symbol
            if (currState == 'ASTERISK_CHECK'):
                expected = ['alphanumeric', ' ', '(']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '%'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's362'
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
                    break
            # . symbol
            if (currState == 'DOT_CHECK'):
                expected = ['alphabetic'] + whitespace
                if (code[i] in alphabetic_chars+whitespace):
                    tokens.append((currToken, '.'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's437'
            # / symbol
            if (currState == 'SLASH_CHECK'):
                expected = ['alphanumeric', ' ', '(']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '/'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's372'
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
                    break
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
                    break
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
                    break
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
                    break
            # } symbol
            if (currState == 'CLOSING_CURLY_CHECK'):
                expected = ['alphanumeric', ' '. ';'] + newline_delim
                if (code[i] in plaintext_delim + newline_delim + [';']):
                    tokens.append((currToken, '}'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # + symbol
            if (currState == 'PLUS_CHECK'):
                expected = ['alphanumeric', ' ', '(', '\"']
                if (code[i] in arithmetic_delim + ['\"']):
                    tokens.append((currToken, '+'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's403'
            # < symbol
            if (currState == 'OPEN_ANGLE_CHECK'):
                expected = ['alphanumeric', ' ', '(']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '<'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's409'
            # > symbol
            if (currState == 'CLOSING_ANGLE_CHECK'):
                expected = ['alphanumeric', ' ', '(', ';']
                if (code[i] in arithmetic_delim + [';']):
                    tokens.append((currToken, '>'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's413'
            # = symbol
            if (currState == 'ASSIGN_CHECK'):
                expected = ['alphanumeric', ' ', '\"']
                if (code[i] in arithmetic_delim + ['\"']):
                    tokens.append((currToken, '='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's417'
            # in statement
            if (currState == 'IN_CHECK'):
                expected = ['<']
                if (code[i] == '<'):
                    tokens.append((currToken, 'in'))
                    currToken = ''
                    currState = 's0'
                else:
                    currState = 's147'
            # print statement
            if (currState == 'PRINT_CHECK'):
                expected = func_delim
                if (code[i] in func_delim):
                    tokens.append((currToken, 'print'))
                    currToken = ''
                    currState = 's0'
                else:
                    currState = 's184'
            # println statement
            if (currState == 'PRINTLN_CHECK'):
                expected = func_delim
                if (code[i] in func_delim):
                    tokens.append((currToken, 'println'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # private statement
            if (currState == 'PRIVATE_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'private'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # property statement
            if (currState == 'PROPERTY_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'property'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # repeat statement
            if (currState == 'REPEAT_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'repeat'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # return statement
            if (currState == 'RETURN_CHECK'):
                expected = newline_delim + [';']
                if (code[i] in newline_delim + [';']):
                    tokens.append((currToken, 'return'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # set statement
            if (currState == 'SET_CHECK'):
                expected = get_set_delim
                if (code[i] in get_set_delim):
                    tokens.append((currToken, 'get'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # static statement
            if (currState == 'STATIC_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'static'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # switch statement
            if (currState == 'SWITCH_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'switch'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # this statement
            if (currState == 'THIS_CHECK'):
                expected = ['.']
                if (code[i] == '.'):
                    tokens.append((currToken, 'this'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # this statement
            if (currState == 'TRUE_CHECK'):
                expected = bool_delim
                if (code[i] in bool_delim):
                    tokens.append((currToken, 'bool_lit'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # void statement
            if (currState == 'VOID_CHECK'):
                expected = whitespace + newline
                if (code[i] in whitespace + newline):
                    tokens.append((currToken, 'void'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # while statement
            if (currState == 'WHILE_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'while'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
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
                    break
            # -= symbol
            if (currState == 'MINUS_ASS_CHECK'):
                expected = ['alphanumeric', ' ', '(']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '-='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
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
                    break
            # %= symbol
            if (currState == 'MODULO_ASS_CHECK'):
                expected = ['alphanumeric', ' ', '(']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '%='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
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
                    break
            # *= symbol
            if (currState == 'MULT_ASS_CHECK'):
                expected = ['alphanumeric', ' ', '(']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '*='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # /= symbol
            if (currState == 'DIV_ASS_CHECK'):
                expected = ['alphanumeric', ' ', '(']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '/='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
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
                    break
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
                    break
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
                    break
            # += symbol
            if (currState == 'ADD_ASS_CHECK'):
                expected = ['alphanumeric', ' ', '(', '\"']
                if (code[i] in arithmetic_delim + ['\"']):
                    tokens.append((currToken, '+='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # <= symbol
            if (currState == 'LESS_OR_EQUAL_CHECK'):
                expected = ['alphanumeric', ' ', '(']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '<='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # >= symbol
            if (currState == 'GREATER_OR_EQUAL_CHECK'):
                expected = ['alphanumeric', ' ', '(']
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '>='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # == symbol
            if (currState == 'EQUAL_CHECK'):
                expected = ['alphanumeric', ' ', '(', '\"']
                if (code[i] in arithmetic_delim + ['\"']):
                    tokens.append((currToken, '=='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
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
                    break
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
                    break
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
                    break
            # case statement 
            if (currState == 'CASE_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'case'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # class statement 
            if (currState == 'CLASS_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'class'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # continue statement 
            if (currState == 'CONTINUE_CHECK'):
                expected = newline_delim + [';']
                if (code[i] in newline_delim + [';']):
                    tokens.append((currToken, 'continue'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # const statement 
            if (currState == 'CONST_CHECK'):
                expected = newline_delim + [';']
                if (code[i] in newline_delim + [';']):
                    tokens.append((currToken, 'continue'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # default statement 
            if (currState == 'DEFAULT_CHECK'):
                expected = default_delim
                if (code[i] in default_delim):
                    tokens.append((currToken, 'default'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # do statement 
            if (currState == 'DO_CHECK'):
                expected = block_delim
                if (code[i] in block_delim):
                    tokens.append((currToken, 'do'))
                    currToken = ''
                    currState = 's0'
                else:
                    currState = 's105'
            # else statement 
            if (currState == 'ELSE_CHECK'):
                expected = block_delim
                if (code[i] in block_delim):
                    tokens.append((currToken, 'else'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # false statement
            if (currState == 'FALSE_CHECK'):
                expected = bool_delim
                if (code[i] in bool_delim):
                    tokens.append((currToken, 'bool_lit'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # for statement
            if (currState == 'FOR_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'for'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # get statement
            if (currState == 'GET_CHECK'):
                expected = get_set_delim
                if (code[i] in get_set_delim):
                    tokens.append((currToken, 'get'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # if statement
            if (currState == 'IF_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'if'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # import statement
            if (currState == 'IMPORT_CHECK'):
                expected = whitespace + ['<']
                if (code[i] in whitespace + ['<']):
                    tokens.append((currToken, 'import'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
            # item statement
            if (currState == 'ITEM_CHECK'):
                expected = iden_delim
                if (code[i] in iden_delim):
                    tokens.append((currToken, 'item'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState ='s421'
                    print('(dbg) now in state 421')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    break
        # end of delim checking if statement
#---SPECIAL STATES---
        #identifier state
        if (currState == 's421'):
            print('(dbg) in identifier check state now')
            if (code[i] in iden_delim):
                print('(dbg) correct delim')    
                if (currToken[0] not in alphabetic_chars + ['_']):
                        errors.append(idenFirstError(currToken, currLine, currCol,lineContent))
                        break
                else:
                    tokens.append((currToken, 'Identifier'))
                currToken = ''
                currState = 's0'
            elif (code[i] in alphanumeric + ['_']): #if not delim but still valid, keep looping
                    currToken += code[i]
                    print('(dbg) accepted for iden')
                    currState ='s421'
                    continue
            else:
                currToken += code[i]
                expected = iden_delim
                # errors.append((currToken, f'Lexical Error: In line {currLine}, column {currCol-len(currToken)}; Unexpected \'{code[i]}\' for \'{currToken[:-1]}\'')) #can be expanded with conditions to check what error
                errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                break
        #end of identifier looping
        #character lit check
        if (currState == 's434'):
            if (code[i] != '\''):
                if (code[i-1] == '\\'):
                    if (code[i] not in ['\'', '\"', '\\', 't', 'n', 'b']):
                        errors.append(charEscSeqError(currToken, currLine, currCol, lineContent))
                        break
                elif (code[i-1] != '\''):
                    errors.append(charLengthError(currToken, currLine, currCol, lineContent))
                    break
                currToken += code[i]
                continue
        #end of charcter lit checking
        #single line comment
        if (currState == 's424'):
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
        if (currState == 's428'):
            if (code[i] != '/'):
                currState = 's427'
        #end of multi-line comment
        #whole number
        if (currState == 's470'):
            if (code[i] in numbers):
                print("(dbg) got another number")
                currWholeCount += 1
                currToken += code[i]
                if (currWholeCount > 19):
                    errors.append(wholeRangeError(currToken, currLine, currCol, lineContent))
                    break
                else:
                    continue
            if (code[i] in num_delim):
                tokens.append((currToken, 'whole_lit'))
                currToken = ''
                currState = 's0'
            elif (code[i] != '.'):
                currToken += code[i]
                expected = num_delim
                errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                break
        #end of whole number
        #fractional part of number
        if (currState == 's437'):
            if (code[i] in numbers):
                currFracCount += 1
                currToken += code[i]
                if (currFracCount > 16): 
                    errors.append(fracPrecError(currToken, currLine, currCol, lineContent))
                    break
                else:
                    continue
            if (code[i] in num_delim):
                    tokens.append((currToken, 'frac_lit'))
                    currToken = ''  
                    currState = 's0'
            else:
                currToken += code[i]
                expected = num_delim
                errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                break
        #end of fractional number

        #iterating through chars
        #check whitespaces
        if (currState not in ['s431', 's424', 's427']):
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
                    currState = 's470'  
                    continue
                currToken += code[i]
                currState = 's421'
                continue
                # else:
                #     currToken += code[i]
                #     errors.append(idenFirstError(currToken, currLine, currCol,lineContent))
                #     currToken = ''
                #     currState = 's0'  
            else:
                if (currState == 's427'):
                    currToken += code[i]
                    continue
                if (currState == 's431'):
                    if (code[i] == '\n'):
                        errors.append(stringNewLineError(currToken, currLine, currCol, lineContent))
                        break
                    else:
                        currToken += code[i]
                        continue
                if (code[i] in alphanumeric + ['_']):
                    currToken += code[i]
                    currState = 's421'
                    continue
                elif (code[i] in iden_delim): #check delim
                    if (currToken[0] not in alphabetic_chars + ['_']):
                        errors.append(idenFirstError(currToken, currLine, currCol,lineContent))
                        break
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
                    break
    
    lexerResults = [tokens, errors] 
    return lexerResults

#---LEXER ERRORS---
def delimError(currToken, currLine, currCol, incorrectDelim, lineContent, expected):
    errorMsg = f'Lexical Error ({currLine}, {currCol-len(currToken)}): Unexpected \'{incorrectDelim}\' for \'{currToken}\'\n' 
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