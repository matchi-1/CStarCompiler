from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # cross-origin requests

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'})

@app.route('/api/compile', methods=['POST'])
def compile_code():
    data = request.json
    code = data.get('code', '')
    return jsonify({'output': f'You submitted: {code}'})

if __name__ == '__main__':
    app.run(debug=True)
