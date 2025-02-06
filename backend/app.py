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
open_paren_delim = list(set(arithmetic_delim + ['\"', '!', ')', '\n', '/', '+', '-', ';']))
closing_delim = list(set(arithmetic_operator + arithmetic_delim + logical_operator_delim + newline_delim + relational_operator_delim + whitespace + ['=', '|', '{', ';', ')', '(', '/', ':', ']', '?', '}', '"',',']))
close_paren_delim = list(set(closing_delim))
semicolon_delim = newline_delim + plaintext_delim + ['}', '/', '(', ')']
negative_delim = list(set(arithmetic_delim + ['/', '+']))
exclamation_delim = alphabetic_chars + newline + whitespace + ['(', '/', '!']
percent_delim = list(set(arithmetic_delim + ['/']))
asterisk_delim = list(set(arithmetic_delim + ['/', '+', '-']))
dot_delim = alphabetic_chars + whitespace + ['\n', '/'] # from plaintext_delim + ['\n', '/']
comma_delim = dot_delim + numbers + ['(', '{', '"']
slash_delim = plaintext_delim + ['\n', '(', '+', '-']
question_delim = newline + plaintext_delim + ['(', '/', '\"']
colon_delim = newline + plaintext_delim + ['(', '/', '\"']
open_bracket_delim = alphanum + whitespace + ['\n', '/', '(', ']','+', '-']
open_curly_delim = newline_delim + plaintext_delim + ['{', '}', '/', '\"', '(', '+', '-']
close_curly_delim = newline_delim + plaintext_delim + [';', '/', ',', '}', '+', '-']
plus_delim = list(set(arithmetic_delim + ['\"', '/', '-']))
great_less_delim = list(set(arithmetic_delim + ['/', '+', '-']))
great_delim = great_less_delim + [';']
equal_delim = list(set(arithmetic_delim + ['\"', '/', '!', '!','{']))
in_delim = newline_delim + ['<', '/']
this_delim = newline_delim + ['.', '/']
void_delim = newline + whitespace + ['/']
decrement_delim = alphabetic_chars + whitespace + newline + [';', ')', '/', '+', '*', '%', '(', ']']
subtract_assign_delim = list(set(arithmetic_delim + ['/','+','-']))
not_equal_delim = alphanum + newline + whitespace + ['(', '!','\"','+','-']
modulo_assign_delim = list(set(arithmetic_delim + ['/', '+', '-']))
and_or_delim =  alphabetic_chars + whitespace + ['(', '\n', '/', '!']
multi_assign_delim = list(set(arithmetic_delim + ['/', '+', '-']))
divi_assign_delim = list(set(arithmetic_delim + ['/', '+', '-']))
increment_delim = alphabetic_chars + whitespace + newline_delim + [')', ';', '/', '-', '*', '%', '(', ']']
add_assign_delim = list(set(arithmetic_delim + ['/', '\"', '+', '-']))
equal_equal_delim = list(set(arithmetic_delim + ['\"', '/', '!', '+', '-']))
import_delim = newline + whitespace + ['<', '/']
loop_delim = whitespace + newline + ['(', '/']
block_delim = whitespace + newline + ['{', '/']
break_ret_cont_delim = newline_delim + [';', '/']
case_delim = newline_delim + ['(', '/']
iden_delim = newline_delim + [',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '.', '|', '(', ')', '[', ']', '{', '}', '?', ':', ';']
str_lit_delim = list(set(newline + whitespace + logical_operator_delim + ['+', ')', ',', ';', '/', ':', '!', '=', '}', '?']))
nbl_delim = list(set(arithmetic_operator + relational_operator_delim + logical_operator_delim + whitespace + newline + [',', ')', ']', '}', ':', '=', ';', '/', '?']))
func_delim = newline_delim + ['(']
closing_bracket_delim = newline_delim + [',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', ')', '[', ']', ':', ';']

def transition(currState, currChar):
    match currState:
        case 's0':
            match currChar:
                case 'b':  currState = 's1'
                case 'c':  currState = 's11'
                case 'd':  currState = 's36'
                case 'e':  currState = 's51'
                case 'f':  currState = 's56'
                case 'i':  currState = 's70'
                case 'l':  currState = 's83'
                case 'p':  currState = 's88'
                case 'r':  currState = 's102'
                case 's':  currState = 's114'
                case 't':  currState = 's132'
                case 'v':  currState = 's141'
                case 'w':  currState = 's146'
                case '-':  currState = 'DASH_CHECK'
                case '!':  currState = 'NEGATION_CHECK'
                case '%':  currState = 'MODULO_CHECK'
                case '&':  currState = 's166'
                case '(':  currState = 'OPEN_PAREN_CHECK'
                case ')':  currState = 'CLOSING_PAREN_CHECK'
                case '*':  currState = 'ASTERISK_CHECK'
                case ',':  currState = 'COMMA_CHECK'
                case '.':  currState = 'DOT_CHECK'
                case '/':  currState = 'SLASH_CHECK'
                case '?':  currState = 'QUESTION_CHECK'
                case ':':  currState = 'COLON_CHECK'
                case '[':  currState = 'OPEN_BRACKET_CHECK'
                case ']':  currState = 'CLOSING_BRACKET_CHECK'
                case '{':  currState = 'OPEN_CURLY_CHECK'
                case '}':  currState = 'CLOSING_CURLY_CHECK'
                case '|':  currState = 's207'
                case '"':  currState = 's253'
                case '+':  currState = 'PLUS_CHECK'
                case '<':  currState = 'OPEN_ANGLE_CHECK'
                case '>':  currState = 'CLOSING_ANGLE_CHECK'
                case '=':  currState = 'ASSIGN_CHECK'
                case ';': currState = 'SEMICOLON_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        #### RESERVED WORDS #####################################

        case 's1':
            match currChar:
                case 'o':  currState = 's2'
                case 'r':  currState = 's6'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's2':
            match currChar:
                case 'o':  currState = 's3'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
        
        case 's3':
            match currChar:
                case 'l': currState = 'BOOL_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's6':
            match currChar:
                case 'e':  currState = 's7'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
        
        case 's7':
            match currChar:
                case 'a':  currState = 's8'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's8':
            match currChar:
                case 'k':  currState = 'BREAK_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
            
        case 's11':
            match currChar:
                case 'a':  currState = 's12'
                case 'h':  currState = 's16'
                case 'l':  currState = 's20'
                case 'o':  currState = 's25'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's12':
            match currChar:
                case 's':  currState = 's13'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's13':
            match currChar:
                case 'e':  currState = 'CASE_CHECK' 
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's16':
            match currChar:
                case 'a':  currState = 's17'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's17':
            match currChar:
                case 'r':  currState = 'CHAR_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's20':
            match currChar:
                case 'a':  currState = 's21'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
        
        case 's21':
            match currChar:
                case 's':  currState = 's22'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
        
        case 's22':
            match currChar:
                case 's':  currState = 'CLASS_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
        
        case 's25':
            match currChar:
                case 'n':  currState = 's26'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's26':
            match currChar:
                case 't':  currState = 's27'
                case 's':  currState = 's33'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
                
        case 's27':
            match currChar:
                case 'i':  currState = 's28'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's28':
            match currChar:
                case 'n':  currState = 's29'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's29':
            match currChar:
                case 'u':  currState = 's30'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's30':
            match currChar:
                case 'e':  currState = 'CONTINUE_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's33':
            match currChar:
                case 't':  currState = 'CONST_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's36':
            match currChar:
                case 'e':  currState = 's37'
                case 'o':  currState = 'DO_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's37':
            match currChar:
                case 'f':  currState = 's38'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's38':
            match currChar:
                case 'a':  currState = 's39'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's39':
            match currChar:
                case 'u':  currState = 's40'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's40':
            match currChar:
                case 'l':  currState = 's41'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's41':
            match currChar:
                case 't':  currState = 'DEFAULT_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's44':
            match currChar:
                case 'u':  currState = 's46'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's46':
            match currChar:
                case 'b':  currState = 's47'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's47':
            match currChar:
                case 'l':  currState = 's48'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's48':
            match currChar:
                case 'e':  currState = 'DOUBLE_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's51':
            match currChar:
                case 'l':  currState = 's52'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's51':
            match currChar:
                case 'l':  currState = 's52'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's52':
            match currChar:
                case 's':  currState = 's53'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's53':
            match currChar:
                case 'e':  currState = 'ELSE_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's56':
            match currChar:
                case 'a':  currState = 's57'
                case 'l':  currState = 's62'
                case 'o':  currState = 's67'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's57':
            match currChar:
                case 'l':  currState = 's58'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's58':
            match currChar:
                case 's':  currState = 's59'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's59':
            match currChar:
                case 'e':  currState = 'FALSE_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's62':
            match currChar:
                case 'o':  currState = 's63'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's63':
            match currChar:
                case 'a':  currState = 's64'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's64':
            match currChar:
                case 't':  currState = 'FLOAT_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's67':
            match currChar:
                case 'r':  currState = 'FOR_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's70':
            print("(dbg) in s70 now")
            match currChar:
                case 'f':  currState = 'IF_CHECK'
                case 'm':  currState = 's73'
                case 'n':  currState = 'IN_CHECK'
                case 'ANY': 
                    print("(dbg) any defined s74")
                    currState = 'DEFINED'
                case _:  
                    print("(dbg) undefined s74 next ")
                    currState = 'UNDEFINED'

        case 's73':
            match currChar:
                case 'p':  currState = 's74'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's74':
            match currChar:
                case 'o':  currState = 's75'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's75':
            match currChar:
                case 'r':  currState = 's76'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's76':
            match currChar:
                case 't':  currState = 'IMPORT_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's79':
            match currChar:
                case 't':  currState = 'INT_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's83':
            match currChar:
                case 'o':  currState = 's84'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's84':
            match currChar:
                case 'n':  currState = 's85'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
    
        case 's85':
            match currChar:
                case 'g':  currState = 'LONG_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's88':
            match currChar:
                case 'r':  currState = 's89'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's89':
            match currChar:
                case 'i':  currState = 's90'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's90':
            match currChar:
                case 'n':  currState = 's91'
                case 'v':  currState = 's97'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
        
        case 's91':
            match currChar:
                case 't':  currState = 'PRINT_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's92':
            match currChar:
                case 'l':  currState = 's94'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's94':
            match currChar:
                case 'n':  currState = 'PRINTLN_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
        
        case 's97':
            match currChar:
                case 'a':  currState = 's98'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's98':
            match currChar:
                case 't':  currState = 's99'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's99':
            match currChar:
                case 'e':  currState = 'PRIVATE_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's102':
            match currChar:
                case 'e':  currState = 's103'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's103':
            match currChar:
                case 'p':  currState = 's104'
                case 't':  currState = 's109'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's104':
            match currChar:
                case 'e':  currState = 's105'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's105':
            match currChar:
                case 'a':  currState = 's106'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's106':
            match currChar:
                case 't':  currState = 'REPEAT_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's109':
            match currChar:
                case 'u':  currState = 's110'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's110':
            match currChar:
                case 'r':  currState = 's111'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's111':
            match currChar:
                case 'n':  currState = 'RETURN_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
    
        case 's114':
            match currChar:
                case 't':  currState = 's115'
                case 'w':  currState = 's126'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's115':
            match currChar:
                case 'a':  currState = 's116'
                case 'r':  currState = 's121'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's116':
            match currChar:
                case 't':  currState = 's117'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's117':
            match currChar:
                case 'i':  currState = 's118'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's118':
            match currChar:
                case 'c':  currState = 'STATIC_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's121':
            match currChar:
                case 'i':  currState = 's122'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's122':
            match currChar:
                case 'n':  currState = 's123'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's123':
            match currChar:
                case 'g':  currState = 'STRING_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's126':
            match currChar:
                case 'i':  currState = 's127'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's127':
            match currChar:
                case 't':  currState = 's128'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
        
        case 's128':
            match currChar:
                case 'c':  currState = 's129'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's129':
            match currChar:
                case 'h':  currState = 'SWITCH_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
        
        case 's132':
            match currChar:
                case 'h':  currState = 's133'
                case 'r':  currState = 's137'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
    
        case 's133':
            match currChar:
                case 'i':  currState = 's134'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's134':
            match currChar:
                case 's':  currState = 'THIS_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's137':
            match currChar:
                case 'u':  currState = 's138'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's138':
            match currChar:
                case 'e':  currState = 'TRUE_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's141':
            match currChar:
                case 'o':  currState = 's142'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's142':
            match currChar:
                case 'i':  currState = 's143'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's143':
            match currChar:
                case 'd':  currState = 'VOID_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's146':
            match currChar:
                case 'h':  currState = 's147'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's147':
            match currChar:
                case 'i':  currState = 's148'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's148':
            match currChar:
                case 'l':  currState = 's149'
                case 'ANY':  currState = 'DEFINED'
                case _:  currState = 'UNDEFINED'

        case 's149':
            match currChar:
                case 'e':  currState = 'WHILE_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        #### RESERVED SYMBOLS #######################################

        case 's152':
            match currChar:
                case '-':  currState = 'DECREMENT_CHECK'
                case '=':  currState = 'MINUS_ASS_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's158':
            match currChar:
                case '=':  currState = 'NOT_EQUAL_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's162':
            match currChar:
                case '=':  currState = 'MODULO_ASS_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's166':
            match currChar:
                case '&':  currState = 'LOGICAND_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's173':
            match currChar:
                case '=':  currState = 'MULT_ASS_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's183':
            match currChar:
                case '*':  currState = 's249'
                case '/':  currState = 's247'
                case '=':  currState = 'DIV_ASS_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's207':
            match currChar:
                case '|':  currState = 'LOGICOR_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's210':
            match currChar:
                case '+':  currState = 'INCREMENT_CHECK'
                case '=':  currState = 'ADD_ASS_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
        
        case 's216':
            match currChar:
                case '=':  currState = 'LESS_OR_EQUAL_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's220':
            match currChar:
                case '=':  currState = 'GREATER_OR_EQUAL_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
    
        case 's224':
            match currChar:
                case '=':  currState = 'EQUAL_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's244':
            match currChar:
                case '_':  currState = 's244'
                case _ if currChar in alphanum:  currState = 's244'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's247':
            match currChar:
                case _ if currChar in ascii:  currState = 's247'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's249':
            match currChar:
                case '\n':  currState = 's249'
                case '*':  currState = 's250' #catches * before ascii check
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's250':
            match currChar:
                case '/':  currState = 'MULTI_COMMENT_CHECK'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's253':
            match currChar:
                case '"':  currState = 'STRING_LIT_CHECK' #catches " before ascii check
                case _ if currChar in ascii:  currState = 's253'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'

        case 's267':
            match currChar:
                case _ if currChar in numbers:  currState = 's267'
                case 'ANY':  currState = 'DEFINED'
                case _:   currState = 'UNDEFINED'
        
        case 's300':
            match currChar:
                case '.':  currState = 's267'
                case _ if currChar in numbers: currState = 's300'
                case 'ANY':  currState = 'DEFINED'
                case _:  currState = 'UNDEFINED' 
    
    print (currState)
    return currState             



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
    leadingSpaces = 0
    isLeadingSpace = True
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
            leadingSpaces = 0
            isLeadingSpace = True
            lineContent = ''
        else:
            if code[i] != ' ':
                isLeadingSpace = False
            if isLeadingSpace:
                leadingSpaces += 1
            currCol += 1
            lineContent += code[i]

        #if no transitions, it means it's time for delim checking
        if (transition(currState, 'ANY') != 'DEFINED'):
            print('(dbg) delim checking')
            match currState:
            #data type keywords
                case 'BOOL_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                case 'DOUBLE_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                case 'FLOAT_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                case 'INT_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                case 'LONG_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                case 'STRING_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                #break statement
                case 'BREAK_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # ( symbol
                case 'OPEN_PAREN_CHECK':
                    expected = ['alphanum', ' ', '\"', '!', ')', '+', '-', '/']
                    if (code[i] in open_paren_delim):
                        add_token(currToken, '(', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # ) symbol
                case 'CLOSING_PAREN_CHECK':
                    expected = ['alphanum', '=', '&', '|', '{', '(', ')', ';', '\n', ',', '/', ':', ']','?',','] + [';', '\n', '/']
                    if (code[i] in close_paren_delim):
                        add_token(currToken, ')', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # ; symbol
                case 'SEMICOLON_CHECK':
                    expected = ['alphanum', ' ', '}', '/', '('] + newline
                    if (code[i] in semicolon_delim):
                        add_token(currToken, ';', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # - symbol
                case 'DASH_CHECK':
                    expected = ['alphanum', ' ', '(', '+', '/']
                    if (code[i] in negative_delim):
                        add_token(currToken, '-', currLine, currCol)
                    elif (code[i] in ['-', '=']):
                        print('(dbg) going to s170')
                        currState = 's152'
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # ! symbol
                case 'NEGATION_CHECK':
                    expected = ['alphabetic_chars', '(', '/', '!'] + whitespace + newline
                    if (code[i] in exclamation_delim):
                        add_token(currToken, '!', currLine, currCol)
                    elif (code[i] == '='):
                        currState = 's158'
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # % symbol
                case 'MODULO_CHECK':
                    expected = ['alphanum', ' ', '(', '+', '-', '/']
                    if (code[i] in percent_delim):
                        add_token(currToken, '%', currLine, currCol)
                    elif (code[i] == '='):
                        currState = 's162'
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # * symbol
                case 'ASTERISK_CHECK':
                    expected = ['alphanum', ' ', '(', '+', '-', '/']
                    if (code[i] in asterisk_delim):
                        add_token(currToken, '*', currLine, currCol)
                    elif (code[i] in ['/', '=']):
                        currState = 's173'
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # , symbol
                case 'COMMA_CHECK':
                    expected = ['alphanum', ' ', '/', '(', '{']
                    if (code[i] in comma_delim):
                        add_token(currToken, ',', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # . symbol
                case 'DOT_CHECK':
                    expected = ['alphabetic_chars', '/'] + whitespace
                    if (code[i] in numbers):
                        currState = 's267'
                    elif (code[i] in dot_delim):
                        add_token(currToken, '.', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # / symbol
                case 'SLASH_CHECK':
                    expected = ['alphanum', ' ', '(', '+', '-']
                    if (code[i] in slash_delim):
                        add_token(currToken, '/', currLine, currCol)
                    elif (code[i] in ['*', '/', '=']):
                        currState = 's183'
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # ? symbol
                case 'QUESTION_CHECK':
                    expected = ['alphanum', '(', '/', '\"'] + newline
                    if (code[i] in question_delim):
                        add_token(currToken, '?', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # : symbol
                case 'COLON_CHECK':
                    expected = ['alphanum', '(', ' ', '/'] + newline
                    if (code[i] in colon_delim):
                        add_token(currToken, ':', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # [ symbol
                case 'OPEN_BRACKET_CHECK':
                    expected = ['alphanum', ']', '/', '\n', '(', '+', '-'] + whitespace
                    if (code[i] in open_bracket_delim):
                        add_token(currToken, '[', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # ] symbol
                case 'CLOSING_BRACKET_CHECK':
                    expected = closing_bracket_delim
                    if (code[i] in expected):
                        add_token(currToken, ']', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # { symbol
                case 'OPEN_CURLY_CHECK':
                    expected = ['alphanum', ' ', '{', '}', '/', '+', '-', '\"', '('] + newline_delim
                    if (code[i] in open_curly_delim):
                        add_token(currToken, '{', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # } symbol
                case 'CLOSING_CURLY_CHECK':
                    expected = ['alphanum', ' ', ';', ',','}', '+', '-'] + newline_delim
                    if (code[i] in close_curly_delim):
                        add_token(currToken, '}', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # + symbol
                case 'PLUS_CHECK':
                    expected = ['alphanum', ' ', '(', '\"', '+', '-', '/']
                    if (code[i] in plus_delim):
                        add_token(currToken, '+', currLine, currCol)
                    else:
                        currState = 's210'
                # < symbol
                case 'OPEN_ANGLE_CHECK':
                    expected = ['alphanum', ' ', '(', '+', '-', '/'] + newline
                    print("(dbg) open angle check curr char ", code[i])
                    if (code[i] in great_less_delim):
                        print("(dbg) arithmetic spotted for <")
                        add_token(currToken, '<', currLine, currCol)
                    elif (code[i] == '='):
                        currState = 's216'
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # > symbol
                case 'CLOSING_ANGLE_CHECK':
                    expected = ['alphanum', ' ', '(', ';', '+', '-', '/'] + newline
                    if (code[i] in great_delim):
                        add_token(currToken, '>', currLine, currCol)
                    elif (code[i] == '='):
                        currState = 's220'
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # = symbol
                case 'ASSIGN_CHECK':
                    expected = ['alphanum', ' ', '\"', '+', '-', '/', '!']
                    if (code[i] in equal_delim):
                        add_token(currToken, '=', currLine, currCol)
                    else:
                        currState = 's224'
                # in statement
                case 'IN_CHECK':
                    expected = ['<', '/']
                    if (code[i] in in_delim):
                        add_token(currToken, 'in', currLine, currCol)
                    elif(code[i] in alphanum + ['_']):
                        currState = 's79'
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # print statement
                case 'PRINT_CHECK':
                    expected = func_delim
                    if (code[i] in func_delim):
                        add_token(currToken, 'print', currLine, currCol)
                    elif(code[i] in alphanum + ['_']):
                        currState = 's92'
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # println statement
                case 'PRINTLN_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # private statement
                case 'PRIVATE_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # repeat statement
                case 'REPEAT_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # return statement
                case 'RETURN_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # static statement
                case 'STATIC_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # switch statement
                case 'SWITCH_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # this statement
                case 'THIS_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # this statement
                case 'TRUE_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # void statement
                case 'VOID_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # while statement
                case 'WHILE_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # -- symbol
                case 'DECREMENT_CHECK':
                    expected = whitespace + ['alphabetic_chars'] + [';', ')', '/', '+', '*', '%', '(', ']'] + newline
                    if (code[i] in decrement_delim):
                        add_token(currToken, '--', currLine, currCol)
                    elif (code[i] in numbers):
                        currToken += code[i]
                        add_error(adjustConstNumError(currToken, currLine, currCol, lineContent, leadingSpaces))
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # -= symbol
                case 'MINUS_ASS_CHECK':
                    expected = ['alphanum', ' ', '(', '+', '-', '/']
                    if (code[i] in subtract_assign_delim):
                        add_token(currToken, '-=', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # != symbol
                case 'NOT_EQUAL_CHECK':
                    expected = whitespace + ['alphanum', '(', '"', '!','+','-'] + newline
                    if (code[i] in not_equal_delim):
                        add_token(currToken, '!=', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # %= symbol
                case 'MODULO_ASS_CHECK':
                    expected = ['alphanum', ' ', '(', '+', '-', '/']
                    if (code[i] in modulo_assign_delim):
                        add_token(currToken, '%=', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # && symbol
                case 'LOGICAND_CHECK':
                    expected = ['alphabetic_chars', ' ', '(', '/', '!']
                    if (code[i] in and_or_delim):
                        add_token(currToken, '&&', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # *= symbol
                case 'MULT_ASS_CHECK':
                    expected = ['alphanum', ' ', '(', '+', '-', '/']
                    if (code[i] in multi_assign_delim):
                        add_token(currToken, '*=', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # /= symbol
                case 'DIV_ASS_CHECK':
                    expected = ['alphanum', ' ', '(', '+', '-', '/']
                    if (code[i] in divi_assign_delim):
                        add_token(currToken, '/=', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # || symbol
                case 'LOGICOR_CHECK':
                    expected = ['alphabetic_chars', ' ', '(', '/', '!']
                    if (code[i] in and_or_delim):
                        add_token(currToken, '||', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # ++ symbol
                case 'INCREMENT_CHECK':
                    expected = whitespace + ['alphabetic_chars', ')', ';', '/', '-', '*', '%', '(', ']']
                    if (code[i] in increment_delim):
                        add_token(currToken, '++', currLine, currCol)
                    elif (code[i] in numbers):
                        currToken += code[i]
                        add_error(adjustConstNumError(currToken, currLine, currCol, lineContent, leadingSpaces))
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # += symbol
                case 'ADD_ASS_CHECK':
                    expected = ['alphanum', ' ', '(', '\"', '+', '-', '/']
                    if (code[i] in add_assign_delim):
                        add_token(currToken, '+=', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # <= symbol
                case 'LESS_OR_EQUAL_CHECK':
                    expected = ['alphanum', ' ', '(', '+', '-', '/']
                    if (code[i] in great_less_delim):
                        add_token(currToken, '<=', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # >= symbol
                case 'GREATER_OR_EQUAL_CHECK':
                    expected = ['alphanum', ' ', '(', '+', '-', '/']
                    if (code[i] in great_less_delim):
                        add_token(currToken, '>=', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # == symbol
                case 'EQUAL_CHECK':
                    expected = ['alphanum', ' ', '(', '\"', '+', '-', '/', '!']
                    if (code[i] in equal_equal_delim):
                        add_token(currToken, '==', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # string literal
                case 'STRING_LIT_CHECK':
                    expected = str_lit_delim
                    if (code[i] in str_lit_delim):
                        add_token(currToken, 'string_lit', currLine, currCol)
                    else:
                        currToken += code[i]
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # multicomments 
                case 'MULTI_COMMENT_CHECK':
                    add_token(currToken, 'multi-line comment', currLine, currCol)
                # case statement 
                case 'CASE_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # class statement 
                case 'CLASS_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # continue statement 
                case 'CONTINUE_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # const statement 
                case 'CONST_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # default statement 
                case 'DEFAULT_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # do statement 
                case 'DO_CHECK':
                    expected = block_delim
                    if (code[i] in block_delim):
                        add_token(currToken, 'do', currLine, currCol)
                    elif(code[i] in alphanum + ['_']):
                        currState = 's44'
                    else:
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # else statement 
                case 'ELSE_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # false statement
                case 'FALSE_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # for statement
                case 'FOR_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # if statement
                case 'IF_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                # import statement
                case 'IMPORT_CHECK':
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
                        add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
        # end of delim checking if statement
#---SPECIAL STATES---
        #identifier state
        if (currState == 's244'):
            print('(dbg) in identifier check state now')
            if (code[i] in iden_delim):
                print('(dbg) correct delim')    
                if (currToken[0] not in alphabetic_chars):
                        add_error(idenFirstError(currToken, currLine, currCol,lineContent, leadingSpaces))
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
                add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
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
                add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
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
                add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
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
                add_error(unexpectedSymbol('&', currLine, currCol, lineContent, leadingSpaces))
        # end of | symbol
        #& symbol
        if (currState == 's223'):
            currToken += code[i]
            if(code[i] == '|'):
                currState = 'LOGICOR_CHECK'
                continue
            else:
                add_error(unexpectedSymbol('|', currLine, currCol, lineContent, leadingSpaces))
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
                    add_error(escSeqError(currToken, currLine, currCol, lineContent, leadingSpaces))
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
                    if currToken not in ['&', '|']:
                        add_token(currToken, 'Identifier', currLine, currCol)
                    else:
                        add_error(unexpectedSymbol(currToken, currLine, currCol, lineContent, leadingSpaces))
                continue
            if (code[i] == '\n'):
                if (i != len(code)-1):
                    if (transition(currState, 'ANY') == 'DEFINED' and currState != 's0'):
                        if currToken not in ['&', '|']:
                            add_token(currToken, 'Identifier', currLine, currCol)
                        else:
                            add_error(unexpectedSymbol(currToken, currLine, currCol, lineContent, leadingSpaces))
                    continue
                
        #check states
        print(f'(dbg) transition val {transition(currState, code[i])}')
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
                elif (code[i] not in alphanum and i != len(code)-1):
                    print("(dbg) unexpected")
                    add_error(unexpectedSymbol(currToken, currLine, currCol, lineContent, leadingSpaces))
                    continue
                currToken += code[i]
                if (code[i] in alphabetic_chars and i != len(code)-1):
                    print(f'(dbg) index {i}')
                    print(f'(dbg) length {len(code)}')
                    currState = 's244'
                continue
            else:
                print('(dbg) not in s0')
                if (currState == 's249'):
                    currToken += code[i]
                    continue
                if (currState == 's253'):
                    if (code[i] == '\n'):
                        add_error(stringMissingClose(currToken, currLine, currCol, lineContent, leadingSpaces))
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
                        print(f'(dbg) currtoken valid: {currToken}')
                        if (currToken[0] not in alphabetic_chars + ['_']):
                            print('(dbg) other idnefirst error')
                            print('(dbg) symbol ', code[i])
                            if code[i] not in symbols:
                                add_error(idenFirstError(currToken, currLine, currCol,lineContent, leadingSpaces))
                            else:
                                add_error(unexpectedSymbol(currToken, currLine, currCol, lineContent, leadingSpaces))
                        else:
                            print("(dbg) other iden append")
                            if (currToken[0] not in alphabetic_chars):
                                add_error(idenFirstError(currToken, currLine, currCol,lineContent, leadingSpaces))
                            else:
                                add_token(currToken, 'Identifier', currLine, currCol)
                            currToken = code[i]
                            currState = transition('s0', code[i])
                    else:
                        add_error(idenFirstError(currToken, currLine, currCol,lineContent, leadingSpaces))
                else:
                    currToken += code[i]
                    expected = iden_delim
                    if (code[i-1] in arithmetic_operator):
                        expected = ['alphanum', ' ', '(']
                    if (code[i-1] == '+'):
                        expected.append('\"')
                    print('(dbg) currState: ', currState)
                    add_error(delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
    
    lexerResults = [tokens, errors] 
    return lexerResults

#---LEXER ERRORS---
def generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces, additionalInfo=None):
    """
    Generates a lexical error message.
    """
    print('(dbg) currToken ', currToken)
    print('(dbg) ERROR msg currCol ', currCol)
    errorMsg = f'Lexical Error ({currLine}, {currCol - len(currToken)}): {errorType} {currToken}\n'
    errorMsg += lineContent + '\n'
    print(f'(dbg) ERROR lineContent |{lineContent}')
    errorMsg += '_' * (currCol - len(currToken) - 2 - leadingSpaces) + '^\n'
    if additionalInfo:
        errorMsg += additionalInfo
    print("(debug) ", errorMsg)
    if (currCol == 0):
        return ''
    return errorMsg

def delimError(currToken, currLine, currCol, incorrectDelim, lineContent, expected, leadingSpaces):
    errorType = f"Unexpected {'newline' if incorrectDelim == '\\n' else incorrectDelim} for"
    additionalInfo = f"Expected delimiters: {expected}"
    return generateError(errorType, currToken[:-1], currLine, currCol, lineContent, leadingSpaces, additionalInfo)

def idenFirstError(currToken, currLine, currCol, lineContent, leadingSpaces):
    errorType = "Identifier must start with an alpha character"
    return generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

def stringMissingClose(currToken, currLine, currCol, lineContent, leadingSpaces):
    errorType = "Missing closing \" for string literal"
    return generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

def escSeqError(currToken, currLine, currCol, lineContent, leadingSpaces):
    errorType = "Invalid escape sequence for string literal"
    return generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

def charLengthError(currToken, currLine, currCol, lineContent, leadingSpaces):
    errorType = "Invalid character length for character literal"
    return generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

def wholeRangeError(currToken, currLine, currCol, lineContent, leadingSpaces):
    errorType = "Numeric exceeding max range"
    return generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

def fracPrecError(currToken, currLine, currCol, lineContent, leadingSpaces):
    errorType = "Numeric exceeding max precision"
    return generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

def unexpectedSymbol(currToken, currLine, currCol, lineContent, leadingSpaces):
    errorType = "Unexpected symbol"
    return generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

def adjustConstNumError(currToken, currLine, currCol, lineContent, leadingSpaces):
    errorType = "Increment or decrement operation is not allowed on constants"
    return generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

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
        errors += analyzer.parse()    # comment out to just test for lexer
    except SyntaxError as e:
        print(e)


    # Convert Token objects to dictionaries
    tokens_dict = [token.to_dict() for token in tokens]
    #print(tokens_dict) #for testing

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