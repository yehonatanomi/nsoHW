import os
from flask import Flask, request, jsonify
from service import MessageService

app = Flask(__name__)

message_service = MessageService()
message_service
@app.route('/AddMessage', methods=['POST'])
def add_message():
    try:
        data = request.json
        result = message_service.add_message(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/GetMessage', methods=['GET'])
def get_message():
    try:
        result = message_service.get_message(request.args)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/DeleteMessage', methods=['DELETE'])
def delete_message():
    try:
        result = message_service.delete_message(request.args)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
