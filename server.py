import os
from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

# MySQL connection parameters
db_config = {
    'user': 'root',
    'password': 'yoniumi2005',
    'host': '127.0.0.1'
}

# Create a connection to MySQL server without specifying the database
cnx = mysql.connector.connect(**db_config)
c = cnx.cursor()

# Check if the messages database exists
c.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'messages'")
db_exists = c.fetchone()

if not db_exists:
    # Create the messages database
    c.execute("CREATE DATABASE messages")
    cnx.database = 'messages'  # Switch to the messages database
    c.execute('''
        CREATE TABLE messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            application_id INT,
            session_id VARCHAR(255),
            message_id VARCHAR(255),
            participants TEXT,
            content TEXT
        )
    ''')
    cnx.commit()

# Close the temporary connection
cnx.close()

# Reconnect to the messages database
cnx = mysql.connector.connect(database='messages', **db_config)
c = cnx.cursor()



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

        c.execute('''
                         INSERT INTO messages (application_id, session_id, message_id, participants, content)
                         VALUES (%s, %s, %s, %s, %s)
                     ''', (application_id, session_id, message_id, ', '.join(participants), content))

        # Commit the transaction
        cnx.commit()
        return jsonify({'message': 'Message added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/GetMessage', methods=['GET'])
def get_message():
    try:
        application_id = request.args.get('applicationId')
        session_id = request.args.get('sessionId')
        message_id = request.args.get('messageId')

        # Build the SQL query based on the provided parameters
        if application_id:
            query = "SELECT * FROM messages WHERE application_id = %s"
            query_params = (int(application_id),)
        elif session_id:
            query = "SELECT * FROM messages WHERE session_id = %s"
            query_params = (session_id,)
        elif message_id:
            query = "SELECT * FROM messages WHERE message_id = %s"
            query_params = (message_id,)
        else:
            return jsonify({'error': 'Invalid parameters'}), 400

        # Execute the query and fetch results
        c.execute(query, query_params)
        result = c.fetchall()

        # Convert query results to a list of dictionaries
        messages = []
        for row in result:
            message = {
                'id': row[0],
                'application_id': row[1],
                'session_id': row[2],
                'message_id': row[3],
                'participants': row[4],
                'content': row[5]
            }
            messages.append(message)

        return jsonify({'messages': messages}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/DeleteMessage', methods=['DELETE'])
def delete_message():
    try:
        application_id = request.args.get('applicationId')
        session_id = request.args.get('sessionId')
        message_id = request.args.get('messageId')

        # Build the SQL query based on the provided parameters
        if application_id:
            query = "DELETE FROM messages WHERE application_id = %s"
            query_params = (int(application_id),)
        elif session_id:
            query = "DELETE FROM messages WHERE session_id = %s"
            query_params = (session_id,)
        elif message_id:
            query = "DELETE FROM messages WHERE message_id = %s"
            query_params = (message_id,)
        else:
            return jsonify({'error': 'Invalid parameters'}), 400

        # Execute the DELETE query
        c.execute(query, query_params)
        cnx.commit()  # Commit the deletion

        return jsonify({'message': 'Messages deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
