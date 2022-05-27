import sqlite3
class Database:
  def __init__(self, database_file):
      self.connection = sqlite3.connect(database_file, check_same_thread=False)
      self.cursor = self.connection.cursor()
  def add_queue(self, chat_id):
    with self.connection:
      return self.cursor.execute('INSERT INTO `queue` (`chat_id`) VALUES (?)', (chat_id,)) # Добавляем пользователя в очередь
  def del_queue(self, chat_id):
    with self.connection:
      return self.cursor.execute('DELETE FROM `queue` WHERE `chat_id` = ?', (chat_id,)) # Удаляем пользователя из очереди
  def del_chat(self, id_chat):
    with self.connection:
      return self.cursor.execute('DELETE FROM `room` WHERE `room_id` = ?', (id_chat,))
  def get_chat(self):
    with self.connection:
      chat = self.cursor.execute('SELECT * FROM `queue`', ()).fetchmany(1)
      if bool(len(chat)):
        for row in chat:
          return row[1] # queue_id = row[0], chat_id = row[1]
      else:
        return False
  def create_chat(self, chat_one, chat_two):
    with self.connection:
      if chat_two != 0: # Функция создания чата
        self.cursor.execute('DELETE FROM `queue` WHERE `chat_id` = ?', (chat_two,))
        self.cursor.execute('INSERT INTO `room` (`user1_id`, `user2_id`) VALUES (?, ?)', (chat_one, chat_two,))
        return True
      else: # Становимся в очередь
        return False 
  def get_active_chat(self, chat_id):
    with self.connection:
      chat = self.cursor.execute('SELECT * FROM `room` WHERE `user1_id` = ?', (chat_id,))
      id_chat = 0
      for row in chat:
        id_chat = row[0]
        chat_info = [row[0], row[2]]
      if id_chat == 0:
        chat = self.cursor.execute('SELECT * FROM `room` WHERE `user2_id` = ?', (chat_id,))
        for row in chat:
          id_chat = row[0]
          chat_info = [row[0], row[1]]
        if chat_id == 0:
          return False
        else:
          return chat_info
      else:
        return chat_info