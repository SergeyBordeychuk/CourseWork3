from abc import ABC, abstractmethod
import requests


class BaseUrl(ABC):
    def __init__(self):
        self.base_url = "https://api.hh.ru/"

    @abstractmethod
    def _connection(self, *args):
        pass


class EmployerHH(BaseUrl):
    """
    Класс получения работодателей с API HeadHunter.
    """

    def _connection(self, keyword) -> list:
        """
        Метод, который подключается к API hh.ru и получает работодателей по ключевому слову.
        """
        url = f"{self.base_url}employers?text={keyword}&only_with_vacancies=true"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"Запрос не был успешным. Возможная причина: {response.reason}")
            return []

    def get_employer_id(self, keyword) -> list:
        employers = self._connection(keyword)

        ids = []
        for employer in employers:
            data = {employer['id']: employer['name']}
            ids.append(data)
        if ids:
            return ids
        else:
            print('Айди не найдены')
            return []

    def get_employer_info(self, employer_id: int):
        """
        Метод для получения информации о работодателе по его ID.
        """
        url = f"{self.base_url}employers/{employer_id}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Не удалось получить информацию о работодателе {employer_id}. Причина: {response.reason}")


class Vacancy(BaseUrl):
    """
    Класс для получения вакансий с API HeadHunter.
    """

    def _connection(self, employer_id) -> list:
        """
        Метод, который подключается к апи hh.ru и получает вакансии по айди работодателя в формате json словарей
        """
        url = f"{self.base_url}vacancies?employer_id={employer_id}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()["items"]
        else:
            print(f"Запрос не был успешным. Причина: {response.reason}")
            return []
