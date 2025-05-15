def _printlog(*args, sep=' ', end='\n'):
    message = sep.join(str(arg) for arg in args) + end
    with open('pos_char.log', 'a', encoding="utf-8") as f:
        f.write(message)
    print(*args, sep=sep, end=end)
class LexicalAnalyzer:
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
    negative_delim = list(set(arithmetic_delim + ['/', '+', '.']))
    exclamation_delim = alphabetic_chars + newline + whitespace + ['(', '/', '!']
    percent_delim = list(set(arithmetic_delim + ['/']))
    asterisk_delim = list(set(arithmetic_delim + ['/', '+', '-']))
    dot_delim = alphabetic_chars + whitespace + ['\n', '/'] # from plaintext_delim + ['\n', '/']
    comma_delim = dot_delim + numbers + ['(', '{', '"', '+', '-']
    slash_delim = plaintext_delim + ['\n', '(', '+', '-']
    question_delim = newline + plaintext_delim + ['(', '/', '\"']
    colon_delim = newline + plaintext_delim + ['/', '}']
    open_bracket_delim = alphanum + whitespace + ['\n', '/', '(', ']', '+', '-']
    open_curly_delim = newline_delim + plaintext_delim + ['{', '}', '/', '\"', '(', '+', '-', '!']
    close_curly_delim = newline_delim + plaintext_delim + [';', '/', ',', '}', '+', '-']
    plus_delim = list(set(arithmetic_delim + ['\"', '/', '-']))
    great_less_delim = list(set(arithmetic_delim + ['/', '+', '-']))
    great_delim = great_less_delim + [';']
    equal_delim = list(set(arithmetic_delim + ['\"', '/', '!', '!','{', '+', '-']))
    in_delim = newline_delim + ['<', '/']
    void_delim = newline + whitespace + ['/']
    decrement_delim = alphabetic_chars + whitespace + newline + [';', ')', '/', '+', '*', '%', '(', ']', ',']
    subtract_assign_delim = list(set(arithmetic_delim + ['/','+','-']))
    not_equal_delim = alphanum + newline + whitespace + ['(', '!','\"','+','-']
    modulo_assign_delim = list(set(arithmetic_delim + ['/', '+', '-']))
    and_or_delim =  alphabetic_chars + whitespace + ['(', '\n', '/', '!']
    multi_assign_delim = list(set(arithmetic_delim + ['/', '+', '-']))
    divi_assign_delim = list(set(arithmetic_delim + ['/', '+', '-']))
    increment_delim = alphabetic_chars + whitespace + newline_delim + [')', ';', '/', '-', '*', '%', '(', ']', ',']
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
    closing_bracket_delim = newline_delim + [',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', ')', '}', '[', ']', ':', ';']
    
    need_frac_num = False
    multi_line_start_found = False

    def transition(self, currState, currChar):
        global need_frac_num
        match currState:
            case 's0':
                match currChar:
                    case 'b':  currState = 's1'
                    case 'c':  currState = 's11'
                    case 'd':  currState = 's32'
                    case 'e':  currState = 's47'
                    case 'f':  currState = 's52'
                    case 'i':  currState = 's66'
                    case 'l':  currState = 's79'
                    case 'p':  currState = 's84'
                    case 'r':  currState = 's98'
                    case 's':  currState = 's110'
                    case 't':  currState = 's123'
                    case 'v':  currState = 's128'
                    case 'w':  currState = 's133'
                    case '-':  currState = 'DASH_CHECK' #s139 -> s140
                    case '!':  currState = 'NEGATION_CHECK' #s145 -> s146
                    case '%':  currState = 'MODULO_CHECK' #s149 -> s150
                    case '&':  currState = 's153'
                    case '(':  currState = 'OPEN_PAREN_CHECK' #s156 -> s157
                    case ')':  currState = 'CLOSING_PAREN_CHECK' #s158 -> s159
                    case '*':  currState = 'ASTERISK_CHECK' #s160 -> s161
                    case ',':  currState = 'COMMA_CHECK' #s164 -> s165
                    case '.':  currState = 'DOT_CHECK' #s166 -> s167
                    case '/':  currState = 'SLASH_CHECK' #s168 -> s169
                    case ':':  currState = 'COLON_CHECK' #s174 -> s175
                    case '[':  currState = 'OPEN_BRACKET_CHECK' #s176 -> s177
                    case ']':  currState = 'CLOSING_BRACKET_CHECK' #s178 -> s179
                    case '{':  currState = 'OPEN_CURLY_CHECK' #s180 -> s181
                    case '}':  currState = 'CLOSING_CURLY_CHECK' #s182 -> s183
                    case '|':  currState = 's184'
                    case '"':  currState = 's213'
                    case '+':  currState = 'PLUS_CHECK' #s187 -> s188
                    case '<':  currState = 'OPEN_ANGLE_CHECK' #s193 -> s194
                    case '>':  currState = 'CLOSING_ANGLE_CHECK' #s197 -> s198
                    case '=':  currState = 'ASSIGN_CHECK' #s201 -> s202
                    case ';': currState = 'SEMICOLON_CHECK' #s172 -> s173
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
                    case 'l': currState = 'BOOL_CHECK' #s4 -> s5
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
                    case 'k':  currState = 'BREAK_CHECK' #s9 -> s10
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
                
            case 's11':
                match currChar:
                    case 'a':  currState = 's12'
                    case 'l':  currState = 's16'
                    case 'o':  currState = 's21'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's12':
                match currChar:
                    case 's':  currState = 's13'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's13':
                match currChar:
                    case 'e':  currState = 'CASE_CHECK' #s14 -> s15
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's16':
                match currChar:
                    case 'a':  currState = 's17'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
            
            case 's17':
                match currChar:
                    case 's':  currState = 's18'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
            
            case 's18':
                match currChar:
                    case 's':  currState = 'CLASS_CHECK' #s19 -> s20
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
            
            case 's21':
                match currChar:
                    case 'n':  currState = 's22'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's22':
                match currChar:
                    case 't':  currState = 's23'
                    case 's':  currState = 's29'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
                    
            case 's23':
                match currChar:
                    case 'i':  currState = 's24'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's24':
                match currChar:
                    case 'n':  currState = 's25'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's25':
                match currChar:
                    case 'u':  currState = 's26'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's26':
                match currChar:
                    case 'e':  currState = 'CONTINUE_CHECK' #s27 -> s28
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's29':
                match currChar:
                    case 't':  currState = 'CONST_CHECK' #s30 -> s31
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's32':
                match currChar:
                    case 'e':  currState = 's33'
                    case 'o':  currState = 'DO_CHECK' #s40 -> s41
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's33':
                match currChar:
                    case 'f':  currState = 's34'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's34':
                match currChar:
                    case 'a':  currState = 's35'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's35':
                match currChar:
                    case 'u':  currState = 's36'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's36':
                match currChar:
                    case 'l':  currState = 's37'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's37':
                match currChar:
                    case 't':  currState = 'DEFAULT_CHECK' #s38 -> s39
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's40':
                match currChar:
                    case 'u':  currState = 's42'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's42':
                match currChar:
                    case 'b':  currState = 's43'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's43':
                match currChar:
                    case 'l':  currState = 's44'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's44':
                match currChar:
                    case 'e':  currState = 'DOUBLE_CHECK' #s45 -> s46
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's47':
                match currChar:
                    case 'l':  currState = 's48'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's48':
                match currChar:
                    case 's':  currState = 's49'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's49':
                match currChar:
                    case 'e':  currState = 'ELSE_CHECK' #s50 -> s51
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's52':
                match currChar:
                    case 'a':  currState = 's53'
                    case 'l':  currState = 's58'
                    case 'o':  currState = 's63'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's53':
                match currChar:
                    case 'l':  currState = 's54'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's54':
                match currChar:
                    case 's':  currState = 's55'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's55':
                match currChar:
                    case 'e':  currState = 'FALSE_CHECK' #s56 -> s57
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's58':
                match currChar:
                    case 'o':  currState = 's59'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's59':
                match currChar:
                    case 'a':  currState = 's60'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's60':
                match currChar:
                    case 't':  currState = 'FLOAT_CHECK' #s61 -> s62
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's63':
                match currChar:
                    case 'r':  currState = 'FOR_CHECK' #s64 -> s65
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's66':
                print("(dbg) in s66 now")
                match currChar:
                    case 'f':  currState = 'IF_CHECK' #s67 -> s68
                    case 'm':  currState = 's69'
                    case 'n':  currState = 'IN_CHECK' #s75 -> s76
                    case 'ANY': 
                        print("(dbg) any defined s74")
                        currState = 'DEFINED'
                    case _:  
                        print("(dbg) undefined s74 next ")
                        currState = 'UNDEFINED'

            case 's69':
                match currChar:
                    case 'p':  currState = 's70'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's70':
                match currChar:
                    case 'o':  currState = 's71'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's71':
                match currChar:
                    case 'r':  currState = 's72'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's72':
                match currChar:
                    case 't':  currState = 'IMPORT_CHECK' #s73 -> s74
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's75':
                match currChar:
                    case 't':  currState = 'INT_CHECK' #s77 -> s78
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's79':
                match currChar:
                    case 'o':  currState = 's80'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's80':
                match currChar:
                    case 'n':  currState = 's81'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
        
            case 's81':
                match currChar:
                    case 'g':  currState = 'LONG_CHECK' #s82 -> s83
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's84':
                match currChar:
                    case 'r':  currState = 's85' 
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's85':
                match currChar:
                    case 'i':  currState = 's86'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's86':
                match currChar:
                    case 'n':  currState = 's87'
                    case 'v':  currState = 's93'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
            
            case 's87':
                match currChar:
                    case 't':  currState = 'PRINT_CHECK' #s88 -> s89
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's88':
                match currChar:
                    case 'l':  currState = 's90'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's90':
                match currChar:
                    case 'n':  currState = 'PRINTLN_CHECK' #s91 -> s92
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
            
            case 's93':
                match currChar:
                    case 'a':  currState = 's94'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's94':
                match currChar:
                    case 't':  currState = 's95'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's95':
                match currChar:
                    case 'e':  currState = 'PRIVATE_CHECK' #s96 -> s97
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's98':
                match currChar:
                    case 'e':  currState = 's99'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's99':
                match currChar:
                    case 'p':  currState = 's100'
                    case 't':  currState = 's105'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's100':
                match currChar:
                    case 'e':  currState = 's101'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's101':
                match currChar:
                    case 'a':  currState = 's102'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's102':
                match currChar:
                    case 't':  currState = 'REPEAT_CHECK' #s103 -> s104
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's105':
                match currChar:
                    case 'u':  currState = 's106'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's106':
                match currChar:
                    case 'r':  currState = 's107'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's107':
                match currChar:
                    case 'n':  currState = 'RETURN_CHECK' #s108 -> s109
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
        
            case 's110':
                match currChar:
                    case 't':  currState = 's111'
                    case 'w':  currState = 's117'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's111':
                match currChar:
                    case 'r':  currState = 's112'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's112':
                match currChar:
                    case 'i':  currState = 's113'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's113':
                match currChar:
                    case 'n':  currState = 's114'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's114':
                match currChar:
                    case 'g':  currState = 'STRING_CHECK' #s115 -> s116
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's117':
                match currChar:
                    case 'i':  currState = 's118'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's118':
                match currChar:
                    case 't':  currState = 's119'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
            
            case 's119':
                match currChar:
                    case 'c':  currState = 's120'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's120':
                match currChar:
                    case 'h':  currState = 'SWITCH_CHECK' #s121 -> s122
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
            
            case 's123':
                match currChar:
                    case 'r':  currState = 's124'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
        
            case 's124':
                match currChar:
                    case 'u':  currState = 's125'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's125':
                match currChar:
                    case 'e':  currState = 'TRUE_CHECK' #s126 -> s127
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's128':
                match currChar:
                    case 'o':  currState = 's129'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's129':
                match currChar:
                    case 'i':  currState = 's130'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's130':
                match currChar:
                    case 'd':  currState = 'VOID_CHECK'  #s131 -> s132
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's133':
                match currChar:
                    case 'h':  currState = 's134'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's134':
                match currChar:
                    case 'i':  currState = 's135'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's135':
                match currChar:
                    case 'l':  currState = 's136'
                    case 'ANY':  currState = 'DEFINED'
                    case _:  currState = 'UNDEFINED'

            case 's136':
                match currChar:
                    case 'e':  currState = 'WHILE_CHECK' #s137 -> s138
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            #### RESERVED SYMBOLS #######################################

            case 's139':
                match currChar:
                    case '-':  currState = 'DECREMENT_CHECK' #s141 -> s142
                    case '=':  currState = 'MINUS_ASS_CHECK' #s143 -> s144
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's145':
                match currChar:
                    case '=':  currState = 'NOT_EQUAL_CHECK' #s147 -> s148
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case '149':
                match currChar:
                    case '=':  currState = 'MODULO_ASS_CHECK' #s149 -> s150
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's153':
                match currChar:
                    case '&':  currState = 'LOGICAND_CHECK' #s154 -> s155
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case '160':
                match currChar:
                    case '=':  currState = 'MULT_ASS_CHECK' #s162 -> s163
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's168':
                match currChar:
                    case '*':  currState = 's209'
                    case '/':  currState = 's207'
                    case '=':  currState = 'DIV_ASS_CHECK' #s170 -> s171
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's184':
                match currChar:
                    case '|':  currState = 'LOGICOR_CHECK' #s184 -> s185
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's187':
                match currChar:
                    case '+':  currState = 'INCREMENT_CHECK' #s187 -> s189
                    case '=':  currState = 'ADD_ASS_CHECK'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
            
            case 's193':
                match currChar:
                    case '=':  currState = 'LESS_OR_EQUAL_CHECK' #s195 -> s196
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's197':
                match currChar:
                    case '=':  currState = 'GREATER_OR_EQUAL_CHECK' #s199 -> s200 
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
        
            case 's201':
                match currChar:
                    case '=':  currState = 'EQUAL_CHECK' #s201 -> s202
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's205':
                match currChar:
                    case '_':  currState = 's205'
                    case _ if currChar in self.alphanum:  currState = 's205'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's207':
                match currChar:
                    case _ if currChar in self.ascii:  currState = 's207'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's209':
                match currChar:
                    case '\n':  currState = 's209'
                    case '*':  currState = 's210' #catches * before ascii check
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
                global  multi_line_start_found
                multi_line_start_found = True  # multi-line comment start found


            case 's210':
                match currChar:
                    case '/':  currState = 'MULTI_COMMENT_CHECK' #s211 -> 212
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's213':
                match currChar:
                    case '"':  currState = 'STRING_LIT_CHECK' #catches " before ascii check #214 - > 215
                    case _ if currChar in self.ascii:  currState = 's213'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'

            case 's216':
                match currChar:
                    case _ if currChar in self.numbers:  currState = 's216'
                    case 'ANY':  currState = 'DEFINED'
                    case _:   currState = 'UNDEFINED'
            
            case 's249':
                match currChar:
                    case '.': 
                        need_frac_num = True
                        currState = 's216'
                    case _ if currChar in self.numbers: currState = 's249'
                    case 'ANY':  currState = 'DEFINED'
                    case _:  currState = 'UNDEFINED' 
        
        print (currState)
        return currState             



    #---TOKEN EXTRACTION AND CLASSIFICATION---#
    def scan(self, code):
        open('pos_char.log', 'w').close()
        code = code.replace('\r\n', '\n')    # replace keyboard return carriages

        for char in code:
            print(f'(debug) {char} : {ord(char)}')

        tokens = [] # list of tokens -- token object with attributes: token.tokenName, token.tokenType, token_line, token_column
        errors = [] # will hold strings of error msges

        currToken = ''    # set current token to empty string at start
        currState = 's0'  # set current state to s0 at start
        lineContent = ''  # empty line content at star
        currLine = 1      # start at line 1
        currCol = 0      # start at column 1
        currWholeCount = 0   # set whole count at start to 0 
        currFracCount = 0     # set frac count at start to 0 

        # flags 
        wholeError = False     
        fracError = False
        char_esc = False  # backslash caught inside string


        leadingSpaces = 0  # start with 0 leading spaces per line for err msgs
        isLeadingSpace = True # flag (true == increment leading spaces)

        global need_frac_num   # flag for whole number loop (if there's "." there should be a digit after)
        global multi_line_start_found   # flag to check multi line (used to determine if multiline was never closed)

        multi_line_start_found = False
        multi_line_start_line = 0  # for err tracking
        multi_line_start_col = 0
        reset_col = False


        # Helper function inside lexer to add a token(set its properties), append to token list, and reset current token and state
        def add_token(name, type, line, column):  
            nonlocal currToken, currState, currLine, currCol # use nonlocal keyword to access currToken, currState
            token = Token(name, type, line, column)   # -2 for column bc fsr it's off by 2
            tokens.append(token)  # append token
            currToken = '' # reset state and currtoken 
            currState = 's0'

        # Helper function to reset state and token when appending errors
        def add_error(string):
            nonlocal currToken, currState 
            errors.append(string)
            currToken = ''
            currState = 's0'

        print("(dbgl ----------SCAN START--------")
        for i in range(len(code)): # need index for later
            print('(dbg) ---NEW CHAR---')
            print('(dbg) state: ', currState)
            print('(dbg) ', code[i])
            print('(dbg) ascii: ', ord(code[i]))

            #update line and col
            if (code[i] == '\n' and i != len(code)-1):   # user pressed enter -- new line  (not the last /n)
                reset_col = True   # reset column
                leadingSpaces = 0   # reset spaces
                isLeadingSpace = True # the very first position (potentially a space)
                lineContent = ''
            elif code[i] == '/' and i + 1 < len(code) and code[i + 1] == '*' and not multi_line_start_found:  # check if current char is / and followed by *, then it means it might be an unclosed multiline comment
                multi_line_start_line = currLine
                multi_line_start_col = currCol
            else:
                if code[i] != ' ':
                    isLeadingSpace = False  # no more leading space for that line 
                if isLeadingSpace:
                    leadingSpaces += 1  # there is a leading space
                currCol += 1  # regardless, add 1 to col 
                _printlog(f'({currLine}, {currCol}) : {code[i]}')
                lineContent += code[i]  # add char to line content

            # DEFINED = there's a path to another state
            # UNDEFINED = delim checking bc there is no more paths
            # ANY = any character

            # if no transitions, it means it's time for delim checking
            if (self.transition(currState, 'ANY') != 'DEFINED'):
                print('(dbg) delim checking')
                match currState:
                
                # Data type keywords (bool, int, long, string, float, double)
                    case 'BOOL_CHECK':  # "bool" keyword #s5
                        expected = self.type_iden_delim
                        if (code[i] in self.type_iden_delim):
                            add_token(currToken, 'bool', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):  # bool_  or boola
                            currToken += code[i]  # add char to token
                            currState ='s205'  # go to iden states
                            print('(dbg) now in state 205')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]  # invalid delim to bool
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    case 'DOUBLE_CHECK':  # "double" keyword #s46
                        expected = self.type_iden_delim
                        if (code[i] in self.type_iden_delim):
                            add_token(currToken, 'double', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    case 'FLOAT_CHECK': # "float" keyword #s62
                        expected = self.type_iden_delim
                        if (code[i] in self.type_iden_delim):
                            add_token(currToken, 'float', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    case 'INT_CHECK':   # "int" keyword #s78
                        print('(dbg) in int_check')
                        expected = self.type_iden_delim
                        if (code[i] in self.type_iden_delim):
                            add_token(currToken, 'int', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    case 'LONG_CHECK': # "long" keyword #s83
                        expected = self.type_iden_delim
                        if (code[i] in self.type_iden_delim):
                            add_token(currToken, 'long', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    case 'STRING_CHECK': # "string" keyword #s116
                        expected = self.type_iden_delim
                        if (code[i] in self.type_iden_delim):
                            add_token(currToken, 'string', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    
                    #break statement
                    case 'BREAK_CHECK': # "break" keyword #s10
                        expected = self.break_ret_cont_delim
                        if (code[i] in self.break_ret_cont_delim):
                            add_token(currToken, 'break', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    
                    # SYMBOLS 
                    # -- if it's a symbol, it doesn't have a pathway to go to an iden (s205)
                    # -- if the symbol has a continuation like --, -= and !=, then it just changes the state (and we go to the next iteration)

                    # ( symbol
                    case 'OPEN_PAREN_CHECK': #s157
                        expected = ['alphanum', ' ', '\"', '!', ')', '+', '-', '/']
                        if (code[i] in self.open_paren_delim):
                            add_token(currToken, '(', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # ) symbol
                    case 'CLOSING_PAREN_CHECK': #s159
                        expected = ['alphanum', '=', '&', '|', '{', '(', ')', ';', '\n', ',', '/', ':', ']','?',','] + [';', '\n', '/']
                        if (code[i] in self.close_paren_delim):
                            add_token(currToken, ')', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # ; symbol
                    case 'SEMICOLON_CHECK': #s173
                        expected = ['alphanum', ' ', '}', '/', '('] + self.newline
                        if (code[i] in self.semicolon_delim):
                            add_token(currToken, ';', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # - symbol
                    case 'DASH_CHECK': #s140
                        expected = ['alphanum', ' ', '(', '+', '/', '.']
                        if (code[i] in self.negative_delim):
                            add_token(currToken, '-', currLine, currCol)
                        elif (code[i] in ['-', '=']):
                            print('(dbg) going to s139')
                            currState = 's139'
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # ! symbol
                    case 'NEGATION_CHECK': #s146
                        expected = ['alphabetic_chars', '(', '/', '!'] + self.whitespace + self.newline
                        if (code[i] in self.exclamation_delim):
                            add_token(currToken, '!', currLine, currCol)
                        elif (code[i] == '='):
                            currState = 's145'
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # % symbol
                    case 'MODULO_CHECK': #s150
                        expected = ['alphanum', ' ', '(', '+', '-', '/']
                        if (code[i] in self.percent_delim):
                            add_token(currToken, '%', currLine, currCol)
                        elif (code[i] == '='):
                            currState = '149'
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # * symbol
                    case 'ASTERISK_CHECK': #s161
                        expected = ['alphanum', ' ', '(', '+', '-', '/']
                        if (code[i] in self.asterisk_delim):
                            add_token(currToken, '*', currLine, currCol)
                        elif (code[i] in ['/', '=']):
                            currState = '160'
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # , symbol
                    case 'COMMA_CHECK': #s165
                        expected = ['alphanum', ' ', '/', '(', '{', '+', '-']
                        if (code[i] in self.comma_delim):
                            add_token(currToken, ',', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # . symbol
                    case 'DOT_CHECK': #s167
                        expected = ['alphabetic_chars', '/'] + self.whitespace
                        if (code[i] in self.numbers):
                            currState = 's216'
                        elif (code[i] in self.dot_delim):
                            add_token(currToken, '.', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # / symbol
                    case 'SLASH_CHECK': #s169
                        expected = ['alphanum', ' ', '(', '+', '-']
                        if (code[i] in self.slash_delim):
                            add_token(currToken, '/', currLine, currCol)
                        elif (code[i] in ['*', '/', '=']):
                            currState = 's168'
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    case 'COLON_CHECK': #s175
                        expected = ['alphanum', '(', ' ', '/'] + self.newline
                        if (code[i] in self.colon_delim):
                            add_token(currToken, ':', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # [ symbol
                    case 'OPEN_BRACKET_CHECK': #s177
                        expected = ['alphanum', ']', '/', '\n', '(', '+', '-'] + self.whitespace
                        if (code[i] in self.open_bracket_delim):
                            add_token(currToken, '[', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # ] symbol
                    case 'CLOSING_BRACKET_CHECK': #s179
                        expected = self.closing_bracket_delim
                        if (code[i] in expected):
                            add_token(currToken, ']', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # { symbol
                    case 'OPEN_CURLY_CHECK': #s181
                        expected = ['alphanum', ' ', '{', '}', '/', '+', '-', '\"', '('] + self.newline_delim
                        if (code[i] in self.open_curly_delim):
                            add_token(currToken, '{', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # } symbol
                    case 'CLOSING_CURLY_CHECK': #s183
                        expected = ['alphanum', ' ', ';', ',','}', '+', '-'] + self.newline_delim
                        if (code[i] in self.close_curly_delim):
                            add_token(currToken, '}', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # + symbol
                    case 'PLUS_CHECK': #s188
                        expected = ['alphanum', ' ', '(', '\"', '+', '-', '/']
                        if (code[i] in self.plus_delim):
                            add_token(currToken, '+', currLine, currCol)
                        else:
                            currState = 's187'
                    # < symbol
                    case 'OPEN_ANGLE_CHECK': #s194
                        expected = ['alphanum', ' ', '(', '+', '-', '/'] + self.newline
                        print("(dbg) open angle check curr char ", code[i])
                        if (code[i] in self.great_less_delim):
                            print("(dbg) arithmetic spotted for <")
                            add_token(currToken, '<', currLine, currCol)
                        elif (code[i] == '='):
                            currState = 's193' #s193 -> s194
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # > symbol
                    case 'CLOSING_ANGLE_CHECK': #s198
                        expected = ['alphanum', ' ', '(', ';', '+', '-', '/'] + self.newline
                        if (code[i] in self.great_delim):
                            add_token(currToken, '>', currLine, currCol)
                        elif (code[i] == '='):
                            currState = 's197' #s197 -> s198
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # = symbol
                    case 'ASSIGN_CHECK': #s202
                        expected = ['alphanum', ' ', '\"', '+', '-', '/', '!']
                        if (code[i] in self.equal_delim):
                            add_token(currToken, '=', currLine, currCol)
                        else:
                            currState = 's201'


                    # in statement
                    case 'IN_CHECK': #s76
                        expected = ['<', '/']
                        if (code[i] in self.in_delim):
                            add_token(currToken, 'in', currLine, currCol)
                        elif(code[i] in self.alphanum + ['_']):
                            currState = 's75' 
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # print statement
                    case 'PRINT_CHECK': #s89
                        expected = self.func_delim
                        if (code[i] in self.func_delim):
                            add_token(currToken, 'print', currLine, currCol)
                        elif(code[i] in self.alphanum + ['_']):
                            currState = 's88'
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # println statement
                    case 'PRINTLN_CHECK': #s92
                        expected = self.func_delim
                        if (code[i] in self.func_delim):
                            add_token(currToken, 'println', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # private statement
                    case 'PRIVATE_CHECK': #s97
                        expected = self.newline_delim
                        if (code[i] in self.newline_delim):
                            add_token(currToken, 'private', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # repeat statement
                    case 'REPEAT_CHECK': #s104
                        expected = self.loop_delim
                        if (code[i] in self.loop_delim):
                            add_token(currToken, 'repeat', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # return statement
                    case 'RETURN_CHECK': #s109
                        expected = self.newline_delim + [';']
                        if (code[i] in self.break_ret_cont_delim):
                            add_token(currToken, 'return', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
        
                    # switch statement
                    case 'SWITCH_CHECK': #s122
                        expected = self.loop_delim
                        if (code[i] in self.loop_delim):
                            add_token(currToken, 'switch', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                
                    # true
                    case 'TRUE_CHECK': #s127
                        expected = self.nbl_delim
                        if (code[i] in self.nbl_delim):
                            add_token(currToken, 'bool_lit', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # void statement
                    case 'VOID_CHECK': # s132
                        expected = self.whitespace + self.newline + ['/']
                        if (code[i] in self.void_delim):
                            add_token(currToken, 'void', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    
                    # while statement
                    case 'WHILE_CHECK': #s138
                        expected = self.loop_delim
                        if (code[i] in self.loop_delim):
                            add_token(currToken, 'while', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # -- symbol
                    case 'DECREMENT_CHECK': #s142
                        expected = self.whitespace + ['alphabetic_chars'] + [';', ')', '/', '+', '*', '%', '(', ']', ','] + self.newline
                        if (code[i] in self.decrement_delim):
                            add_token(currToken, '--', currLine, currCol)
                        elif (code[i] in self.numbers):
                            currToken += code[i]
                            add_error(self.adjustConstNumError(currToken, currLine, currCol, lineContent, leadingSpaces))
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # -= symbol
                    case 'MINUS_ASS_CHECK': #s44
                        expected = ['alphanum', ' ', '(', '+', '-', '/']
                        if (code[i] in self.subtract_assign_delim):
                            add_token(currToken, '-=', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # != symbol
                    case 'NOT_EQUAL_CHECK': #s148
                        expected = self.whitespace + ['alphanum', '(', '"', '!','+','-'] + self.newline
                        if (code[i] in self.not_equal_delim):
                            add_token(currToken, '!=', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # %= symbol
                    case 'MODULO_ASS_CHECK': #s152
                        expected = ['alphanum', ' ', '(', '+', '-', '/']
                        if (code[i] in self.modulo_assign_delim):
                            add_token(currToken, '%=', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # && symbol
                    case 'LOGICAND_CHECK': #s155
                        expected = ['alphabetic_chars', ' ', '(', '/', '!']
                        if (code[i] in self.and_or_delim):
                            add_token(currToken, '&&', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # *= symbol
                    case 'MULT_ASS_CHECK': #s163
                        expected = ['alphanum', ' ', '(', '+', '-', '/']
                        if (code[i] in self.multi_assign_delim):
                            add_token(currToken, '*=', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # /= symbol
                    case 'DIV_ASS_CHECK': #s171
                        expected = ['alphanum', ' ', '(', '+', '-', '/']
                        if (code[i] in self.divi_assign_delim):
                            add_token(currToken, '/=', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # || symbol
                    case 'LOGICOR_CHECK': #s185
                        expected = ['alphabetic_chars', ' ', '(', '/', '!']
                        if (code[i] in self.and_or_delim):
                            add_token(currToken, '||', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # ++ symbol
                    case 'INCREMENT_CHECK':  #s189
                        expected = self.whitespace + ['alphabetic_chars', ')', ';', '/', '-', '*', '%', '(', ']', ',']
                        if (code[i] in self.increment_delim):
                            add_token(currToken, '++', currLine, currCol)
                        elif (code[i] in self.numbers):
                            currToken += code[i]
                            add_error(self.adjustConstNumError(currToken, currLine, currCol, lineContent, leadingSpaces))
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # += symbol
                    case 'ADD_ASS_CHECK': #s192
                        expected = ['alphanum', ' ', '(', '\"', '+', '-', '/']
                        if (code[i] in self.add_assign_delim):
                            add_token(currToken, '+=', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # <= symbol
                    case 'LESS_OR_EQUAL_CHECK': #s196
                        expected = ['alphanum', ' ', '(', '+', '-', '/']
                        if (code[i] in self.great_less_delim):
                            add_token(currToken, '<=', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # >= symbol
                    case 'GREATER_OR_EQUAL_CHECK': #s200 
                        expected = ['alphanum', ' ', '(', '+', '-', '/']
                        if (code[i] in self.great_less_delim):
                            add_token(currToken, '>=', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # == symbol
                    case 'EQUAL_CHECK': #s202
                        expected = ['alphanum', ' ', '(', '\"', '+', '-', '/', '!']
                        if (code[i] in self.equal_equal_delim):
                            add_token(currToken, '==', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # string literal
                    case 'STRING_LIT_CHECK': #s213
                        expected = self.str_lit_delim
                        if (code[i] in self.str_lit_delim):
                            add_token(currToken, 'string_lit', currLine, currCol)
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # multicomments 
                    case 'MULTI_COMMENT_CHECK': #s212
                        multi_line_start_found = False
                        add_token(currToken, 'multi-line comment', currLine, currCol)
                    # case statement 
                    case 'CASE_CHECK': #s15
                        expected = self.newline_delim
                        if (code[i] in self.case_delim):
                            add_token(currToken, 'case', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # class statement 
                    case 'CLASS_CHECK': #s20
                        expected = self.newline_delim
                        if (code[i] in self.newline_delim):
                            add_token(currToken, 'class', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # continue statement 
                    case 'CONTINUE_CHECK': #s28
                        expected = self.newline_delim + [';']
                        if (code[i] in self.break_ret_cont_delim):
                            add_token(currToken, 'continue', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # const statement 
                    case 'CONST_CHECK': #s31
                        expected = self.newline_delim
                        if (code[i] in self.newline_delim):
                            add_token(currToken, 'const', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # default statement 
                    case 'DEFAULT_CHECK': #s39
                        expected = self.default_delim
                        if (code[i] in self.default_delim):
                            add_token(currToken, 'default', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # do statement 
                    case 'DO_CHECK': #s41
                        expected = self.block_delim
                        if (code[i] in self.block_delim):
                            add_token(currToken, 'do', currLine, currCol)
                        elif(code[i] in self.alphanum + ['_']):
                            currState = 's40'
                        else:
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # else statement 
                    case 'ELSE_CHECK': #s51
                        expected = self.block_delim
                        if (code[i] in self.block_delim):
                            add_token(currToken, 'else', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # false statement
                    case 'FALSE_CHECK': #s57
                        expected = self.nbl_delim
                        if (code[i] in self.nbl_delim):
                            add_token(currToken, 'bool_lit', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # for statement
                    case 'FOR_CHECK': #s65
                        expected = self.loop_delim
                        if (code[i] in self.loop_delim):
                            add_token(currToken, 'for', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # if statement
                    case 'IF_CHECK': #s68
                        expected = self.loop_delim
                        if (code[i] in self.loop_delim):
                            add_token(currToken, 'if', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    # import statement
                    case 'IMPORT_CHECK': #s74
                        expected = self.whitespace + ['<', '/'] + self.newline
                        if (code[i] in self.import_delim):
                            add_token(currToken, 'import', currLine, currCol)
                        elif (code[i] in self.alphanum + ['_']):
                            currToken += code[i]
                            currState ='s205'
                            print('(dbg) now in state 215')
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else:
                            currToken += code[i]
                            add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
            # end of delim checking if statement
            

            #------------------ SPECIAL STATES ------------------
            # s205 - Identifier
            # s207 - Single line comment
            # s210 - Multi-line comment
            # s213 - String literal
            # s249 - Whole number
            # s216 - Fractional number

            # >>> identifier state
            if (currState == 's205'):  # you're still in the iden loop state
                print('(dbg) in identifier check state now')
                if (code[i] in self.iden_delim):  # u found an iden delim during the loop of iden state
                    print('(dbg) correct delim')    
                    if (currToken[0] not in self.alphabetic_chars):  # if the first char of the iden is not an alphabetic char, then it wasnt a valid iden start
                            add_error(self.idenFirstError(currToken, currLine, currCol,lineContent, leadingSpaces))
                    else: # found a valid iden and delimeter, so add the identifier
                        add_token(currToken, 'Identifier', currLine, currCol)

                elif (code[i] in self.alphanum + ['_']): # if not delim but still a valid char for an identifier (alphanum and _), keep looping
                        currToken += code[i]
                        print('(dbg) accepted for iden')
                        currState ='s205'  # keep the state at 205
                        if reset_col:
                            currLine += 1
                            currCol = 0
                            reset_col = False
                        continue
                else:
                    # the identifier wasn't delimeted by a valid iden delim
                    currToken += code[i]
                    expected = self.iden_delim
                    # add_error((currToken, f'Lexical Error: In line {currLine}, column {currCol-len(currToken)}; Unexpected \'{code[i]}\' for \'{currToken[:-1]}\'')) #can be expanded with conditions to check what error
                    
                    add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
            # >>> end of identifier looping

            # >>> single line comment
            if (currState == 's207'):
                if (code[i] == '\n'): # if we're inside the single line comment loop (anything after "//") and we find a new line, then we know that the comment is over
                    add_token(currToken, 'single_comment', currLine, currCol) # so we add the token
                    if reset_col:
                        currLine += 1
                        currCol = 0
                        reset_col = False
                    continue
                else:
                    currToken += code[i]  # else we just keep adding any char to the single line comment token
                    if reset_col:
                        currLine += 1
                        currCol = 0
                        reset_col = False
                    continue
            # >>> end of single line comment

            # >>> multi-line comment
            if (currState == 's210'):  # 210 is the asterisk transition before the ending /
                if (code[i] != '/'):   # if it's not / then it'll just keep looping with the chars inside /* * _______
                    currState = 's209'
            # >>> end of multi-line comment
            

            # >>> whole number
            if (currState == 's249'): # start of a number 
                if (code[i] in self.numbers):  # if the next char is still a number 
                    print("(dbg) got another number")
                    currWholeCount += 1  # increment the whole count
                    currToken += code[i]  # add the current digit to the number being built
                    if (currWholeCount > 19):  # if the current whole number count is above 19, then it exceeded max digit count for whole numbers
                        if (wholeError):  # if there is a whole error before, then u pop the last error to keep updating the error to the new one
                            errors.pop()
                        errors.append(self.wholeRangeError(currToken, currLine, currCol, lineContent, leadingSpaces)) # add the latest exceeded max digit count error
                        wholeError = True 
                        if reset_col:
                            currLine += 1
                            currCol = 0
                            reset_col = False
                        continue
                    else:
                        if reset_col:
                            currLine += 1
                            currCol = 0
                            reset_col = False
                        continue
                if (code[i] in self.nbl_delim and not wholeError): # if we're currently still in the whole number loop, and we encounter a numbool delim, and there were no errors,
                    add_token(currToken, 'whole_lit', currLine, currCol) # then we just add the whole num token
                    currWholeCount = 0 # reset the digit counters
                    currFracCount = 0
                elif (code[i] != '.' and not wholeError): # no errors, and the next symbol is not a decimal point, then the delim is invalid for the number
                    currToken += code[i]
                    expected = self.nbl_delim
                    print('(dbg) whole lit delim error')
                    add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    currWholeCount = 0
                    currFracCount = 0
                elif (code[i] != '.'): # there was a whole error found, and no fractional part, then just reset the flags, states, tokens, and count
                    wholeError = False # reset everything so u continue to scan for next chars (continue analysis)
                    currState = 's0'
                    currToken = ''
                    currWholeCount = 0
                    currFracCount = 0
            # >>> end of whole number


            # >>> fractional part of number
            if (currState == 's216'): # is after the decimal state (fractional part)
                if (code[i] in self.numbers): # if its a number,
                    need_frac_num = False # no more for this error bc u found a number
                    currFracCount += 1 # increment digit count for fra num 
                    currToken += code[i] # add the num to the token
                    if (currFracCount > 16):  # exceeded frac max digit count
                        if (fracError):
                            errors.pop() # same logic in whole number, just remove last err
                        errors.append(self.fracPrecError(currToken, currLine, currCol, lineContent, leadingSpaces)) # then update with current one
                        fracError = True 
                        if reset_col:
                            currLine += 1
                            currCol = 0
                            reset_col = False
                        continue
                    else:
                        if reset_col:
                            currLine += 1
                            currCol = 0
                            reset_col = False
                        continue
                elif need_frac_num: # we had a decimal point without a number next to it
                    need_frac_num = False #reset
                    currToken += code[i]
                    expected = self.nbl_delim
                    add_error(self.missingNumError(currToken, currLine, currCol, lineContent, leadingSpaces)) # throw this err
                    currWholeCount = 0
                    currFracCount = 0
                elif (code[i] in self.nbl_delim and not (wholeError or fracError)): # we found a valid delim in the frac num loop
                        add_token(currToken, 'frac_lit', currLine, currCol) # so we add the token
                        currWholeCount = 0
                        currFracCount = 0
                elif not (wholeError or fracError): # we didn't have any whole/frac digit count err, then we encountered an invalid delim
                    currToken += code[i]
                    expected = self.nbl_delim
                    add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
                    currWholeCount = 0
                    currFracCount = 0
                else: # there was a digit count err, so we reset everything and just continue checking
                    wholeError = False
                    fracError = False
                    currState = 's0'
                    currToken = ''
                    currWholeCount = 0
                    currFracCount = 0
            # >>> end of fractional number
            
            
            # >>> string
            if (currState == 's213'):  # we encountered " or encountered " before so we are inside the string loop
                if (code[i] == '\\' and not char_esc): # if the curr char is a backslash , and we didnt encounter a backslash before, then we know that we are escaping a char
                    char_esc = True     # will be treated as an attempt to escape a char
                    currToken += code[i]  # add to the string token
                    if reset_col:
                        currLine += 1
                        currCol = 0
                        reset_col = False
                    continue
                if (char_esc):  # if we found a backslash before, 
                    if (code[i] not in ['\"', '\\', 't', 'n']):  # and the next character is not a valid escape sequence, then we know that the escape sequence is invalid
                        print('(dbg) esc seq error') 
                        add_error(self.escSeqError(currToken, currLine, currCol, lineContent, leadingSpaces))
                    else: # it was a valid esc char
                        currToken += code[i]
                    char_esc = False  # reset the esc flag
                    if reset_col:
                        currLine += 1
                        currCol = 0
                        reset_col = False
                    continue
            # >>> end of string
             
            # -------------- END OF SPECIAL STATES  --------------


            # ------------- REGULAR STATES: Iterating through chars that aren't special states -------------

            # Check whitespaces
            # Check s213 = string, s207 = single line comment, s209 = multi-line comment (bc if ur in these states, space is a part of the token)
            if (currState not in ['s213', 's207', 's209']):  
                if (code[i] == ' '):
                    if (self.transition(currState, 'ANY') == 'DEFINED' and currState != 's0'):  # still in a valid token, not delim checking
                        if currToken not in ['&', '|']:  
                            add_token(currToken, 'Identifier', currLine, currCol)  # if we ever get to this point, we know that we didn't reach any keyword and was delimited by a space
                        else: # check if the token is & or | and was delimited by a space, throw an error bc we dont have those symbols 
                            add_error(self.unexpectedSymbol(currToken, currLine, currCol, lineContent, leadingSpaces))
                    if reset_col:  # if there's a newline character, reset col, add new line.
                        currLine += 1
                        currCol = 0
                        reset_col = False
                    continue

                if (code[i] == '\n'):
                    if (i != len(code)-1):  # if it's a newline character and its not the helper newline in the end
                        if (self.transition(currState, 'ANY') == 'DEFINED' and currState != 's0'):  # same logic as above
                            if currToken not in ['&', '|']:
                                add_token(currToken, 'Identifier', currLine, currCol)
                            else:
                                add_error(self.unexpectedSymbol(currToken, currLine, currCol, lineContent, leadingSpaces))
                        if reset_col:
                            currLine += 1
                            currCol = 0
                            reset_col = False
                        continue
                    
            # ------ CHECK REGULAR STATE TRANSITIONS
            print(f'(dbg) transition val {self.transition(currState, code[i])}')
            # if it's a valid char start, it exists in the next transition of the current state
            if (self.transition(currState, code[i]) != 'UNDEFINED'):  
                print(f'(dbg) in {currState} transitions')  
                currToken += code[i]  # add the char to the token being built
                print(f'(dbg) transitioning: {currState} - {code[i]} -> {self.transition(currState, code[i])}')
                currState = self.transition(currState, code[i])  # update currstate to the next state
                if reset_col:
                    currLine += 1
                    currCol = 0
                    reset_col = False
                continue
            else:  # if not a valid character in transitions
                print(f"(dbg) not in {currState} transitions")
                if (currState == 's0'):   
                    if (code[i] in self.numbers):  # in s0, it saw a number
                        currToken += code[i]  # add to token buildin
                        print("(dbg)s0 is num")
                        # go to whole num loop state
                        currWholeCount += 1  # start counting whole number
                        currState = 's249'  # s249 = whole number start loop 
                        if reset_col:
                            currLine += 1
                            currCol = 0
                            reset_col = False
                        continue
                    elif (code[i] not in self.alphanum and i != len(code)-1):  # not an alphanum, it's a symbol not in Transitions
                        print("(dbg) unexpected")
                        add_error(self.unexpectedSymbol(currToken, currLine, currCol, lineContent, leadingSpaces))
                        if reset_col:
                            currLine += 1
                            currCol = 0
                            reset_col = False
                        continue
                    currToken += code[i]
                    if (code[i] in self.alphabetic_chars and i != len(code)-1):  # found an alphabetic char at start, is an identifier bc it doesn't have any valid transitions above
                        print(f'(dbg) index {i}')
                        print(f'(dbg) length {len(code)}')
                        currState = 's205'  # s205 - identifier state
                    if reset_col:
                        currLine += 1
                        currCol = 0
                        reset_col = False
                    continue
                else:
                    print('(dbg) not in s0')  # not at the start, meaning it doesn't have a valid transition after the start
                    if (currState == 's209'): # if it's a multi-line comment state, just keep adding to the token cos it's a comment. it's searching for */
                        currToken += code[i]
                        if reset_col:
                            currLine += 1
                            currCol = 0
                            reset_col = False
                        continue
                    if (currState == 's213'): # if it's a string literal, just keep adding to the token cos it's a string. it's searching for "
                        if (code[i] == '\n'): # if it encounters newline, then it means the string is not closed (we do not support multiline strings)
                            add_error(self.stringMissingClose(currToken, currLine, currCol, lineContent, leadingSpaces))
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                        else: # else if its any char, just add it to the string (unless it's ", it won't reach this part)
                            currToken += code[i]
                            if reset_col:
                                currLine += 1
                                currCol = 0
                                reset_col = False
                            continue
                    if (code[i] in self.alphanum + ['_']): # if it's an alphanum or underscore, it's part of an identifier probably
                                                            #(_ is not a start bc we already checked that above. ex. print vs prin_)
                        currToken += code[i]
                        currState = 's205'
                        if reset_col:
                            currLine += 1
                            currCol = 0
                            reset_col = False
                        continue

                    # if you're building a token and you found a char that isn't in the transition of that keyword, you check if its a delim of idens
                    elif (code[i] in self.iden_delim): # check delim if valid iden delim
                       
                        print("(dbg) other iden append")
                        if (currToken[0] not in self.alphabetic_chars):  # if the first of token is not a valid start, then it throws an invalid start symbol for iden
                            add_error(self.idenFirstError(currToken, currLine, currCol,lineContent, leadingSpaces))
                        else:
                            add_token(currToken, 'Identifier', currLine, currCol) # else it's a valid identifier

                        currToken = code[i]  # add the symbol (bc when u added the identifier, the token was reset)
                        currState = self.transition('s0', code[i]) # find the next transition of the next curr char 
                        
                    
                    else: # if it's not a valid delim to any transition
                        currToken += code[i]  # just add the char to the current token building to add in err msgs
                        expected = self.iden_delim  # you're expecting an identifier delim here bc we never rly finished any valid keyword
                        if (code[i-1] in self.arithmetic_operator): # if the prev char was an arith op, then add the ff delims
                            expected = ['alphanum', ' ', '(']
                        if (code[i-1] == '+'): # if it was a plus, add " cos of string concat
                            expected.append('\"')
                        print('(dbg) currState: ', currState)

                        # add delim error (for idens)
                        add_error(self.delimError(currToken, currLine, currCol, code[i], lineContent, expected, leadingSpaces))
        
        # mulitline unclosed error
        if multi_line_start_found:
            multi_line_errorMsg = f'Lexical Error ({multi_line_start_line}, {multi_line_start_col}): Unterminated multi-line comment.\n/*\n^'
            add_error(multi_line_errorMsg)

        # reset col if last char was newline
        if reset_col:
            currLine += 1
            currCol = 0
            reset_col = False

        # return a list of tokens and errors (list of tokens and lis of errors)
        lexerResults = [tokens, errors] 
        return lexerResults

    #---LEXER ERRORS---
    def generateError(self, errorType, currToken, currLine, currCol, lineContent, leadingSpaces, additionalInfo=None):
        """
        Generates a lexical error message.
        """
        print('(dbg) currToken ', currToken)
        print('(dbg) ERROR msg currCol ', currCol)
        errorMsg = f'Lexical Error ({currLine}, {currCol}): {errorType} {currToken}\n'
        errorMsg += str(lineContent )+ '\n'
        print(f'(dbg) ERROR lineContent |{lineContent}')
        errorMsg += '_' * (currCol) + '^\n'
        if additionalInfo:
            errorMsg += additionalInfo
        print("(debug) ", errorMsg)
        if (currCol == 0):
            return ''
        return errorMsg

    def delimError(self, currToken, currLine, currCol, incorrectDelim, lineContent, expected, leadingSpaces):
        errorType = f"Unexpected {'newline' if incorrectDelim == '\\n' else incorrectDelim} for"
        additionalInfo = f"Expected delimiters: {expected}"
        return self.generateError(errorType, currToken[:-1], currLine, currCol, lineContent, leadingSpaces, additionalInfo)

    def missingNumError(self, currToken, currLine, currCol, lineContent, leadingSpaces):
        errorType = "Fractional literal must have a fractional part consisting of at least one digit: "
        return self.generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

    def idenFirstError(self, currToken, currLine, currCol, lineContent, leadingSpaces):
        errorType = "Identifier must start with an alpha character"
        return self.generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

    def stringMissingClose(self, currToken, currLine, currCol, lineContent, leadingSpaces):
        errorType = "Missing closing \" for string literal"
        return self.generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

    def escSeqError(self, currToken, currLine, currCol, lineContent, leadingSpaces):
        errorType = "Invalid escape sequence for string literal"
        return self.generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

    def charLengthError(self, currToken, currLine, currCol, lineContent, leadingSpaces):
        errorType = "Invalid character length for character literal"
        return self.generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

    def wholeRangeError(self, currToken, currLine, currCol, lineContent, leadingSpaces):
        errorType = "Numeric exceeding max digit count"
        return self.generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

    def fracPrecError(self, currToken, currLine, currCol, lineContent, leadingSpaces):
        errorType = "Numeric exceeding max precision"
        return self.generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

    def unexpectedSymbol(self, currToken, currLine, currCol, lineContent, leadingSpaces):
        errorType = "Unexpected symbol"
        return self.generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

    def adjustConstNumError(self, currToken, currLine, currCol, lineContent, leadingSpaces):
        errorType = "Numbers are not valid delimeters for pre-increment or pre-decrement operators."
        return self.generateError(errorType, currToken, currLine, currCol, lineContent, leadingSpaces)

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