
from flask import Flask, abort

import storage

app = Flask(__name__)
storage = storage.storage


@app.route('/add/<ymd>/<amount>', methods=['POST'])
def add(ymd: str, amount: str):
    """Добавляет сумму к определённой дате."""
    try:
        storage[ymd] = int(amount)
        return f"Дата {ymd}, сумма {amount} добавлена"
    except ValueError:
        abort(400)  # Некорректная сумма


@app.route('/calculate/', methods=['GET'])
def calculate_total():
    """Возвращает общий баланс."""
    return str(sum(storage.values()))


@app.route('/calculate/<int:year>', methods=['GET'])
def calculate_year(year: int):
    """Возвращает баланс за указанный год."""
    total = sum(v for k, v in storage.items() if k.startswith(str(year)))
    return str(total)


if __name__ == '__main__':
    app.run(debug=True)