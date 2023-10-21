# DataBase
from src.database.db import get_connection


class Lend():

    def __init__(self, id, idUser, ISBN, departury_date, return_date) -> None:
        self.id = id
        self.idUser = idUser
        self.ISBN = ISBN
        self.departury_date = departury_date
        self.return_date = return_date

    def to_json(self):
        return {
            'id': self.id,
            'ISBN': self.idUser,
            'departury_date': self.departury_date,
            'return_date': self.return_date
        }

    @classmethod
    def from_row(cls, row):
        return cls(row[0], row[1], row[2], row[3])

    @staticmethod
    def lend_book(lend):
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = " call sp_lendBook({0},'{1}')".format(lend.idUser, lend.ISBN)
            cursor.execute(sql)
            connection.commit()
