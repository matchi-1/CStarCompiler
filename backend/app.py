from flask import Flask, json, jsonify, request
from flask_cors import CORS
import lexical_analyzer, syntax_analyzer, semantic_analyzer

app = Flask(__name__)
CORS(app)  # cross-origin requests
    
#---INSTANTIATE LEXER---
lexer = lexical_analyzer.LexicalAnalyzer()
#--GLOBAL LISTS--
tokens = []

#---FLASK ROUTES---
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'})

# @app.route('/api/compile', methods=['POST'])
# def compile_code():
#     global tokens
#     #empty out token list every time lexer is called
#     tokens.clear()
#     data = request.json
#     code = data.get('code', '')
#     code += '\n'
    
#     lexer_results = lexer.scan(code)  # Returns [tokens, errors]
#     tokens, errors = lexer_results  # Unpack the results

#     # # Calls syntax analyzer
#     # try:
#     #     analyzer = syntax_analyzer.SyntaxAnalyzer(tokens)
#     #     errors += analyzer.parse()    # comment out to just test for lexer
#     # except SyntaxError as e:
#     #     print(e)


#     # Convert Token objects to dictionaries
#     tokens_dict = [token.to_dict() for token in tokens]
#     #print(tokens_dict) #for testing

#     # Create a JSON-serializable response
#     response = {
#         "tokens": tokens_dict or [],  # should not send out None/null 
#         "errors": errors or []        
#     }

#     # print json output
#     # print('\n\n', json.dumps(response, indent=2))
#     return jsonify(response)

@app.route('/api/compile', methods=['POST'])
def compile_code():
    global tokens
    # empty out token list every time lexer is called
    tokens.clear()
    data = request.json
    code = data.get('code', '')
    code += '\n'
    
    lexer_results = lexer.scan(code)  # returns [tokens, errors]
    tokens, errors = lexer_results  # unpack 

    # calls syntax & seman analyzer
    try:
        syn_analyzer = syntax_analyzer.SyntaxAnalyzer(tokens)
        parseErrs, parseTree = syn_analyzer.parse()
        errors += parseErrs  # comment out to just test for lexer

        if "Parsing completed successfully. No Syntax Errors found." in parseErrs:
            seman_analyzer = semantic_analyzer.SemanticAnalyzer()
            semanErrs = seman_analyzer.interpret(parseTree)  # comment/uncomment for testing
            errors += semanErrs

            if "Semantic analysis completed successfully. No Semantic Errors found." not in semanErrs:
                # remove parsing success message since there's a semantic error
                errors.remove("Parsing completed successfully. No Syntax Errors found.")
                output_strings = []
            
            
            # NEW: collect outputs from semantic phase
            output_strings = seman_analyzer.output
        else:
            output_strings = []


    except SyntaxError as e:
        print(e)

    # convert Token objects to dictionaries
    tokens_dict = [token.to_dict() for token in tokens]

    # create a JSON-serializable response
    response = {
        "tokens": tokens_dict or [],  # should not send out None/null 
        "errors": errors or [],      
        "output": output_strings or []  # NEW: output strings from println/print
    }

    # print json output
    # print('\n\n', json.dumps(response, indent=2))
    
    #---SEMANTIC ANALYSIS---
    # try:
    #     seman = semantic_analyzer.SemanticAnalyzer()
    #     seman.interpret(parseTree) #comment/uncomment for testing
    # except SyntaxError as e:
    #     print(e)

    return jsonify(response)


@app.route('/api/submit-input', methods=['POST'])
def submit_input():
    user_input = request.json.get('user_input')  # User input from frontend
    input_request = request.json.get('input_request')  # Current input request
    
    # Process the input
    seman_analyzer = current_seman_analyzer
    result = seman_analyzer.process_input(user_input)

    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True) 
