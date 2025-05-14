
import eventlet
import os
eventlet.monkey_patch()
from flask_socketio import SocketIO
# from inoutTest import run_loop, wait_flag_container   # input output test with websocket
from runtime import setup_runtime
from flask import Flask, json, jsonify, request
from flask_cors import CORS
import lexical_analyzer, syntax_analyzer, semantic_analyzer, runtime   # import files of the analyzers + runtime

app = Flask(__name__)
CORS(app)  # cross-origin requests


# <> ------------------------------------- | WEBSOCKET TEST CONFIG
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
# Inject socketio to runtime
setup_runtime(socketio)

# <> ------------------------------------- | WEBSOCKET TEST CONFIG


#---FLASK ROUTES---
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'})


@app.route('/api/compile', methods=['POST'])
def compile_code():
    tokens = []  # holds tokens to be sent back to frontend
    tokens.clear() # empty out token list every time lexer is called
    data = request.json   # gets json payload from frontend, becomes a dictionary [code : ""]
    code = data.get('code', '')  # extracts the code string from the dictionary, defaulting to an empty string if "code" is not present.
    code += '\n'
    errors = []  # list of errors

    try:
        # --- LEXICAL ANALYZER ---
        lexer = lexical_analyzer.LexicalAnalyzer()  # instantiate lexical analyzer
        lexer_results = lexer.scan(code)  # returns [tokens, errors]  -- list of tokens and errors
        tokens, lexerrors = lexer_results  # unpack 
        errors += lexerrors  # add lexer errors to the list
        
        #--- SYNTAX ANALYZER ---
        syn_analyzer = syntax_analyzer.SyntaxAnalyzer(tokens)  # instantiate syntax analyzer
        parseErrs, parseTree = syn_analyzer.parse()  # returns list of errors and parse tree
        errors += parseErrs  # add syntax errors to list of errors

        # syntax parsing success
        if "Parsing completed successfully. No Syntax Errors found." in parseErrs and not lexerrors: 
            #-- SEMANTIC ANALYZER ---  
            seman_analyzer = semantic_analyzer.SemanticAnalyzer() # instantiate semantic analyzer
            semanErrs = seman_analyzer.interpret(parseTree)  # pass parse tree to semantic analyzer. returns list of semantic errors
            errors += semanErrs  # add semantic errors to list of errors

            # remove parsing success message since there's a semantic error
            if "Semantic analysis completed successfully. No Semantic Errors found." not in semanErrs:
                errors.remove("Parsing completed successfully. No Syntax Errors found.")
            
            # semantic parsing success
            else:   
                runtime_res = runtime.Runtime()  # instantiate runtime
                runtimeErrs = runtime_res.interpret(parseTree)  # pass parse tree to runtime to go over the code and execute them. returns list of runtime errors
                
    except SyntaxError as e:
        print(e)

    # remove all immediate flag errors [NOTE: handle this better next time and the ones above ^]
    messages_to_remove = [
        "Parsing completed successfully. No Syntax Errors found.",
        "Semantic analysis completed successfully. No Semantic Errors found.",
        "Runtime success. No Runtime Errors found."
    ]

    for msg in messages_to_remove:
        if msg in errors:
            errors.remove(msg)

    # convert Token objects to dictionaries
    tokens_dict = [token.to_dict() for token in tokens]

    # create a JSON-serializable response
    response = {
        "tokens": tokens_dict or [],  # should not send out None/null 
        "errors": errors or [], 
        # "output": output_strings or []  # NEW: output strings from println/print
    }

    return jsonify(response)

if __name__ == '__main__':
    #app.run(debug=True) 
    #socketio.run(app, debug=True) # <> ------------------------------------- | WEBSOCKET TEST | CC

    port = int(os.environ.get("PORT", 5000))  # fallback to 5000 if PORT not set
    socketio.run(app, host="0.0.0.0", port=port, debug=True)