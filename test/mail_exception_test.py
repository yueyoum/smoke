import sys
from wsgiref.simple_server import make_server

sys.path.append('..')

from app import App
from smoke.exceptions import EmailExceptionMiddleware

def exception_func_1():
    return exception_func_2()

def exception_func_2():
    return exception_func_3()

def exception_func_3():
    return 1 / 0


app = EmailExceptionMiddleware(
    App(exception_func_1),
    smoke_html=True,
    to_address=[],
    smtp_server='127.0.0.1'
)


server = make_server('127.0.0.1', 8000, app)
server.serve_forever()
