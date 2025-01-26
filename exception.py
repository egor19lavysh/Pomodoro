class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "password is not correct"


class TokenExpired(Exception):
    detail = "token has expired"


class TokenNotCorrect(Exception):
    detail = "token is not correct"


class TaskNotFoundException(Exception):
    detail = "task is not found"
