import mysql.connector
from repository import MessageRepository

class MessageService:
    def __init__(self):
        self.repo = MessageRepository()
    def add_message(self, data):
        return self.repo.add_message(data)

    def get_message(self, params):
        return self.repo.get_message(params)

    def delete_message(self, params):
        return self.repo.delete_message(params)
