from flask import Flask, json, jsonify, request
from flask_cors import CORS
import syntax_analyzer

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
arithmetic_delim = newline + plaintext_delim + ['(', '/']
relational_operator_delim = ['<', '>', '=', '!']
logical_operator_delim = ['!', '&', '|']
newline_delim = newline + whitespace + ['/']
default_delim = newline + whitespace + [':', '/']
type_iden_delim = newline + whitespace + ['[', '>', '/',')']
get_set_delim = newline + whitespace + ['{', ';', '/']
open_paren_delim = list(set(arithmetic_delim + ['\"', '!', ')', '\n', '/']))
closing_delim = list(set(arithmetic_operator + arithmetic_delim + logical_operator_delim + newline_delim + relational_operator_delim + whitespace + ['=', '|', '{', ';', ')', '(', '/', ':', ']', '?']))
close_paren_delim = list(set(closing_delim + [';', '/']))
semicolon_delim = newline_delim + plaintext_delim + ['}', '/']
negative_delim = list(set(arithmetic_delim + ['/', '+']))
exclamation_delim = alphanum + newline + whitespace + ['(', '/', '!']
percent_delim = list(set(arithmetic_delim + ['/']))
asterisk_delim = list(set(arithmetic_delim + ['/', '+', '-']))
commdot_delim = plaintext_delim + ['\n', '/']
slash_delim = plaintext_delim + ['\n', '(', '+', '-']
question_delim = newline + plaintext_delim + ['(', '/', '\"']
colon_delim = newline + plaintext_delim + ['(', '/', '\"']
open_bracket_delim = alphanum + whitespace + ['\n', '/', '(']
open_curly_delim = newline_delim + plaintext_delim + ['{', '}', '/']
close_curly_delim = newline_delim + plaintext_delim + [';', '/', ',', '}']
plus_delim = list(set(arithmetic_delim + ['\"', '/', '-']))
great_less_delim = list(set(arithmetic_delim + ['/']))
great_delim = great_less_delim + [';']
equal_delim = list(set(arithmetic_delim + ['\"', '/', '!', '!','{']))
in_delim = newline_delim + ['<', '/']
this_delim = newline_delim + ['.', '/']
void_delim = newline + whitespace + ['/']
decrement_delim = alphanum + whitespace + newline + [';', ')', '/', '+', '*', '%', '(']
subtract_assign_delim = list(set(arithmetic_delim + ['/']))
not_equal_delim = alphanum + newline + whitespace + ['(', '!','\"']
modulo_assign_delim = list(set(arithmetic_delim + ['/', '+', '-']))
and_delim = plaintext_delim + ['(', '\"', '\n', '/', '!']
multi_assign_delim = list(set(arithmetic_delim + ['/']))
divi_assign_delim = list(set(arithmetic_delim + ['/']))
or_delim = plaintext_delim + ['(', '\"', '\n', '/', '!']
increment_delim = alphanum + newline_delim + [')', ';', '/', '-', '*', '%', '(']
add_assign_delim = list(set(arithmetic_delim + ['/', '\"']))
equal_equal_delim = list(set(arithmetic_delim + ['\"', '/', '!']))
import_delim = newline + whitespace + ['<', '/']
loop_delim = whitespace + newline + ['(', '/']
block_delim = whitespace + newline + ['{', '/']
break_ret_cont_delim = newline_delim + [';', '/']
case_delim = newline_delim + ['(', '/']
iden_delim = newline_delim + [',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '.', '|', '(', ')', '[', ']', '{', '?', ':', ';']
str_lit_delim = list(set(newline + whitespace + logical_operator_delim + ['+', ')', ',', ';', '/', ':', '!', '=']))
nbl_delim = list(set(arithmetic_operator + relational_operator_delim + logical_operator_delim + whitespace + newline + [',', ')', ']', '}', ':', '=', ';', '/']))
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
        # elif(currChar == 'g'):
        #     return 's70'
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
            return 's253'
        elif(currChar == '+'):
            return 'PLUS_CHECK'
        elif(currChar == '<'):
            return 'OPEN_ANGLE_CHECK'
        elif(currChar == '>'):
            return 'CLOSING_ANGLE_CHECK'
        elif(currChar == '='):
            return 'ASSIGN_CHECK'
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
        # if(currChar == 'e'):
        #     return 's130'
        if (currChar == 't'):
            return 's133'
        elif(currChar == 'w'):
            return 's144'
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
        elif (currChar in alphanum):
            return 's244'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's247'):
        if(currChar in ascii):
            return 's247'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's249'):
        if(currChar == '\n'):
            return 's249'
        elif(currChar == '*'): #catches * before ascii check
            return 's250'
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
        if(currChar == '"'): #catches " before ascii check
            return 'STRING_LIT_CHECK'
        elif (currChar in ascii):
            return 's253'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's267'):
        if(currChar in numbers):
            return 's267'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'
    elif (currState == 's300'):
        if(currChar == '.'):
            return 's267'
        elif (currChar in numbers):
            return 's300'
        elif (currChar == 'ANY'):
            return 'DEFINED'
        else:
            return 'UNDEFINED'


