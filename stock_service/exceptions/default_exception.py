from typing import Union, Any


class DefaultException(Exception):
    code: int
    message: Union[str, None]
    detail: Union[Any, None]

    def __init__(
            self, code: int = 400, message: str = 'Bad Request', detail: Union[Any, None] = None
    ):
        self.code = code
        self.message = message
        self.detail = detail

    def __str__(self):
        return f'''
            code: {self.code}
            message: {self.message}
            detail: {self.detail}
            traceback: {self.__traceback__}
            '''

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
            'detail': self.detail,
        }
