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
arithmetic_delim = plaintext_delim + ['(', '-' , '\n']
str_lit_delim = whitespace + ['+', ')', ',', ';', '\n']
newline_delim = [' ', '\n']
index_delim = [']', '\n'] + digit
default_delim = whitespace + newline_delim + [':']
type_iden_delim = [')', ' ', '\n', '>', '[']
get_set_delim = newline_delim + ['{', ';']

# identifier delim
iden_delim = ['"',',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '.', '|', '(', ')', '[', ']', '?', ':', ';', '{'] + newline_delim
closing_delim = arithmetic_operator + relational_operator + whitespace + logical_operator + assignment_operator + ['&', '|', '{', '(', ')', ';', '\n', ',']

# literals delim
num_delim = arithmetic_operator + whitespace + relational_operator + [',', ')', ']', '}', '=', ';'] + newline
string_delim = newline_delim + ['+', ';']
bool_delim = whitespace + logical_operator + [';', ',', ')', '=', '!', '\n']

# control flow delim
loop_delim = newline_delim+ whitespace + ['(']
block_delim = newline_delim+whitespace+['{']

# methods delim
func_delim = newline_delim + ['(']

# other delim
single_delim = newline
comment_delim = ascii + whitespace


def transition(currState, currChar):
    if (currState == 's0'):
        if(currChar == 'b'):
            return 's1'
        elif(currChar == 'c'):
            return 's11'
        elif(currChar == 'd'):
            return 's36'
        elif(currChar == 'e'):
            return 's51'
        elif(currChar == 'f'):
            return 's56'
        elif(currChar == 'g'):
            return 's70'
        elif(currChar == 'i'):
            return 's74'
        elif(currChar == 'l'):
            return 's91'
        elif(currChar == 'p'):
            return 's96'
        elif(currChar == 'r'):
            return 's117'
        elif(currChar == 's'):
            return 's129'
        elif(currChar == 't'):
            return 's150'
        elif(currChar == 'v'):
            return 's159'
        elif(currChar == 'w'):
            return 's164'
        elif(currChar == '-'):
            return 'DASH_CHECK'
        elif(currChar == '!'):
            return 'NEGATION_CHECK'
        elif(currChar == '%'):
            return 'MODULO_CHECK'
        elif(currChar == '&'):
            return 's184'
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
            return 's223'
        elif(currChar == '"'):
            return 's258'
        elif(currChar == '+'):
            return 'PLUS_CHECK'
        elif(currChar == '<'):
            return 'OPEN_ANGLE_CHECK'
        elif(currChar == '>'):
            return 'CLOSING_ANGLE_CHECK'
        elif(currChar == '='):
            return 'ASSIGN_CHECK'
        elif(currChar == '\''):
            return 's261'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's1'):
        if(currChar == 'o'):
            return 's2'
        elif(currChar == 'r'):
            return 's6'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's2'):
        if(currChar == 'o'):
            return 's3'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's3'):
        if(currChar == 'l'):
            return 'BOOL_CHECK'
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
        if(currChar == 'e'):
            return 's7'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's7'):
        if(currChar == 'a'):
            return 's8'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's8'):
        if(currChar == 'k'):
            return 'BREAK_CHECK'
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
        if(currChar == 'a'):
            return 's12'
        elif(currChar == 'h'):
            return 's16'
        elif(currChar == 'l'):
            return 's20'
        elif(currChar == 'o'):
            return 's25'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's12'):
        if(currChar == 's'):
            return 's13'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's13'):
        if(currChar == 'e'):
            return 'CASE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's16'):
        if(currChar == 'a'):
            return 's17'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's17'):
        if(currChar == 'r'):
            return 'CHAR_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's20'):
        if(currChar == 'a'):
            return 's21'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's21'):
        if(currChar == 's'):
            return 's22'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's22'):
        if(currChar == 's'):
            return 'CLASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's25'):
        if(currChar == 'n'):
            return 's26'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's26'):
        if(currChar == 't'):
            return 's27'
        elif(currChar == 's'):
            return 's33'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's27'):
        if(currChar == 'i'):
            return 's28'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's28'):
        if(currChar == 'n'):
            return 's29'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's29'):
        if(currChar == 'u'):
            return 's30'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's30'):
        if(currChar == 'e'):
            return 'CONTINUE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's33'):
        if(currChar == 't'):
            return 'CONST_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's36'):
        if(currChar == 'e'):
            return 's37'
        elif(currChar == 'o'):
            return 'DO_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's37'):
        if(currChar == 'f'):
            return 's38'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's38'):
        if(currChar == 'a'):
            return 's39'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's39'):
        if(currChar == 'u'):
            return 's40'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's40'):
        if(currChar == 'l'):
            return 's41'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's41'):
        if(currChar == 't'):
            return 'DEFAULT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's44'):
        if(currChar == 'u'):
            return 's46'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's46'):
        if(currChar == 'b'):
            return 's47'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's47'):
        if(currChar == 'l'):
            return 's48'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's48'):
        if(currChar == 'e'):
            return 'DOUBLE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's51'):
        if(currChar == 'l'):
            return 's52'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's52'):
        if(currChar == 's'):
            return 's53'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's53'):
        if(currChar == 'e'):
            return 'ELSE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's56'):
        if(currChar == 'a'):
            return 's57'
        elif(currChar == 'l'):
            return 's62'
        elif(currChar == 'o'):
            return 's67'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's57'):
        if(currChar == 'l'):
            return 's58'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's58'):
        if(currChar == 's'):
            return 's58'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's59'):
        if(currChar == 'e'):
            return 'FALSE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's62'):
        if(currChar == 'o'):
            return 's63'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's63'):
        if(currChar == 'a'):
            return 's64'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's64'):
        if(currChar == 't'):
            return 'FLOAT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's67'):
        if(currChar == 'r'):
            return 'FOR_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's70'):
        if(currChar == 'e'):
            return 's71'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's71'):
        if(currChar == 't'):
            return 'GET_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's74'):
        print("(dbg) in s74 now")
        if(currChar == 'f'):
            return 'IF_CHECK'
        elif(currChar == 'm'):
            return 's77'
        elif(currChar == 'n'):
            return 'IN_CHECK'
        elif(currChar == 't'):
            return 's87'
        elif (currChar == 'ANY'):
            print("(dbg) any defined s74")
            return 'DEFINED'
        else:
            print("(dbg) undefined s74 next ")
            return 'UNDEFINED'
    elif (currState == 's77'):
        if(currChar == 'p'):
            return 's78'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's78'):
        if(currChar == 'o'):
            return 's79'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's79'):
        if(currChar == 'r'):
            return 's80'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's80'):
        if(currChar == 't'):
            return 'IMPORT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's83'):
        if(currChar == 't'):
            return 'INT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's87'):
        if(currChar == 'e'):
            return 's88'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's88'):
        if(currChar == 'm'):
            return 'ITEM_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's91'):
        if(currChar == 'o'):
            return 's92'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's92'):
        if(currChar == 'n'):
            return 's93'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's93'):
        if(currChar == 'g'):
            return 'LONG_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's96'):
        if(currChar == 'r'):
            return 's97'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's97'):
        if(currChar == 'i'):
            return 's98'
        elif(currChar == 'o'):
            return 's110'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's98'):
        if(currChar == 'n'):
            return 's99'
        elif(currChar == 'v'):
            return 's105'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's99'):
        if(currChar == 't'):
            return 'PRINT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's100'):
        if(currChar == 'l'):
            return 's102'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's102'):
        if(currChar == 'n'):
            return 'PRINTLN_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's105'):
        if(currChar == 'a'):
            return 's106'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's106'):
        if(currChar == 't'):
            return 's107'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's107'):
        if(currChar == 'e'):
            return 'PRIVATE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's110'):
        if(currChar == 'p'):
            return 's111'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's111'):
        if(currChar == 'e'):
            return 's112'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's112'):
        if(currChar == 'r'):
            return 's113'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's113'):
        if(currChar == 't'):
            return 's114'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's114'):
        if(currChar == 'y'):
            return 'PROPERTY_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's117'):
        if(currChar == 'e'):
            return 's118'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's118'):
        if(currChar == 'p'):
            return 's119'
        elif(currChar == 't'):
            return 's124'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's119'):
        if(currChar == 'e'):
            return 's120'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's120'):
        if(currChar == 'a'):
            return 's121'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's121'):
        if(currChar == 't'):
            return 'REPEAT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's124'):
        if(currChar == 'u'):
            return 's125'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's125'):
        if(currChar == 'r'):
            return 's126'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's126'):
        if(currChar == 'n'):
            return 'RETURN_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's129'):
        if(currChar == 'e'):
            return 's130'
        elif(currChar == 't'):
            return 's133'
        elif(currChar == 'w'):
            return 's144'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's130'):
        if(currChar == 't'):
            return 'SET_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's133'):
        if(currChar == 'a'):
            return 's134'
        elif(currChar == 'r'):
            return 's139'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's134'):
        if(currChar == 't'):
            return 's135'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's135'):
        if(currChar == 'i'):
            return 's136'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's136'):
        if(currChar == 'c'):
            return 'STATIC_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's139'):
        if(currChar == 'i'):
            return 's140'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's140'):
        if(currChar == 'n'):
            return 's141'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's141'):
        if(currChar == 'g'):
            return 'STRING_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's144'):
        if(currChar == 'i'):
            return 's145'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's145'):
        if(currChar == 't'):
            return 's146'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's146'):
        if(currChar == 'c'):
            return 's147'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's147'):
        if(currChar == 'h'):
            return 'SWITCH_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's150'):
        if(currChar == 'h'):
            return 's151'
        elif(currChar == 'r'):
            return 's155'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's151'):
        if(currChar == 'i'):
            return 's152'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's152'):
        if(currChar == 's'):
            return 'THIS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's155'):
        if(currChar == 'u'):
            return 's156'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's156'):
        if(currChar == 'e'):
            return 'TRUE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's159'):
        if(currChar == 'o'):
            return 's160'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's160'):
        if(currChar == 'i'):
            return 's161'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's161'):
        if(currChar == 'd'):
            return 'VOID_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's164'):
        if(currChar == 'h'):
            return 's165'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's165'):
        if(currChar == 'i'):
            return 's166'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's166'):
        if(currChar == 'l'):
            return 's167'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's167'):
        if(currChar == 'e'):
            return 'WHILE_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's170'):
        if(currChar == '-'):
            return 'DECREMENT_CHECK'
        elif(currChar == '='):
            return 'MINUS_ASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's178'):
        if(currChar == '='):
            return 'NOT_EQUAL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's180'):
        if(currChar == '='):
            return 'MODULO_ASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's184'):
        if(currChar == '&'):
            return 'LOGICAND_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's191'):
        if(currChar == '='):
            return 'MULT_ASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's201'):
        if(currChar == '*'):
            return 's254'
        elif(currChar == '/'):
            return 's251'
        elif(currChar == '='):
            return 'DIV_ASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's223'):
        if(currChar == '|'):
            return 'LOGICOR_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's230'):
        if(currChar == '+'):
            return 'INCREMENT_CHECK'
        elif(currChar == '='):
            return 'ADD_ASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's236'):
        if(currChar == '='):
            return 'LESS_OR_EQUAL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's240'):
        if(currChar == '='):
            return 'GREATER_OR_EQUAL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's244'):
        if(currChar == '='):
            return 'EQUAL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's248'):
        if(currChar == '_'):
            return 's248'
        elif(currChar == 'a'):
            return 's248'
        elif(currChar == 'b'):
            return 's248'
        elif(currChar == 'c'):
            return 's248'
        elif(currChar == 'd'):
            return 's248'
        elif(currChar == 'e'):
            return 's248'
        elif(currChar == 'f'):
            return 's248'
        elif(currChar == 'g'):
            return 's248'
        elif(currChar == 'h'):
            return 's248'
        elif(currChar == 'i'):
            return 's248'
        elif(currChar == 'j'):
            return 's248'
        elif(currChar == 'k'):
            return 's248'
        elif(currChar == 'l'):
            return 's248'
        elif(currChar == 'm'):
            return 's248'
        elif(currChar == 'n'):
            return 's248'
        elif(currChar == 'o'):
            return 's248'
        elif(currChar == 'p'):
            return 's248'
        elif(currChar == 'q'):
            return 's248'
        elif(currChar == 'r'):
            return 's248'
        elif(currChar == 's'):
            return 's248'
        elif(currChar == 't'):
            return 's248'
        elif(currChar == 'u'):
            return 's248'
        elif(currChar == 'v'):
            return 's248'
        elif(currChar == 'w'):
            return 's248'
        elif(currChar == 'x'):
            return 's248'
        elif(currChar == 'y'):
            return 's248'
        elif(currChar == 'z'):
            return 's248'
        elif(currChar == 'A'):
            return 's248'
        elif(currChar == 'B'):
            return 's248'
        elif(currChar == 'C'):
            return 's248'
        elif(currChar == 'D'):
            return 's248'
        elif(currChar == 'E'):
            return 's248'
        elif(currChar == 'F'):
            return 's248'
        elif(currChar == 'G'):
            return 's248'
        elif(currChar == 'H'):
            return 's248'
        elif(currChar == 'I'):
            return 's248'
        elif(currChar == 'J'):
            return 's248'
        elif(currChar == 'K'):
            return 's248'
        elif(currChar == 'L'):
            return 's248'
        elif(currChar == 'M'):
            return 's248'
        elif(currChar == 'N'):
            return 's248'
        elif(currChar == 'O'):
            return 's248'
        elif(currChar == 'P'):
            return 's248'
        elif(currChar == 'Q'):
            return 's248'
        elif(currChar == 'R'):
            return 's248'
        elif(currChar == 'S'):
            return 's248'
        elif(currChar == 'T'):
            return 's248'
        elif(currChar == 'U'):
            return 's248'
        elif(currChar == 'V'):
            return 's248'
        elif(currChar == 'W'):
            return 's248'
        elif(currChar == 'X'):
            return 's248'
        elif(currChar == 'Y'):
            return 's248'
        elif(currChar == 'Z'):
            return 's248'
        elif(currChar == '0'):
            return 's248'
        elif(currChar == '1'):
            return 's248'
        elif(currChar == '2'):
            return 's248'
        elif(currChar == '3'):
            return 's248'
        elif(currChar == '4'):
            return 's248'
        elif(currChar == '5'):
            return 's248'
        elif(currChar == '6'):
            return 's248'
        elif(currChar == '7'):
            return 's248'
        elif(currChar == '8'):
            return 's248'
        elif(currChar == '9'):
            return 's248'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's251'):
        if(currChar == 'a'):
            return 's251'
        elif(currChar == 'b'):
            return 's251'
        elif(currChar == 'c'):
            return 's251'
        elif(currChar == 'd'):
            return 's251'
        elif(currChar == 'e'):
            return 's251'
        elif(currChar == 'f'):
            return 's251'
        elif(currChar == 'g'):
            return 's251'
        elif(currChar == 'h'):
            return 's251'
        elif(currChar == 'i'):
            return 's251'
        elif(currChar == 'j'):
            return 's251'
        elif(currChar == 'k'):
            return 's251'
        elif(currChar == 'l'):
            return 's251'
        elif(currChar == 'm'):
            return 's251'
        elif(currChar == 'n'):
            return 's251'
        elif(currChar == 'o'):
            return 's251'
        elif(currChar == 'p'):
            return 's251'
        elif(currChar == 'q'):
            return 's251'
        elif(currChar == 'r'):
            return 's251'
        elif(currChar == 's'):
            return 's251'
        elif(currChar == 't'):
            return 's251'
        elif(currChar == 'u'):
            return 's251'
        elif(currChar == 'v'):
            return 's251'
        elif(currChar == 'w'):
            return 's251'
        elif(currChar == 'x'):
            return 's251'
        elif(currChar == 'y'):
            return 's251'
        elif(currChar == 'z'):
            return 's251'
        elif(currChar == 'A'):
            return 's251'
        elif(currChar == 'B'):
            return 's251'
        elif(currChar == 'C'):
            return 's251'
        elif(currChar == 'D'):
            return 's251'
        elif(currChar == 'E'):
            return 's251'
        elif(currChar == 'F'):
            return 's251'
        elif(currChar == 'G'):
            return 's251'
        elif(currChar == 'H'):
            return 's251'
        elif(currChar == 'I'):
            return 's251'
        elif(currChar == 'J'):
            return 's251'
        elif(currChar == 'K'):
            return 's251'
        elif(currChar == 'L'):
            return 's251'
        elif(currChar == 'M'):
            return 's251'
        elif(currChar == 'N'):
            return 's251'
        elif(currChar == 'O'):
            return 's251'
        elif(currChar == 'P'):
            return 's251'
        elif(currChar == 'Q'):
            return 's251'
        elif(currChar == 'R'):
            return 's251'
        elif(currChar == 'S'):
            return 's251'
        elif(currChar == 'T'):
            return 's251'
        elif(currChar == 'U'):
            return 's251'
        elif(currChar == 'V'):
            return 's251'
        elif(currChar == 'W'):
            return 's251'
        elif(currChar == 'X'):
            return 's251'
        elif(currChar == 'Y'):
            return 's251'
        elif(currChar == 'Z'):
            return 's251'
        elif(currChar == '0'):
            return 's251'
        elif(currChar == '1'):
            return 's251'
        elif(currChar == '2'):
            return 's251'
        elif(currChar == '3'):
            return 's251'
        elif(currChar == '4'):
            return 's251'
        elif(currChar == '5'):
            return 's251'
        elif(currChar == '6'):
            return 's251'
        elif(currChar == '7'):
            return 's251'
        elif(currChar == '8'):
            return 's251'
        elif(currChar == '9'):
            return 's251'
        elif(currChar == '@'):
            return 's251'
        elif(currChar == '#'):
            return 's251'
        elif(currChar == '$'):
            return 's251'
        elif(currChar == '^'):
            return 's251'
        elif(currChar == '"'):
            return 's251'
        elif(currChar == ','):
            return 's251'
        elif(currChar == '+'):
            return 's251'
        elif(currChar == '-'):
            return 's251'
        elif(currChar == '*'):
            return 's251'
        elif(currChar == '/'):
            return 's251'
        elif(currChar == '%'):
            return 's251'
        elif(currChar == '>'):
            return 's251'
        elif(currChar == '<'):
            return 's251'
        elif(currChar == '!'):
            return 's251'
        elif(currChar == '='):
            return 's251'
        elif(currChar == '&'):
            return 's251'
        elif(currChar == '.'):
            return 's251'
        elif(currChar == '|'):
            return 's251'
        elif(currChar == '('):
            return 's251'
        elif(currChar == ')'):
            return 's251'
        elif(currChar == '['):
            return 's251'
        elif(currChar == ']'):
            return 's251'
        elif(currChar == '?'):
            return 's251'
        elif(currChar == ':'):
            return 's251'
        elif(currChar == ';'):
            return 's251'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's254'):
        if(currChar == '\n'):
            return 's254'
        elif(currChar == '*'):
            return 's255'
        elif(currChar == 'a'):
            return 's254'
        elif(currChar == 'b'):
            return 's254'
        elif(currChar == 'c'):
            return 's254'
        elif(currChar == 'd'):
            return 's254'
        elif(currChar == 'e'):
            return 's254'
        elif(currChar == 'f'):
            return 's254'
        elif(currChar == 'g'):
            return 's254'
        elif(currChar == 'h'):
            return 's254'
        elif(currChar == 'i'):
            return 's254'
        elif(currChar == 'j'):
            return 's254'
        elif(currChar == 'k'):
            return 's254'
        elif(currChar == 'l'):
            return 's254'
        elif(currChar == 'm'):
            return 's254'
        elif(currChar == 'n'):
            return 's254'
        elif(currChar == 'o'):
            return 's254'
        elif(currChar == 'p'):
            return 's254'
        elif(currChar == 'q'):
            return 's254'
        elif(currChar == 'r'):
            return 's254'
        elif(currChar == 's'):
            return 's254'
        elif(currChar == 't'):
            return 's254'
        elif(currChar == 'u'):
            return 's254'
        elif(currChar == 'v'):
            return 's254'
        elif(currChar == 'w'):
            return 's254'
        elif(currChar == 'x'):
            return 's254'
        elif(currChar == 'y'):
            return 's254'
        elif(currChar == 'z'):
            return 's254'
        elif(currChar == 'A'):
            return 's254'
        elif(currChar == 'B'):
            return 's254'
        elif(currChar == 'C'):
            return 's254'
        elif(currChar == 'D'):
            return 's254'
        elif(currChar == 'E'):
            return 's254'
        elif(currChar == 'F'):
            return 's254'
        elif(currChar == 'G'):
            return 's254'
        elif(currChar == 'H'):
            return 's254'
        elif(currChar == 'I'):
            return 's254'
        elif(currChar == 'J'):
            return 's254'
        elif(currChar == 'K'):
            return 's254'
        elif(currChar == 'L'):
            return 's254'
        elif(currChar == 'M'):
            return 's254'
        elif(currChar == 'N'):
            return 's254'
        elif(currChar == 'O'):
            return 's254'
        elif(currChar == 'P'):
            return 's254'
        elif(currChar == 'Q'):
            return 's254'
        elif(currChar == 'R'):
            return 's254'
        elif(currChar == 'S'):
            return 's254'
        elif(currChar == 'T'):
            return 's254'
        elif(currChar == 'U'):
            return 's254'
        elif(currChar == 'V'):
            return 's254'
        elif(currChar == 'W'):
            return 's254'
        elif(currChar == 'X'):
            return 's254'
        elif(currChar == 'Y'):
            return 's254'
        elif(currChar == 'Z'):
            return 's254'
        elif(currChar == '0'):
            return 's254'
        elif(currChar == '1'):
            return 's254'
        elif(currChar == '2'):
            return 's254'
        elif(currChar == '3'):
            return 's254'
        elif(currChar == '4'):
            return 's254'
        elif(currChar == '5'):
            return 's254'
        elif(currChar == '6'):
            return 's254'
        elif(currChar == '7'):
            return 's254'
        elif(currChar == '8'):
            return 's254'
        elif(currChar == '9'):
            return 's254'
        elif(currChar == '@'):
            return 's254'
        elif(currChar == '#'):
            return 's254'
        elif(currChar == '$'):
            return 's254'
        elif(currChar == '^'):
            return 's254'
        elif(currChar == '"'):
            return 's254'
        elif(currChar == ','):
            return 's254'
        elif(currChar == '+'):
            return 's254'
        elif(currChar == '-'):
            return 's254'
        elif(currChar == '/'):
            return 's254'
        elif(currChar == '%'):
            return 's254'
        elif(currChar == '>'):
            return 's254'
        elif(currChar == '<'):
            return 's254'
        elif(currChar == '!'):
            return 's254'
        elif(currChar == '='):
            return 's254'
        elif(currChar == '&'):
            return 's254'
        elif(currChar == '.'):
            return 's254'
        elif(currChar == '|'):
            return 's254'
        elif(currChar == '('):
            return 's254'
        elif(currChar == ')'):
            return 's254'
        elif(currChar == '['):
            return 's254'
        elif(currChar == ']'):
            return 's254'
        elif(currChar == '?'):
            return 's254'
        elif(currChar == ':'):
            return 's254'
        elif(currChar == ';'):
            return 's254'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's255'):
        if(currChar == '/'):
            return 'MULTI_COMMENT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's258'):
        if(currChar == '"'):
            return 'STRING_LIT_CHECK'
        elif(currChar == 'a'):
            return 's258'
        elif(currChar == 'b'):
            return 's258'
        elif(currChar == 'c'):
            return 's258'
        elif(currChar == 'd'):
            return 's258'
        elif(currChar == 'e'):
            return 's258'
        elif(currChar == 'f'):
            return 's258'
        elif(currChar == 'g'):
            return 's258'
        elif(currChar == 'h'):
            return 's258'
        elif(currChar == 'i'):
            return 's258'
        elif(currChar == 'j'):
            return 's258'
        elif(currChar == 'k'):
            return 's258'
        elif(currChar == 'l'):
            return 's258'
        elif(currChar == 'm'):
            return 's258'
        elif(currChar == 'n'):
            return 's258'
        elif(currChar == 'o'):
            return 's258'
        elif(currChar == 'p'):
            return 's258'
        elif(currChar == 'q'):
            return 's258'
        elif(currChar == 'r'):
            return 's258'
        elif(currChar == 's'):
            return 's258'
        elif(currChar == 't'):
            return 's258'
        elif(currChar == 'u'):
            return 's258'
        elif(currChar == 'v'):
            return 's258'
        elif(currChar == 'w'):
            return 's258'
        elif(currChar == 'x'):
            return 's258'
        elif(currChar == 'y'):
            return 's258'
        elif(currChar == 'z'):
            return 's258'
        elif(currChar == 'A'):
            return 's258'
        elif(currChar == 'B'):
            return 's258'
        elif(currChar == 'C'):
            return 's258'
        elif(currChar == 'D'):
            return 's258'
        elif(currChar == 'E'):
            return 's258'
        elif(currChar == 'F'):
            return 's258'
        elif(currChar == 'G'):
            return 's258'
        elif(currChar == 'H'):
            return 's258'
        elif(currChar == 'I'):
            return 's258'
        elif(currChar == 'J'):
            return 's258'
        elif(currChar == 'K'):
            return 's258'
        elif(currChar == 'L'):
            return 's258'
        elif(currChar == 'M'):
            return 's258'
        elif(currChar == 'N'):
            return 's258'
        elif(currChar == 'O'):
            return 's258'
        elif(currChar == 'P'):
            return 's258'
        elif(currChar == 'Q'):
            return 's258'
        elif(currChar == 'R'):
            return 's258'
        elif(currChar == 'S'):
            return 's258'
        elif(currChar == 'T'):
            return 's258'
        elif(currChar == 'U'):
            return 's258'
        elif(currChar == 'V'):
            return 's258'
        elif(currChar == 'W'):
            return 's258'
        elif(currChar == 'X'):
            return 's258'
        elif(currChar == 'Y'):
            return 's258'
        elif(currChar == 'Z'):
            return 's258'
        elif(currChar == '0'):
            return 's258'
        elif(currChar == '1'):
            return 's258'
        elif(currChar == '2'):
            return 's258'
        elif(currChar == '3'):
            return 's258'
        elif(currChar == '4'):
            return 's258'
        elif(currChar == '5'):
            return 's258'
        elif(currChar == '6'):
            return 's258'
        elif(currChar == '7'):
            return 's258'
        elif(currChar == '8'):
            return 's258'
        elif(currChar == '9'):
            return 's258'
        elif(currChar == '@'):
            return 's258'
        elif(currChar == '#'):
            return 's258'
        elif(currChar == '$'):
            return 's258'
        elif(currChar == '^'):
            return 's258'
        elif(currChar == ','):
            return 's258'
        elif(currChar == '+'):
            return 's258'
        elif(currChar == '-'):
            return 's258'
        elif(currChar == '*'):
            return 's258'
        elif(currChar == '/'):
            return 's258'
        elif(currChar == '%'):
            return 's258'
        elif(currChar == '>'):
            return 's258'
        elif(currChar == '<'):
            return 's258'
        elif(currChar == '!'):
            return 's258'
        elif(currChar == '='):
            return 's258'
        elif(currChar == '&'):
            return 's258'
        elif(currChar == '.'):
            return 's258'
        elif(currChar == '|'):
            return 's258'
        elif(currChar == '('):
            return 's258'
        elif(currChar == ')'):
            return 's258'
        elif(currChar == '['):
            return 's258'
        elif(currChar == ']'):
            return 's258'
        elif(currChar == '?'):
            return 's258'
        elif(currChar == ':'):
            return 's258'
        elif(currChar == ';'):
            return 's258'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's261'):
        if(currChar == '\''):
            return 'CHAR_LIT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's264'):
        if(currChar == '0'):
            return 's264'
        elif(currChar == '1'):
            return 's264'
        elif(currChar == '2'):
            return 's264'
        elif(currChar == '3'):
            return 's264'
        elif(currChar == '4'):
            return 's264'
        elif(currChar == '5'):
            return 's264'
        elif(currChar == '6'):
            return 's264'
        elif(currChar == '7'):
            return 's264'
        elif(currChar == '8'):
            return 's264'
        elif(currChar == '9'):
            return 's264'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's297'):
        if(currChar == '.'):
            return 's264'
        elif(currChar == '0'):
            return 's297'
        elif(currChar == '1'):
            return 's297'
        elif(currChar == '2'):
            return 's297'
        elif(currChar == '3'):
            return 's297'
        elif(currChar == '4'):
            return 's297'
        elif(currChar == '5'):
            return 's297'
        elif(currChar == '6'):
            return 's297'
        elif(currChar == '7'):
            return 's297'
        elif(currChar == '8'):
            return 's297'
        elif(currChar == '9'):
            return 's297'
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
    for i in range(len(code)): #need index for later
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
                if (code[i] in whitespace + alphanumeric + [')', ';', '\n']):
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
                        currState = transition('s0', code[i])
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
