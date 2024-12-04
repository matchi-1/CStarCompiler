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
type_iden_delim = [')', ' ', '\n', '>']
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
def transition(currState, currChar):
    print(f'(dbg) trans func {currState} : {currChar}')
    if (currState == 's0'):
        if(currChar == 'a'):
            return 's1'
        elif(currChar == 'b'):
            return 's24'
        elif(currChar == 'c'):
            return 's34'
        elif(currChar == 'd'):
            return 's97'
        elif(currChar == 'e'):
            return 's112'
        elif(currChar == 'f'):
            return 's117'
        elif(currChar == 'g'):
            return 's134'
        elif(currChar == 'i'):
            return 's138'
        elif(currChar == 'l'):
            return 's155'
        elif(currChar == 'm'):
            return 's160'
        elif(currChar == 'p'):
            return 's180'
        elif(currChar == 'r'):
            return 's201'
        elif(currChar == 's'):
            return 's233'
        elif(currChar == 't'):
            return 's318'
        elif(currChar == 'v'):
            return 's330'
        elif(currChar == 'w'):
            return 's335'
        elif(currChar == '-'):
            return 'DASH_CHECK'
        elif(currChar == '!'):
            return 'NEGATION_CHECK'
        elif(currChar == '%'):
            return 'MODULO_CHECK'
        elif(currChar == '&'):
            return 's355'
        elif(currChar == '('):
            return 'OPEN_PAREN_CHECK'
        elif(currChar == ')'):
            return 'CLOSING_PAREN_CHECK'
        elif(currChar == '*'):
            return 'ASTERISK_CHECK'
        elif(currChar == ','):
            return 'COMMA_CHECK'
        elif(currChar == '.'):
            return 'DOT_CHECK'
        elif(currChar == '/'):
            return 'SLASH_CHECK'
        elif(currChar == ';'):
            return 'SEMICOLON_CHECK'
        elif(currChar == '?'):
            return 'QUESTION_CHECK'
        elif(currChar == ':'):
            return 'COLON_CHECK'
        elif(currChar == '['):
            return 'OPEN_BRACKET_CHECK'
        elif(currChar == ']'):
            return 'CLOSING_BRACKET_CHECK'
        elif(currChar == '{'):
            return 'OPEN_CURLY_CHECK'
        elif(currChar == '}'):
            return 'CLOSING_CURLY_CHECK'
        elif(currChar == '|'):
            return 's396'
        elif(currChar == '"'):
            return 's431'
        elif(currChar == '+'):
            return 'PLUS_CHECK'
        elif(currChar == '<'):
            return 'OPEN_ANGLE_CHECK'
        elif(currChar == '>'):
            return 'CLOSING_ANGLE_CHECK'
        elif(currChar == '='):
            return 'ASSIGN_CHECK'
        elif(currChar == '\''):
            return 's434'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's1'):
        if(currChar == 'b'):
            return 's2'
        elif(currChar == 'r'):
            return 's5'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's2'):
        if(currChar == 's'):
            return 'ABS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's5'):
        if(currChar == 'r'):
            return 's6'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's6'):
        if(currChar == '_'):
            return 's7'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's7'):
        if(currChar == 'f'):
            return 's8'
        elif(currChar == 'l'):
            return 's17'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's8'):
        if(currChar == 'o'):
            return 's9'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's9'):
        if(currChar == 'r'):
            return 's10'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's10'):
        if(currChar == 'I'):
            return 's11'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's11'):
        if(currChar == 't'):
            return 's12'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's12'):
        if(currChar == 'e'):
            return 's13'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's13'):
        if(currChar == 'm'):
            return 's14'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's14'):
        if(currChar == 's'):
            return 'ARR_FORITEMS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's17'):
        if(currChar == 'e'):
            return 's18'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's18'):
        if(currChar == 'n'):
            return 's19'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's19'):
        if(currChar == 'g'):
            return 's20'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's20'):
        if(currChar == 't'):
            return 's21'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's21'):
        if(currChar == 'h'):
            return 'ARR_LENGTH_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's24'):
        if(currChar == 'o'):
            return 's25'
        elif(currChar == 'r'):
            return 's29'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's25'):
        if(currChar == 'o'):
            return 's26'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's26'):
        if(currChar == 'l'):
            return 'BOOL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's29'):
        if(currChar == 'e'):
            return 's30'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's30'):
        if(currChar == 'a'):
            return 's31'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's31'):
        if(currChar == 'k'):
            return 'BREAK_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's34'):
        if(currChar == 'a'):
            return 's35'
        elif(currChar == 'e'):
            return 's39'
        elif(currChar == 'h'):
            return 's43'
        elif(currChar == 'l'):
            return 's81'
        elif(currChar == 'o'):
            return 's86'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's35'):
        if(currChar == 's'):
            return 's36'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's36'):
        if(currChar == 'e'):
            return 'CASE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's39'):
        if(currChar == 'i'):
            return 's40'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's40'):
        if(currChar == 'l'):
            return 'CEIL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's43'):
        if(currChar == 'a'):
            return 's44'
        elif(currChar == 'r'):
            return 's47'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's44'):
        if(currChar == 'r'):
            return 'CHAR_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's47'):
        if(currChar == '_'):
            return 's48'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's48'):
        if(currChar == 't'):
            return 's49'
        elif(currChar == 'i'):
            return 's63'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's49'):
        if(currChar == 'o'):
            return 's50'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's50'):
        if(currChar == 'L'):
            return 's51'
        elif(currChar == 'U'):
            return 's57'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's51'):
        if(currChar == 'o'):
            return 's52'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's52'):
        if(currChar == 'w'):
            return 's53'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's53'):
        if(currChar == 'e'):
            return 's54'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's54'):
        if(currChar == 'r'):
            return 'CHR_TOLOWER_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's57'):
        if(currChar == 'p'):
            return 's58'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's58'):
        if(currChar == 'p'):
            return 's59'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's59'):
        if(currChar == 'e'):
            return 's60'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's60'):
        if(currChar == 'r'):
            return 'CHR_TOUPPER_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's63'):
        if(currChar == 's'):
            return 's64'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's64'):
        if(currChar == 'A'):
            return 's65'
        elif(currChar == 'D'):
            return 's75'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's65'):
        if(currChar == 'l'):
            return 's66'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's66'):
        if(currChar == 'p'):
            return 's67'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's67'):
        if(currChar == 'h'):
            return 's68'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's68'):
        if(currChar == 'a'):
            return 'CHR_ISALPHA_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's69'):
        if(currChar == 'N'):
            return 's70'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's71'):
        if(currChar == 'u'):
            return 's72'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's72'):
        if(currChar == 'm'):
            return 'CHR_ISALPHANUM_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's75'):
        if(currChar == 'i'):
            return 's76'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's76'):
        if(currChar == 'g'):
            return 's77'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's77'):
        if(currChar == 'i'):
            return 's78'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's78'):
        if(currChar == 't'):
            return 'CHR_ISDIGIT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's81'):
        if(currChar == 'a'):
            return 's82'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's82'):
        if(currChar == 's'):
            return 's83'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's83'):
        if(currChar == 's'):
            return 'CLASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's86'):
        if(currChar == 'n'):
            return 's87'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's87'):
        if(currChar == 't'):
            return 's88'
        elif(currChar == 's'):
            return 's94'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's88'):
        if(currChar == 'i'):
            return 's89'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's89'):
        if(currChar == 'n'):
            return 's90'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's90'):
        if(currChar == 'u'):
            return 's91'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's91'):
        if(currChar == 'e'):
            return 'CONTINUE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's94'):
        if(currChar == 't'):
            return 'CONST_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's97'):
        if(currChar == 'e'):
            return 's98'
        elif(currChar == 'o'):
            return 'DO_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's98'):
        if(currChar == 'f'):
            return 's99'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's99'):
        if(currChar == 'a'):
            return 's100'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's100'):
        if(currChar == 'u'):
            return 's101'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's101'):
        if(currChar == 'l'):
            return 's102'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's102'):
        if(currChar == 't'):
            return 'DEFAULT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's105'):
        if(currChar == 'u'):
            return 's107'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's107'):
        if(currChar == 'b'):
            return 's108'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's108'):
        if(currChar == 'l'):
            return 's109'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's109'):
        if(currChar == 'e'):
            return 'DOUBLE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's112'):
        if(currChar == 'l'):
            return 's113'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's113'):
        if(currChar == 's'):
            return 's114'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's114'):
        if(currChar == 'e'):
            return 'ELSE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's117'):
        if(currChar == 'a'):
            return 's118'
        elif(currChar == 'o'):
            return 's131'
        elif(currChar == 'l'):
            return 's123'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's118'):
        if(currChar == 'l'):
            return 's119'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's119'):
        if(currChar == 's'):
            return 's120'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's120'):
        if(currChar == 'e'):
            return 'FALSE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's123'):
        if(currChar == 'o'):
            return 's124'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's124'):
        if(currChar == 'a'):
            return 's125'
        elif(currChar == 'o'):
            return 's128'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's125'):
        if(currChar == 't'):
            return 'FLOAT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's128'):
        if(currChar == 'r'):
            return 'FLOOR_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's131'):
        if(currChar == 'r'):
            return 'FOR_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's134'):
        if(currChar == 'e'):
            return 's135'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's135'):
        if(currChar == 't'):
            return 'GET_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's138'):
        if(currChar == 'f'):
            return 'IF_CHECK'
        elif(currChar == 'm'):
            return 's141'
        elif(currChar == 'n'):
            return 'IN_CHECK'
        elif(currChar == 't'):
            return 's151'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's141'):
        if(currChar == 'p'):
            return 's142'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's142'):
        if(currChar == 'o'):
            return 's143'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's143'):
        if(currChar == 'r'):
            return 's144'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's144'):
        if(currChar == 't'):
            return 'IMPORT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's147'):
        if(currChar == 't'):
            return 'INT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's151'):
        if(currChar == 'e'):
            return 's152'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's152'):
        if(currChar == 'm'):
            return 'ITEM_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's155'):
        if(currChar == 'o'):
            return 's156'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's156'):
        if(currChar == 'n'):
            return 's157'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's157'):
        if(currChar == 'g'):
            return 'LONG_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's160'):
        if(currChar == 'a'):
            return 's161'
        elif(currChar == 'e'):
            return 's164'
        elif(currChar == 'i'):
            return 's173'
        elif(currChar == 'o'):
            return 's176'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's161'):
        if(currChar == 'x'):
            return 'MAX_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's164'):
        if(currChar == 'a'):
            return 's165'
        elif(currChar == 'd'):
            return 's168'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's165'):
        if(currChar == 'n'):
            return 'MEAN_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's168'):
        if(currChar == 'i'):
            return 's169'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's169'):
        if(currChar == 'a'):
            return 's170'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's170'):
        if(currChar == 'n'):
            return 'MEDIAN_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's173'):
        if(currChar == 'n'):
            return 'MIN_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's176'):
        if(currChar == 'd'):
            return 's177'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's177'):
        if(currChar == 'e'):
            return 'MODE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's180'):
        if(currChar == 'r'):
            return 's181'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's181'):
        if(currChar == 'i'):
            return 's182'
        elif(currChar == 'o'):
            return 's194'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's182'):
        if(currChar == 'n'):
            return 's183'
        elif(currChar == 'v'):
            return 's189'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's183'):
        if(currChar == 't'):
            return 'PRINT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's184'):
        if(currChar == 'l'):
            return 's186'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's186'):
        if(currChar == 'n'):
            return 'PRINTLN_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's189'):
        if(currChar == 'a'):
            return 's190'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's190'):
        if(currChar == 't'):
            return 's191'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's191'):
        if(currChar == 'e'):
            return 'PRIVATE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's194'):
        if(currChar == 'p'):
            return 's195'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's195'):
        if(currChar == 'e'):
            return 's196'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's196'):
        if(currChar == 'r'):
            return 's197'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's197'):
        if(currChar == 't'):
            return 's198'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's198'):
        if(currChar == 'y'):
            return 'PROPERTY_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's201'):
        if(currChar == 'a'):
            return 's202'
        elif(currChar == 'e'):
            return 's222'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's202'):
        if(currChar == 'n'):
            return 's203'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's203'):
        if(currChar == 'd'):
            return 's204'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's204'):
        if(currChar == 'D'):
            return 's205'
        elif(currChar == 'F'):
            return 's212'
        elif(currChar == 'I'):
            return 's218'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's205'):
        if(currChar == 'o'):
            return 's206'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's206'):
        if(currChar == 'u'):
            return 's207'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's207'):
        if(currChar == 'b'):
            return 's208'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's208'):
        if(currChar == 'l'):
            return 's209'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's209'):
        if(currChar == 'e'):
            return 'RANDDOUBLE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's212'):
        if(currChar == 'l'):
            return 's213'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's213'):
        if(currChar == 'o'):
            return 's214'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's214'):
        if(currChar == 'a'):
            return 's215'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's215'):
        if(currChar == 't'):
            return 'RANDFLOAT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's218'):
        if(currChar == 'n'):
            return 's219'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's219'):
        if(currChar == 't'):
            return 'RANDINT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's222'):
        if(currChar == 'p'):
            return 's223'
        elif(currChar == 't'):
            return 's228'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's223'):
        if(currChar == 'e'):
            return 's224'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's224'):
        if(currChar == 'a'):
            return 's225'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's225'):
        if(currChar == 't'):
            return 'REPEAT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's228'):
        if(currChar == 'u'):
            return 's229'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's229'):
        if(currChar == 'r'):
            return 's230'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's230'):
        if(currChar == 'n'):
            return 'RETURN_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's233'):
        if(currChar == 'e'):
            return 's234'
        elif(currChar == 'q'):
            return 's237'
        elif(currChar == 't'):
            return 's241'
        elif(currChar == 'w'):
            return 's312'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's234'):
        if(currChar == 't'):
            return 'SET_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's237'):
        if(currChar == 'r'):
            return 's238'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's238'):
        if(currChar == 't'):
            return 'SQRT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's241'):
        if(currChar == 'a'):
            return 's242'
        elif(currChar == 'r'):
            return 's247'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's242'):
        if(currChar == 't'):
            return 's243'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's243'):
        if(currChar == 'i'):
            return 's244'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's244'):
        if(currChar == 'c'):
            return 'STATIC_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's247'):
        if(currChar == '_'):
            return 's248'
        elif(currChar == 'i'):
            return 's308'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's248'):
        if(currChar == 'i'):
            return 's249'
        elif(currChar == 'l'):
            return 's257'
        elif(currChar == 'p'):
            return 's264'
        elif(currChar == 's'):
            return 's288'
        elif(currChar == 't'):
            return 's294'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's249'):
        if(currChar == 's'):
            return 's250'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's250'):
        if(currChar == 'E'):
            return 's251'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's251'):
        if(currChar == 'm'):
            return 's252'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's252'):
        if(currChar == 'p'):
            return 's253'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's253'):
        if(currChar == 't'):
            return 's254'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's254'):
        if(currChar == 'y'):
            return 'STR_ISEMPTY_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's257'):
        if(currChar == 'e'):
            return 's258'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's258'):
        if(currChar == 'n'):
            return 's259'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's259'):
        if(currChar == 'g'):
            return 's260'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's260'):
        if(currChar == 't'):
            return 's261'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's261'):
        if(currChar == 'h'):
            return 'STR_LENGTH_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's264'):
        if(currChar == 'o'):
            return 's265'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's265'):
        if(currChar == 'p'):
            return 's266'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's266'):
        if(currChar == 'A'):
            return 's267'
        elif(currChar == 'D'):
            return 's273'
        elif(currChar == 'S'):
            return 's280'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's267'):
        if(currChar == 'l'):
            return 's268'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's268'):
        if(currChar == 'p'):
            return 's269'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's269'):
        if(currChar == 'h'):
            return 's270'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's270'):
        if(currChar == 'a'):
            return 'STR_POPALPHA_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's273'):
        if(currChar == 'i'):
            return 's274'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's274'):
        if(currChar == 'g'):
            return 's275'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's275'):
        if(currChar == 'i'):
            return 's276'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's276'):
        if(currChar == 't'):
            return 's277'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's277'):
        if(currChar == 's'):
            return 'STR_POPDIGITS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's280'):
        if(currChar == 'p'):
            return 's281'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's281'):
        if(currChar == 'e'):
            return 's282'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's282'):
        if(currChar == 'c'):
            return 's283'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's283'):
        if(currChar == 'i'):
            return 's284'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's284'):
        if(currChar == 'a'):
            return 's285'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's285'):
        if(currChar == 'l'):
            return 'STR_POPSPECIAL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's288'):
        if(currChar == 'l'):
            return 's289'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's289'):
        if(currChar == 'i'):
            return 's290'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's290'):
        if(currChar == 'c'):
            return 's291'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's291'):
        if(currChar == 'e'):
            return 'STR_SLICE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's294'):
        if(currChar == 'o'):
            return 's295'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's295'):
        if(currChar == 'L'):
            return 's296'
        elif(currChar == 'U'):
            return 's302'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's296'):
        if(currChar == 'o'):
            return 's297'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's297'):
        if(currChar == 'w'):
            return 's298'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's298'):
        if(currChar == 'e'):
            return 's299'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's299'):
        if(currChar == 'r'):
            return 'STR_TOLOWER_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's302'):
        if(currChar == 'p'):
            return 's303'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's303'):
        if(currChar == 'p'):
            return 's304'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's304'):
        if(currChar == 'e'):
            return 's305'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's305'):
        if(currChar == 'r'):
            return 'STR_TOUPPER_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's308'):
        if(currChar == 'n'):
            return 's309'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's309'):
        if(currChar == 'g'):
            return 'STRING_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's312'):
        if(currChar == 'i'):
            return 's313'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's313'):
        if(currChar == 't'):
            return 's314'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's314'):
        if(currChar == 'c'):
            return 's315'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's315'):
        if(currChar == 'h'):
            return 'SWITCH_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's318'):
        if(currChar == 'h'):
            return 's319'
        elif(currChar == 'r'):
            return 's323'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's319'):
        if(currChar == 'i'):
            return 's320'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's320'):
        if(currChar == 's'):
            return 'THIS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's323'):
        if(currChar == 'u'):
            return 's324'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's324'):
        if(currChar == 'e'):
            return 'TRUE_CHECK'
        elif(currChar == 'n'):
            return 's327'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's327'):
        if(currChar == 'c'):
            return 'TRUNC_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's330'):
        if(currChar == 'o'):
            return 's331'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's331'):
        if(currChar == 'i'):
            return 's332'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's332'):
        if(currChar == 'd'):
            return 'VOID_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's335'):
        if(currChar == 'h'):
            return 's336'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's336'):
        if(currChar == 'i'):
            return 's337'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's337'):
        if(currChar == 'l'):
            return 's338'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's338'):
        if(currChar == 'e'):
            return 'WHILE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's341'):
        if(currChar == '-'):
            return 'DECREMENT_CHECK'
        elif(currChar == '='):
            return 'MINUS_ASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's347'):
        if(currChar == '='):
            return 'NOT_EQUAL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's351'):
        if(currChar == '='):
            return 'MODULO_ASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's355'):
        if(currChar == '&'):
            return 'LOGICAND_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's362'):
        if(currChar == '='):
            return 'MULT_ASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's372'):
        if(currChar == '*'):
            return 's427'
        elif(currChar == '/'):
            return 's424'
        elif(currChar == '='):
            return 'DIV_ASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's386'):
        if(currChar == ':'):
            return 'SCOPE_ACC_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's396'):
        if(currChar == '|'):
            return 'LOGICOR_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's403'):
        if(currChar == '+'):
            return 'INCREMENT_CHECK'
        elif(currChar == '='):
            return 'ADD_ASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's409'):
        if(currChar == '='):
            return 'LESS_OR_EQUAL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's413'):
        if(currChar == '='):
            return 'GREATER_OR_EQUAL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's417'):
        if(currChar == '='):
            return 'EQUAL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's421'):
        if(currChar == '_'):
            return 's421'
        elif(currChar == 'a'):
            return 's421'
        elif(currChar == 'b'):
            return 's421'
        elif(currChar == 'c'):
            return 's421'
        elif(currChar == 'd'):
            return 's421'
        elif(currChar == 'e'):
            return 's421'
        elif(currChar == 'f'):
            return 's421'
        elif(currChar == 'g'):
            return 's421'
        elif(currChar == 'h'):
            return 's421'
        elif(currChar == 'i'):
            return 's421'
        elif(currChar == 'j'):
            return 's421'
        elif(currChar == 'k'):
            return 's421'
        elif(currChar == 'l'):
            return 's421'
        elif(currChar == 'm'):
            return 's421'
        elif(currChar == 'n'):
            return 's421'
        elif(currChar == 'o'):
            return 's421'
        elif(currChar == 'p'):
            return 's421'
        elif(currChar == 'q'):
            return 's421'
        elif(currChar == 'r'):
            return 's421'
        elif(currChar == 's'):
            return 's421'
        elif(currChar == 't'):
            return 's421'
        elif(currChar == 'u'):
            return 's421'
        elif(currChar == 'v'):
            return 's421'
        elif(currChar == 'w'):
            return 's421'
        elif(currChar == 'x'):
            return 's421'
        elif(currChar == 'y'):
            return 's421'
        elif(currChar == 'z'):
            return 's421'
        elif(currChar == 'A'):
            return 's421'
        elif(currChar == 'B'):
            return 's421'
        elif(currChar == 'C'):
            return 's421'
        elif(currChar == 'D'):
            return 's421'
        elif(currChar == 'E'):
            return 's421'
        elif(currChar == 'F'):
            return 's421'
        elif(currChar == 'G'):
            return 's421'
        elif(currChar == 'H'):
            return 's421'
        elif(currChar == 'I'):
            return 's421'
        elif(currChar == 'J'):
            return 's421'
        elif(currChar == 'K'):
            return 's421'
        elif(currChar == 'L'):
            return 's421'
        elif(currChar == 'M'):
            return 's421'
        elif(currChar == 'N'):
            return 's421'
        elif(currChar == 'O'):
            return 's421'
        elif(currChar == 'P'):
            return 's421'
        elif(currChar == 'Q'):
            return 's421'
        elif(currChar == 'R'):
            return 's421'
        elif(currChar == 'S'):
            return 's421'
        elif(currChar == 'T'):
            return 's421'
        elif(currChar == 'U'):
            return 's421'
        elif(currChar == 'V'):
            return 's421'
        elif(currChar == 'W'):
            return 's421'
        elif(currChar == 'X'):
            return 's421'
        elif(currChar == 'Y'):
            return 's421'
        elif(currChar == 'Z'):
            return 's421'
        elif(currChar == '0'):
            return 's421'
        elif(currChar == '1'):
            return 's421'
        elif(currChar == '2'):
            return 's421'
        elif(currChar == '3'):
            return 's421'
        elif(currChar == '4'):
            return 's421'
        elif(currChar == '5'):
            return 's421'
        elif(currChar == '6'):
            return 's421'
        elif(currChar == '7'):
            return 's421'
        elif(currChar == '8'):
            return 's421'
        elif(currChar == '9'):
            return 's421'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's424'):
        if(currChar == 'a'):
            return 's424'
        elif(currChar == 'b'):
            return 's424'
        elif(currChar == 'c'):
            return 's424'
        elif(currChar == 'd'):
            return 's424'
        elif(currChar == 'e'):
            return 's424'
        elif(currChar == 'f'):
            return 's424'
        elif(currChar == 'g'):
            return 's424'
        elif(currChar == 'h'):
            return 's424'
        elif(currChar == 'i'):
            return 's424'
        elif(currChar == 'j'):
            return 's424'
        elif(currChar == 'k'):
            return 's424'
        elif(currChar == 'l'):
            return 's424'
        elif(currChar == 'm'):
            return 's424'
        elif(currChar == 'n'):
            return 's424'
        elif(currChar == 'o'):
            return 's424'
        elif(currChar == 'p'):
            return 's424'
        elif(currChar == 'q'):
            return 's424'
        elif(currChar == 'r'):
            return 's424'
        elif(currChar == 's'):
            return 's424'
        elif(currChar == 't'):
            return 's424'
        elif(currChar == 'u'):
            return 's424'
        elif(currChar == 'v'):
            return 's424'
        elif(currChar == 'w'):
            return 's424'
        elif(currChar == 'x'):
            return 's424'
        elif(currChar == 'y'):
            return 's424'
        elif(currChar == 'z'):
            return 's424'
        elif(currChar == 'A'):
            return 's424'
        elif(currChar == 'B'):
            return 's424'
        elif(currChar == 'C'):
            return 's424'
        elif(currChar == 'D'):
            return 's424'
        elif(currChar == 'E'):
            return 's424'
        elif(currChar == 'F'):
            return 's424'
        elif(currChar == 'G'):
            return 's424'
        elif(currChar == 'H'):
            return 's424'
        elif(currChar == 'I'):
            return 's424'
        elif(currChar == 'J'):
            return 's424'
        elif(currChar == 'K'):
            return 's424'
        elif(currChar == 'L'):
            return 's424'
        elif(currChar == 'M'):
            return 's424'
        elif(currChar == 'N'):
            return 's424'
        elif(currChar == 'O'):
            return 's424'
        elif(currChar == 'P'):
            return 's424'
        elif(currChar == 'Q'):
            return 's424'
        elif(currChar == 'R'):
            return 's424'
        elif(currChar == 'S'):
            return 's424'
        elif(currChar == 'T'):
            return 's424'
        elif(currChar == 'U'):
            return 's424'
        elif(currChar == 'V'):
            return 's424'
        elif(currChar == 'W'):
            return 's424'
        elif(currChar == 'X'):
            return 's424'
        elif(currChar == 'Y'):
            return 's424'
        elif(currChar == 'Z'):
            return 's424'
        elif(currChar == '0'):
            return 's424'
        elif(currChar == '1'):
            return 's424'
        elif(currChar == '2'):
            return 's424'
        elif(currChar == '3'):
            return 's424'
        elif(currChar == '4'):
            return 's424'
        elif(currChar == '5'):
            return 's424'
        elif(currChar == '6'):
            return 's424'
        elif(currChar == '7'):
            return 's424'
        elif(currChar == '8'):
            return 's424'
        elif(currChar == '9'):
            return 's424'
        elif(currChar == '@'):
            return 's424'
        elif(currChar == '#'):
            return 's424'
        elif(currChar == '$'):
            return 's424'
        elif(currChar == '^'):
            return 's424'
        elif(currChar == '"'):
            return 's424'
        elif(currChar == ','):
            return 's424'
        elif(currChar == '+'):
            return 's424'
        elif(currChar == '-'):
            return 's424'
        elif(currChar == '*'):
            return 's424'
        elif(currChar == '/'):
            return 's424'
        elif(currChar == '%'):
            return 's424'
        elif(currChar == '>'):
            return 's424'
        elif(currChar == '<'):
            return 's424'
        elif(currChar == '!'):
            return 's424'
        elif(currChar == '='):
            return 's424'
        elif(currChar == '&'):
            return 's424'
        elif(currChar == '.'):
            return 's424'
        elif(currChar == '|'):
            return 's424'
        elif(currChar == '('):
            return 's424'
        elif(currChar == ')'):
            return 's424'
        elif(currChar == '['):
            return 's424'
        elif(currChar == ']'):
            return 's424'
        elif(currChar == '?'):
            return 's424'
        elif(currChar == ':'):
            return 's424'
        elif(currChar == ';'):
            return 's424'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's427'):
        if(currChar == '\n'):
            return 's427'
        elif(currChar == '*'):
            return 's428'
        elif(currChar == 'a'):
            return 's427'
        elif(currChar == 'b'):
            return 's427'
        elif(currChar == 'c'):
            return 's427'
        elif(currChar == 'd'):
            return 's427'
        elif(currChar == 'e'):
            return 's427'
        elif(currChar == 'f'):
            return 's427'
        elif(currChar == 'g'):
            return 's427'
        elif(currChar == 'h'):
            return 's427'
        elif(currChar == 'i'):
            return 's427'
        elif(currChar == 'j'):
            return 's427'
        elif(currChar == 'k'):
            return 's427'
        elif(currChar == 'l'):
            return 's427'
        elif(currChar == 'm'):
            return 's427'
        elif(currChar == 'n'):
            return 's427'
        elif(currChar == 'o'):
            return 's427'
        elif(currChar == 'p'):
            return 's427'
        elif(currChar == 'q'):
            return 's427'
        elif(currChar == 'r'):
            return 's427'
        elif(currChar == 's'):
            return 's427'
        elif(currChar == 't'):
            return 's427'
        elif(currChar == 'u'):
            return 's427'
        elif(currChar == 'v'):
            return 's427'
        elif(currChar == 'w'):
            return 's427'
        elif(currChar == 'x'):
            return 's427'
        elif(currChar == 'y'):
            return 's427'
        elif(currChar == 'z'):
            return 's427'
        elif(currChar == 'A'):
            return 's427'
        elif(currChar == 'B'):
            return 's427'
        elif(currChar == 'C'):
            return 's427'
        elif(currChar == 'D'):
            return 's427'
        elif(currChar == 'E'):
            return 's427'
        elif(currChar == 'F'):
            return 's427'
        elif(currChar == 'G'):
            return 's427'
        elif(currChar == 'H'):
            return 's427'
        elif(currChar == 'I'):
            return 's427'
        elif(currChar == 'J'):
            return 's427'
        elif(currChar == 'K'):
            return 's427'
        elif(currChar == 'L'):
            return 's427'
        elif(currChar == 'M'):
            return 's427'
        elif(currChar == 'N'):
            return 's427'
        elif(currChar == 'O'):
            return 's427'
        elif(currChar == 'P'):
            return 's427'
        elif(currChar == 'Q'):
            return 's427'
        elif(currChar == 'R'):
            return 's427'
        elif(currChar == 'S'):
            return 's427'
        elif(currChar == 'T'):
            return 's427'
        elif(currChar == 'U'):
            return 's427'
        elif(currChar == 'V'):
            return 's427'
        elif(currChar == 'W'):
            return 's427'
        elif(currChar == 'X'):
            return 's427'
        elif(currChar == 'Y'):
            return 's427'
        elif(currChar == 'Z'):
            return 's427'
        elif(currChar == '0'):
            return 's427'
        elif(currChar == '1'):
            return 's427'
        elif(currChar == '2'):
            return 's427'
        elif(currChar == '3'):
            return 's427'
        elif(currChar == '4'):
            return 's427'
        elif(currChar == '5'):
            return 's427'
        elif(currChar == '6'):
            return 's427'
        elif(currChar == '7'):
            return 's427'
        elif(currChar == '8'):
            return 's427'
        elif(currChar == '9'):
            return 's427'
        elif(currChar == '@'):
            return 's427'
        elif(currChar == '#'):
            return 's427'
        elif(currChar == '$'):
            return 's427'
        elif(currChar == '^'):
            return 's427'
        elif(currChar == '"'):
            return 's427'
        elif(currChar == ','):
            return 's427'
        elif(currChar == '+'):
            return 's427'
        elif(currChar == '-'):
            return 's427'
        elif(currChar == '/'):
            return 's427'
        elif(currChar == '%'):
            return 's427'
        elif(currChar == '>'):
            return 's427'
        elif(currChar == '<'):
            return 's427'
        elif(currChar == '!'):
            return 's427'
        elif(currChar == '='):
            return 's427'
        elif(currChar == '&'):
            return 's427'
        elif(currChar == '.'):
            return 's427'
        elif(currChar == '|'):
            return 's427'
        elif(currChar == '('):
            return 's427'
        elif(currChar == ')'):
            return 's427'
        elif(currChar == '['):
            return 's427'
        elif(currChar == ']'):
            return 's427'
        elif(currChar == '?'):
            return 's427'
        elif(currChar == ':'):
            return 's427'
        elif(currChar == ';'):
            return 's427'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's428'):
        if(currChar == '/'):
            return 'MULTI_COMMENT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's431'):
        if(currChar == '"'):
            return 'STRING_LIT_CHECK'
        elif(currChar == 'a'):
            return 's431'
        elif(currChar == 'b'):
            return 's431'
        elif(currChar == 'c'):
            return 's431'
        elif(currChar == 'd'):
            return 's431'
        elif(currChar == 'e'):
            return 's431'
        elif(currChar == 'f'):
            return 's431'
        elif(currChar == 'g'):
            return 's431'
        elif(currChar == 'h'):
            return 's431'
        elif(currChar == 'i'):
            return 's431'
        elif(currChar == 'j'):
            return 's431'
        elif(currChar == 'k'):
            return 's431'
        elif(currChar == 'l'):
            return 's431'
        elif(currChar == 'm'):
            return 's431'
        elif(currChar == 'n'):
            return 's431'
        elif(currChar == 'o'):
            return 's431'
        elif(currChar == 'p'):
            return 's431'
        elif(currChar == 'q'):
            return 's431'
        elif(currChar == 'r'):
            return 's431'
        elif(currChar == 's'):
            return 's431'
        elif(currChar == 't'):
            return 's431'
        elif(currChar == 'u'):
            return 's431'
        elif(currChar == 'v'):
            return 's431'
        elif(currChar == 'w'):
            return 's431'
        elif(currChar == 'x'):
            return 's431'
        elif(currChar == 'y'):
            return 's431'
        elif(currChar == 'z'):
            return 's431'
        elif(currChar == 'A'):
            return 's431'
        elif(currChar == 'B'):
            return 's431'
        elif(currChar == 'C'):
            return 's431'
        elif(currChar == 'D'):
            return 's431'
        elif(currChar == 'E'):
            return 's431'
        elif(currChar == 'F'):
            return 's431'
        elif(currChar == 'G'):
            return 's431'
        elif(currChar == 'H'):
            return 's431'
        elif(currChar == 'I'):
            return 's431'
        elif(currChar == 'J'):
            return 's431'
        elif(currChar == 'K'):
            return 's431'
        elif(currChar == 'L'):
            return 's431'
        elif(currChar == 'M'):
            return 's431'
        elif(currChar == 'N'):
            return 's431'
        elif(currChar == 'O'):
            return 's431'
        elif(currChar == 'P'):
            return 's431'
        elif(currChar == 'Q'):
            return 's431'
        elif(currChar == 'R'):
            return 's431'
        elif(currChar == 'S'):
            return 's431'
        elif(currChar == 'T'):
            return 's431'
        elif(currChar == 'U'):
            return 's431'
        elif(currChar == 'V'):
            return 's431'
        elif(currChar == 'W'):
            return 's431'
        elif(currChar == 'X'):
            return 's431'
        elif(currChar == 'Y'):
            return 's431'
        elif(currChar == 'Z'):
            return 's431'
        elif(currChar == '0'):
            return 's431'
        elif(currChar == '1'):
            return 's431'
        elif(currChar == '2'):
            return 's431'
        elif(currChar == '3'):
            return 's431'
        elif(currChar == '4'):
            return 's431'
        elif(currChar == '5'):
            return 's431'
        elif(currChar == '6'):
            return 's431'
        elif(currChar == '7'):
            return 's431'
        elif(currChar == '8'):
            return 's431'
        elif(currChar == '9'):
            return 's431'
        elif(currChar == '@'):
            return 's431'
        elif(currChar == '#'):
            return 's431'
        elif(currChar == '$'):
            return 's431'
        elif(currChar == '^'):
            return 's431'
        elif(currChar == ','):
            return 's431'
        elif(currChar == '+'):
            return 's431'
        elif(currChar == '-'):
            return 's431'
        elif(currChar == '*'):
            return 's431'
        elif(currChar == '/'):
            return 's431'
        elif(currChar == '%'):
            return 's431'
        elif(currChar == '>'):
            return 's431'
        elif(currChar == '<'):
            return 's431'
        elif(currChar == '!'):
            return 's431'
        elif(currChar == '='):
            return 's431'
        elif(currChar == '&'):
            return 's431'
        elif(currChar == '.'):
            return 's431'
        elif(currChar == '|'):
            return 's431'
        elif(currChar == '('):
            return 's431'
        elif(currChar == ')'):
            return 's431'
        elif(currChar == '['):
            return 's431'
        elif(currChar == ']'):
            return 's431'
        elif(currChar == '?'):
            return 's431'
        elif(currChar == ':'):
            return 's431'
        elif(currChar == ';'):
            return 's431'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's434'):
        if(currChar == '\''):
            return 'CHAR_LIT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's437'):
        if(currChar == '0'):
            return 's437'
        elif(currChar == '1'):
            return 's437'
        elif(currChar == '2'):
            return 's437'
        elif(currChar == '3'):
            return 's437'
        elif(currChar == '4'):
            return 's437'
        elif(currChar == '5'):
            return 's437'
        elif(currChar == '6'):
            return 's437'
        elif(currChar == '7'):
            return 's437'
        elif(currChar == '8'):
            return 's437'
        elif(currChar == '9'):
            return 's437'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's470'):
        if(currChar == '.'):
            return 's437'
        elif(currChar == '0'):
            return 's470'
        elif(currChar == '1'):
            return 's470'
        elif(currChar == '2'):
            return 's470'
        elif(currChar == '3'):
            return 's470'
        elif(currChar == '4'):
            return 's470'
        elif(currChar == '5'):
            return 's470'
        elif(currChar == '6'):
            return 's470'
        elif(currChar == '7'):
            return 's470'
        elif(currChar == '8'):
            return 's470'
        elif(currChar == '9'):
            return 's470'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'


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
        if (transition(currState, 'ANY') != 'DEFINED'):
            print('(dbg) delim checking')
            #data type keywords
            if (currState == 'BOOL_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            if (currState == 'CHAR_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            if (currState == 'DOUBLE_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            if (currState == 'FLOAT_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            if (currState == 'INT_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            if (currState == 'LONG_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            if (currState == 'STRING_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            #built-in funcs spit out as identifiers 
            if (currState in builtin_func):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            #break statement
            if (currState == 'BREAK_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # ( symbol
            if (currState == 'OPEN_PAREN_CHECK'):
                if (code[i] in arithmetic_delim + ['\"', '!', ')']):
                    tokens.append((currToken, '('))
                    currToken = ''
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # ) symbol
            if (currState == 'CLOSING_PAREN_CHECK'):
                if (code[i] in closing_delim + [';']):
                    tokens.append((currToken, ')'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # ; symbol
            if (currState == 'SEMICOLON_CHECK'):
                if (code[i] in plaintext_delim + newline + ['}']):
                    tokens.append((currToken, ';'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # - symbol
            if (currState == 'DASH_CHECK'):
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '-'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's341'
            # ! symbol
            if (currState == 'NEGATION_CHECK'):
                if (code[i] in whitespace + alphabetic_chars + ['(']):
                    tokens.append((currToken, '!'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's347'
            # % symbol
            if (currState == 'MODULO_CHECK'):
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '%'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's351'
            # ( symbol
            if (currState == 'OPEN_PAREN_CHECK'):
                if (code[i] in arithmetic_delim + ['\"', '!', ')']):
                    tokens.append((currToken, '('))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # ) symbol
            if (currState == 'CLOSING_PAREN_CHECK'):
                if (code[i] in closing_delim + [';']):
                    tokens.append((currToken, ')'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # * symbol
            if (currState == 'ASTERISK_CHECK'):
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '%'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's362'
            # , symbol
            if (currState == 'COMMA_CHECK'):
                if (code[i] in plaintext_delim):
                    tokens.append((currToken, ','))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # . symbol
            if (currState == 'DOT_CHECK'):
                if (code[i] in alphabetic_chars+whitespace):
                    tokens.append((currToken, '.'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's437'
            # / symbol
            if (currState == 'SLASH_CHECK'):
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '/'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's372'
            # ? symbol
            if (currState == 'QUESTION_CHECK'):
                if (code[i] in plaintext_delim + newline + ['(']):
                    tokens.append((currToken, '?'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # : symbol
            if (currState == 'COLON_CHECK'):
                if (code[i] in plaintext_delim + newline + ['(']):
                    tokens.append((currToken, ':'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's386'
            # [ symbol
            if (currState == 'OPEN_BRACKET_CHECK'):
                if (code[i] in numbers):
                    tokens.append((currToken, '['))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # ] symbol
            if (currState == 'CLOSING_BRACKET_CHECK'):
                if (code[i] in iden_delim):
                    tokens.append((currToken, ']'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # { symbol
            if (currState == 'OPEN_CURLY_CHECK'):
                if (code[i] in plaintext_delim + newline_delim + ['{', '}']):
                    tokens.append((currToken, '{'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # } symbol
            if (currState == 'CLOSING_CURLY_CHECK'):
                if (code[i] in plaintext_delim + newline_delim + [';']):
                    tokens.append((currToken, '}'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # + symbol
            if (currState == 'PLUS_CHECK'):
                if (code[i] in arithmetic_delim + ['\"']):
                    tokens.append((currToken, '+'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's403'
            # < symbol
            if (currState == 'OPEN_ANGLE_CHECK'):
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '<'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's409'
            # > symbol
            if (currState == 'CLOSING_ANGLE_CHECK'):
                if (code[i] in arithmetic_delim + [';']):
                    tokens.append((currToken, '>'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's413'
            # = symbol
            if (currState == 'ASSIGN_CHECK'):
                if (code[i] in arithmetic_delim + ['\"']):
                    tokens.append((currToken, '='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's417'
            # in statement
            if (currState == 'IN_CHECK'):
                if (code[i] == '<'):
                    tokens.append((currToken, 'in'))
                    currToken = ''
                    currState = 's0'
                else:
                    currState = 's147'
            # print statement
            if (currState == 'PRINT_CHECK'):
                if (code[i] in func_delim):
                    tokens.append((currToken, 'print'))
                    currToken = ''
                    currState = 's0'
                else:
                    currState = 's184'
            # println statement
            if (currState == 'PRINTLN_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # private statement
            if (currState == 'PRIVATE_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # property statement
            if (currState == 'PROPERTY_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # repeat statement
            if (currState == 'REPEAT_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # return statement
            if (currState == 'RETURN_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # set statement
            if (currState == 'SET_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # static statement
            if (currState == 'STATIC_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # switch statement
            if (currState == 'SWITCH_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # this statement
            if (currState == 'THIS_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # this statement
            if (currState == 'TRUE_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # void statement
            if (currState == 'VOID_CHECK'):
                if (code[i] in type_iden_delim):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # while statement
            if (currState == 'WHILE_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # -- symbol
            if (currState == 'DECREMENT_CHECK'):
                if (code[i] in whitespace + alphanumeric + [';', ')']):
                    tokens.append((currToken, '--'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # -= symbol
            if (currState == 'MINUS_ASS_CHECK'):
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '-='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # != symbol
            if (currState == 'NOT_EQUAL_CHECK'):
                if (code[i] in whitespace + alphabetic_chars + ['(']):
                    tokens.append((currToken, '!='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # %= symbol
            if (currState == 'MODULO_ASS_CHECK'):
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '%='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # && symbol
            if (currState == 'LOGICAND_CHECK'):
                if (code[i] in plaintext_delim + ['(', '\"']):
                    tokens.append((currToken, '%='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # *= symbol
            if (currState == 'MULT_ASS_CHECK'):
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '*='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # /= symbol
            if (currState == 'DIV_ASS_CHECK'):
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '/='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # :: symbol
            if (currState == 'SCOPE_ACC_CHECK'):
                if (code[i] in plaintext_delim + newline):
                    tokens.append((currToken, '::'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # || symbol
            if (currState == 'LOGICOR_CHECK'):
                if (code[i] in plaintext_delim + ['(', '\"']):
                    tokens.append((currToken, '||'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # ++ symbol
            if (currState == 'INCREMENT_CHECK'):
                if (code[i] in whitespace + alphanumeric + [')', ';']):
                    tokens.append((currToken, '++'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # += symbol
            if (currState == 'ADD_ASS_CHECK'):
                if (code[i] in arithmetic_delim + ['\"']):
                    tokens.append((currToken, '+='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # <= symbol
            if (currState == 'LESS_OR_EQUAL_CHECK'):
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '<='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # >= symbol
            if (currState == 'GREATER_OR_EQUAL_CHECK'):
                if (code[i] in arithmetic_delim):
                    tokens.append((currToken, '>='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # == symbol
            if (currState == 'EQUAL_CHECK'):
                if (code[i] in arithmetic_delim + ['\"']):
                    tokens.append((currToken, '=='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # string literal
            if (currState == 'STRING_LIT_CHECK'):
                if (code[i] in str_lit_delim):
                    tokens.append((currToken, 'string_lit'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # character literal
            if (currState == 'CHAR_LIT_CHECK'):
                if (code[i] in num_delim + newline_delim):
                    tokens.append((currToken, 'char_lit'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # multicomments 
            if (currState == 'MULTI_COMMENT_CHECK'):
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'multi-line comment'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # case statement 
            if (currState == 'CASE_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # class statement 
            if (currState == 'CLASS_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # continue statement 
            if (currState == 'CONTINUE_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # const statement 
            if (currState == 'CONST_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # default statement 
            if (currState == 'DEFAULT_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # do statement 
            if (currState == 'DO_CHECK'):
                if (code[i] in block_delim):
                    tokens.append((currToken, 'do'))
                    currToken = ''
                    currState = 's0'
                else:
                    currState = 's105'
            # else statement 
            if (currState == 'ELSE_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # false statement
            if (currState == 'FALSE_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # for statement
            if (currState == 'FOR_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # get statement
            if (currState == 'GET_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # if statement
            if (currState == 'IF_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # import statement
            if (currState == 'IMPORT_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
            # item statement
            if (currState == 'ITEM_CHECK'):
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
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
        # end of delim checking if statement
#---SPECIAL STATES---
        #identifier state
        if (currState == 's421'):
            print('(dbg) in identifier check state now')
            if (code[i] in iden_delim):
                print('(dbg) correct delim')    
                if (currToken[0] not in alphabetic_chars + ['_']):
                        errors.append(idenFirstError(currToken, currLine, currCol,lineContent))
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
                # errors.append((currToken, f'Lexical Error: In line {currLine}, column {currCol-len(currToken)}; Unexpected \'{code[i]}\' for \'{currToken[:-1]}\'')) #can be expanded with conditions to check what error
                errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                currToken = ''
                currState = 's0'
        #end of identifier looping
        #character lit check
        if (currState == 's434'):
            if (code[i] != '\''):
                if (code[i-1] == '\\'):
                    if (code[i] not in ['\'', '\"', '\\', 't', 'n', 'b']):
                        errors.append(charEscSeqError(currToken, currLine, currCol, lineContent))
                        continue
                elif (code[i-1] != '\''):
                    errors.append(charLengthError(currToken, currLine, currCol, lineContent))
                    continue
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
                else:
                    continue
            if (code[i] in num_delim):
                tokens.append((currToken, 'whole_lit'))
                currToken = ''
                currState = 's0'
            elif (code[i] != '.'):
                currToken += code[i]
                errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                currToken = ''
                currState = 's0'
        #end of whole number
        #fractional part of number
        if (currState == 's437'):
            if (code[i] in numbers):
                currFracCount += 1
                currToken += code[i]
                if (currFracCount > 16): 
                    errors.append(fracPrecError(currToken, currLine, currCol, lineContent))
                else:
                    continue
            if (code[i] in num_delim):
                    tokens.append((currToken, 'frac_lit'))
                    currToken = ''  
                    currState = 's0'
            else:
                currToken += code[i]
                errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                currToken = ''
                currState = 's0'
        #end of fractional number

        #iterating through chars
        #check whitespaces
        if (currState not in ['s431', 's424', 's427']):
            if (code[i] == ' '):
                tokens.append(('\' \' ', 'Space'))
                continue
            if (code[i] == '\n'):
                tokens.append(('\\n', 'New line'))
                continue
        #check states
        if (transition(currState, code[i]) != 'UNDEFINED'):
            print(f'(dbg) in {currState} transitions')  
            currToken += code[i]
            print(f'(dbg) transitioning: {currState} - {code[i]} -> {transition(currState, code[i])}')
            currState = transition(currState, code[i])
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
                        currToken = ''
                        currState == 's0'
                        continue
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
                        currToken = ''
                        currState = 's0'
                    else:
                        print("(dbg) other iden append")
                        tokens.append((currToken, 'Identifier'))
                        currToken = code[i]
                        currState = transition('s0', code[i])
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent))
                    currToken = ''
                    currState = 's0'
    
    lexerResults = [tokens, errors] 
    return lexerResults

#---LEXER ERRORS---
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
    lexres = lexer(code)
    # print(lexres)
    return jsonify(lexres)

if __name__ == '__main__':
    app.run(debug=True) 