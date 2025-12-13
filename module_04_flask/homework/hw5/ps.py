"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""
import shlex
from flask import Flask, request
import subprocess

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    get_args: list = request.args.getlist("arg")  # Исправлено: get_apgs → get_args

    if get_args:
        args = shlex.quote(" ".join(get_args))  # Исправлено: ch for in get_args → get_args
        result = subprocess.check_output(f"ps {args}", shell=True).decode()
    else:
        result = subprocess.check_output("ps", shell=True).decode()  # Упрощено

    return f'<pre>{result}</pre>'


if __name__ == "__main__":
    app.run(debug=True)
