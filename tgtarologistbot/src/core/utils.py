from datetime import datetime

from dateutil import parser


def parse_datetime(input_string: str) -> datetime:
    """
    Парсит строку с датой и временем в объект datetime

    :param input_string: Строка с датой и временем

    :return: datetime
    """
    try:
        parsed_date = parser.parse(input_string)
        return parsed_date
    except parser.ParserError as e:
        raise ValueError(f"Невозможно распознать дату/время из строки: {input_string}") from e
