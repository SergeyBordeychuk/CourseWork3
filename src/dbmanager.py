import psycopg2

class DBManager:
    host:str
    database:str
    password:str
    user:str

    def __init__(self, host, database, user, password):
        self.connection = psycopg2.connect(host=host, database=database, user=user, password=password)


    def get_companies_and_vacancies_count(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT employers.name, COUNT(v.id) AS vacancy_count 
                from employers
                LEFT JOIN vacancies USING(employer_id)
                GROUP BY employers.name;
                """
            )
            data = cursor.fetchall()
            return data


    def get_all_vacancies(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT vacancies.name AS vacancy_name, employers.name AS company_name, vacancies.salary, vacancies.url 
                from vacancies
                LEFT JOIN employers USING(employer_id);
                """
            )
            data = cursor.fetchall()
            return data


    def get_avg_salary(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT ROUND(AVG(salary))
                from vacancies;
                """
            )
        data = cursor.fetchall()
        return data


    def get_vacancies_with_higher_salary(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT *
                from vacancies
                WHERE salary > (SELECT AVG(salary) from vacancies)
                """
            )
            data = cursor.fetchall()
            return data

    def get_vacancies_with_keyword(self, word):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT * 
                from vacancies
                WHERE name LIKE %s;
                """,
                (f'%{word}')
            )
        data = cursor.fetchall()
        return data


    def close_database(self):
        if self.connection:
            self.connection.close()