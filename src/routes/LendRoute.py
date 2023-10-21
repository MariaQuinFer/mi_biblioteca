from flask import Blueprint, request, jsonify
import traceback

# Logger
from src.utils.Logger import Logger
# Security
# from src.utils.Security import Security
# Services
from src.services.LendService import LendService
# Model
from src.models.LendModel import Lend
# DataBase
from src.database.db import get_connection


lend = Blueprint("lend", __name__)


# Ruta para solicitar un préstamo:
@lend.route("/lend", methods=['POST'])
def lend_book():

    # has_access = Security.verify_token(request.headers)

    # if has_access:

    try:
        idUser = request.json["idUser"]
        ISBN = request.json["ISBN"]

        lend = Lend(id, idUser, ISBN, None, None)
        created_loan = LendService.lend_book(lend)

        return jsonify({"message": 'Loan created successfully', "success": True}), 201
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
    # else:
    #     response = jsonify({'message': 'Unauthorized'})
    #     return response, 401

# Ruta para obtener el usuario con sesion iniciada junto con el libro prestado si tiene préstamo


@lend.route("/lend/<id>", methods=['GET'])
def lend_user_book(id):
    # try:
    try:
        connection = get_connection()
        cursor = connection.cursor()
        sql = """
                SELECT u.username, u.email, u.password, u.fullname, p.ISBN, p.return_date, l.titulo, a.nombre
                FROM users u
                JOIN prestamo p
                ON u.id = p.idUSer
                JOIN libros l
                ON p.ISBN = l.ISBN
                JOIN autores a
                ON l.idAutor = a.id
                WHERE u.id = {0}
                """.format(id)
        # print(nombre)
        cursor.execute(sql)
        data = cursor.fetchone()

        if data != None:
            # print("data", data)
            user = {
                "username": data[0],
                "email": data[1],
                "password": data[2],
                "fullname": data[3],
                "ISBN": data[4],
                "return_date": data[5],
                "titulo": data[6],
                "nombre": data[7],
            }
            return jsonify({"User": user, "message": 'Usuario actual', "success": True}), 200
        else:
            return jsonify({"mesagge": "Usuario sin préstamo actualmente", "success": False}), 205
    except Exception as ex:  # para atrapar cualquier error que pueda haber
        return jsonify({"message": "Error", "success": False})
    # except Exception as ex:
    #     Logger.add_to_log("error", str(ex))
    #     Logger.add_to_log("error", traceback.format_exc())
