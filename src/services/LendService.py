# Model
from src.models.LendModel import Lend


class LendService():
    @staticmethod
    def lend_book(lend):
        lend = Lend(id, idUser=lend.idUser, ISBN=lend.ISBN,
                    departury_date=lend.departury_date, return_date=lend.return_date)
        lend.lend_book(lend)
