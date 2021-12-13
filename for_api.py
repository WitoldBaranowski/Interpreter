import random
import string
from operator import index

from pydantic import BaseModel
import run_on_venv


# program = "print('Enter your name:')\nx = input()\nprint('Hello, ' + x)"
# stdin = ""


class Response(BaseModel):
    stdout_c: str
    stderr_c: str


def prepare_response(program, stdin):
    file_name = ''.join(random.choices(string.ascii_lowercase, k=8))
    with open(file_name + ".py", "w") as file:
        file.write(program)
    stdout, stderr = run_on_venv.venv_controll(file_name + ".py", stdin)
    if stderr == b'':
        response = Response(stdout_c=stdout, stderr_c="")
    else:
        response = Response(stdout_c="", stderr_c=stderr.decode('ISO-8859-1')[stderr.decode('ISO-8859-1').index(',')+2:])
    print(stdout)
    return response
