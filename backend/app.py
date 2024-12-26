from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # cross-origin requests

#---DEFINITIONS---
alpha_small = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alpha_capital = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
alphabetic_chars = alpha_small + alpha_capital
symbols = ['"',',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '.', '|', '(', ')', '[', ']', '?', ':', ';']
whitespace = [' ']

zero = ['0']
digit = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
numbers = zero + digit

alphanum = alphabetic_chars + numbers
basic_punctuation_symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '{', '}', '\\', '|', ':', ';', '\'', '\"', ',', '<', '>', '.', '/', '?']
ascii = alphanum + basic_punctuation_symbols

arithmetic_operator = ['+', '-', '*', '/', '%']
relational_operator = ['>', '<', '==', '<=', '>=', '!=']
logical_operator = ['!', '&&', '||']
unary_operator = ['++', '-', '--']
assignment_operator = ['=', '+=', '-=', '*=', '/=']

newline = ['\n']

plaintext_delim = whitespace + alphanum
equal_delim = newline + whitespace + ['=', '/']
arithmetic_delim = newline + plaintext_delim + ['(', '/']
relational_operator_delim = ['<', '>', '=', '!']
logical_operator_delim = ['!', '&', '|']
newline_delim = newline + whitespace
default_delim = newline + whitespace + [':', '/']
type_iden_delim = newline + whitespace + ['[', '>', '/']
get_set_delim = newline + whitespace + ['{', ';', '/']
open_paren_delim = arithmetic_delim + ['\"', '!', ')', '\n', '/']
closing_delim = arithmetic_operator + arithmetic_delim + logical_operator_delim + newline_delim + relational_operator_delim + whitespace + ['=', '|', '{', ';', ')', '(', '/', ':', ']', '?']
close_paren_delim = closing_delim + [';', '/']
semicolon_delim = newline_delim + plaintext_delim + ['}', '/']
negative_delim = arithmetic_delim + ['/', '+']
exclamation_delim = alphanum + newline + whitespace + ['(', '/', '!']
percent_delim = arithmetic_delim + ['/']
asterisk_delim = arithmetic_delim + ['/', '+', '-']
comma_delim = dot_delim = plaintext_delim + ['\n', '/']
slash_delim = plaintext_delim + ['\n', '(', '+', '-']
question_delim = newline + plaintext_delim + ['(', '/', '\"']
colon_delim = newline + plaintext_delim + ['(', '/', '\"']
open_bracket_delim = alphanum + whitespace + ['\n', ']', '/', '(']
open_curly_delim = newline_delim + plaintext_delim + ['{', '}', '/']
close_curly_delim = newline_delim + plaintext_delim + [';', '/', ',', '}']
plus_delim = arithmetic_delim + ['\"', '/', '-']
less_than_delim = greater_than_delim = arithmetic_delim + newline + ['/']
equal_delim = arithmetic_delim + ['\"', '/', '!', '!']
in_delim = newline_delim + ['<', '/']
this_delim = newline_delim + ['.', '/']
void_delim = newline + whitespace + ['/']
decrement_delim = alphanum + whitespace + newline + [';', ')', '/', '+', '*', '%', '(']
subtract_assign_delim = arithmetic_delim + ['/']
not_equal_delim = alphanum + newline + whitespace + ['(', '!','\"']
modulo_assign_delim = arithmetic_delim + ['/', '+', '-']
and_delim = plaintext_delim + ['(', '\"', '\n', '/', '!']
multi_assign_delim = arithmetic_delim + ['/']
divi_assign_delim = arithmetic_delim + ['/']
or_delim = plaintext_delim + ['(', '\"', '\n', '/', '!']
increment_delim = alphanum + newline_delim + [')', ';', '/', '-', '*', '%', '(']
add_assign_delim = arithmetic_delim + ['/', '\"']
less_equal_delim = greater_equal_delim = arithmetic_delim + ['/']
equal_equal_delim = arithmetic_delim + ['\"', '/', '!']
import_delim = newline + whitespace + ['<', '/']
loop_delim = whitespace + newline + ['(', '/']
block_delim = whitespace + newline + ['{', '/']
break_delim = return_delim = continue_delim = newline_delim + [';']
case_delim = newline_delim + ['(']
iden_delim = newline_delim + [',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '.', '|', '(', ')', '[', ']', '{', '?', ':', ';']
str_lit_delim = newline + whitespace + logical_operator_delim + ['+', ')', ',', ';', '/', ':', '!', '=']
num_delim = bool_delim = arithmetic_operator + relational_operator_delim + logical_operator_delim + whitespace + newline + [',', ')', ']', '}', ':', '=', ';', '/']
func_delim = newline_delim + ['/', '(']


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
            return 's253'
        elif(currChar == '+'):
            return 'PLUS_CHECK'
        elif(currChar == '<'):
            return 'OPEN_ANGLE_CHECK'
        elif(currChar == '>'):
            return 'CLOSING_ANGLE_CHECK'
        elif(currChar == '='):
            return 'ASSIGN_CHECK'
        # elif(currChar == '\''):
        #     return 's257'
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
    elif (currState == 's11'):
        if(currChar == 'a'):
            return 's12'
        # elif(currChar == 'h'):
        #     return 's16'
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
    # elif (currState == 's16'):
    #     if(currChar == 'a'):
    #         return 's17'
    #     elif (currChar == 'ANY'):
    #         return 'DEFINED'
    #     else:
    #         return 'UNDEFINED'
    # elif (currState == 's17'):
    #     if(currChar == 'r'):
    #         return 'CHAR_CHECK'
    #     elif (currChar == 'ANY'):
    #         return 'DEFINED'
    #     else:
    #         return 'UNDEFINED'
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
            return 's59'
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
    elif (currState == 's246'):
        if(currChar == '*'):
            return 's249'
        elif(currChar == '/'):
            return 's247'
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
    elif (currState == 's226'):
        if(currChar == '+'):
            return 'INCREMENT_CHECK'
        elif(currChar == '='):
            return 'ADD_ASS_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's232'):
        if(currChar == '='):
            return 'LESS_OR_EQUAL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's236'):
        if(currChar == '='):
            return 'GREATER_OR_EQUAL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's240'):
        if(currChar == '='):
            return 'EQUAL_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's244'):
        if(currChar == '_'):
            return 's244'
        elif(currChar == 'a'):
            return 's244'
        elif(currChar == 'b'):
            return 's244'
        elif(currChar == 'c'):
            return 's244'
        elif(currChar == 'd'):
            return 's244'
        elif(currChar == 'e'):
            return 's244'
        elif(currChar == 'f'):
            return 's244'
        elif(currChar == 'g'):
            return 's244'
        elif(currChar == 'h'):
            return 's244'
        elif(currChar == 'i'):
            return 's244'
        elif(currChar == 'j'):
            return 's244'
        elif(currChar == 'k'):
            return 's244'
        elif(currChar == 'l'):
            return 's244'
        elif(currChar == 'm'):
            return 's244'
        elif(currChar == 'n'):
            return 's244'
        elif(currChar == 'o'):
            return 's244'
        elif(currChar == 'p'):
            return 's244'
        elif(currChar == 'q'):
            return 's244'
        elif(currChar == 'r'):
            return 's244'
        elif(currChar == 's'):
            return 's244'
        elif(currChar == 't'):
            return 's244'
        elif(currChar == 'u'):
            return 's244'
        elif(currChar == 'v'):
            return 's244'
        elif(currChar == 'w'):
            return 's244'
        elif(currChar == 'x'):
            return 's244'
        elif(currChar == 'y'):
            return 's244'
        elif(currChar == 'z'):
            return 's244'
        elif(currChar == 'A'):
            return 's244'
        elif(currChar == 'B'):
            return 's244'
        elif(currChar == 'C'):
            return 's244'
        elif(currChar == 'D'):
            return 's244'
        elif(currChar == 'E'):
            return 's244'
        elif(currChar == 'F'):
            return 's244'
        elif(currChar == 'G'):
            return 's244'
        elif(currChar == 'H'):
            return 's244'
        elif(currChar == 'I'):
            return 's244'
        elif(currChar == 'J'):
            return 's244'
        elif(currChar == 'K'):
            return 's244'
        elif(currChar == 'L'):
            return 's244'
        elif(currChar == 'M'):
            return 's244'
        elif(currChar == 'N'):
            return 's244'
        elif(currChar == 'O'):
            return 's244'
        elif(currChar == 'P'):
            return 's244'
        elif(currChar == 'Q'):
            return 's244'
        elif(currChar == 'R'):
            return 's244'
        elif(currChar == 'S'):
            return 's244'
        elif(currChar == 'T'):
            return 's244'
        elif(currChar == 'U'):
            return 's244'
        elif(currChar == 'V'):
            return 's244'
        elif(currChar == 'W'):
            return 's244'
        elif(currChar == 'X'):
            return 's244'
        elif(currChar == 'Y'):
            return 's244'
        elif(currChar == 'Z'):
            return 's244'
        elif(currChar == '0'):
            return 's244'
        elif(currChar == '1'):
            return 's244'
        elif(currChar == '2'):
            return 's244'
        elif(currChar == '3'):
            return 's244'
        elif(currChar == '4'):
            return 's244'
        elif(currChar == '5'):
            return 's244'
        elif(currChar == '6'):
            return 's244'
        elif(currChar == '7'):
            return 's244'
        elif(currChar == '8'):
            return 's244'
        elif(currChar == '9'):
            return 's244'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's247'):
        if(currChar == 'a'):
            return 's247'
        elif(currChar == 'b'):
            return 's247'
        elif(currChar == 'c'):
            return 's247'
        elif(currChar == 'd'):
            return 's247'
        elif(currChar == 'e'):
            return 's247'
        elif(currChar == 'f'):
            return 's247'
        elif(currChar == 'g'):
            return 's247'
        elif(currChar == 'h'):
            return 's247'
        elif(currChar == 'i'):
            return 's247'
        elif(currChar == 'j'):
            return 's247'
        elif(currChar == 'k'):
            return 's247'
        elif(currChar == 'l'):
            return 's247'
        elif(currChar == 'm'):
            return 's247'
        elif(currChar == 'n'):
            return 's247'
        elif(currChar == 'o'):
            return 's247'
        elif(currChar == 'p'):
            return 's247'
        elif(currChar == 'q'):
            return 's247'
        elif(currChar == 'r'):
            return 's247'
        elif(currChar == 's'):
            return 's247'
        elif(currChar == 't'):
            return 's247'
        elif(currChar == 'u'):
            return 's247'
        elif(currChar == 'v'):
            return 's247'
        elif(currChar == 'w'):
            return 's247'
        elif(currChar == 'x'):
            return 's247'
        elif(currChar == 'y'):
            return 's247'
        elif(currChar == 'z'):
            return 's247'
        elif(currChar == 'A'):
            return 's247'
        elif(currChar == 'B'):
            return 's247'
        elif(currChar == 'C'):
            return 's247'
        elif(currChar == 'D'):
            return 's247'
        elif(currChar == 'E'):
            return 's247'
        elif(currChar == 'F'):
            return 's247'
        elif(currChar == 'G'):
            return 's247'
        elif(currChar == 'H'):
            return 's247'
        elif(currChar == 'I'):
            return 's247'
        elif(currChar == 'J'):
            return 's247'
        elif(currChar == 'K'):
            return 's247'
        elif(currChar == 'L'):
            return 's247'
        elif(currChar == 'M'):
            return 's247'
        elif(currChar == 'N'):
            return 's247'
        elif(currChar == 'O'):
            return 's247'
        elif(currChar == 'P'):
            return 's247'
        elif(currChar == 'Q'):
            return 's247'
        elif(currChar == 'R'):
            return 's247'
        elif(currChar == 'S'):
            return 's247'
        elif(currChar == 'T'):
            return 's247'
        elif(currChar == 'U'):
            return 's247'
        elif(currChar == 'V'):
            return 's247'
        elif(currChar == 'W'):
            return 's247'
        elif(currChar == 'X'):
            return 's247'
        elif(currChar == 'Y'):
            return 's247'
        elif(currChar == 'Z'):
            return 's247'
        elif(currChar == '0'):
            return 's247'
        elif(currChar == '1'):
            return 's247'
        elif(currChar == '2'):
            return 's247'
        elif(currChar == '3'):
            return 's247'
        elif(currChar == '4'):
            return 's247'
        elif(currChar == '5'):
            return 's247'
        elif(currChar == '6'):
            return 's247'
        elif(currChar == '7'):
            return 's247'
        elif(currChar == '8'):
            return 's247'
        elif(currChar == '9'):
            return 's247'
        elif(currChar == '@'):
            return 's247'
        elif(currChar == '#'):
            return 's247'
        elif(currChar == '$'):
            return 's247'
        elif(currChar == '^'):
            return 's247'
        elif(currChar == '"'):
            return 's247'
        elif(currChar == ','):
            return 's247'
        elif(currChar == '+'):
            return 's247'
        elif(currChar == '-'):
            return 's247'
        elif(currChar == '*'):
            return 's247'
        elif(currChar == '/'):
            return 's247'
        elif(currChar == '%'):
            return 's247'
        elif(currChar == '>'):
            return 's247'
        elif(currChar == '<'):
            return 's247'
        elif(currChar == '!'):
            return 's247'
        elif(currChar == '='):
            return 's247'
        elif(currChar == '&'):
            return 's247'
        elif(currChar == '.'):
            return 's247'
        elif(currChar == '|'):
            return 's247'
        elif(currChar == '('):
            return 's247'
        elif(currChar == ')'):
            return 's247'
        elif(currChar == '['):
            return 's247'
        elif(currChar == ']'):
            return 's247'
        elif(currChar == '?'):
            return 's247'
        elif(currChar == ':'):
            return 's247'
        elif(currChar == ';'):
            return 's247'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's249'):
        if(currChar == '\n'):
            return 's249'
        elif(currChar == '*'):
            return 's250'
        elif(currChar == 'a'):
            return 's249'
        elif(currChar == 'b'):
            return 's249'
        elif(currChar == 'c'):
            return 's249'
        elif(currChar == 'd'):
            return 's249'
        elif(currChar == 'e'):
            return 's249'
        elif(currChar == 'f'):
            return 's249'
        elif(currChar == 'g'):
            return 's249'
        elif(currChar == 'h'):
            return 's249'
        elif(currChar == 'i'):
            return 's249'
        elif(currChar == 'j'):
            return 's249'
        elif(currChar == 'k'):
            return 's249'
        elif(currChar == 'l'):
            return 's249'
        elif(currChar == 'm'):
            return 's249'
        elif(currChar == 'n'):
            return 's249'
        elif(currChar == 'o'):
            return 's249'
        elif(currChar == 'p'):
            return 's249'
        elif(currChar == 'q'):
            return 's249'
        elif(currChar == 'r'):
            return 's249'
        elif(currChar == 's'):
            return 's249'
        elif(currChar == 't'):
            return 's249'
        elif(currChar == 'u'):
            return 's249'
        elif(currChar == 'v'):
            return 's249'
        elif(currChar == 'w'):
            return 's249'
        elif(currChar == 'x'):
            return 's249'
        elif(currChar == 'y'):
            return 's249'
        elif(currChar == 'z'):
            return 's249'
        elif(currChar == 'A'):
            return 's249'
        elif(currChar == 'B'):
            return 's249'
        elif(currChar == 'C'):
            return 's249'
        elif(currChar == 'D'):
            return 's249'
        elif(currChar == 'E'):
            return 's249'
        elif(currChar == 'F'):
            return 's249'
        elif(currChar == 'G'):
            return 's249'
        elif(currChar == 'H'):
            return 's249'
        elif(currChar == 'I'):
            return 's249'
        elif(currChar == 'J'):
            return 's249'
        elif(currChar == 'K'):
            return 's249'
        elif(currChar == 'L'):
            return 's249'
        elif(currChar == 'M'):
            return 's249'
        elif(currChar == 'N'):
            return 's249'
        elif(currChar == 'O'):
            return 's249'
        elif(currChar == 'P'):
            return 's249'
        elif(currChar == 'Q'):
            return 's249'
        elif(currChar == 'R'):
            return 's249'
        elif(currChar == 'S'):
            return 's249'
        elif(currChar == 'T'):
            return 's249'
        elif(currChar == 'U'):
            return 's249'
        elif(currChar == 'V'):
            return 's249'
        elif(currChar == 'W'):
            return 's249'
        elif(currChar == 'X'):
            return 's249'
        elif(currChar == 'Y'):
            return 's249'
        elif(currChar == 'Z'):
            return 's249'
        elif(currChar == '0'):
            return 's249'
        elif(currChar == '1'):
            return 's249'
        elif(currChar == '2'):
            return 's249'
        elif(currChar == '3'):
            return 's249'
        elif(currChar == '4'):
            return 's249'
        elif(currChar == '5'):
            return 's249'
        elif(currChar == '6'):
            return 's249'
        elif(currChar == '7'):
            return 's249'
        elif(currChar == '8'):
            return 's249'
        elif(currChar == '9'):
            return 's249'
        elif(currChar == '@'):
            return 's249'
        elif(currChar == '#'):
            return 's249'
        elif(currChar == '$'):
            return 's249'
        elif(currChar == '^'):
            return 's249'
        elif(currChar == '"'):
            return 's249'
        elif(currChar == ','):
            return 's249'
        elif(currChar == '+'):
            return 's249'
        elif(currChar == '-'):
            return 's249'
        elif(currChar == '/'):
            return 's249'
        elif(currChar == '%'):
            return 's249'
        elif(currChar == '>'):
            return 's249'
        elif(currChar == '<'):
            return 's249'
        elif(currChar == '!'):
            return 's249'
        elif(currChar == '='):
            return 's249'
        elif(currChar == '&'):
            return 's249'
        elif(currChar == '.'):
            return 's249'
        elif(currChar == '| '):
            return 's249'
        elif(currChar == '('):
            return 's249'
        elif(currChar == ')'):
            return 's249'
        elif(currChar == '['):
            return 's249'
        elif(currChar == ']'):
            return 's249'
        elif(currChar == '?'):
            return 's249'
        elif(currChar == ':'):
            return 's249'
        elif(currChar == ';'):
            return 's249'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's250'):
        if(currChar == '/'):
            return 'MULTI_COMMENT_CHECK'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's253'):
        if(currChar == '"'):
            return 'STRING_LIT_CHECK'
        if (currChar == 'a'):
            return 's253'
        elif(currChar == 'b'):
            return 's253'
        elif(currChar == 'c'):
            return 's253'
        elif(currChar == 'd'):
            return 's253'
        elif(currChar == 'e'):
            return 's253'
        elif(currChar == 'f'):
            return 's253'
        elif(currChar == 'g'):
            return 's253'
        elif(currChar == 'h'):
            return 's253'
        elif(currChar == 'i'):
            return 's253'
        elif(currChar == 'j'):
            return 's253'
        elif(currChar == 'k'):
            return 's253'
        elif(currChar == 'l'):
            return 's253'
        elif(currChar == 'm'):
            return 's253'
        elif(currChar == 'n'):
            return 's253'
        elif(currChar == 'o'):
            return 's253'
        elif(currChar == 'p'):
            return 's253'
        elif(currChar == 'q'):
            return 's253'
        elif(currChar == 'r'):
            return 's253'
        elif(currChar == 's'):
            return 's253'
        elif(currChar == 't'):
            return 's253'
        elif(currChar == 'u'):
            return 's253'
        elif(currChar == 'v'):
            return 's253'
        elif(currChar == 'w'):
            return 's253'
        elif(currChar == 'x'):
            return 's253'
        elif(currChar == 'y'):
            return 's253'
        elif(currChar == 'z'):
            return 's253'
        elif(currChar == 'A'):
            return 's253'
        elif(currChar == 'B'):
            return 's253'
        elif(currChar == 'C'):
            return 's253'
        elif(currChar == 'D'):
            return 's253'
        elif(currChar == 'E'):
            return 's253'
        elif(currChar == 'F'):
            return 's253'
        elif(currChar == 'G'):
            return 's253'
        elif(currChar == 'H'):
            return 's253'
        elif(currChar == 'I'):
            return 's253'
        elif(currChar == 'J'):
            return 's253'
        elif(currChar == 'K'):
            return 's253'
        elif(currChar == 'L'):
            return 's253'
        elif(currChar == 'M'):
            return 's253'
        elif(currChar == 'N'):
            return 's253'
        elif(currChar == 'O'):
            return 's253'
        elif(currChar == 'P'):
            return 's253'
        elif(currChar == 'Q'):
            return 's253'
        elif(currChar == 'R'):
            return 's253'
        elif(currChar == 'S'):
            return 's253'
        elif(currChar == 'T'):
            return 's253'
        elif(currChar == 'U'):
            return 's253'
        elif(currChar == 'V'):
            return 's253'
        elif(currChar == 'W'):
            return 's253'
        elif(currChar == 'X'):
            return 's253'
        elif(currChar == 'Y'):
            return 's253'
        elif(currChar == 'Z'):
            return 's253'
        elif(currChar == '0'):
            return 's253'
        elif(currChar == '1'):
            return 's253'
        elif(currChar == '2'):
            return 's253'
        elif(currChar == '3'):
            return 's253'
        elif(currChar == '4'):
            return 's253'
        elif(currChar == '5'):
            return 's253'
        elif(currChar == '6'):
            return 's253'
        elif(currChar == '7'):
            return 's253'
        elif(currChar == '8'):
            return 's253'
        elif(currChar == '9'):
            return 's253'
        elif(currChar == '@'):
            return 's253'
        elif(currChar == '#'):
            return 's253'
        elif(currChar == '$'):
            return 's253'
        elif(currChar == '^'):
            return 's253'
        elif(currChar == ','):
            return 's253'
        elif(currChar == '+'):
            return 's253'
        elif(currChar == '-'):
            return 's253'
        elif(currChar == '*'):
            return 's253'
        elif(currChar == '/'):
            return 's253'
        elif(currChar == '%'):
            return 's253'
        elif(currChar == '>'):
            return 's253'
        elif(currChar == '<'):
            return 's253'
        elif(currChar == '!'):
            return 's253'
        elif(currChar == '='):
            return 's253'
        elif(currChar == '&'):
            return 's253'
        elif(currChar == '.'):
            return 's253'
        elif(currChar == '|'):
            return 's253'
        elif(currChar == '('):
            return 's253'
        elif(currChar == ')'):
            return 's253'
        elif(currChar == '['):
            return 's253'
        elif(currChar == ']'):
            return 's253'
        elif(currChar == '?'):
            return 's253'
        elif(currChar == ':'):
            return 's253'
        elif(currChar == ';'):
            return 's253'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    # elif (currState == 's257'):
    #     if(currChar == '\''):
    #         return 'CHAR_LIT_CHECK'
    #     elif (currChar == 'ANY'):
    #         return 'DEFINED'
    #     else:
    #         return 'UNDEFINED'
    elif (currState == 's267'):
        if(currChar == '0'):
            return 's267'
        elif(currChar == '1'):
            return 's267'
        elif(currChar == '2'):
            return 's267'
        elif(currChar == '3'):
            return 's267'
        elif(currChar == '4'):
            return 's267'
        elif(currChar == '5'):
            return 's267'
        elif(currChar == '6'):
            return 's267'
        elif(currChar == '7'):
            return 's267'
        elif(currChar == '8'):
            return 's267'
        elif(currChar == '9'):
            return 's267'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's300'):
        if(currChar == '.'):
            return 's267'
        elif(currChar == '0'):
            return 's300'
        elif(currChar == '1'):
            return 's300'
        elif(currChar == '2'):
            return 's300'
        elif(currChar == '3'):
            return 's300'
        elif(currChar == '4'):
            return 's300'
        elif(currChar == '5'):
            return 's300'
        elif(currChar == '6'):
            return 's300'
        elif(currChar == '7'):
            return 's300'
        elif(currChar == '8'):
            return 's300'
        elif(currChar == '9'):
            return 's300'
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
    char_esc = False
    # first_char = True
    print("(dbgl ----------SCAN START--------")
    for i in range(len(code)): #need index for later
        print('(dbg) ---NEW CHAR---')
        print('(dbg) state: ', currState)
        print('(dbg) ', code[i])
        print('(dbg) ascii: ', ord(code[i]))
        #update line and col
        if (code[i] == '\n' and i != len(code)-1): 
            currLine += 1
            currCol = 1
            lineContent = ''
        else:
            currCol += 1
            lineContent += code[i]
        #if no transitions, it means it's time for delim checking
        if (transition(currState, 'ANY') != 'DEFINED'):
            print('(dbg) delim checking')
            delim_check = True
            #data type keywords
            if (currState == 'BOOL_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'bool'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''
                    currState = 's0'
            # if (currState == 'CHAR_CHECK'):
            #     expected = type_iden_delim
            #     if (code[i] in type_iden_delim):
            #         tokens.append((currToken, 'char'))
            #         currToken = ''
            #         currState = 's0'
            #     elif (code[i] in alphanum + ['_']):
            #         currToken += code[i]
            #         currState ='s244'
            #         print('(dbg) now in state 244')
            #         continue
            #     else:
            #         currToken += code[i]
            #         errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            #         currToken = ''
            #         currState = 's0'
            if (currState == 'DOUBLE_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'double'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
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
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
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
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            if (currState == 'LONG_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'long'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            if (currState == 'STRING_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    tokens.append((currToken, 'string'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            #break statement
            if (currState == 'BREAK_CHECK'):
                expected = break_delim
                if (code[i] in break_delim):
                    tokens.append((currToken, 'break'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # ( symbol
            if (currState == 'OPEN_PAREN_CHECK'):
                expected = ['alphanum', ' ', '\"', '!', ')', '+', '-', '/']
                if (code[i] in open_paren_delim):
                    tokens.append((currToken, '('))
                    currToken = ''
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # ) symbol
            if (currState == 'CLOSING_PAREN_CHECK'):
                expected = ['alphanum', '=', '&', '|', '{', '(', ')', ';', '\n', ',', '/', ':', ']','?'] + [';', '\n', '/']
                if (code[i] in close_paren_delim):
                    tokens.append((currToken, ')'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # ; symbol
            if (currState == 'SEMICOLON_CHECK'):
                expected = ['alphanum', ' ', '}', '/'] + newline
                if (code[i] in semicolon_delim):
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
                expected = ['alphanum', ' ', '(', '+', '/']
                if (code[i] in negative_delim):
                    tokens.append((currToken, '-'))
                    currToken = ''  
                    currState = 's0'
                else:
                    print('(dbg) going to s170')
                    currState = 's170'
            # ! symbol
            if (currState == 'NEGATION_CHECK'):
                expected = ['alphanum', '(', '/', '!'] + whitespace + newline
                if (code[i] in exclamation_delim):
                    tokens.append((currToken, '!'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's178'
            # % symbol
            if (currState == 'MODULO_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in percent_delim):
                    tokens.append((currToken, '%'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's180'
            # * symbol
            if (currState == 'ASTERISK_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in asterisk_delim):
                    tokens.append((currToken, '*'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's191'
            # , symbol
            if (currState == 'COMMA_CHECK'):
                expected = ['alphanum', ' ', '/']
                if (code[i] in comma_delim):
                    tokens.append((currToken, ','))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # . symbol
            if (currState == 'DOT_CHECK'):
                expected = ['alphabetic', '/'] + whitespace
                if (code[i] in dot_delim):
                    tokens.append((currToken, '.'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's267'
            # / symbol
            if (currState == 'SLASH_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-']
                if (code[i] in slash_delim):
                    tokens.append((currToken, '/'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's246'
            # ? symbol
            if (currState == 'QUESTION_CHECK'):
                expected = ['alphanum', '(', '/', '\"'] + newline
                if (code[i] in question_delim):
                    tokens.append((currToken, '?'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # : symbol
            if (currState == 'COLON_CHECK'):
                expected = ['alphanum', '(', ' ', '/'] + newline
                if (code[i] in colon_delim):
                    tokens.append((currToken, ':'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # [ symbol
            if (currState == 'OPEN_BRACKET_CHECK'):
                expected = ['alphanum', ']', '/', '\n', '('] + whitespace
                if (code[i] in open_bracket_delim):
                    tokens.append((currToken, '['))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
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
                    currtoken = ''
                    currstate = 's0'
            # { symbol
            if (currState == 'OPEN_CURLY_CHECK'):
                expected = ['alphanum', ' ', '{', '}', '/'] + newline_delim
                if (code[i] in open_curly_delim):
                    tokens.append((currToken, '{'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # } symbol
            if (currState == 'CLOSING_CURLY_CHECK'):
                expected = ['alphanum', ' ', ';', '/', ',','}'] + newline_delim
                if (code[i] in close_curly_delim):
                    tokens.append((currToken, '}'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # + symbol
            if (currState == 'PLUS_CHECK'):
                expected = ['alphanum', ' ', '(', '\"', '+', '-', '/']
                if (code[i] in plus_delim):
                    tokens.append((currToken, '+'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's226'
            # < symbol
            if (currState == 'OPEN_ANGLE_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/'] + newline
                print("(dbg) open angle check curr char ", code[i])
                if (code[i] in less_than_delim):
                    print("(dbg) arithmetic spotted for <")
                    tokens.append((currToken, '<'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's232'
            # > symbol
            if (currState == 'CLOSING_ANGLE_CHECK'):
                expected = ['alphanum', ' ', '(', ';', '+', '-', '/'] + newline
                if (code[i] in greater_than_delim):
                    tokens.append((currToken, '>'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's236'
            # = symbol
            if (currState == 'ASSIGN_CHECK'):
                expected = ['alphanum', ' ', '\"', '+', '-', '/', '!']
                if (code[i] in equal_delim):
                    tokens.append((currToken, '='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currState = 's240'
            # in statement
            if (currState == 'IN_CHECK'):
                expected = ['<', '/']
                if (code[i] in in_delim):
                    tokens.append((currToken, 'in'))
                    currToken = ''
                    currState = 's0'
                elif(code[i] in alphanum + ['_']):
                    currState = 's83'
                else:
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # print statement
            if (currState == 'PRINT_CHECK'):
                expected = func_delim
                if (code[i] in func_delim):
                    tokens.append((currToken, 'print'))
                    currToken = ''
                    currState = 's0'
                elif(code[i] in alphanum + ['_']):
                    currState = 's100'
                else:
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # println statement
            if (currState == 'PRINTLN_CHECK'):
                expected = func_delim
                if (code[i] in func_delim):
                    tokens.append((currToken, 'println'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # private statement
            if (currState == 'PRIVATE_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'private'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # property statement
            if (currState == 'PROPERTY_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'property'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # repeat statement
            if (currState == 'REPEAT_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'repeat'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # return statement
            if (currState == 'RETURN_CHECK'):
                expected = newline_delim + [';']
                if (code[i] in return_delim):
                    tokens.append((currToken, 'return'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # set statement
            if (currState == 'SET_CHECK'):
                expected = get_set_delim
                if (code[i] in get_set_delim):
                    tokens.append((currToken, 'set'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # static statement
            if (currState == 'STATIC_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'static'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # switch statement
            if (currState == 'SWITCH_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'switch'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # this statement
            if (currState == 'THIS_CHECK'):
                expected = this_delim
                if (code[i] in this_delim):
                    tokens.append((currToken, 'this'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # this statement
            if (currState == 'TRUE_CHECK'):
                expected = bool_delim
                if (code[i] in bool_delim):
                    tokens.append((currToken, 'bool_lit'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # void statement
            if (currState == 'VOID_CHECK'):
                expected = whitespace + newline + ['/']
                if (code[i] in void_delim):
                    tokens.append((currToken, 'void'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # while statement
            if (currState == 'WHILE_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'while'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # -- symbol
            if (currState == 'DECREMENT_CHECK'):
                expected = whitespace + ['alphanum'] + [';', ')', '/', '+', '*', '%', '('] + newline
                if (code[i] in decrement_delim):
                    tokens.append((currToken, '--'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # -= symbol
            if (currState == 'MINUS_ASS_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in subtract_assign_delim):
                    tokens.append((currToken, '-='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # != symbol
            if (currState == 'NOT_EQUAL_CHECK'):
                expected = whitespace + ['alphanum', '(', '"', '!'] + newline
                if (code[i] in not_equal_delim):
                    tokens.append((currToken, '!='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # %= symbol
            if (currState == 'MODULO_ASS_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in modulo_assign_delim):
                    tokens.append((currToken, '%='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # && symbol
            if (currState == 'LOGICAND_CHECK'):
                expected = ['alphanum', ' ', '(', '\"', '/', '!']
                if (code[i] in and_delim):
                    tokens.append((currToken, '&&'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # *= symbol
            if (currState == 'MULT_ASS_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in multi_assign_delim):
                    tokens.append((currToken, '*='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # /= symbol
            if (currState == 'DIV_ASS_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in divi_assign_delim):
                    tokens.append((currToken, '/='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # || symbol
            if (currState == 'LOGICOR_CHECK'):
                expected = ['alphanum', ' ', '(', '\"', '/', '!']
                if (code[i] in or_delim):
                    tokens.append((currToken, '||'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # ++ symbol
            if (currState == 'INCREMENT_CHECK'):
                expected = whitespace + ['alphanum', ')', ';', '/', '-', '*', '%', '(']
                if (code[i] in increment_delim):
                    tokens.append((currToken, '++'))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # += symbol
            if (currState == 'ADD_ASS_CHECK'):
                expected = ['alphanum', ' ', '(', '\"', '+', '-', '/']
                if (code[i] in add_assign_delim):
                    tokens.append((currToken, '+='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # <= symbol
            if (currState == 'LESS_OR_EQUAL_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in less_equal_delim):
                    tokens.append((currToken, '<='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # >= symbol
            if (currState == 'GREATER_OR_EQUAL_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in greater_equal_delim):
                    tokens.append((currToken, '>='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # == symbol
            if (currState == 'EQUAL_CHECK'):
                expected = ['alphanum', ' ', '(', '\"', '+', '-', '/', '!']
                if (code[i] in equal_equal_delim):
                    tokens.append((currToken, '=='))
                    currToken = ''  
                    currState = 's0'
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
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
                    currtoken = ''
                    currstate = 's0'
            # # character literal
            # if (currState == 'CHAR_LIT_CHECK'):
            #     expected = num_delim + [')', ']', '/', ':']
            #     if (code[i] in num_delim + newline_delim + [')', ']', '/', ':']):
            #         tokens.append((currToken, 'char_lit'))
            #         currToken = ''  
            #         currState = 's0'
            #     else:
            #         currToken += code[i]
            #         errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            #         currtoken = ''
            #         currstate = 's0'
            # multicomments 
            if (currState == 'MULTI_COMMENT_CHECK'):
                tokens.append((currToken, 'multi-line comment'))        
                currToken = ''  
                currState = 's0'
            # case statement 
            if (currState == 'CASE_CHECK'):
                expected = newline_delim
                if (code[i] in case_delim):
                    tokens.append((currToken, 'case'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # class statement 
            if (currState == 'CLASS_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'class'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # continue statement 
            if (currState == 'CONTINUE_CHECK'):
                expected = newline_delim + [';']
                if (code[i] in continue_delim):
                    tokens.append((currToken, 'continue'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # const statement 
            if (currState == 'CONST_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    tokens.append((currToken, 'const'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # default statement 
            if (currState == 'DEFAULT_CHECK'):
                expected = default_delim
                if (code[i] in default_delim):
                    tokens.append((currToken, 'default'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # do statement 
            if (currState == 'DO_CHECK'):
                expected = block_delim
                if (code[i] in block_delim):
                    tokens.append((currToken, 'do'))
                    currToken = ''
                    currState = 's0'
                elif(code[i] in alphanum + ['_']):
                    currState = 's44'
                else:
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # else statement 
            if (currState == 'ELSE_CHECK'):
                expected = block_delim
                if (code[i] in block_delim):
                    tokens.append((currToken, 'else'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # false statement
            if (currState == 'FALSE_CHECK'):
                expected = bool_delim
                if (code[i] in bool_delim):
                    tokens.append((currToken, 'bool_lit'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # for statement
            if (currState == 'FOR_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'for'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # get statement
            if (currState == 'GET_CHECK'):
                expected = get_set_delim
                if (code[i] in get_set_delim):
                    tokens.append((currToken, 'get'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # if statement
            if (currState == 'IF_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    tokens.append((currToken, 'if'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # import statement
            if (currState == 'IMPORT_CHECK'):
                expected = whitespace + ['<', '/'] + newline
                if (code[i] in import_delim):
                    tokens.append((currToken, 'import'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
            # item statement
            if (currState == 'ITEM_CHECK'):
                expected = iden_delim
                if (code[i] in iden_delim):
                    tokens.append((currToken, 'item'))
                    currToken = ''
                    currState = 's0'
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currtoken = ''
                    currstate = 's0'
        # end of delim checking if statement
#---SPECIAL STATES---
        #identifier state
        if (currState == 's244'):
            print('(dbg) in identifier check state now')
            if (code[i] in iden_delim):
                print('(dbg) correct delim')    
                if (currToken[0] not in alphabetic_chars):
                        errors.append(idenFirstError(currToken, currLine, currCol,lineContent))
                        currToken = ''
                        currState = 's0'
                else:
                    tokens.append((currToken, 'Identifier'))
                currToken = ''
                currState = 's0'
            elif (code[i] in alphanum + ['_']): #if not delim but still valid, keep looping
                    currToken += code[i]
                    print('(dbg) accepted for iden')
                    currState ='s244'
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
        # if (currState == 's257'):
        #     if (code[i] != '\''):
        #         print('(dbg) not \'')
        #         if (char_esc):
        #             print('(dbg) curr scan ', code[i])
        #             if (code[i] not in ['\'', '\"', '\\', 't', 'n', 'b']):
        #                 print('(dbg) esc seq error')
        #                 errors.append(charEscSeqError(currToken, currLine, currCol, lineContent))
        #                 currToken = ''
        #                 currState = 's0'
        #             char_esc = False
        #             if code[i] == '\\':
        #                 currToken += code[i]
        #                 continue
        #         elif (not first_char):
        #             errors.append(charLengthError(currToken, currLine, currCol, lineContent))
        #             currToken = ''
        #             currState = 's0'
        #         if not char_esc:
        #             first_char = False
        #             if(code[i] == '\\'):
        #                 char_esc = True
        #         currToken += code[i]
        #         continue
        #     else:
        #         print("(dbg) chr close found")
        #         currToken += code[i]
        #         if (char_esc):
        #             char_esc = False
        #             continue
        #         else:
        #             first_char = True
        #             currState = 'CHAR_LIT_CHECK'
        #             continue
        #end of charcter lit checking
        #single line comment
        if (currState == 's247'):
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
        if (currState == 's250'):
            if (code[i] != '/'):
                currState = 's249'
        #end of multi-line comment
        #whole number
        if (currState == 's300'):
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
        if (currState == 's267'):
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
        #& symbol
        if (currState == 's184'):
            currToken += code[i]
            if(code[i] == '&'):
                currState = 'LOGICAND_CHECK'
                continue
            else:
                errors.append(unexpectedSymbol('&', currLine, currCol, lineContent))
                currToken = ''
                currState = 's0'
        # end of | symbol
        #& symbol
        if (currState == 's223'):
            currToken += code[i]
            if(code[i] == '|'):
                currState = 'LOGICOR_CHECK'
                continue
            else:
                errors.append(unexpectedSymbol('|', currLine, currCol, lineContent))
                currToken = ''
                currState = 's0'
        # end of | symbol
        #string
        if (currState == 's253'):
            if (code[i] == '\\' and not char_esc):
                char_esc = True
                currToken += code[i]
                continue
            if (char_esc):
                if (code[i] not in ['\'', '\"', '\\', 't', 'n', 'b']):
                    print('(dbg) esc seq error')
                    errors.append(charEscSeqError(currToken, currLine, currCol, lineContent))
                    currToken = ''
                    currState = 's0'
                else:
                    currToken += code[i]
                char_esc = False
                continue

        #end of special states

        #iterating through chars
        #check whitespaces
        if (currState not in ['s253', 's247', 's249']):
            if (code[i] == ' '):
                # tokens.append(('\' \' ', 'Space'))
                continue
            if (code[i] == '\n'):
                if (i != len(code)-1):
                    # tokens.append(('\\n', 'New line'))
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
                    currState = 's300'  
                    continue
                elif (code[i] not in alphanum + ['_'] and i != len(code)-1):
                    print("(dbg) unexpected")
                    errors.append(unexpectedSymbol(currToken, currLine, currCol, lineContent))
                    currToken = ''
                    currState = 's0'
                    continue
                currToken += code[i]
                if (code[i] in alphabetic_chars and i != len(code)-1):
                    print(f'(dbg) index {i}')
                    print(f'(dbg) length {len(code)}')
                    currState = 's244'
                # elif (code[i] != ''):
                #     print("(dbg "error found"")
                #     errors.append(idenFirstError(currToken, currLine, currCol, lineContent))
                continue
                # else:
                #     currToken += code[i]
                #     errors.append(idenFirstError(currToken, currLine, currCol,lineContent))
                #     currToken = ''
                #     currState = 's0'  
            else:
                if (currState == 's249'):
                    currToken += code[i]
                    continue
                if (currState == 's253'):
                    if (code[i] == '\n'):
                        errors.append(stringMissingClose(currToken, currLine, currCol, lineContent))
                        currToken = ''
                        currState = 's0'
                        continue
                    else:
                        currToken += code[i]
                        continue
                if (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState = 's244'
                    continue
                elif (code[i] in iden_delim): #check delim
                    if (currToken):
                        if (currToken[0] not in alphabetic_chars + ['_']):
                            print('(dbg) other idnefirst error')
                            print('(dbg) symbol ', code[i])
                            if code[i] not in symbols:
                                errors.append(idenFirstError(currToken, currLine, currCol,lineContent))
                            else:
                                errors.append(unexpectedSymbol(currToken, currLine, currCol, lineContent))
                            currToken = ''
                            currState = 's0'
                        else:
                            print("(dbg) other iden append")
                            if (currToken[0] not in alphabetic_chars):
                                errors.append(idenFirstError(currToken, currLine, currCol,lineContent))
                                currToken = ''
                                currState = 's0' 
                            else:
                                tokens.append((currToken, 'Identifier'))
                            currToken = code[i]
                            currState = transition('s0', code[i])
                    else:
                        errors.append(idenFirstError(currToken, currLine, currCol,lineContent))
                        currToken = ''
                        currState = 's0'
                else:
                    currToken += code[i]
                    expected = iden_delim
                    if (code[i-1] in arithmetic_operator):
                        expected = ['alphanum', ' ', '(']
                    if (code[i-1] == '+'):
                        expected.append('\"')
                    print('(dbg) currState: ', currState)
                    errors.append(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                    currToken = ''
                    currState = 's0'
    
    lexerResults = [tokens, errors] 
    return lexerResults

#---LEXER ERRORS---
def generateError(errorType, currToken, currLine, currCol, lineContent, additionalInfo=None):
    """
    Generates a lexical error message.
    """
    print('(dbg) currToken ', currToken)
    print('(dbg) currCol ', currCol)
    errorMsg = f'Lexical Error ({currLine}, {currCol - len(currToken)}): {errorType} {currToken}\n'
    errorMsg += lineContent + '\n'
    errorMsg += '_' * (currCol - len(currToken) - 1) + '^\n'
    if additionalInfo:
        errorMsg += additionalInfo
    print("(debug) ", errorMsg)
    if (currCol == 0):
        return ''
    return errorMsg

def delimError(currToken, currLine, currCol, incorrectDelim, lineContent, expected):
    errorType = f"Unexpected {'newline' if incorrectDelim == '\\n' else incorrectDelim} for"
    additionalInfo = f"Expected delimiters: {expected}"
    return generateError(errorType, currToken, currLine, currCol, lineContent, additionalInfo)

def idenFirstError(currToken, currLine, currCol, lineContent):
    errorType = "Identifier must start with an alpha character"
    return generateError(errorType, currToken, currLine, currCol, lineContent)

def stringMissingClose(currToken, currLine, currCol, lineContent):
    errorType = "Missing closing \" for string literal"
    return generateError(errorType, currToken, currLine, currCol, lineContent)

def charEscSeqError(currToken, currLine, currCol, lineContent):
    errorType = "Invalid escape sequence for character literal"
    return generateError(errorType, currToken, currLine, currCol, lineContent)

def charLengthError(currToken, currLine, currCol, lineContent):
    errorType = "Invalid character length for character literal"
    return generateError(errorType, currToken, currLine, currCol, lineContent)

def wholeRangeError(currToken, currLine, currCol, lineContent):
    errorType = "Numeric exceeding max range"
    return generateError(errorType, currToken, currLine, currCol, lineContent)

def fracPrecError(currToken, currLine, currCol, lineContent):
    errorType = "Numeric exceeding max precision"
    return generateError(errorType, currToken, currLine, currCol, lineContent)

def unexpectedSymbol(currToken, currLine, currCol, lineContent):
    errorType = "Unexpected symbol"
    return generateError(errorType, currToken, currLine, currCol, lineContent)


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
    app.run(debug=True, host="0.0.0.0", port=5000)