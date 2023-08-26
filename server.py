from flask import Flask, request, jsonify

app = Flask(__name__)

messages = []
#Post method
@app.route('/AddMessage', methods=['POST'])
def add_message():
    try:
        data = request.json

        application_id = data['application_id']
        session_id = data['session_id']
        message_id = data['message_id']
        participants = data['participants']
        content = data['content']

        new_message = {
            'application_id': application_id,
            'session_id': session_id,
            'message_id': message_id,
            'participants': participants,
            'content': content
        }

        messages.append(new_message)

        return jsonify({'message': 'Message added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/GetMessage', methods=['GET'])
def get_message():
    try:
        application_id = request.args.get('applicationId')
        session_id = request.args.get('sessionId')
        message_id = request.args.get('messageId')

        if application_id:
            filtered_messages = [msg for msg in messages if msg['application_id'] == int(application_id)]
        elif session_id:
            filtered_messages = [msg for msg in messages if msg['session_id'] == session_id]
        elif message_id:
            filtered_messages = [msg for msg in messages if msg['message_id'] == message_id]
        else:
            return jsonify({'error': 'Invalid parameters'}), 400

        return jsonify({'messages': filtered_messages}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
