import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class MessageRepository:
    def __init__(self):
        self.db_config = {
            'user': os.getenv('user'),
            'password': os.getenv('MYSQL_ROOT_PASSWORD'),
            'host': os.getenv('host'),
            'database': 'messages'  # Specify the database here
        }
        self.cnx = mysql.connector.connect(**self.db_config)
        self.c = self.cnx.cursor()
        self.setup_database()



    def setup_database(self):
        self.c.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'messages'")
        db_exists = self.c.fetchone()

        if not db_exists:
            self.c.execute("CREATE DATABASE messages")
            self.cnx.database = 'messages'
            self.c.execute('''
                CREATE TABLE messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    application_id INT,
                    session_id VARCHAR(255),
                    message_id VARCHAR(255),
                    participants TEXT,
                    content TEXT
                )
            ''')
            self.cnx.commit()

    def add_message(self, data):
        application_id = data['application_id']
        session_id = data['session_id']
        message_id = data['message_id']
        participants = data['participants']
        content = data['content']

        self.c.execute('''
            INSERT INTO messages (application_id, session_id, message_id, participants, content)
            VALUES (%s, %s, %s, %s, %s)
        ''', (application_id, session_id, message_id, ', '.join(participants), content))

        self.cnx.commit()

        return {'message': 'Message added successfully'}

    def get_message(self, params):
        application_id = params.get('applicationId')
        session_id = params.get('sessionId')
        message_id = params.get('messageId')

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
            return []

        self.c.execute(query, query_params)
        result = self.c.fetchall()

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

        return messages

    def delete_message(self, params):
        application_id = params.get('applicationId')
        session_id = params.get('sessionId')
        message_id = params.get('messageId')

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
            return {'error': 'Invalid parameters'}

        self.c.execute(query, query_params)
        self.cnx.commit()

        return {'message': 'Message deleted successfully'}
