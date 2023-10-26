from flask import Blueprint, jsonify

from src.database.db import get_connection
from src.validations_books import *


books_by_genre = Blueprint("books_by_genre", __name__)


@books_by_genre.route("/books_by_genre/<name>", methods=["GET"])
def read_booK_by_genre(name):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
            SELECT l.ISBN, l.titulo, a.nombre AS autor, g.name AS genero, e.name AS editorial, l.idioma, l.paginas, l.portada, l.descripcion, l.estado 
            FROM libros l 
            JOIN autores a 
            ON l.idAutor=a.id 
            JOIN genres g 
            ON l.idGenre=g.id 
            JOIN editorials e 
            ON l.idEditorial=e.id 
            WHERE g.name LIKE '{0}'
        """.format(
            '%' + name + '%'
        )
        # print(name)
        cursor.execute(sql)
        data = cursor.fetchall()
        if data != None:
            # print(data)
            books = []
            for row in data:
                book = {
                    "ISBN": row[0],
                    "titulo": row[1],
                    "autor": row[2],
                    "genero": row[3],
                    "editorial": row[4],
                    "idioma": row[5],
                    "paginas": row[6],
                    "portada": row[7],
                    "descripcion": row[8],
                    "estado": row[9],
                }
                books.append(book)
            # print('libro:', book)
            # print('libros:', books)
            return jsonify({"books": books, "message": "Booksss list", "success": True})
        else:
            return None
    except Exception as ex:  # para atrapar cualquier error que pueda haber
        return jsonify({"message": "Error", "success": False})
