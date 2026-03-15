import random
import sqlite3


CREATE_TABLES = """
drop table if exists 'customer';
create table 'customer' (
    customer_id integer primary key autoincrement,
    full_name varchar(50) not null,
    city varchar(50) not null,
    manager_id integer references manager(manager_id)
);

drop table if exists 'manager';
create table 'manager' (
    manager_id integer primary key autoincrement,
    full_name varchar(50) not null,
    city varchar(50) not null
);

drop table if exists 'order';
create table 'order' (
    order_no integer primary key autoincrement,
    purchase_amount integer not null,
    date varchar(255) not null,
    customer_id integer references customer(customer_id),
    manager_id integer references manager(manager_id)
);
"""


def _get_random_date() -> str:
    day = random.randint(1, 30)
    month = random.randint(1, 12)
    return f"2020-{month}-{day}"


families = """Иванов
Васильев
Петров
Смирнов
Михайлов
Фёдоров
Соколов
Яковлев
Попов
Андреев
Алексеев
Александров
Лебедев
Григорьев
Степанов
Семёнов
Павлов
Богданов
Николаев
Дмитриев
Егоров
Волков
Кузнецов
Никитин
Соловьёв""".split()

name_letters = "абвгдежзиклмнопрстуфхцчшщэюя".upper()


def _get_random_full_name() -> str:
    is_male = random.choice((True, False))

    family_name = random.choice(families)
    if not is_male:
        family_name += "а"

    first_letter, last_letter = random.choice(name_letters), random.choice(name_letters)

    return f"{family_name} {first_letter}.{last_letter}."


cities = """
Москва
Омск
Барнаул
Ярославль
Краснодар
Севастополь
Ялта
Сочи
Ижевск
Иркутск
Мурманск
Санкт-Петербург
Архангельск
""".split()


def prepare_tables():
    if __name__ == "__main__":
        with sqlite3.connect("hw.db") as conn:

            cursor = conn.cursor()
            cursor.executescript(CREATE_TABLES)
            conn.commit()
            managers = [
                (_get_random_full_name(), random.choice(cities))
                for _ in range(30)
            ]
            conn.executemany(
                """
                    insert into 'manager'(full_name, city)
                    values (?, ?)
                """,
                managers
            )

            customers = [
                (
                    _get_random_full_name(),
                    random.choice(cities),
                    random.choice([i for i in range(1, 21)] + [None])
                )
                for _ in range(500)
            ]
            conn.executemany(
                """
                    insert into 'customer'(full_name, city, manager_id)
                    values(?, ?, ?)
                """,
                customers
            )

            orders = [
                (
                    random.randint(10, 1000),
                    _get_random_date(),
                    random.randint(1, 100),
                    random.choice([i for i in range(1, 21)] + [None])
                )
                for _ in range(10000)
            ]

            conn.executemany(
                """
                    insert into 'order'(purchase_amount, date, customer_id, manager_id)
                    values(?, ?, ?, ?)
                """,
                orders
            )


if __name__ == '__main__':
    prepare_tables()
