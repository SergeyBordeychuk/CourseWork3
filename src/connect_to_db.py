import psycopg2


def create_database(params: dict, db_name: str):
    """
    Функция для создания БД
    """
    conn = psycopg2.connect(**params)
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE {db_name};")


def create_employers_table(params: dict, db_name: str) -> None:
    """
    Функция для создания таблицы сотрудников
    """
    params["database"] = db_name
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS employers (
                    id serial PRIMARY KEY,
                    employer_id varchar(25) UNIQUE,
                    name varchar NOT NULL,
                    url varchar,
                    open_vacancies integer
                );
                """
                )
            conn.commit()

def create_vacancies_table(params: dict, db_name: str) -> None:
    """
    Функция для создания таблицы вакансий
    """
    params["database"] = db_name
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS vacancies (
                    id serial PRIMARY KEY,
                    name varchar NOT NULL,
                    description text,
                    salary integer,
                    published_at date,
                    employer_id varchar NOT NULL,
                    CONSTRAINT fk_employer_id FOREIGN KEY(employer_id) 
                    REFERENCES employers(employer_id) ON DELETE CASCADE,
                    url varchar NOT NULL
                );
            """
            )
            conn.commit()


def insert_data_in_employers(params: dict, db_name: str, data: dict) -> None:
    """
    Функция для заполнения таблицы сотрудников
    """
    params["database"] = db_name
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            for employer_id, employer_info in data.items():
                if isinstance(employer_info, dict) and employer_info:
                    open_vacancies = employer_info.get("open_vacancies", 0)
                    name = employer_info.get("name", "Неизвестно")
                    url = employer_info.get("url", "")

                    cur.execute(
                        """INSERT INTO employers (employer_id, name, url, open_vacancies)
                                   VALUES (%s, %s, %s, %s)
                                   """,
                        (employer_id, name, url, open_vacancies),
                    )
                else:
                    print(
                        f"Неверный формат данных для работодателя {employer_id}: {employer_info}"
                    )
            conn.commit()


def insert_data_in_vacancies(params: dict, db_name: str, data: list) -> None:
    """
    Функция для заполнения таблицы вакансий
    """
    params["database"] = db_name
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            for v in data:
                salary = None
                if v.get("salary") is not None:
                    salary = v["salary"].get("from", None)
                cur.execute(
                    """INSERT INTO vacancies (name, description, salary, employer_id, url)
                VALUES (%s, %s, %s, %s, %s)
                """,
                    (
                        v["name"],
                        v.get("responsibility", "Нет описания"),
                        salary,
                        v["employer"]["id"],
                        v["alternate_url"],
                    ),
                )
            conn.commit()