#---TOKEN EXTRACTION AND CLASSIFICATION---#
def lexer(code):
    code = code.replace('\r\n', '\n')   
    for char in code:
        print(f'(debug) {char} : {ord(char)}')
    tokens = [] #list of tokens (token.tokenName, token.tokenType)
    errors = [] #will hold strings of error msges
    currToken = ''
    currState = 's0'
    lineContent = ''
    currLine = 1
    currCol = 1
    currWholeCount = 0
    currFracCount = 0
    wholeError = False
    fracError = False
    char_esc = False
    # first_char = True

    # Helper function inside lexer to add a token(set its properties), append to token list, and reset current token and state
    def add_token(name, type, line, column): # alex: added line and column for syntax error tracing
        nonlocal currToken, currState, currLine, currCol # use nonlocal keyword to access currToken, currState
        token = Token(name, type, line, column) 
        tokens.append(token)
        currToken = ''
        currState = 's0'

    # Helper function to reset state and token when appending errors
    def add_error(string):
        nonlocal currToken, currState 
        errors.append(string)
        currToken = ''
        currState = 's0'

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

            #data type keywords
            if (currState == 'BOOL_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    add_token(currToken, 'bool', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            if (currState == 'DOUBLE_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    add_token(currToken, 'double', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            if (currState == 'FLOAT_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    add_token(currToken, 'float', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            if (currState == 'INT_CHECK'):
                print('(dbg) in int_check')
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    add_token(currToken, 'int', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            if (currState == 'LONG_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    add_token(currToken, 'long', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            if (currState == 'STRING_CHECK'):
                expected = type_iden_delim
                if (code[i] in type_iden_delim):
                    add_token(currToken, 'string', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            #break statement
            if (currState == 'BREAK_CHECK'):
                expected = break_ret_cont_delim
                if (code[i] in break_ret_cont_delim):
                    add_token(currToken, 'break', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # ( symbol
            if (currState == 'OPEN_PAREN_CHECK'):
                expected = ['alphanum', ' ', '\"', '!', ')', '+', '-', '/']
                if (code[i] in open_paren_delim):
                    add_token(currToken, '(', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # ) symbol
            if (currState == 'CLOSING_PAREN_CHECK'):
                expected = ['alphanum', '=', '&', '|', '{', '(', ')', ';', '\n', ',', '/', ':', ']','?'] + [';', '\n', '/']
                if (code[i] in close_paren_delim):
                    add_token(currToken, ')', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # ; symbol
            if (currState == 'SEMICOLON_CHECK'):
                expected = ['alphanum', ' ', '}', '/'] + newline
                if (code[i] in semicolon_delim):
                    add_token(currToken, ';', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # - symbol
            if (currState == 'DASH_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '/']
                if (code[i] in negative_delim):
                    add_token(currToken, '-', currLine, currCol)
                else:
                    print('(dbg) going to s170')
                    currState = 's170'
            # ! symbol
            if (currState == 'NEGATION_CHECK'):
                expected = ['alphanum', '(', '/', '!'] + whitespace + newline
                if (code[i] in exclamation_delim):
                    add_token(currToken, '!', currLine, currCol)
                else:
                    currState = 's178'
            # % symbol
            if (currState == 'MODULO_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in percent_delim):
                    add_token(currToken, '%', currLine, currCol)
                else:
                    currState = 's180'
            # * symbol
            if (currState == 'ASTERISK_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in asterisk_delim):
                    add_token(currToken, '*', currLine, currCol)
                else:
                    currState = 's191'
            # , symbol
            if (currState == 'COMMA_CHECK'):
                expected = ['alphanum', ' ', '/']
                if (code[i] in commdot_delim):
                    add_token(currToken, ',', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # . symbol
            if (currState == 'DOT_CHECK'):
                expected = ['alphanum', '/'] + whitespace
                if (code[i] in numbers):
                    currState = 's267'
                elif (code[i] in commdot_delim):
                    add_token(currToken, '.', currLine, currCol)
                else:
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # / symbol
            if (currState == 'SLASH_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-']
                if (code[i] in slash_delim):
                    add_token(currToken, '/', currLine, currCol)
                else:
                    currState = 's246'
            # ? symbol
            if (currState == 'QUESTION_CHECK'):
                expected = ['alphanum', '(', '/', '\"'] + newline
                if (code[i] in question_delim):
                    add_token(currToken, '?', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # : symbol
            if (currState == 'COLON_CHECK'):
                expected = ['alphanum', '(', ' ', '/'] + newline
                if (code[i] in colon_delim):
                    add_token(currToken, ':', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # [ symbol
            if (currState == 'OPEN_BRACKET_CHECK'):
                expected = ['alphanum', ']', '/', '\n', '('] + whitespace
                if (code[i] in open_bracket_delim):
                    add_token(currToken, '[', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # ] symbol
            if (currState == 'CLOSING_BRACKET_CHECK'):
                expected = iden_delim
                if (code[i] in iden_delim):
                    add_token(currToken, ']', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # { symbol
            if (currState == 'OPEN_CURLY_CHECK'):
                expected = ['alphanum', ' ', '{', '}', '/'] + newline_delim
                if (code[i] in open_curly_delim):
                    add_token(currToken, '{', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # } symbol
            if (currState == 'CLOSING_CURLY_CHECK'):
                expected = ['alphanum', ' ', ';', '/', ',','}'] + newline_delim
                if (code[i] in close_curly_delim):
                    add_token(currToken, '}', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # + symbol
            if (currState == 'PLUS_CHECK'):
                expected = ['alphanum', ' ', '(', '\"', '+', '-', '/']
                if (code[i] in plus_delim):
                    add_token(currToken, '+', currLine, currCol)
                else:
                    currState = 's226'
            # < symbol
            if (currState == 'OPEN_ANGLE_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/'] + newline
                print("(dbg) open angle check curr char ", code[i])
                if (code[i] in great_less_delim):
                    print("(dbg) arithmetic spotted for <")
                    add_token(currToken, '<', currLine, currCol)
                else:
                    currState = 's232'
            # > symbol
            if (currState == 'CLOSING_ANGLE_CHECK'):
                expected = ['alphanum', ' ', '(', ';', '+', '-', '/'] + newline
                if (code[i] in great_delim):
                    add_token(currToken, '>', currLine, currCol)
                else:
                    currState = 's236'
            # = symbol
            if (currState == 'ASSIGN_CHECK'):
                expected = ['alphanum', ' ', '\"', '+', '-', '/', '!']
                if (code[i] in equal_delim):
                    add_token(currToken, '=', currLine, currCol)
                else:
                    currState = 's240'
            # in statement
            if (currState == 'IN_CHECK'):
                expected = ['<', '/']
                if (code[i] in in_delim):
                    add_token(currToken, 'in', currLine, currCol)
                elif(code[i] in alphanum + ['_']):
                    currState = 's83'
                else:
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # print statement
            if (currState == 'PRINT_CHECK'):
                expected = func_delim
                if (code[i] in func_delim):
                    add_token(currToken, 'print', currLine, currCol)
                elif(code[i] in alphanum + ['_']):
                    currState = 's100'
                else:
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # println statement
            if (currState == 'PRINTLN_CHECK'):
                expected = func_delim
                if (code[i] in func_delim):
                    add_token(currToken, 'println', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # private statement
            if (currState == 'PRIVATE_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    add_token(currToken, 'private', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # property statement
            if (currState == 'PROPERTY_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    add_token(currToken, 'property', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # repeat statement
            if (currState == 'REPEAT_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    add_token(currToken, 'repeat', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # return statement
            if (currState == 'RETURN_CHECK'):
                expected = newline_delim + [';']
                if (code[i] in break_ret_cont_delim):
                    add_token(currToken, 'return', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # static statement
            if (currState == 'STATIC_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    add_token(currToken, 'static', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # switch statement
            if (currState == 'SWITCH_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    add_token(currToken, 'switch', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # this statement
            if (currState == 'THIS_CHECK'):
                expected = this_delim
                if (code[i] in this_delim):
                    add_token(currToken, 'this', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # this statement
            if (currState == 'TRUE_CHECK'):
                expected = nbl_delim
                if (code[i] in nbl_delim):
                    add_token(currToken, 'bool_lit', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # void statement
            if (currState == 'VOID_CHECK'):
                expected = whitespace + newline + ['/']
                if (code[i] in void_delim):
                    add_token(currToken, 'void', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # while statement
            if (currState == 'WHILE_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    add_token(currToken, 'while', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # -- symbol
            if (currState == 'DECREMENT_CHECK'):
                expected = whitespace + ['alphanum'] + [';', ')', '/', '+', '*', '%', '('] + newline
                if (code[i] in decrement_delim):
                    add_token(currToken, '--', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # -= symbol
            if (currState == 'MINUS_ASS_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in subtract_assign_delim):
                    add_token(currToken, '-=', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # != symbol
            if (currState == 'NOT_EQUAL_CHECK'):
                expected = whitespace + ['alphanum', '(', '"', '!'] + newline
                if (code[i] in not_equal_delim):
                    add_token(currToken, '!=', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # %= symbol
            if (currState == 'MODULO_ASS_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in modulo_assign_delim):
                    add_token(currToken, '%=', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # && symbol
            if (currState == 'LOGICAND_CHECK'):
                expected = ['alphanum', ' ', '(', '\"', '/', '!']
                if (code[i] in and_delim):
                    add_token(currToken, '&&', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # *= symbol
            if (currState == 'MULT_ASS_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in multi_assign_delim):
                    add_token(currToken, '*=', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # /= symbol
            if (currState == 'DIV_ASS_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in divi_assign_delim):
                    add_token(currToken, '/=', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # || symbol
            if (currState == 'LOGICOR_CHECK'):
                expected = ['alphanum', ' ', '(', '\"', '/', '!']
                if (code[i] in or_delim):
                    add_token(currToken, '||', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # ++ symbol
            if (currState == 'INCREMENT_CHECK'):
                expected = whitespace + ['alphanum', ')', ';', '/', '-', '*', '%', '(']
                if (code[i] in increment_delim):
                    add_token(currToken, '++', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # += symbol
            if (currState == 'ADD_ASS_CHECK'):
                expected = ['alphanum', ' ', '(', '\"', '+', '-', '/']
                if (code[i] in add_assign_delim):
                    add_token(currToken, '+=', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # <= symbol
            if (currState == 'LESS_OR_EQUAL_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in great_less_delim):
                    add_token(currToken, '<=', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # >= symbol
            if (currState == 'GREATER_OR_EQUAL_CHECK'):
                expected = ['alphanum', ' ', '(', '+', '-', '/']
                if (code[i] in great_less_delim):
                    add_token(currToken, '>=', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # == symbol
            if (currState == 'EQUAL_CHECK'):
                expected = ['alphanum', ' ', '(', '\"', '+', '-', '/', '!']
                if (code[i] in equal_equal_delim):
                    add_token(currToken, '==', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # string literal
            if (currState == 'STRING_LIT_CHECK'):
                expected = str_lit_delim
                if (code[i] in str_lit_delim):
                    add_token(currToken, 'string_lit', currLine, currCol)
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # multicomments 
            if (currState == 'MULTI_COMMENT_CHECK'):
                add_token(currToken, 'multi-line comment', currLine, currCol)
            # case statement 
            if (currState == 'CASE_CHECK'):
                expected = newline_delim
                if (code[i] in case_delim):
                    add_token(currToken, 'case', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # class statement 
            if (currState == 'CLASS_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    add_token(currToken, 'class', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # continue statement 
            if (currState == 'CONTINUE_CHECK'):
                expected = newline_delim + [';']
                if (code[i] in break_ret_cont_delim):
                    add_token(currToken, 'continue', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # const statement 
            if (currState == 'CONST_CHECK'):
                expected = newline_delim
                if (code[i] in newline_delim):
                    add_token(currToken, 'const', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # default statement 
            if (currState == 'DEFAULT_CHECK'):
                expected = default_delim
                if (code[i] in default_delim):
                    add_token(currToken, 'default', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # do statement 
            if (currState == 'DO_CHECK'):
                expected = block_delim
                if (code[i] in block_delim):
                    add_token(currToken, 'do', currLine, currCol)
                elif(code[i] in alphanum + ['_']):
                    currState = 's44'
                else:
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # else statement 
            if (currState == 'ELSE_CHECK'):
                expected = block_delim
                if (code[i] in block_delim):
                    add_token(currToken, 'else', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # false statement
            if (currState == 'FALSE_CHECK'):
                expected = nbl_delim
                if (code[i] in nbl_delim):
                    add_token(currToken, 'bool_lit', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # for statement
            if (currState == 'FOR_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    add_token(currToken, 'for', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # if statement
            if (currState == 'IF_CHECK'):
                expected = loop_delim
                if (code[i] in loop_delim):
                    add_token(currToken, 'if', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # import statement
            if (currState == 'IMPORT_CHECK'):
                expected = whitespace + ['<', '/'] + newline
                if (code[i] in import_delim):
                    add_token(currToken, 'import', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
            # item statement
            if (currState == 'ITEM_CHECK'):
                expected = iden_delim
                if (code[i] in iden_delim):
                    add_token(currToken, 'item', currLine, currCol)
                elif (code[i] in alphanum + ['_']):
                    currToken += code[i]
                    currState ='s244'
                    print('(dbg) now in state 244')
                    continue
                else:
                    currToken += code[i]
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
        # end of delim checking if statement
#---SPECIAL STATES---
        #identifier state
        if (currState == 's244'):
            print('(dbg) in identifier check state now')
            if (code[i] in iden_delim):
                print('(dbg) correct delim')    
                if (currToken[0] not in alphabetic_chars):
                        add_error(idenFirstError(currToken, currLine, currCol,lineContent))
                else:
                    add_token(currToken, 'Identifier', currLine, currCol)
            elif (code[i] in alphanum + ['_']): #if not delim but still valid, keep looping
                    currToken += code[i]
                    print('(dbg) accepted for iden')
                    currState ='s244'
                    continue
            else:
                currToken += code[i]
                expected = iden_delim
                # add_error((currToken, f'Lexical Error: In line {currLine}, column {currCol-len(currToken)}; Unexpected \'{code[i]}\' for \'{currToken[:-1]}\'')) #can be expanded with conditions to check what error
                add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
        #end of identifier looping
        #single line comment
        if (currState == 's247'):
            if (code[i] == '\n'):
                add_token(currToken, 'single_comment', currLine, currCol)
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
                    if (wholeError):
                        errors.pop()
                    errors.append(wholeRangeError(currToken, currLine, currCol, lineContent))
                    wholeError = True
                    continue
                else:
                    continue
            if (code[i] in nbl_delim and not wholeError):
                add_token(currToken, 'whole_lit', currLine, currCol)
                currWholeCount = 0
                currFracCount = 0
            elif (code[i] != '.' and not wholeError):
                currToken += code[i]
                expected = nbl_delim
                print('(dbg) whole lit delim error')
                add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                currWholeCount = 0
                currFracCount = 0
            elif (code[i] != '.'):
                wholeError = False
                currState = 's0'
                currToken = ''
                currWholeCount = 0
                currFracCount = 0
        #end of whole number
        #fractional part of number
        if (currState == 's267'):
            if (code[i] in numbers):
                currFracCount += 1
                currToken += code[i]
                if (currFracCount > 16): 
                    if (fracError):
                        errors.pop()
                    errors.append(fracPrecError(currToken, currLine, currCol, lineContent))
                    fracError = True
                    continue
                else:
                    continue
            if (code[i] in nbl_delim and not (wholeError or fracError)):
                    add_token(currToken, 'frac_lit', currLine, currCol)
                    currWholeCount = 0
                    currFracCount = 0
            elif not (wholeError or fracError):
                currToken += code[i]
                expected = nbl_delim
                add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
                currWholeCount = 0
                currFracCount = 0
            else:
                wholeError = False
                fracError = False
                currState = 's0'
                currToken = ''
                currWholeCount = 0
                currFracCount = 0
        #end of fractional number
        #& symbol
        if (currState == 's184'):
            currToken += code[i]
            if(code[i] == '&'):
                currState = 'LOGICAND_CHECK'
                continue
            else:
                add_error(unexpectedSymbol('&', currLine, currCol, lineContent))
        # end of | symbol
        #& symbol
        if (currState == 's223'):
            currToken += code[i]
            if(code[i] == '|'):
                currState = 'LOGICOR_CHECK'
                continue
            else:
                add_error(unexpectedSymbol('|', currLine, currCol, lineContent))
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
                    add_error(escSeqError(currToken, currLine, currCol, lineContent))
                else:
                    currToken += code[i]
                char_esc = False
                continue

        #end of special states

        #iterating through chars
        #check whitespaces
        if (currState not in ['s253', 's247', 's249']):
            if (code[i] == ' '):
                if (transition(currState, 'ANY') == 'DEFINED' and currState != 's0'):
                    add_token(currToken, 'Identifier', currLine, currCol)
                continue
            if (code[i] == '\n'):
                if (i != len(code)-1):
                    if (transition(currState, 'ANY') == 'DEFINED' and currState != 's0'):
                        add_token(currToken, 'Identifier', currLine, currCol)
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
                if (code[i] in numbers):
                    currToken += code[i]
                    print("(dbg)s0 is num")
                    #go to whole num loop state
                    currWholeCount += 1
                    currState = 's300'  
                    continue
                elif (code[i] not in alphanum + ['_'] and i != len(code)-1):
                    print("(dbg) unexpected")
                    add_error(unexpectedSymbol(currToken, currLine, currCol, lineContent))
                    continue
                currToken += code[i]
                if (code[i] in alphabetic_chars and i != len(code)-1):
                    print(f'(dbg) index {i}')
                    print(f'(dbg) length {len(code)}')
                    currState = 's244'
                continue
            else:
                if (currState == 's249'):
                    currToken += code[i]
                    continue
                if (currState == 's253'):
                    if (code[i] == '\n'):
                        add_error(stringMissingClose(currToken, currLine, currCol, lineContent))
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
                                add_error(idenFirstError(currToken, currLine, currCol,lineContent))
                            else:
                                add_error(unexpectedSymbol(currToken, currLine, currCol, lineContent))
                        else:
                            print("(dbg) other iden append")
                            if (currToken[0] not in alphabetic_chars):
                                add_error(idenFirstError(currToken, currLine, currCol,lineContent))
                            else:
                                add_token(currToken, 'Identifier', currLine, currCol)
                            currToken = code[i]
                            currState = transition('s0', code[i])
                    else:
                        add_error(idenFirstError(currToken, currLine, currCol,lineContent))
                else:
                    currToken += code[i]
                    expected = iden_delim
                    if (code[i-1] in arithmetic_operator):
                        expected = ['alphanum', ' ', '(']
                    if (code[i-1] == '+'):
                        expected.append('\"')
                    print('(dbg) currState: ', currState)
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected))
    
    lexerResults = [tokens, errors] 
    return lexerResults

#---LEXER ERRORS---
def generateError(errorType, currToken, currLine, currCol, lineContent, additionalInfo=None):
    """
    Generates a lexical error message.
    """
    print('(dbg) currToken ', currToken)
    print('(dbg) currCol ', currCol)
    errorMsg = f'Lexical Error ({currLine}, {currCol - len(currToken)}): {errorType} {currToken[:-1]}\n'
    errorMsg += lineContent + '\n'
    errorMsg += '_' * (currCol - len(currToken) - 2) + '^\n'
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

def escSeqError(currToken, currLine, currCol, lineContent):
    errorType = "Invalid escape sequence for string literal"
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

#---TOKEN CLASS---#
class Token:
    def __init__(self, token_name, token_type, token_line, token_col):
        self.token_name = token_name
        self.token_type = token_type
        self.token_line = token_line
        self.token_col = token_col

    # Convert list of Token objects to dicts before passing them to jsonify bc Token objects are not JSON serializable by default
    def to_dict(self): 
        return {
            "tokenName": self.token_name,
            "tokenType": self.token_type,
            "tokenLine": self.token_line,
            "tokenCol": self.token_col
        }

#---FLASK ROUTES---
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'})

@app.route('/api/compile', methods=['POST'])
def compile_code():
    data = request.json
    code = data.get('code', '')
    code += '\n'
    
    lexer_results = lexer(code)  # Returns [tokens, errors]
    tokens, errors = lexer_results  # Unpack the results

    # Calls syntax analyzer
    try:
        analyzer = syntax_analyzer.SyntaxAnalyzer(tokens)
        # errors += analyzer.parse()    # comment out to just test for lexer
    except SyntaxError as e:
        print(e)


    # Convert Token objects to dictionaries
    tokens_dict = [token.to_dict() for token in tokens]

    # Create a JSON-serializable response
    response = {
        "tokens": tokens_dict or [],  # should not send out None/null 
        "errors": errors or []        
    }

    # print json output
    # print('\n\n', json.dumps(response, indent=2))
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True) 