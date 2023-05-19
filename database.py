import sqlite3

s = "subject"
ta = "task"
te = "teacher"

class Database:
    def __init__(self): # подключение к БД
        self.connection = sqlite3.connect("../database.db")
        self.cursor = self.connection.cursor()

    def check_teacher(self, tg_id): # проверка наличия преподователя в БД
        with self.connection:
            res = self.cursor.execute("SELECT (tg_id) FROM `teacher` WHERE tg_id = ?", (tg_id,))
            return res.fetchone() is not None
    
    def get_teacher_info(self, tg_id):
        with self.connection:
            info = self.cursor.execute("SELECT * FROM `teacher` WHERE tg_id = ?", (tg_id,))
            for i in info:
                return [i[0], i[1], i[2], i[3], i[4], i[5]]

    def add_task(self, subject, grade, file_id, tg_client_id):  # запись предмета задания в БД
        with self.connection:
            return self.cursor.execute(f"INSERT INTO {ta} (subject, grade, urlfile_task, tg_client_id) VALUES (?, ?, ?, ?)", (subject, grade, file_id, tg_client_id))

    def get_task(self, subject, grade):
        with self.connection:
            tasks = self.cursor.execute("SELECT * FROM `task` WHERE subject = ? AND grade = ?", (subject, grade))
            for i in tasks:
                return [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]]