from fastapi import HTTPException, status


class AutoException(HTTPException):

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):

        super().__init__(status_code=self.status_code, detail=self.detail)

class InvalidPriceFilter(AutoException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Минимальная цена больше максимальной."


class CarNotFound(AutoException):

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Автомобиль не найден."


class CarAlreadyExists(AutoException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Автомобиль уже существует."


class InvalidCarNumber(AutoException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный формат номера, пример: Т456КУ"


class UserAlreadyExistsException(AutoException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный логин или пароль"


class TokenExpiredException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(AutoException):
    status_code = status.HTTP_401_UNAUTHORIZED
